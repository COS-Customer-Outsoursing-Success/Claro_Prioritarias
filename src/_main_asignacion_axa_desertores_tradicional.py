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
        self.table = 'tb_asignacion_desertores_tradicional_v2'

        self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.current_folder)
        self.start_path =  os.path.join(self.project_root, 'data', 'asignacion','nueva','asignacion_desertores_tradicional')
        self.end_path = os.path.join(self.project_root, 'data', 'asignacion','cargado', 'asignacion_desertores_tradicional')

        self.engine = MySQLConnector().get_connection(database=self.schema)
        self.df = None
        self.loader = MySQLLoader(self.engine,self.schema,self.table)
        
    def read_data(self):

        telefonos = [
            'telefono',  'telefono_contacto', 'telefono_fijo', 'telefono_correspondencia',
            'telefono1', 'telefono2', 'telefono3', 'telefono4', 'telefono5',
            'telefono6', 'telefono7', 'telefono8', 'telefono9', 'telefono10',
            'telefono_1', 'telefono_2', 'telefono_3', 'telefono_4', 'telefono_5',
            'telefono_6', 'telefono_7', 'telefono_8', 'telefono_9', 'telefono_10',
            'tele_numb', 'tele_numb_2', 'tele_numb_3', 'tele_numb_4', 'tele_numb_5',
            'celular', 'celular_1', 'celular_2', 'celular_3', 'celular_4', 'celular_5',
            'celular_6', 'celular_7', 'celular_8', 'celular_9', 'celular_10'
        ]

        if not hasattr(self, 'start_path') or not os.path.exists(self.start_path):
            raise ValueError(f"Ruta no válida: {getattr(self, 'start_path', 'No definida')}")

        files = [f for f in os.listdir(self.start_path) if os.path.isfile(os.path.join(self.start_path, f))]
        if not files:
            print(f"No se encontraron archivos en la ruta: {self.start_path}")
            return None

        try:
            reader = FileReader(start_path=self.start_path, end_path=self.end_path,)
            latest_file_path = reader.get_latest_file()

            if latest_file_path is None:
                print("No se pudo determinar el archivo más reciente")
                return None

            nombre_archivo = os.path.basename(latest_file_path)
            nombre_base = os.path.splitext(nombre_archivo)[0]
            
            hoja = 'Fide'
            
            self.df = reader.read_directory( latest_file_path, sheet_name = hoja)
            if self.df is None or self.df.empty:
                print("Error: No se pudo leer el archivo o está vacío")
                return None
            print('columnas_antes')
            print(self.df.columns)

            self.df = self.df.rename(columns={   

            'nombre_colectivo_doc_titular': 'nombre_colectivo',
            'tipo_identificacionbeneficiario': 'tipo__identificacion_beneficiario',
            'no__identificacion_colectivo': 'no_identificacion_colectivo', 
            'no__identificacion_contrante': 'no_identificacion_contrante', 
            'observacion_':'observacion'
            })
            self.df['nombre_base'] = nombre_base
            self.df['hoja'] = hoja
            print('columnas_despues')
            print(self.df.columns)

            columnas_necesarias = [

            'dia_de_gestion', 
            'tipo_consulta', 
            'sucursal', 
            'mes_envio', 
            'tipo',
            'plan', 
            'contrato', 
            'frecuencia_de_pago', 
            'tarifa', 
            'nombre_colectivo',
            'tipo__identificacion_beneficiario', 
            'no_identificacion_colectivo',
            'tipo_identificacion_contrante', 
            'no_identificacion_contrante',
            'primer_apellido', 
            'segundo_apellido', 
            'nombres', 
            'correo_electronico',
            'celular', 
            'celular_2', 
            'telefono_fijo', 
            'clave', 
            'asesor', 
            'director',
            'clave_director', 
            'telefono_correspondencia',
            'direccion_correspondencia', 
            'cod_ciudad_correspondencia',
            'mes_gestion_emermedica', 
            'tipologia_contactabilidad', 
            'observacion',
            'telefono_3', 
            'telefono_4', 
            'telefono_5', 
            'fecha_asignacion', 
            'anio',
            'periodo', 
            'nombre_base',
            'hoja'
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

            cols_duplicados = ['contrato', 'anio']

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
        
    def load_data(self):
        self.loader.upsert_into_table(self.df)
        return print('Load document completed')
    
    def main(self):
        self.read_data()
        self.load_data()

if __name__ == '__main__':
    loader_asignacion = load_asignacion() 
    loader_asignacion.main()