# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:56:32 2024
@author: Emerson.Aguilar
"""

# -----------> USUARIO DE RED <-----------
usuario_red = 'emerson.aguilar'

import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import json

# --------> Ruta al archivo JSON
json_credenciales = rf"C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\config\credenciales_sql.json"

# --------> Cargar credenciales desde el archivo
with open(json_credenciales, "r") as file:
    config = json.load(file)

# --------> Seleccionar la base de datos a conectar
conexion = config["conexion_reversion_movil"]  # --------> Esto cambia dependiendo la bbdd

#  --------> Configuración de conexión a la base de datos
host = conexion["host"]
database = conexion["database"]
user = conexion["user"]
password = conexion["password"]

# --------> Crear la cadena de conexión
cadena_de_conexion = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(cadena_de_conexion)
nombre_de_tabla = 'tb_arbol_tipificacion'

# -----------> Cargar el archivo Excel
archivo_excel = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\03.Tercer_Anillo_Reversion\Arbol_Tipificacion_3Anillo_rev.xlsx'
if not os.path.exists(archivo_excel):
    raise FileNotFoundError(f"El archivo '{archivo_excel}' no existe.")

df = pd.read_excel(archivo_excel)

# -----------> Reemplazar valores `NaN` con cadenas vacías
df = df.fillna('')

# -----------> Imprimir las columnas y tipos de datos del DataFrame
print("Columnas del DataFrame:", df.columns)
print("Tipos de datos del DataFrame:", df.dtypes)

# -----------> Función para borrar los registros de la tabla
def borrar_registros_tabla(tabla):
    try:
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM `{tabla}`"))
            conn.execute(text("COMMIT"))
            print(f"Registros eliminados de la tabla '{tabla}'")
    except SQLAlchemyError as e:
        print(f"Error al eliminar registros: {e}")

# -----------> Función para subir el DataFrame a SQL
def subir_arbol_sql(df):
    try:
        df.to_sql(nombre_de_tabla, engine, if_exists='append', index=False)
        print("Datos subidos exitosamente")
    except SQLAlchemyError as e:
        print(f"Error al subir datos: {e}")

# -----------> Función para ejecutar una consulta SQL
def ejecutar_query(query):
    try:
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.execute(text("COMMIT"))
            print("Consulta ejecutada exitosamente")
    except SQLAlchemyError as e:
        print(f"Error al ejecutar la consulta: {e}")

# -----------> Consulta de actualización
query_actualizacion = f"""
UPDATE {nombre_de_tabla}
SET Status_ = "NA"
WHERE Status_ = "";
"""
# -----------> Borrar los registros, subir nuevos datos y ejecutar actualización
borrar_registros_tabla(nombre_de_tabla)
subir_arbol_sql(df)
ejecutar_query(query_actualizacion)