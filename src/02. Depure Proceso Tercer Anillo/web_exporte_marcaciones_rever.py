# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:33:41 2024

@author: Emerson.Aguilar
"""

# Created By Emerson Aguilar Cruz

import os
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# Credenciales y cadena de conexión
usuario = 'emersonaguilar0694'
contrasena = 'gBXJ,!cW!4yUqPIlTKA8'
host = '172.70.7.61'
base_de_datos = 'bbdd_cos_bog_claro_reversion_movil'
tabla = 'tb_marcaciones_depure_today'
cadena_de_conexion = f'mysql+pymysql://{usuario}:{contrasena}@{host}/{base_de_datos}'

# Crear el motor de conexión
engine = create_engine(cadena_de_conexion)
# fechas_formateadas -------------------------------------------------------------------

fecha = datetime.now()
fecha_formateada = fecha.strftime("%d-%m-%Y")
fecha_actual = datetime.now().strftime("%Y-%m-%d")
# Variables Rutas
url_vcdl = 'http://1031120694:wfm1031120694@172.70.7.56/vicidial/call_report_export.php'  
ruta_compartida = rf'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\03.Tercer_Anillo_Reversion\Procesos\Marcaciones\{fecha_formateada}'


class VicidialDescargaMarcaciones:
    def __init__(self, url, download_path):
        self.url = url
        self.download_path = download_path
        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {'download.default_directory': download_path}
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def clear_table(self, tabla):
        try:
            with engine.connect() as conn:
                conn.execute(text(f"DELETE FROM {base_de_datos}.{tabla}"))
                conn.execute(text("COMMIT"))
            print(f"Todos los registros eliminados de la tabla '{tabla}'.")
        except SQLAlchemyError as e:
            print(f"Error al eliminar registros de la tabla: {e}")

    def load_page_with_retry(self, max_attempts=3):
        attempt = 0
        while attempt < max_attempts:
            try:
                self.driver.get(self.url)
                print("Página cargada exitosamente.")
                return True
            except Exception as e:
                print(f"Error al cargar la página. Reintentando... Intento {attempt + 1}: {e}")
                attempt += 1
                time.sleep(3)
        return False

    def remove_existing_files(self):
        for filename in os.listdir(self.download_path):
            file_path = os.path.join(self.download_path, filename)
            if os.path.isfile(file_path) and not filename.endswith('.crdownload'):
                os.remove(file_path)
                print(f"Archivo existente '{filename}' eliminado.")

    def download_report(self):
        try:
            if not self.load_page_with_retry():
                print("No se pudo cargar la página después de varios intentos. Verifica la conexión y vuelve a intentarlo.")
                return
            
            wait = WebDriverWait(self.driver, 15)
            # Selección del primer <select>
            select1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[1]/select[8]')))
            select1.click()
    
            select2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[1]/select[8]/option[1]')))
            select2.click() 
            
            select3 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[1]/select[8]/option[2]')))
            select3.click()
            
            select_xpath_2 = '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[2]/center/select'
            
            select_element_2 = wait.until(EC.element_to_be_clickable((By.XPATH, select_xpath_2)))
            select_2 = Select(select_element_2)
            
            select_2.select_by_visible_text("REVERANI")
            select_2.select_by_visible_text("SANILLO")

            select6 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[3]/center/select/option[1]')))
            select6.click()
    
            select7 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[4]/center/select/option[1]')))
            select7.click()
            
            select8 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[5]/center/select/option[1]')))
            select8.click()
    
            select9 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[1]/td[6]/center/select/option[1]')))
            select9.click()
    
            self.remove_existing_files()
    
            download_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vicidial_report"]/table/tbody/tr[3]/td/input')))
            download_link.click()
    
            download_complete = False
            timeout = 200  
            start_time = time.time()
            while not download_complete and time.time() - start_time < timeout:
                if any(filename.endswith('.txt') for filename in os.listdir(self.download_path)):
                    download_complete = True
                else:
                    print("Esperando que la descarga finalice...")
                    time.sleep(1)
    
            if download_complete:
                print("La descarga se completó correctamente.")
                self.process_downloaded_file()
            else:
                print("La descarga no se ha completado dentro del tiempo esperado.")
    
        except TimeoutException:
            print("Error: Tiempo de espera agotado al cargar la página. Recargando la página...")
            self.load_page_with_retry()
            self.download_report()

    def process_downloaded_file(self):
        for filename in os.listdir(self.download_path):
            if filename.endswith('.txt'):
                txt_file_path = os.path.join(self.download_path, filename)
                
                # Esperar hasta que el archivo .crdownload desaparezca
                crdownload_file_path = txt_file_path + ".crdownload"
                while os.path.exists(crdownload_file_path):
                    print("Esperando que la descarga finalice completamente...")
                    time.sleep(1)
                
                df = pd.read_csv(txt_file_path, delimiter='\t', low_memory=False)  # Ajusta el delimitador según el formato de tu archivo .txt

                # Subir DataFrame a la base de datos
                df.to_sql(tabla, engine, if_exists='append', index=False)
                print(f"Datos subidos a la tabla '{tabla}' en la base de datos '{base_de_datos}'.")

                os.remove(txt_file_path)
                print(f"Archivo original '{txt_file_path}' eliminado.")

    def close_browser(self):
        self.driver.quit()

if __name__ == "__main__":
    url = url_vcdl
    download_path = ruta_compartida
    
    # Crear la carpeta del día actual si no existe
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    downloader = VicidialDescargaMarcaciones(url, download_path)
    # Limpiar la tabla antes de cualquier otro proceso
    downloader.clear_table(tabla)
    downloader.download_report()
    downloader.close_browser()
