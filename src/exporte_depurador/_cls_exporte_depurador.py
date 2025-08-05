

import sys
import os 
current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(current_folder) 
sys.path.append(current_folder)

from conexiones_db._cls_sqlalchemy import MySQLConnector
import pandas as pd


class ExportarReporte:

    def __init__(self):
        
        self.schema = 'bbdd_cos_bog_grupo_axa'
        self.engine = MySQLConnector().get_connection(database=self.schema)
        self.folder_excel = os.path.join(project_root, 'data', 'upload_vcdl')
        os.makedirs(self.folder_excel, exist_ok=True )

        self.ruta_salida = os.path.join (self.folder_excel, 'depurador falabella.xlsx')

        self.sql_path = os.path.join(project_root, 'sql', '_sql_depurador_predictivo_falabella.sql')


    def export_sql(self):

        try:
            with open(self.sql_path, 'r', encoding='utf-8') as file:
                query_sql = file.read()
                print("Leyendo Archivo SQL")
        except Exception as e: 
            print(f"Error: Falla debido a {e}")

        try:
            self.df = pd.read_sql(query_sql, self.engine)
            print(self.df)
        except Exception as e:
            print(f"Error: Falla debido a {e}")    
        return self.df
    
    def exportar_excel(self):

        self.df.to_excel(self.ruta_salida, index=False)
        print("Exportado Correctamente")

if __name__ == '__main__':

    processor = ExportarReporte()
    processor.export_sql()
    processor.exportar_excel()