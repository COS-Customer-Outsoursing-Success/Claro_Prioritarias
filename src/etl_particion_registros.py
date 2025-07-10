"""
CREATED BY EMERSON AGUILAR CRUZ
"""

import pandas as pd
import os
from datetime import datetime

# -------> Rutas Compartidas
ruta_archivo = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\19. Axa\Depuracion\listas_vicidial\cargar'
ruta_salida = ruta_archivo  # Puedes cambiar si quieres otro destino

# -------> Fecha Formateada
fecha_formateada = datetime.now().strftime('%Y%m%d')
print(f"Fecha actual: {fecha_formateada}")

# -------> Crear carpeta si no existe
os.makedirs(ruta_salida, exist_ok=True)

# -------> Buscar primer archivo Excel en la carpeta
archivos = [f for f in os.listdir(ruta_archivo) if f.endswith('.xlsx') or f.endswith('.xls')]
if not archivos:
    raise FileNotFoundError("No se encontró ningún archivo Excel en la ruta indicada.")

archivo_excel = os.path.join(ruta_archivo, archivos[0])
nombre_columna_particionar = 'campana'

def particionar_por_columna(archivo_excel):

    print(f"Arhchivo De Excel A Procesar: {archivo_excel}")
    df = pd.read_excel(archivo_excel)

    # -------> Validar columna
    if nombre_columna_particionar not in df.columns:
        raise ValueError(f"La columna {nombre_columna_particionar} no existe en el archivo.")

    # -------> Agrupar y guardar archivos
    for campaign_id, grupo in df.groupby(nombre_columna_particionar):
        nombre_archivo = f"{str(campaign_id).replace('/', '_')} - {fecha_formateada}.csv"
        ruta_guardado = os.path.join(ruta_salida, nombre_archivo)
        grupo.to_csv(ruta_guardado, index=False)
        print(f"Archivo guardado: {ruta_guardado}")

    os.remove(archivo_excel)
    print(f"Archivo General: {archivo_excel} Eliminado Con exito") 

if __name__ == '__main__':

    print("Comenzando Proceso De Particion de archivos segun campaign_id")
    particionar_por_columna(archivo_excel)
    print("Proceso Terminado Con Exito")
