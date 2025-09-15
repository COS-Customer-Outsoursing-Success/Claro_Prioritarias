"""
Created By Emerson Aguilar Cruz
"""

import os
import json
from datetime import datetime
from exporte_sql._cls_exporte_sql import ExportarSql

current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

json_formulario = os.path.join(current_folder, 'config', 'config_load_vicidial.json')
with open(json_formulario, "r") as file_json_formulario:
    config_formulario = json.load(file_json_formulario)


class ExporteFormulario:

    @staticmethod
    def elegir_campana():
        print("Campañas disponibles:")
        for i, campana in enumerate(config_formulario.keys(), 1):
            print(f"{i}. {campana}")

        seleccion = input("Seleccione el número de la campaña a ejecutar: ")
        adicional = input("Información adicional sobre lista: ")
        

        try:
            seleccion = int(seleccion)
            campana = list(config_formulario.keys())[seleccion - 1]
            print(f"Ejecutando exporte para campaña: {campana}")
            return campana, adicional
        except (ValueError, IndexError):
            print("Selección inválida. Intente nuevamente.")
            return None, None

    @staticmethod
    def exportar_xlsx_vicidial(campana_key, adicional):
        
        try:
            schema = 'bbdd_cos_bog_grupo_axa'
            folder_salida = os.path.join(current_folder, 'data', 'upload_vcdl', 'nuevo')
            os.makedirs(folder_salida, exist_ok=True)

            # ----> Aquí uso el valor real de la campaña para el nombre del SQL
            campana_sql = config_formulario[campana_key]["campana"]
            hoy_formateado = datetime.now().strftime('%d%m')
            nombre_archivo = f"{campana_key} - {hoy_formateado}_{adicional}"
            sql_path = os.path.join(current_folder, 'sql', f"_sql_depurador_predictivo_{campana_sql}.sql")

            processor = ExportarSql(
                schema=schema,
                sql_path=sql_path,
                folder_salida=folder_salida,
                nombre_archivo=nombre_archivo
            )
            processor.exportar_excel()

        except Exception as e:
            print(f"Error: Error al exportar debido a {e}")


if __name__ == '__main__':
    campana, adicional = ExporteFormulario.elegir_campana()
    if campana:
        ExporteFormulario.exportar_xlsx_vicidial(campana, adicional)
