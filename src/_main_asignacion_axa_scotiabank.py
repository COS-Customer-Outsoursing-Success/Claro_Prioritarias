"""
Created By Emerson Aguilar Cruz
"""
import os
from datetime import datetime
from conexiones_db._cls_sqlalchemy import MySQLConnector 
from read_data._cls_read_data import *
from load_data._cls_load_data import *

class load_asignacion():
    
    def __init__(self):
        self.fecha = datetime.now().strftime("%Y-%m-%d")

        self.schema = 'bbdd_cos_bog_grupo_axa'
        self.table = 'tb_asignacion_scotiabank_v2'

        self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.current_folder)
        self.project_root = os.path.dirname(self.current_folder)
        self.start_path =  os.path.join(self.project_root, 'data', 'asignacion','nueva','asignacion_scotiabank')
        self.end_path = os.path.join(self.project_root, 'data', 'asignacion','cargado')
        self.engine = MySQLConnector().get_connection(database=self.schema)
        self.df = None
        self.loader = MySQLLoader(self.engine,self.schema,self.table)
        
    def read_data(self):

        telefonos = [
            'telefono', 'tele_numb', 'tele_numb_3', 'tele_numb_4', 'telefono_contacto',
            'telefono1', 'telefono2', 'telefono3', 'telefono4', 'telefono5',
            'telefono6', 'telefono7', 'telefono8', 'telefono9', 'telefono10','Celular del tomador',
            'celular','celular2','Tel1','Tel2','Tel3','Tel4','Tel5','Tel6','Tel7','Tel8'
        ]

        if not hasattr(self, 'start_path') or not os.path.exists(self.start_path):
            raise ValueError(f"Ruta no válida: {getattr(self, 'start_path', 'No definida')}")

        files = [f for f in os.listdir(self.start_path) if os.path.isfile(os.path.join(self.start_path, f))]
        if not files:
            print(f"No se encontraron archivos en la ruta: {self.start_path}")
            return None

        try:
            reader = FileReader(start_path=self.start_path, end_path=self.end_path)
            latest_file_path = reader.get_latest_file()

            if latest_file_path is None:
                print("No se pudo determinar el archivo más reciente")
                return None

            nombre_archivo = os.path.basename(latest_file_path)
            nombre_base = os.path.splitext(nombre_archivo)[0]

            self.df = reader.read_file(latest_file_path)
            if self.df is None or self.df.empty:
                print("Error: No se pudo leer el archivo o está vacío")
                return None
            print('columnas_antes')
            print(self.df.columns)

            # Renombrar columnas clave
            self.df = self.df.rename(columns={  

                'fecha_fin_vigencia_actual_':'fecha_fin_vigencia_actual',
                'esencial_':'esencial',
                'asistencia_':'asistencia',
                '__de_vehiculos':'No_de_vehiculos'

                })
            self.df['nombre_base'] = nombre_base
            print('columnas_despues')
            print(self.df.columns)

            columnas_necesarias = [

                'typeid', 'codid', 'prioridad', 'primer_apellido', 'segundo_apellido',        
                'primer_nombre', 'segundo_nombre', 'genero', 'segcal', 'edad',
                'antig_edad_segmento', 'placa', 'codmunicipio', 'nommunicipio',
                'coddpto', 'nomdepto', 'direccion', 'tel1', 'tel2', 'tel3', 'tel4',
                'tel5', 'tel6', 'tel7', 'tel8', 'numpro', 'opty_id', 'id_campana',
                'cod_canal', 'tipo_producto', 'nombre_franquicia',
                'fecha_vencimiento_tarjeta', 'cupo_hoy', 'cupo_disponible',
                'codigo_agrupador', 'fecha_fin_vigencia_actual',
                'fecha_inicio_nueva_vigencia', 'modelo', 'linea', 'motor', 'chasis',
                'cod_fasecolda', 'marca', 'asistencia', 'valor_asegurado', 'esencial',      
                'no__temporario_plus', 'prima_plus', 'iva', 'fecha',
                'aseguradora_actual', 'clase_vehiculo', 'fechadenacimiento',
                'No_de_vehiculos', 'servicio', 'email', 'fecha_asignacion', 'anio',
                'periodo', 'nombre_base'

            ]

            columnas_existentes = [col for col in columnas_necesarias if col in self.df.columns]
            self.df = self.df[columnas_existentes]
            for col in self.df.columns:
                if self.df[col].dtype in ['float64', 'int64']:
                    self.df[col] = self.df[col].astype(object)
                self.df[col] = self.df[col].where(pd.notnull(self.df[col]), None)

 
            for col in self.df.select_dtypes(include='object').columns:
                self.df[col] = self.df[col].fillna('-')

            self.df = self.df.where(pd.notnull(self.df), None)
            
            def estandarizar_telefono(x):
                if pd.isna(x) or x == '-':
                    return '-'
                x = str(x).strip()
                x = '601' + x if len(x) == 7 and x.isdigit() else x
                return x.replace('.0', '')

            for col in telefonos:
                if col in self.df.columns:
                    self.df[col] = self.df[col].apply(estandarizar_telefono)

            cols_duplicados = ['codid', 'anio']

            if all(col in self.df.columns for col in cols_duplicados):
                filas_antes = len(self.df)
                self.df.drop_duplicates(subset=cols_duplicados, inplace=True)
                print(f"Duplicados eliminados: {filas_antes - len(self.df)}")
            else:
                print("Advertencia: Columnas para verificación de duplicados no encontradas")

            print('Proceso de lectura completado exitosamente')
            print('Columnas Necesarias:', columnas_existentes)

            for col in self.df.columns:
                if self.df[col].dtype in ['float64', 'int64']:
                    self.df[col] = self.df[col].astype(object)
                self.df[col] = self.df[col].where(pd.notnull(self.df[col]), None)

            if self.df.isnull().values.any():
                print("Advertencia: Hay valores nulos que podrían causar errores en la carga.")
                print(self.df[self.df.isnull().any(axis=1)])
            return self.df

        except Exception as e:
            print(f"Error inesperado al leer datos: {str(e)}")
            return None
        
        #reader.read_directory()

    def load_data(self):
        self.loader.upsert_into_table(self.df)
        return print('Load document completed')
    
    def main(self):
        self.read_data()
        self.load_data()

if __name__ == '__main__':
    loader_asignacion = load_asignacion() 
    loader_asignacion.main()