import mysql.connector
from mysql.connector import Error
import time

# Variables de conexión
HOST = '172.70.7.61'
DATABASE = 'bbdd_cos_bog_claro_reversion_movil'
USER = 'emersonaguilar0694'
PASSWORD = 'gBXJ,!cW!4yUqPIlTKA8'

def ejecutar_sp():
    try:
        # Establecer conexión a la base de datos
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # Ejecutar el procedimiento almacenado
            cursor.callproc('sp_depurador_desgloce_today')
            print("Procedimiento almacenado ejecutado exitosamente.")

            # Esperar 5 segundos para asegurar que los datos se inserten
            time.sleep(10)

            # Consultar el número de registros en la tabla de destino
            cursor.execute("SELECT COUNT(*) FROM tb_marcaciones_desgloce_dts_depure_today")
            count = cursor.fetchone()[0]
            print(f"Número de registros en tb_marcaciones_desgloce_dts_today: {count}")

            # Confirmar si se insertaron datos correctamente
            if count > 0:
                print("Datos insertados correctamente.")
            else:
                print("No se encontraron datos insertados en tb_marcaciones_desgloce_dts_today.")

            # Confirmar la transacción
            connection.commit()

    except Error as e:
        print(f"Error al ejecutar el procedimiento almacenado: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")

# Llamar a la función con el número de días deseado
ejecutar_sp(    )


