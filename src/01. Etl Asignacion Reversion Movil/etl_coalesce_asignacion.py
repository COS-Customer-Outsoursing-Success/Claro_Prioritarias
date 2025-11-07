# -*- coding: utf-8 -*-
"""
@author: emerson.aguilar
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import time
from datetime import datetime
import json

usuario_red = 'crismar.quintero.GROUPCOS'

# --------> Ruta al archivo JSON
json_credenciales = rf"C:\Users\{usuario_red}\Documents\GIT\Claro-Prioritarias\config\credenciales_sql.json"

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
tabla_destino = 'tb_coalesce_asignacion_rever'

# --------> Crear la cadena de conexión
cadena_de_conexion = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# -------> Crear conexión
try:
    engine = create_engine(cadena_de_conexion)
except SQLAlchemyError as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit()

# -------> Consulta SQL
query = """
SELECT 
    DATE_FORMAT(file_date, '%%Y%%m') AS periodo,
    telefono AS cuenta,
    IF(telefono REGEXP '^3[0-9]{9}$|^60[0-9]{8}$',
        telefono,
        NULL) AS telefono,
    identificacion,
    nombre_cliente,
    co_id_post,
    co_id_prep,
    tipo_linea,
    region,
    departamento,
    ciudad,
    fecha_corte,
    mes_ult AS ultimo_mes_activo,
    CASE 
        WHEN edad >= 90 THEN '90'
        WHEN edad >= 0 THEN CONCAT(FLOOR(edad / 10) * 10, '-', FLOOR(edad / 10) * 10 + 9)
        ELSE ''
    END AS edad,
    RANGO_CARGA_ULTIMO_MES AS rango_carga_ultimo_mes,
    CASE
        WHEN VAL_CARGAS BETWEEN 0 AND 9900 THEN '0-9900'
        WHEN VAL_CARGAS BETWEEN 10000 AND 19900 THEN '10000-19900'
        WHEN VAL_CARGAS BETWEEN 20000 AND 29900 THEN '20000-29900'
        WHEN VAL_CARGAS BETWEEN 30000 AND 39900 THEN '30000-39900'
        WHEN VAL_CARGAS BETWEEN 40000 AND 49900 THEN '40000-49900'
        WHEN VAL_CARGAS BETWEEN 50000 AND 59900 THEN '50000-59900'
        WHEN VAL_CARGAS BETWEEN 60000 AND 69900 THEN '60000-69900'
        WHEN VAL_CARGAS BETWEEN 70000 AND 79900 THEN '70000-79900'
        WHEN VAL_CARGAS BETWEEN 80000 AND 89900 THEN '80000-89900'
        WHEN VAL_CARGAS BETWEEN 90000 AND 99900 THEN '90000-99900'
        WHEN VAL_CARGAS >= 100000 THEN '100000'
        ELSE ''
    END AS valor_cargas,
    CASE
        WHEN VAL_MIN_CARGAS BETWEEN 0 AND 9900 THEN '0-9900'
        WHEN VAL_MIN_CARGAS BETWEEN 10000 AND 19900 THEN '10000-19900'
        WHEN VAL_MIN_CARGAS BETWEEN 20000 AND 29900 THEN '20000-29900'
        WHEN VAL_MIN_CARGAS BETWEEN 30000 AND 39900 THEN '30000-39900'
        WHEN VAL_MIN_CARGAS BETWEEN 40000 AND 49900 THEN '40000-49900'
        WHEN VAL_MIN_CARGAS BETWEEN 50000 AND 59900 THEN '50000-59900'
        WHEN VAL_MIN_CARGAS BETWEEN 60000 AND 69900 THEN '60000-69900'
        WHEN VAL_MIN_CARGAS BETWEEN 70000 AND 79900 THEN '70000-79900'
        WHEN VAL_MIN_CARGAS BETWEEN 80000 AND 89900 THEN '80000-89900'
        WHEN VAL_MIN_CARGAS >= 90000 THEN '90000'
        ELSE ''
    END AS valor_minimo_cargas,
    CASE
        WHEN VAL_TOTAL_DATOS BETWEEN 0 AND 9900 THEN '0-9900'
        WHEN VAL_TOTAL_DATOS BETWEEN 10000 AND 19900 THEN '10000-19900'
        WHEN VAL_TOTAL_DATOS BETWEEN 20000 AND 29900 THEN '20000-29900'
        WHEN VAL_TOTAL_DATOS BETWEEN 30000 AND 39900 THEN '30000-39900'
        WHEN VAL_TOTAL_DATOS BETWEEN 40000 AND 49900 THEN '40000-49900'
        WHEN VAL_TOTAL_DATOS BETWEEN 50000 AND 59900 THEN '50000-59900'
        WHEN VAL_TOTAL_DATOS BETWEEN 60000 AND 69900 THEN '60000-69900'
        WHEN VAL_TOTAL_DATOS BETWEEN 70000 AND 79900 THEN '70000-79900'
        WHEN VAL_TOTAL_DATOS BETWEEN 80000 AND 89900 THEN '80000-89900'
        WHEN VAL_TOTAL_DATOS >= 90000 THEN '90000'
        ELSE ''
    END AS valor_total_datos,
    CASE
        WHEN VAL_TOTAL_VOZ BETWEEN 0 AND 9900 THEN '0-9900'
        WHEN VAL_TOTAL_VOZ BETWEEN 10000 AND 19900 THEN '10000-19900'
        WHEN VAL_TOTAL_VOZ BETWEEN 20000 AND 29900 THEN '20000-29900'
        WHEN VAL_TOTAL_VOZ BETWEEN 30000 AND 39900 THEN '30000-39900'
        WHEN VAL_TOTAL_VOZ BETWEEN 40000 AND 49900 THEN '40000-49900'
        WHEN VAL_TOTAL_VOZ BETWEEN 50000 AND 59900 THEN '50000-59900'
        WHEN VAL_TOTAL_VOZ BETWEEN 60000 AND 69900 THEN '60000-69900'
        WHEN VAL_TOTAL_VOZ BETWEEN 70000 AND 79900 THEN '70000-79900'
        WHEN VAL_TOTAL_VOZ BETWEEN 80000 AND 89900 THEN '80000-89900'
        WHEN VAL_TOTAL_VOZ >= 90000 THEN '90000'
        ELSE ''
    END AS valor_total_voz,
    file_name AS nombre_base,
    ban_documento_bloqueado,
    direccion,
    email,
    IF(fijo_1 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$',
        fijo_1,
        NULL) AS fijo_1,
    IF(fijo_2 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$',
        fijo_2,
        NULL) AS fijo_2,
    IF(tel_1 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$',
        tel_1,
        NULL) AS tel_1,
    IF(tel_2 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$',
        tel_2,
        NULL) AS tel_2,
    IF(cel_1 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$',
        cel_1,
        NULL) AS cel_1,
    DATE(file_date) AS fecha_llegada
