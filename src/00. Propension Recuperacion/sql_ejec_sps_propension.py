"""
CREATED BY EMERSON AGUILAR CRUZ
"""

# -----------> USUARIO DE RED <-----------
usuario_red = 'emerson.aguilar'

import threading
import time
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import json

# --------> Ruta al archivo JSON
json_credenciales = rf"C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\config\credenciales_sql.json"

# --------> Cargar credenciales desde el archivo
with open(json_credenciales, "r") as file:
    config = json.load(file)

# --------> Seleccionar la base de datos a conectar
conexion = config["conexion_recuperacion"]  # --------> Esto cambia dependiendo la bbdd

#  --------> Configuración de conexión a la base de datos
host = conexion["host"]
database = conexion["database"]
user = conexion["user"]
password = conexion["password"]

# --------> Crear la cadena de conexión
cadena_de_conexion = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# --------> Obtener año y mes actuales
año_actual = datetime.now().year #ej---> 2025
mes_actual = datetime.now().month #ej---> 3

stored_procedures = [
    {'nombre': 'sp_tb_asignacion_dts', 'parametros': {'param1': año_actual, 'param2': mes_actual}},
    {'nombre': 'sp_mejor_marcacion_dts', 'parametros': {'param1': año_actual, 'param2': mes_actual}},
    {'nombre': 'sp_insertar_dts_final', 'parametros': {'param1': año_actual, 'param2': mes_actual}},
    {'nombre': 'sp_tb_asignacion_dts_mes_actual', 'parametros': None}
]

cadena_de_conexion = f'mysql+pymysql://{user}:{password}@{host}/{database}'

def cargar_indicador(parar_sp):
    while not parar_sp.is_set():
        for symbol in "|/-\\":
            print(f"\rEjecutando SP... {symbol}", end="", flush=True)
            time.sleep(0.1)

def ejecutar_sps():
    try:
        print("Iniciando conexión a MySQL usando SQLAlchemy...")
        engine = create_engine(cadena_de_conexion, connect_args={"connect_timeout": 600})
        
        with engine.connect() as conexion:
            print("Conexión a MySQL exitosa.")
            
            for sp in stored_procedures:
                sp_nombre = sp['nombre']
                sp_parametros = sp['parametros']
                
                parar_sp = threading.Event()
                cargar_hilo = threading.Thread(target=cargar_indicador, args=(parar_sp,))
                cargar_hilo.start()
                
                print(f"\nEjecutando el Stored Procedure: {sp_nombre}")
                if sp_parametros:
                    parametros_sql = ', '.join(f":{k}" for k in sp_parametros.keys())
                    conexion.execute(text(f"CALL {sp_nombre}({parametros_sql})"), sp_parametros)
                else:
                    conexion.execute(text(f"CALL {sp_nombre}()"))
                
                conexion.commit()
                
                parar_sp.set()
                cargar_hilo.join()
                
                print(f"\nProcedimiento almacenado '{sp_nombre}' ejecutado exitosamente.")
                time.sleep(2)
        
        print("Todos los Stored Procedures se ejecutaron correctamente.")
        
    except SQLAlchemyError as e:
        print(f"Error al ejecutar los SPs: {e}")
    
    finally:
        engine.dispose()
        print("Conexión cerrada.")

if __name__ == '__main__':
    print(datetime.now())
    ejecutar_sps()
