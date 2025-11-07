# -- coding: utf-8 --
"""
@Author: Emerson.Aguilar
@Edit: Ronald. Barberi
"""

import time
import win32com.client
from PIL import ImageGrab
import psutil
import os
import glob

#---------------------------------------------------------------------------------
# ------------> VARIABLES A CAMBIAR SEGUN CASO CORRESPONDAAAA --------------------
#---------------------------------------------------------------------------------

usuario_red = 'emerson.aguilar'

archivo = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\04.Informes\01. Cos Performance\01.Informe_Cos_Performance_Claro_Prioritarias_Buck.xlsx'

hojas_captura = ['Ausentismo_Adherencia', 
                 'Ocupacion_Utilizacion', 
                 'Comportamiento_Auxiliares'
                 ]

rangos_captura = ['B2:V47', 
                  'B2:V47', 
                  'B2:V47' 
                  ]

rutas_destino_img = [
                rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Correos\Cos Performance\Img\Ausentismo_Adherencia.png',
                rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Correos\Cos Performance\Img\Ocupacion_Utilizacion.png',
                rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Correos\Cos Performance\Img\Comportamiento_Auxiliares.png'
                    ]

rutas_eliminar = [
                rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Correos\Cos Performance'
                ]


#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------V------------------------------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------------------------------------------------------
#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------V------------------------------

def eliminar_archivos_ruta(rutas_eliminar):
    try:
        for ruta in rutas_eliminar:
            archivos = glob.glob(os.path.join(ruta, '*'))  # Obtiene todos los archivos
            for archivo in archivos:
                os.remove(archivo)
                print(f'Archivo eliminado: {archivo}')
    except Exception as e:
        print(f'Error al eliminar archivos: {e}')

def matar_excel():
    print("Los archivos de Excel se cerrarán en 3 segundos. Cuenta regresiva iniciada.")
    
    for i in range(1, 0, -1):
        print(f"Tiempo restante: {i} segundos", end='\r')  
        time.sleep(1)
    
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'EXCEL.EXE':
            pid = process.info['pid']
            process = psutil.Process(pid)
            process.terminate()
            print(f"Proceso de Excel (PID: {pid}) terminado.")
            
def exportar_imagenes(archivo, hojas_captura, rangos_captura, rutas_destino_img):
    excel = win32com.client.Dispatch('Excel.Application')
    excel.Visible = False
    excel.WindowState = 3
    print("Ejecutando Captura De Imagenes Con Excel Oculto")
    
    try:
        libro = excel.Workbooks.Open(archivo)
        print("Abriendo Excel")
        for hoja_captura, rango_captura, ruta_destino_img in zip(hojas_captura, rangos_captura, rutas_destino_img): 
            hoja = libro.Worksheets(hoja_captura)
            hoja.Activate()
            print("Hojas Activas Comenzando Capturas")
            captura_rango = hoja.Range(rango_captura)
            if captura_rango and captura_rango.Cells.Count > 0:
                captura_rango.CopyPicture(Format =2)
                time.sleep(3)
        
            img = None
            
            for _ in range(3):
                img = ImageGrab.grabclipboard()
                if img:
                    break
                time.sleep(3)
            
            if img:
                img.save(ruta_destino_img, 'PNG')
                print(f"imagen guardada correctamente en {ruta_destino_img}")

            else:
                print(f"Rango No valido o Vacio en la hoja {hoja_captura}")
    except Exception as e:
        print(f"Error Con la captura debido a {e}")


if __name__ == '__main__':
    
    eliminar_archivos_ruta(rutas_eliminar)
    matar_excel()
    exportar_imagenes(archivo, hojas_captura, rangos_captura, rutas_destino_img)
