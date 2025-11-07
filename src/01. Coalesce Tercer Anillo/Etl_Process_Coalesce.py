# -*- coding: utf-8 -*-
"""
@author: emerson.aguilar
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from datetime import datetime
import time

# Datos de conexión
usuario = 'crismarquintero1948'
contrasena = 'pWCGy!M0n8s0Qq&eLJ'
host = '172.70.7.61'
base_de_datos = 'bbdd_cos_bog_claro_tercer_anillo'
tabla_destino = 'tb_coalesce_asignacion_3anillo'

# Cadena de conexión
cadena_de_conexion = f'mysql+pymysql://{usuario}:{contrasena}@{host}/{base_de_datos}'

# Consulta SQL
query = """
SELECT
    DATE_FORMAT(fecha_llegada, '%%Y%%m') AS periodo,
    CONCAT(basg.celular, DATE(basg.fecha_ejecucion_validacion), DATE(basg.fecha_llegada)) AS llave_cuenta,
    basg.celular AS celular, 
    basg.custcode,
    basg.co_id,
    basg.tmcode,
    basg.segmento_camp,
    basg.plan_actual,
    DATE(basg.fech_tickl) AS fecha_tickler,
    DATE(basg.fecha_ejecucion_validacion) AS fecha_ejecucion,
    cal.Dia AS dia_ejecucion,
    cal.Mes AS mes_ejecucion,
    cal.`Year` AS anho_ejecu,
    cal.Dia_Habil AS dia_habil_ejecucion,
    cal.Festivo AS festivo_ejecucion,
    cal.Descripcion_Festivo,
    basg.ciclo,
    basg.canal AS canal_cancelacion,
    basg.documento AS documento_cliente,
    basg.nombre AS nombre_cliente,
    basg.ciudad,
    basg.municipio,
    basg.genero,
    basg.edad_mora,
    basg.cfm_con_imp,
    DATE(basg.fecha_llegada) AS fecha_llegada
FROM bbdd_cos_bog_claro_tercer_anillo.tb_base_tercer_anillo basg
LEFT JOIN (
    SELECT 
        Fecha,
        Dia,
        Mes,
        `Year`,
        Dia_Habil,
        Festivo,
        Descripcion_Festivo
    FROM bbdd_config.tb_calendario_day
    WHERE Fecha >= curdate()
) cal
ON DATE(basg.fecha_ejecucion_validacion) = cal.Fecha
WHERE YEAR(basg.fecha_llegada) = YEAR(CURRENT_DATE) AND MONTH(basg.fecha_llegada) = MONTH(CURRENT_DATE);
"""
#
def crear_conexion(cadena):
    """Crea una conexión a la base de datos."""
    try:
        engine = create_engine(cadena)
        return engine
    except SQLAlchemyError as e:
        print(f"Error al crear la conexión: {e}")
        return None

def limpiar_tabla(engine, tabla):
    """Elimina los registros del mes actual de la tabla destino."""
    try:
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM `{tabla}` WHERE YEAR(fecha_llegada) = YEAR(CURRENT_DATE) AND MONTH(fecha_llegada) = MONTH(CURRENT_DATE)"))
            conn.execute(text("COMMIT"))
        print(f"Registros eliminados de la tabla '{tabla}' para el mes actual.")
    except SQLAlchemyError as e:
        print(f"Error al eliminar registros: {e}")

def coalesce_proceso(engine, tabla_destino, query):
    """Procesa y carga los datos transformados a la base de datos."""
    print("Leyendo datos e iniciando proceso coalesce...")
    try:
        df = pd.read_sql(query, engine)
        
        # Convertir los valores de las columnas de teléfonos a cadenas
        phone_columns = ['celular']
        df[phone_columns] = df[phone_columns].astype(str)
        
        # Transformar el DataFrame
        df_melted = df.melt(id_vars=['periodo','llave_cuenta','custcode', 'co_id', 'tmcode', 'segmento_camp', 'plan_actual', 'fecha_tickler', 'fecha_ejecucion', 'dia_ejecucion', 'mes_ejecucion', 'anho_ejecu', 'dia_habil_ejecucion', 'festivo_ejecucion', 'Descripcion_Festivo', 'ciclo', 'canal_cancelacion', 'documento_cliente','nombre_cliente','ciudad','municipio', 'genero','edad_mora','cfm_con_imp','fecha_llegada'],
                            value_vars=phone_columns,
                            var_name='tipo_telefono',
                            value_name='telefono')
        
        # Filtrar filas con valores no nulos en la columna 'campo_telefono'
        df_melted = df_melted.dropna(subset=['telefono'])
        
        # Convertir los valores de la columna 'campo_telefono' a cadenas y eliminar '.0'
        df_melted['telefono'] = df_melted['telefono'].apply(lambda x: x.rstrip('.0') if pd.notna(x) and '.' in x else x)
        
        # Agregar columna con fecha y hora de ejecución
        df_melted['upload_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Guardar en la base de datos en partes de 10,000 registros
        chunk_size = 10000
        with engine.begin() as connection:
            for i in range(0, len(df_melted), chunk_size):
                chunk = df_melted.iloc[i:i + chunk_size]
                try:
                    chunk.to_sql(tabla_destino, connection, if_exists='append', index=False)
                    print(f"Se insertó un bloque de registros desde el índice {i} hasta {i + len(chunk)}")
                except SQLAlchemyError as e:
                    print(f"Error al insertar el bloque de registros desde el índice {i} hasta {i + len(chunk)}: {e}")

        print(f"Datos insertados en la tabla {tabla_destino}")

    except SQLAlchemyError as e:
        print(f"Error en la conexión con la base de datos: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print("Comenzando Proceso...")
    engine = crear_conexion(cadena_de_conexion)
    if engine:
        limpiar_tabla(engine, tabla_destino)
        time.sleep(1)
        coalesce_proceso(engine, tabla_destino, query)