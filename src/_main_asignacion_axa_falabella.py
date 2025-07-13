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

       # self.schema = 'bbdd_cos_bog_grupo_axa'
        #self.table = 'tb_asignacion_axa_falabella'

        self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(self.current_folder))
        self.start_path = r'C:\Users\Emerson.Aguilar\Documents\git_hub\Axa\data\asignacion\nueva'
#        self.start_path = os.path.join(self.project_root, 'Axa', 'data','asignacion', 'nuevo')
        self.end_path = os.path.join(self.project_root, 'Axa', 'data', 'asignacion', 'cargado')


        #self.engine = MySQLConnector().get_connection(database=self.schema)
        self.df = None
        #self.loader = MySQLLoader(self.engine,self.schema,self.table)
        
    def read_data(self):

        telefonos = [
            'telefono', 'tele_numb', 'tele_numb_3', 'tele_numb_4', 'telefono_contacto',
            'telefono1', 'telefono2', 'telefono3', 'telefono4', 'telefono5',
            'telefono6', 'telefono7', 'telefono8', 'telefono9', 'telefono10'
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

            self.df = reader.read_file(latest_file_path)
            if self.df is None or self.df.empty:
                print("Error: No se pudo leer el archivo o está vacío")
                return None
            print('columnas_antes')
            print(self.df.columns)

            # Renombrar columnas clave
            self.df = self.df.rename(columns={
                'registerid': 'registro',
                'codid': 'co_id',
                'primernombre': 'nombre',
                'segundonombre': 'segundo_nombre',
                'primerapellido': 'apellido',
                'segundoapellido': 'segundo_apellido',
                'fechanacimiento': 'fecha_nacimiento',
                'codmunicipio': 'cod_municipio',
                'nommunicipio': 'municipio',
                'coddpto': 'cod_departamento',
                'nomdepto': 'departamento',
                'fecha_fin_vigencia_actual_': 'fecha_fin_vigencia_actual',
                'no_temporario__tradicional': 'no_temporario_tradicional',
                'no_temporario__vip': 'no_temporario_vip'            
            })
            self.df['nombre_base'] = nombre_base
            print('columnas_despues')
            print(self.df.columns)

            columnas_necesarias = [
                    'registro',
                    'co_id', 
                    'genero', 
                    'nombre', 
                    'segundo_nombre', 
                    'apellido',
                    'segundo_apellido', 
                    'fecha_nacimiento', 
                    'placa', 
                    'cod_municipio',
                    'municipio', 
                    'cod_departamento', 
                    'departamento', 
                    'direccion',
                    'telefono1', 
                    'telefono2', 
                    'telefono3', 
                    'telefono4', 
                    'telefono5',
                    'fecha_fin_vigencia_actual', 
                    'modelo', 
                    'linea', 
                    'motor', 
                    'chasis',
                    'cod_fasecolda', 
                    'marca', 
                    'marca_y_linea', 
                    'tasa', 
                    'suma_asegurada',
                    'aseguradora_actual', 
                    'clase_vehiculo', 
                    'servicio', 
                    'email',
                    'no_temporario_plus', 
                    'prima_temporario_plus',
                    'prima_temporario_sin_iva_plus', 
                    'no_temporario_tradicional',
                    'prima_tradicional', 
                    'prima_tradicional_sin_iva', 
                    'no_temporario_vip',
                    'prima_temporario_vip', 
                    'prima_temporario_vip_sin_iva',
                    'no_temporario_nuevo_vip', 
                    'prima_nueva_vip', 
                    'prima_nueva_vip_sin_iva',
                    'no_temporario_esencial', 
                    'prima_temporario_esencial',
                    'prima_temporario_esencial_sin_iva', 
                    'no_temporario_nuevo_esencial',
                    'prima_nueva_esencial', 
                    'prima_nueva_esencial_sin_iva', 
                    'grupos_1_y_2',
                    'segmentacion_grupo_1_y_2_final',
                    'fecha_asignacion', 
                    'anio',
                    'periodo', 
                    'nombre_base'
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

            cols_duplicados = ['co_id', 'anio']

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
#        self.load_data()

if __name__ == '__main__':
    loader_asignacion = load_asignacion() 
    loader_asignacion.main()