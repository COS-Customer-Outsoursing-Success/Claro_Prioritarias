"""""
Created By Emerson Aguilar Cruz
"""""

import os
import sys
import pandas as pd
import time
from datetime import datetime

current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_folder)
sys.path.append(current_folder)

from excel_app._cls_excel_auto_manager import Process_Excel, Envio_Pdc_Wpp, EnvioErrorPdc
from vicidial._cls_scraping_detalle_agente import DetalleAgenteVcdl
from conexiones_db._cls_sqlalchemy import MySQLConnector
import json

config_path = os.path.join(project_root, 'config', 'config_pdc.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)
    
config_pdc_chubb = config["config_pdc_chubb"]

parametro_num_day = 1    
sql_file_path = os.path.join(project_root, 'sql', '_sql_max_call_date_chubb.sql')

def main():
  
    # -- Config Servidor --
    schema = config_pdc_chubb["schema"]
    table = 'tb_detalle_agente_daily_new_dts' # -----> Esto no se cambia

    stored_procedures = config_pdc_chubb["stored_procedures"] 
    
    # -- Config Vcdl --
    user_vcdl = '1031120694' # -----> Esto no se cambia
    pass_vcdl = 'wfm1031120694' # -----> Esto no se cambia
    
    server_vcdl = config_pdc_chubb["server_vcdl"]
    
    campanas_vcdl = config_pdc_chubb["campanas_vcdl"]

    download_path = os.path.join(project_root, 'data', 'detalle_agente', config_pdc_chubb["campana"])

    # -- Config Excel --
    archivo_excel = config_pdc_chubb["archivo_excel"]

    ruta_img = os.path.join(project_root, 'data', 'img', 'pdc', config_pdc_chubb["campana"])
    ruta_txt = os.path.join(project_root, 'data', 'txt', 'pdc', config_pdc_chubb["campana"])

    # -- Config Imagenes y Grupos --
    var_captura_img = config_pdc_chubb["var_captura_img"]

    # -- Inicializador de clases -- 
    processor_detalle_ag = DetalleAgenteVcdl(

        schema=schema, 
        table=table,
        user_vcdl=user_vcdl,
        pass_vcdl=pass_vcdl,
        server_vcdl=server_vcdl,
        campanas_vcdl=campanas_vcdl, 
        download_path=download_path

    )

    # -- Inicializador de clases -- 
    processor_excel = Process_Excel(
        schema=schema,
        stored_procedures=stored_procedures,
        archivo_excel=archivo_excel,
        var_captura_img=var_captura_img,
        ruta_img=ruta_img,
        ruta_txt=ruta_txt
    )

    # -- Ejecucion de funciones -- 
    processor_envio_wpp = Envio_Pdc_Wpp(processor_excel)
    
    try:
        processor_detalle_ag.eliminar_archivos_ruta()
        processor_detalle_ag.descargar_reporte()
        processor_detalle_ag.process_downloaded_file()
        processor_detalle_ag.load_data()
    except Exception as e:
        print(f"❌ Error en el proceso principal: {str(e)}")

     #-- Ejecucion de funciones -- 
    try:
        processor_excel.ejecutar_sps()
        processor_excel.delete_archivos_ruta()
        excel, libro = processor_excel.refresh_archivo_excel()
        processor_excel.exportar_imagenes_excel(excel, libro)
        processor_excel.copiar_celdas_txt(excel, libro)
    except Exception as e:
        print(f"❌ Error en el proceso principal: {str(e)}")
    
    try:
        processor_envio_wpp.env_pdc_bot()
    except Exception as e:
        print(f"❌ Error en el proceso de envio wpp: {str(e)}")

# -- Funcion Lectura de Marcaciones -- 
def leer_query(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:     
            return file.read()
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo en {path}")
        raise
    except Exception as e:
        print(f"Error al leer el archivo SQL: {str(e)}")
        raise

# -- Funcion de envio mensaje de error --     
def env_error():
    
    tabla_alerta = config_pdc_chubb["tabla_alerta"]
    
    engine = MySQLConnector().get_connection(database='bbdd_config')
    print("Consultando maxima hora de actualizacion")

    query_max = leer_query(sql_file_path)
    print(f"Consulta leída, ejecutando...")

    df = pd.read_sql(query_max, engine)
    df['hora_ultima_llamada'] = pd.to_datetime(df['hora_ultima_llamada'], errors='coerce')
    df['hora_ultima_llamada'] = df['hora_ultima_llamada'].fillna(pd.to_datetime('00:00:00'))

    hora_ultima_llamada = df['hora_ultima_llamada'].iloc[0].strftime('%H:%M')
    print(f"Hora última llamada: {hora_ultima_llamada}")

    hora_actual = datetime.now().strftime('%H:%M')
    print(f"Hora actual: {hora_actual}")

    hora_ultima = datetime.strptime(hora_ultima_llamada, '%H:%M')
    hora_actual_obj = datetime.strptime(hora_actual, '%H:%M')

    diferencia_minutos = (hora_actual_obj - hora_ultima).total_seconds() / 60
    print(f"Diferencia en minutos: {diferencia_minutos:.2f}")

    processor_env_error = EnvioErrorPdc(
        tabla_alerta=tabla_alerta,
        diferencia_minutos=diferencia_minutos
        )
    
    try:
        processor_env_error.bot_envio_error()
    except Exception as e:
        print(f"❌ Error en el proceso de envio wpp: {str(e)}")

# -- If final que indica que enviar si no actualiza la tabla de marcaciones -- 
if __name__ == '__main__':

    engine = MySQLConnector().get_connection(database='bbdd_config')
    print("Consultando maxima hora de actualizacion")

    query_max = leer_query(sql_file_path)
    print(f"Consulta leída, ejecutando...")
    
    intentos = 0
    intentos_max =  7 
    intervalo_max = 40
    intervalo_consulta = 140
    processor_excel = None

    while intentos < intentos_max:
        print(f"Intento {intentos + 1} de {intentos_max}")
        try:
            df = pd.read_sql(query_max, engine)
            df['hora_ultima_llamada'] = pd.to_datetime(df['hora_ultima_llamada'], errors='coerce')
            df['hora_ultima_llamada'] = df['hora_ultima_llamada'].fillna(pd.to_datetime('00:00:00'))

            hora_ultima_llamada = df['hora_ultima_llamada'].iloc[0].strftime('%H:%M')
            print(f"Hora última llamada: {hora_ultima_llamada}")

            hora_actual = datetime.now().strftime('%H:%M')
            print(f"Hora actual: {hora_actual}")

            hora_ultima = datetime.strptime(hora_ultima_llamada, '%H:%M')
            hora_actual_obj = datetime.strptime(hora_actual, '%H:%M')

            diferencia_minutos = (hora_actual_obj - hora_ultima).total_seconds() / 60
            print(f"Diferencia en minutos: {diferencia_minutos:.2f}")

            if diferencia_minutos < intervalo_max:
                print(f"Diferencia menor a {intervalo_max} minutos, ejecutando MAIN proceso PDC")
                main()
                break
            else:
                print(f"Diferencia mayor o igual a {intervalo_max} minutos, esperando {intervalo_consulta/60} minutos e intentando nuevamente...")
                intentos += 1
                time.sleep(intervalo_consulta)
        except Exception as e:
            print(f"Error al realizar consulta debido a: {e}")
            intentos += 1
            time.sleep(intervalo_consulta)

    if intentos == intentos_max:
        print("Maximos intentos realizados, enviando mensaje de error")
        env_error()