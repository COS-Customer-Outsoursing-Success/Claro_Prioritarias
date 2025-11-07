"""
CREATED BY EMERSON AGUILAR CRUZ
"""

# -----------> USUARIO DE RED <-----------
usuario_red = 'crismar.quintero.GROUPCOS'

import threading
import time
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import json

# --------> Ruta al archivo JSON
json_credenciales = rf"C:\Users\{usuario_red}\Documents\GIT\Claro-Prioritarias\config\credenciales_sql.json"

# --------> Cargar credenciales desde el archivo
with open(json_credenciales, "r") as file:  
    config = json.load(file)

# --------> Seleccionar la base de datos a conectar
conexion = config["conexion_recuperacion"]  # --------> Esto cambia dependiendo la bbdd

# --------> Configuración de conexión a la base de datos
host = conexion["host"]
database = conexion["database"]
user = conexion["user"]
password = conexion["password"]

# --------> Crear la cadena de conexión
cadena_de_conexion = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# --------> Lista de SPs a ejecutar
stored_procedures = [
    {'nombre': 'sp_01_marcaciones_desgloce_dts', 'parametros': {'param1': 1}},
    {'nombre': 'sp_insertar_tb_temporales', 'parametros': None},
    {'nombre': 'sp_depurador_general_recuperacion_dts', 'parametros': None}
]

def cargar_indicador(parar_sp):
    while not parar_sp.is_set():
        for symbol in "|/-\\":
            print(f"\rEjecutando SP... {symbol}", end="", flush=True)
            time.sleep(0.1)

def ejecutar_sps():
    try:
        print("Iniciando conexión a MySQL usando SQLAlchemy...")
        engine = create_engine(cadena_de_conexion, connect_args={"connect_timeout": 600})
        print("Conexión a MySQL preparada.")

        for sp in stored_procedures:
            sp_nombre = sp['nombre']
            sp_parametros = sp['parametros']

            parar_sp = threading.Event()
            cargar_hilo = threading.Thread(target=cargar_indicador, args=(parar_sp,))
            cargar_hilo.start()

            print(f"\nEjecutando el Stored Procedure: {sp_nombre}")

            # ✅ Usamos una conexión y transacción por cada SP
            with engine.connect() as conn:
                with conn.begin():
                    if sp_parametros:
                        parametros_sql = ', '.join(f":{k}" for k in sp_parametros.keys())
                        conn.execute(text(f"CALL {sp_nombre}({parametros_sql})"), sp_parametros)
                    else:
                        conn.execute(text(f"CALL {sp_nombre}()"))

            parar_sp.set()
            cargar_hilo.join()

            print(f"\n✅ Procedimiento almacenado '{sp_nombre}' ejecutado exitosamente.")
            time.sleep(2)

        print("\n✅ Todos los Stored Procedures se ejecutaron correctamente.")

    except SQLAlchemyError as e:
        print(f"\n❌ Error al ejecutar los SPs: {e}")

    finally:
        engine.dispose()
        print("🔚 Conexión cerrada.")

if __name__ == '__main__':
    print(">>> Script iniciado")
    print(datetime.now())
    ejecutar_sps()



