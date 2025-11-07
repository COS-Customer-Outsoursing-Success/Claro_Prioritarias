"""""
 Created By Emerson Aguilar Cruz
"""""

# -----------> USUARIO DE RED <-----------
usuario_red = 'crismar.quintero.GROUPCOS'

# --------> Importar las librerías necesarias
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from datetime import datetime
import time
import json

# --------> Ruta al archivo JSON
json_credenciales = rf"C:\Users\{usuario_red}\Documents\GIT\Claro-Prioritarias\config\credenciales_sql.json"

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
tabla_destino = 'tb_coalesce_asignacion_recu'

# --------> Consulta SQL
query = """
    SELECT 
    DATE_FORMAT(fecha_llegada, '%%Y%%m') periodo,
    cuenta,
    can_serv AS cantidad_servicios,
    convergente,
    motivo,
    sub_motivo,
    tipo_base,
    division,
    area,
    zona,
    ciudad,
    red,
    numero_de_documento,
    nombre AS nombre_cliente,
    antiguedad,
    altura_cartera,
    fecha_corte,
    fecha_solicitud,
    ofrecimiento_1,
    ofrecimiento_2,
    ofrecimiento_3,
    canal,
    tarifa,
    categoria_fidelizacion,
    estrato,
    productos AS paquete,
    IF(telefono_claro REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', telefono_claro, NULL) AS telefono_claro,
    IF(te1 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', te1, NULL) AS tel_1,
    IF(te2 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', te2, NULL) AS tel_2,
    IF(te3 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', te3, NULL) AS tel_3,
    IF(movil REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil, NULL) AS movil_1,
    IF(movil2 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil2, NULL) AS movil_2,
    IF(movil3 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil3, NULL) AS movil_3,
    IF(movil4 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil4, NULL) AS movil_4,
    IF(movil5 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil5, NULL) AS movil_5,
    IF(movil6 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil6, NULL) AS movil_6,
    IF(movil9 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil9, NULL) AS movil_9,
    IF(movil10 REGEXP '^3[0-9]{9}$|^60[0-9]{8}$', movil10, NULL) AS movil_10,
    MAX,
    fecha_llegada
FROM bbdd_cos_bog_claro_recuperacion.tb_base_recuperacion
WHERE YEAR(fecha_llegada) = YEAR(CURRENT_DATE) 
  AND MONTH(fecha_llegada) = MONTH(CURRENT_DATE)
  AND tipo_base NOT IN ('WEB', 'QUASIREAL')
"""

# --------> Función para limpiar la tabla
def limpiar_tabla(tabla_destino):
    try:
        engine = create_engine(cadena_de_conexion)
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM `{tabla_destino}` WHERE YEAR(fecha_llegada) = YEAR(current_date) AND MONTH(fecha_llegada) = MONTH(current_date)"))
            conn.execute(text("COMMIT"))
            print(f"Registros del mes actual eliminados de la tabla '{tabla_destino}'")
    except SQLAlchemyError as e:
        print(f"Error al eliminar registros: {e}")

# --------> Función principal del proceso
def coalesce_proceso(tabla_destino, query):
    print("Leyendo datos e inciando proceso coalesce...")
    try:
        # --------> Crear conexión
        engine = create_engine(cadena_de_conexion)
        
        # --------> Leer datos
        df = pd.read_sql(query, engine)

        # --------> Columnas importantes de teléfonos
        phone_columns = ['telefono_claro', 'tel_1', 'tel_2', 'tel_3', 'movil_1', 'movil_2', 'movil_3', 'movil_4', 'movil_5', 'movil_6', 'movil_9', 'movil_10']

        # --------> Convertir los valores de las columnas de teléfonos a cadenas
        df[phone_columns] = df[phone_columns].astype(str)

        # --------> Transformar el DataFrame
        df_melted = df.melt(id_vars=[col for col in df.columns if col not in phone_columns],
                            value_vars=phone_columns,
                            var_name='tipo_telefono',
                            value_name='telefono')

        # --------> Filtrar filas con valores no nulos y limpiar números de teléfono
        df_melted = df_melted.dropna(subset=['telefono'])
        df_melted['telefono'] = df_melted['telefono'].str.rstrip('.0')
        df_melted = df_melted[df_melted['telefono'].str.len() == 10]

        # --------> Eliminar duplicados
        df_melted = df_melted.drop_duplicates(subset=['telefono'])

        # --------> Agregar columna con fecha y hora de ejecución
        df_melted['upload_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # --------> Guardar en la base de datos en bloques
        chunk_size = 10000
        with engine.begin() as connection:
            for i in range(0, len(df_melted), chunk_size):
                chunk = df_melted.iloc[i:i + chunk_size]
                chunk.to_sql(tabla_destino, connection, if_exists='append', index=False)
                print(f"Se insertó un bloque de registros desde el índice {i} hasta {i + len(chunk)}")

        print(f"Datos insertados en la tabla {tabla_destino}")

    except SQLAlchemyError as e:
        print(f"Error en la conexión con la base de datos: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    limpiar_tabla(tabla_destino)
    time.sleep(1)
    coalesce_proceso(tabla_destino, query)
    print("Proceso Finalizado")