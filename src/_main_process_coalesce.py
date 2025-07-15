"""
Creater By Emerson Aguilar Cruz
"""

import os
import sys
import json
from coalesce._cls_etl_coalesce_ import EtlCoalesceTel

current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_folder)

sys.path.append(project_root)

config_path = os.path.join(project_root, "config", "config_coalesce.json")
with open(config_path, "r", encoding="utf-8") as f:
    campaigns_config = json.load(f)

ruta_sql = os.path.join(project_root, "sql")

def elegir_campania() -> str:
    campaigns = list(campaigns_config.keys())

    print("\nCampañas disponibles:")
    for idx, nombre in enumerate(campaigns, start=1):
        print(f"  {idx}. {nombre}")

    while True:
        try:
            choice = int(input("\nIngrese el número de la campaña a ejecutar: "))
            if 1 <= choice <= len(campaigns):
                return campaigns[choice - 1]
            print("❌ Selección fuera de rango. Intente de nuevo.")
        except ValueError:
            print("❌ Entrada no válida. Debe ser un número entero.")

def main():
    try:
        campania = elegir_campania()
        config = campaigns_config[campania]
        sql_file = os.path.join(ruta_sql, config["sql_file_path"])

        procesador = EtlCoalesceTel(
            schema=config["schema"],
            table=config["table"],
            sql_file_path=sql_file,
            cuenta=config["cuenta"],
            phone_columns=config["phone_columns"],
        )

        procesador.coalesce_etl()
        procesador.load_data()

        print(f"✅ Proceso de la campaña '{campania}' completado con éxito")

    except Exception as error:
        print(f"❌ Error en el proceso principal: {error}")


if __name__ == "__main__":
    main()