FROM bbdd_cos_bog_claro_reversion_movil.tb_asignacion_portaciones_migracion_final
WHERE DATE_FORMAT(file_date, '%%Y-%%m') = DATE_FORMAT(CURRENT_DATE, '%%Y-%%m');
"""

def limpiar_tabla(tabla):

    try:
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM `{tabla}` WHERE YEAR(fecha_llegada) = YEAR(CURRENT_DATE) AND MONTH(fecha_llegada) = MONTH(CURRENT_DATE)"))
            conn.execute(text("COMMIT"))
        print(f"Registros eliminados de la tabla '{tabla}' para el mes actual.")
    except SQLAlchemyError as e:
        print(f"Error al eliminar registros: {e}")

def coalesce_proceso(tabla_destino, query):

    try:
        df = pd.read_sql(query, engine)
        
        # -------> Columnas de teléfonos
        phone_columns = [
            'telefono',
              'fijo_1',
                'fijo_2',
                  'tel_1',
                    'tel_2',
                      'cel_1']
        df[phone_columns] = df[phone_columns].astype(str)

        # -------> Transformar el DataFrame
        df_melted = df.melt(
            id_vars=[
                'periodo', 
                      'cuenta',
                        'identificacion',
                          'nombre_cliente',
                            'co_id_post',
                              'co_id_prep', 
                               'tipo_linea',
                                 'edad',
                                   'region',
                                     'departamento',
                                       'ciudad',
                                         'fecha_corte',
                                          'ultimo_mes_activo', 
                                            'rango_carga_ultimo_mes',
                                              'valor_cargas',
                                                'valor_minimo_cargas', 
                                                  'valor_total_datos',
                                                    'valor_total_voz',
                                                      'email',
                                                        'direccion',
                                                          'ban_documento_bloqueado',
                                                            'nombre_base',
                                                              'fecha_llegada'
                                                        ],
            value_vars=phone_columns,
            var_name='tipo_telefono',
            value_name='phone'
        )

        # -------> Filtrar valores nulos y duplicados
        df_melted = df_melted.dropna(subset=['phone']).drop_duplicates(subset=['phone'])

        # -------> Agregar columna de fecha de carga
        df_melted['upload_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # -------> Insertar datos en la tabla destino en bloques
        total_registros = len(df_melted)
        print(f"Iniciando inserción de {total_registros} registros en bloques de 10,000 en '{tabla_destino}'...")

        for i, chunk in enumerate(range(0, total_registros, 10000), start=1):
            df_melted.iloc[chunk:chunk+10000].to_sql(tabla_destino, engine, if_exists='append', index=False, method='multi')
            print(f"Bloque {i}: {min(chunk+10000, total_registros)} registros insertados...")

        print(f"¡Inserción completada en la tabla '{tabla_destino}'! 🚀")
    except SQLAlchemyError as e:
        print(f"Error en la inserción de datos: {e}")

if __name__ == '__main__':
    limpiar_tabla(tabla_destino)
    time.sleep(1)
    coalesce_proceso(tabla_destino, query)
