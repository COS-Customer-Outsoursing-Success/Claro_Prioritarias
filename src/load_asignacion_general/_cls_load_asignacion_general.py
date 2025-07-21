"""
Created By Emerson Aguilar Cruz
"""
import os
from datetime import datetime
from conexiones_db._cls_sqlalchemy import MySQLConnector 
from read_data._cls_read_data import *
from load_data._cls_load_data import *
import json

import os
import json
from datetime import datetime

class Load_Asignacion:

    def __init__(self, config_path=None, ):
        
        self.fecha = datetime.now().strftime("%Y-%m-%d")
        self.config_path = config_path

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config_asignacion = json.load(f)

        self.campanas_disponibles = [key for key in self.config_asignacion.keys() if key not in ['schema', 'table']]
        print("Campañas disponibles:")
        for i, campaña in enumerate(self.campanas_disponibles, start=1):
            print(f"{i}. {campaña}")

        while True:
            try:
                seleccion = int(input("Ingrese el número de la campaña que desea ejecutar: "))
                if 1 <= seleccion <= len(self.campanas_disponibles):
                    self.campana_seleccionada = self.campanas_disponibles[seleccion - 1]
                    break
                else:
                    print("Número inválido. Intente nuevamente.")
            except ValueError:
                print("Entrada no válida. Ingrese un número.")

        self.campana_config = self.config_asignacion[self.campana_seleccionada]

        self.start_path = os.path.join(self.project_root, 'data', 'asignacion', 'nueva', self.campana_config['nombre_asignacion'])
        self.end_path = os.path.join(self.project_root, 'data', 'asignacion', 'cargado', self.campana_config['nombre_asignacion'])
        os.makedirs(self.start_path, exist_ok=True)
        os.makedirs(self.end_path, exist_ok=True)
        
        self.schema = self.campana_config['schema']
        self.table = self.campana_config['table']

        self.engine = MySQLConnector().get_connection(database=self.schema)
        self.df = None
        self.loader = MySQLLoader(self.engine, self.schema, self.table)

        print(f"\n Campaña seleccionada: {self.campana_seleccionada}")
        print(f" Ruta origen: {self.start_path}")
        print(f" Ruta destino: {self.end_path}")

        
    def read_data(self):

        telefonos = self.campana_config['telefonos']

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
            
            hojas_disponibles, hoja_seleccionada = reader.sheet_names(latest_file_path)
            print("Hojas encontradas:", hojas_disponibles)
            print("Hoja seleccionada:", hoja_seleccionada)

            if hoja_seleccionada:
                self.df = reader.read_directory(latest_file_path, sheet_name=hoja_seleccionada)
            else:
                print("No se seleccionó una hoja válida. No se cargaron datos.")

            if self.df is None or self.df.empty:
                print("Error: No se pudo leer el archivo o está vacío")
                return None
            print(f"cantidad de registros antes: {len(self.df)}")
            print("columnas_antes")
            print(self.df.columns)

            self.df = self.df.rename(columns=self.campana_config['renombrar_columnas'])

            self.df['nombre_base'] = nombre_base
            self.df['hoja'] = hoja_seleccionada

            print(f"cantidad de registros despues: {len(self.df)}")
            print('columnas_despues')
            print(self.df.columns)

            columnas_necesarias = self.campana_config['columnas_necesarias']

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

            columnas_fecha = self.campana_config['columnas_fecha']

            for col in columnas_fecha:
                if col in self.df.columns:
                    try:
                        self.df[col] = pd.to_datetime(self.df[col], errors='coerce', dayfirst=True)
                    except Exception as e:
                        print(f"Error al convertir la columna {col} a fecha: {e}")
                        
            self.duplicados = os.path.join(self.project_root, 'data', 'asignacion', 'duplicados', self.campana_config['nombre_asignacion'])
            os.makedirs(self.duplicados, exist_ok=True)

            cols_duplicados = self.campana_config['cols_duplicados']

            if all(col in self.df.columns for col in cols_duplicados):
                filas_antes = len(self.df)

                df_duplicados = self.df[self.df.duplicated(subset=cols_duplicados, keep=False)]

                if not df_duplicados.empty:
                    archivo_duplicados = os.path.join(self.duplicados, 'duplicados_detectados_periodo.csv')
                    df_duplicados[cols_duplicados].to_csv(archivo_duplicados, index=False)
                    print(f"Archivo 'duplicados_detectados_periodo.csv' guardado con {len(df_duplicados)} registros duplicados.")

                self.df.drop_duplicates(subset=cols_duplicados, inplace=True)
                print(f"Duplicados eliminados: {filas_antes - len(self.df)}")
            else:
                print("Advertencia: Columnas para verificación de duplicados no encontradas")

            print(f"Cantidad de registros después de eliminar duplicados: {len(self.df)}")

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
    loader_asignacion = Load_Asignacion() 
    loader_asignacion.main()