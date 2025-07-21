"""""
Created By Emerson Aguilar Cruz
"""""

from conexiones_db._cls_sqlalchemy import MySQLConnector
from load_data._cls_load_data import *
from read_data._cls_read_data import FileReader
import os

class SubirInformacion:

    def __init__(self, schema=None, table=None, archivo_excel=None):
        
        self.schema = schema 
        self.table = table
        self.archivo_excel = archivo_excel 
        os.makedirs(self.archivo_excel, exist_ok=True)
        self.engine = MySQLConnector().get_connection(database=self.schema)
        self.df = None
        self.loader = MySQLLoader(self.engine, self.schema, self.table)

    def read_arbol(self):
        
        if not hasattr(self, 'archivo_excel') or not os.path.exists(self.archivo_excel):
            raise ValueError(f"Error ruta no valida: {getattr(self.archivo_excel, 'No definida')}")
        
        archivos = [f for f in os.listdir(self.archivo_excel) if os.path.isfile(os.path.join(self.archivo_excel, f))]
        if not archivos:
            print(f"Error: No se encuentran archivos en la ruta: {self.archivo_excel}")
            return None
        
        try:
            reader = FileReader(start_path=self.archivo_excel, end_path=self.archivo_excel)
            latest_file_path = reader.get_latest_file()

            if latest_file_path is None:
                print("Error: No se puede determinar el archivo mas reciente")
                return None
            
            nombre_archivo = os.path.basename(latest_file_path)
            print(f"Libro Encontrado {nombre_archivo}")

            hojas_disponibles, hoja_seleccionada = reader.sheet_names(latest_file_path)
            print("Hojas encontradas:", hojas_disponibles)
            print("Hoja seleccionada:", hoja_seleccionada)

            if hoja_seleccionada:
                self.df = reader.read_directory(latest_file_path, sheet_name=hoja_seleccionada)
            else:
                print("No se seleccionó una hoja válida. No se cargaron datos.")
            
            if self.df is None or self.df.empty:
                print("Error: El archivo no se pudo leer o está vacio")
                return None

        except Exception as e:
            print(f"Error: Error al leer el archivo por {e}")

    
    def  load_data(self):
        self.loader.upsert_into_table(self.df)
        return print("Lectura Completada")
    
    def main(self):
        self.read_arbol()
        self.load_data()
