r"""
CREATED BY \\ EMERSON AGUILAR CRUZ \\

--------------- VERSION PARA UTILIZAR EN CONJUNTO A LA TORRE DE CONTROL O DATA ANALYST ---------------
--------------- VERSION PARA UTILIZAR EN CONJUNTO A LA TORRE DE CONTROL O DATA ANALYST ---------------

NOTA 1: ANTES DE LA EJECUCION DE ESTE CODIGO ES NECESARIO CREAR LAS CARPETAS A CONTINUACION EN EL
        DISCO LOCAL C:
        DICHAS CARPETAS SON:
            [ chrome_driver = C:\Users\usuario_red\Documents\chromedriver.exe]
            [ C:\Users\usuario_red\Documents\03.BOTS\IMG\02.Recuperacion\00. Depurador]
            [ C:\Users\usuario_red\Documents\03.BOTS\IMG\02.Recuperacion\00. Depurador\captura_cargue_vicidial.png]

NOTA 2: RECUERDE EN CASO DE SER NECESARIO CAMBIAR VARIABLES INDICADAS AL INICIO DEL CODIGO COMO LO 
        SON:
            [USUARIO DE RED]
            [CREDENCIALES DE SQL]
            [CONFIGRACIONES DE VICIDIAL (CAMPAÑA, MAXIMA LISTA PERMITIDA, INDICATIVO, FORMATO COPIAR,
             CREDENCIALES DE VICIDIAL, ETC)]

NOTA 3: ¿QUE FALTA?:
        [AÑADIR MAS PRINTS]
        [VERIFICAR UNA FORMA DE NO UTILIZAR LA CARPETA COMPARTIDA Y SOLO DISCO LOCAL]
"""

# -----------> USUARIO DE RED <-----------
usuario_red = 'emerson.aguilar'

# -----------> LIBRERIAS UTILIZADAS
import pandas as pd
import time
import glob
import os
import win32com.client
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
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

fecha_actual = datetime.now().strftime('%Y-%m-%d')

# -----------> CHROME DRIVER
chrome_driver = rf'C:\Users\{usuario_red}\Documents\chromedriver.exe'

# -----------> RUTAS DE CARPETA COMPARTIDA
ruta_depurador = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\01.Recuperacion\Procesos\01. Depuracion_Recu\Depurador Bot\depurador_recuperacion.xlsx'

rutas_eliminar = [
                r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\01.Recuperacion\Procesos\01. Depuracion_Recu\Depurador Bot',
                rf'C:\Users\{usuario_red}\Documents\03.BOTS\IMG\02.Recuperacion\00. Depurador'
                ]

ruta_cargue_vicidial = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\01.Recuperacion\Procesos\01. Depuracion_Recu\Cargar Vicidial\Cargar'

ruta_cargado_vicidial = rf'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\01.Recuperacion\Procesos\01. Depuracion_Recu\Cargar Vicidial\Cargues\{fecha_actual}'

ruta_imagen = rf'C:\Users\{usuario_red}\Documents\03.BOTS\IMG\02.Recuperacion\00. Depurador\captura_cargue_vicidial.png'

archivos = os.listdir(ruta_cargue_vicidial)

# -----------> FILTRAR ARCHIVOS XLSX
archivos_xlsx = [archivo for archivo in archivos if archivo.endswith(".xlsx")]

#---------------------------------------------------------
# -----------> CONSULTA DEPURADOR GENERAL SQL <-----------
#--------------------------------------------------------- 
query = text("""
SELECT * FROM bbdd_cos_bog_claro_recuperacion.tb_depurador_general_recuperacion_dts
ORDER BY cant_marcaciones ASC, Probabilidad DESC
;
""")

#---------------------------------------------------------------------------------------
# -----------> \\CONFIGURACIONES DE VICIDIAL\\CONFIGURACIONES DE VICIDIAL\\ <-----------
# -----------> \\CONFIGURACIONES DE VICIDIAL\\CONFIGURACIONES DE VICIDIAL\\ <-----------
#---------------------------------------------------------------------------------------

# -----------> CREDENCIALES VICIDIAL
usuario_vicidial = '1031120694'
contrasena_vicidial = '103112069400'

# -----------> CAMPAÑA DE VICIDIAL
campana_vicidial = 'CAR'

# -----------> LINK DE VICIDIAL SEGUN CAMPAÑA CORRESPONDA
link_vicidial = rf"https://{usuario_vicidial}:{contrasena_vicidial}@miosapp.groupcos.com/vicidial/admin.php?ADD=34&campaign_id={campana_vicidial}"

# ----------->  NUMERO MAXIMO DE LISTAS PERMITIDAS
numero_maximo_listas = 48388

# -----------> DEJAR LISTA ACTIVA
activo = 'NO'

# -----------> OPCION DE COPIADO DE CAMPOS PERSONALIZADOS (APPEND, INSERT, REPLACE)
opcion_copiado = 'REPLACE'

# -----------> INDICATIVO PAIS 
indicativo_pais = '57 - COL'

# ------------------------------------------------------------------------------------------
# -----------> ESTRUCTURA PARA PARTE FINAL DE VICIDIAL EN CAMPOS PERSONALIZADOS <-----------
# ------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# ----------->  DEFINICION DE XPATHS PARA PROCESO DE CARGUE DE LISTAS <-----------
#---------------------------------------------------------------------------------
xpath_boton_listas = "//tr[contains(@onclick, 'admin.php?ADD=100')]"
xpath_crear_lista = "//tr[contains(@onclick, 'admin.php?ADD=111')]"
xpath_lista_id = '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[1]/td[2]/input'
xpath_name = '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[2]/td[2]/input'
xpath_list_description = '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[3]/td[2]/input'
xpath_campaign = '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[4]/td[2]/select'
xpath_active = '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[5]/td[2]/select'
xpath_submit_crear = '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[6]/td/input'
xpath_copiar_campos = "//tr[contains(@onclick, 'admin_lists_custom.php?action=COPY_FIELDS_FORM')]"
xpath_copiar_desde_lista = '/html/body/center/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[1]/td[2]/select'
xpath_copiar_a_lista = '/html/body/center/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[2]/td[2]/select'
xpath_opcion_de_copiado = '/html/body/center/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[3]/td[2]/select'
xpath_submit_copiar = '/html/body/center/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[4]/td/input'
xpath_cargar_contactos = "//tr[contains(@onclick, 'admin_listloader_fourth_gen.php')]"
xpath_adjuntar_archivo = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input'
xpath_list_id_cargar = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td[2]/font/select'
xpath_indicativo_pais = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[3]/td[2]/font/select'
xpath_plantilla_personalizado = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[4]/td[2]/font/input[2]'
xpath_submit_enviar_contactos = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[12]/td/input[1]'
xpath_tabla_final_vicidial="/html/body/table[2]/tbody/tr/td/form/table/tbody/tr"
xpath_submit_cargar_final = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[36]/th/input[1]'

# --------------------------------------------------------------------------------------------------
# -----------> COLUMNAS A UTILIZAR EN LA TRANSFORMACION DE DATOS PARA SUBIR EN VICIDIAL <-----------
# --------------------------------------------------------------------------------------------------
columnas_subir_vicidial = [
            'cuenta',
            'telefono',    
            'cantidad_servicios',    
            'nombre_cliente',    
            'ciudad',    
            'paquete',    
            'estrato',    
            'fecha_solicitud',    
            'Novedad',
        ]
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
# -----------> \\\\ CODIGO INICIA SIN VARIABLES EXPLICITAS DENTRO \\\\ <-----------
# -----------> \\\\ CODIGO INICIA SIN VARIABLES EXPLICITAS DENTRO \\\\ <-----------
# -----------> \\\\ CODIGO INICIA SIN VARIABLES EXPLICITAS DENTRO \\\\ <-----------
# -----------> \\\\ CODIGO INICIA SIN VARIABLES EXPLICITAS DENTRO \\\\ <-----------
# -----------> \\\\ CODIGO INICIA SIN VARIABLES EXPLICITAS DENTRO \\\\ <-----------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
def eliminar_archivos_ruta(rutas_eliminar):
    try:
        for ruta in rutas_eliminar:
            archivos = glob.glob(os.path.join(ruta, '*'))  # Obtiene todos los archivos
            for archivo in archivos:
                os.remove(archivo)
                print(f'Archivo eliminado: {archivo}')
    except Exception as e:
        print(f'Error al eliminar archivos: {e}')

def depurador_general():
    try:
        print("\n🔄 Conectando a la base de datos añañai...") 
        engine = create_engine(cadena_de_conexion)
        time.sleep(1)
        
        with engine.begin() as conn:
            print("🔎 Ejecutando consulta, espere socio...")
            time.sleep(1)
            df = pd.read_sql(query, conn)

        # Validación de resultados
        if df.empty:
            print("⚠️ La consulta no devolvió resultados mi so.")
            return None
        else:
            print(f"✅ Consulta finalizada con éxito. {len(df)} registros obtenidos.")
            return df

    except SQLAlchemyError as e:
        print(f"❌ Error al ejecutar la consulta: {e}")
        return None

def estrategia_marcador():
    df_resultado = depurador_general()
    if df_resultado is not None:
        print("\n📊 Primeros 5 registros:")
        print(df_resultado.head())

        try:
            df_resultado.to_excel(ruta_depurador, index=False)
            print(f"📁 Archivo guardado en: {ruta_depurador}")
        except Exception as e:
            print(f"❌ Error al guardar el archivo Excel: {e}")
            return  # Si hay error, detener ejecución breveee?

    # Verifica si el archivo existe y es un archivo .xlsx, si no F 
    reintentos_abrir_excel = 3  # Número máximo de intentos

    if ruta_depurador.endswith('.xlsx') and os.path.exists(ruta_depurador):
        print("✅ Abriendo el archivo en Excel...")

        try:
            # Inicializa Excel sin alertas
            excel = win32com.client.Dispatch("Excel.Application")
            excel.DisplayAlerts = False
            excel.AskToUpdateLinks = False
            excel.Visible = True

            # Verifica si el archivo ya está abierto
            for libro in excel.Workbooks:
                if libro.FullName.lower() == ruta_depurador.lower():
                    print("📄 El archivo ya está abierto en Excel.")
                    break
            else:
                # Intentar abrir con reintentos
                for intento in range(1, reintentos_abrir_excel + 1):
                    try:
                        libro = excel.Workbooks.Open(ruta_depurador)
                        print(f"📄 Archivo abierto en intento {intento}. Puedes editarlo manualmente.")
                        print("⚠️ Recuerda copiar lo necesario en otro libro y guardarlo en la ruta de cargue a vicidial. Ciérralo manualmente cuando termines.")
                        break  # Sale del bucle si el archivo se abre con éxito
                    except Exception as e:
                        print(f"⚠️ Intento {intento} fallido: {e}")
                        time.sleep(2)  # Espera antes de reintentar
                else:
                    print("❌ No se pudo abrir el archivo después de varios intentos.")
                    excel.Quit()  # Cierra Excel solo si no se pudo abrir

        except Exception as e:
            print(f"❌ Error crítico al manejar Excel: {e}")
            excel.Quit()  # Cierra Excel en caso de error grave

def cargar_vicidial():
    
    if archivos_xlsx:
        nombre_archivo_cargue = archivos_xlsx[0]  # Toma el primer archivo encontrado
        print("Nombre del archivo encontrado:", nombre_archivo_cargue)
    else:
        print("No se encontró ningún archivo .xlsx en la carpeta")
    if not archivos_xlsx:
        print("No se encontró ningún archivo .xlsx en la carpeta")
        return

    nombre_archivo_cargue = archivos_xlsx[0]
    ruta_archivo_cargue = f'{ruta_cargue_vicidial}\{nombre_archivo_cargue}'
    
    chrome_options = Options()
    service = Service(executable_path=chrome_driver)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    try:
        driver.get(link_vicidial)
        print("Página cargada correctamente.")
        
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, "last_list_statuses")))
        values = element.get_attribute("value").split('|')
        
        list_numbers = [int(val) for i, val in enumerate(values) if i % 2 == 0 and val.isdigit()]
        if not list_numbers:
            raise ValueError("No se encontraron números en la lista de cargue.")
        
        max_list = max(list_numbers)
        print(f"Lista de cargue más alta: {max_list}")
        
        if max_list >= numero_maximo_listas:
            print("El número de lista excede el máximo asignado. Validar con telecomunicaciones.")
            return

        # Crear lista
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_boton_listas))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_crear_lista))).click()
        time.sleep(2)
        
        campos = [
            (xpath_lista_id, max_list+1),
            (xpath_name, nombre_archivo_cargue),
            (xpath_list_description, nombre_archivo_cargue),
            (xpath_campaign, campana_vicidial),
            (xpath_active, activo)
        ]
        
        for xpath, valor in campos:
            campo = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            campo.send_keys(valor)
            print(f"Campo {xpath} llenado con: {valor}")
            time.sleep(1)
        
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_submit_crear))).click()
        time.sleep(2)
        
        # Copiar configuración
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_copiar_campos))).click()
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_copiar_desde_lista))).send_keys(max_list)
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_copiar_a_lista))).send_keys(max_list+1)
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_opcion_de_copiado))).send_keys(opcion_copiado)
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_submit_copiar))).click()
        time.sleep(2)
        
        # Cargar archivo
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cargar_contactos))).click()
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_adjuntar_archivo))).send_keys(ruta_archivo_cargue)
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_list_id_cargar))).send_keys(f"{max_list+1} - {nombre_archivo_cargue}")
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_indicativo_pais))).send_keys(indicativo_pais)
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_plantilla_personalizado))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_submit_enviar_contactos))).click()
        time.sleep(5)
        
        # Mapeo de datos
        mapping = {
            "VENDOR LEAD CODE:": '"cuenta"',
            "SOURCE ID:": '"cuenta"',
            "PHONE NUMBER:": '"telefono"',
            "CUENTA:": '"cuenta"',
            "NOMBRE:": '"nombre_cliente"',
            "FECHASOLICITUD:": '"fecha_solicitud"',
            "SERVICIOSACANCELAR:": '"cantidad_servicios"',
            "CIUDAD:": '"ciudad"',
            "ESTRATO:": '"estrato"',
            "SERVICIO ACTUAL:": '"paquete"',
            "OFRECIMIENTO:": '"Novedad"',
            "BASEGESTION:": '"Novedad"',
            "CELULAR:": '"telefono"'
        }

        # Esperar la tabla correctamente
        tabla = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr/td/form/table/tbody/tr"))
        )
        print("✅ Tabla encontrada.")

        # Intentar encontrar todas las filas que tienen bgcolor="#69D3E0" (para omitir el encabezado)
        filas = driver.find_elements(By.XPATH, "//tr[@bgcolor='#69D3E0']")

        print(f"🔍 Total de filas encontradas: {len(filas)}")

        # Recorrer las filas y asignar valores del mapping
        for i, fila in enumerate(filas):
            columnas = fila.find_elements(By.TAG_NAME, "td")

            # Asegurar que la fila tiene al menos dos columnas (nombre del campo y select)
            if len(columnas) < 2:
                continue  

            clave = columnas[0].text.strip()  # Obtener el texto de la primera columna

            try:
                select_element = columnas[1].find_element(By.TAG_NAME, "select")  # Obtener el select
                
                if clave in mapping:
                    valor_a_seleccionar = mapping[clave]  # Obtener el valor del mapping
                    select_element.send_keys(valor_a_seleccionar)  # Insertar valor en el select
                    print(f'✅ {clave} asignado a {valor_a_seleccionar}')
                else:
                    print(f'⚠️ {clave} no está en el mapping, se deja vacío.')
            
            except Exception as e:
                print(f'❌ Error en {clave}: {e}')

        boton_submit_cargar_final = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_submit_cargar_final))
        )
        boton_submit_cargar_final.click()

        time.sleep(1)
        
        print(f"Esperando Cargue final de lista")
        boton_cargado = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/table[2]/tbody/tr/td/table/tbody/tr[9]/td/form/font'))
        )

        boton_cargado.click()
        print("Lista Cargada Sin Problema")
        time.sleep(2)

        # --------> Captura de pantalla desde selenium
        imagen = driver.get_screenshot_as_file(ruta_imagen)
        print(f"Captura guardada en: {ruta_imagen}")
        
    except Exception as e:
        print(f"Error en el proceso: {e}")
    finally:
        time.sleep(2)
        driver.quit()

            # --------> Mover archivo procesado a la carpeta de cargados
        try:
            if not os.path.exists(ruta_cargado_vicidial):
                os.makedirs(ruta_cargado_vicidial)

            nueva_ruta = os.path.join(ruta_cargado_vicidial, nombre_archivo_cargue)
            os.rename(ruta_archivo_cargue, nueva_ruta)
            print(f"Archivo movido a {nueva_ruta}")

        except Exception as e:
            print(f"Error moviendo el archivo: {e}")

if __name__ == "__main__":
    while True:
        print("\nOpciones:")
        print("1 - Eliminar archivos y continuar en orden")
        print("2 - Ejecutar estrategia de marcador y continuar en orden")
        print("3 - Cargar Vicidial directamente")
        print("4 - Ejecutar todo en orden desde el inicio")
        print("5 - Salir sin ejecutar nada")

        opcion = input("Elige una opción (1/2/3/4/5/6): ").strip()

        if opcion == "1":
            eliminar_archivos_ruta(rutas_eliminar)
            estrategia_marcador()

        elif opcion == "2":
            estrategia_marcador()

        elif opcion == "3":
            cargar_vicidial()
            continue  # ---------> No ejecuta nada más

        elif opcion == "4":
            eliminar_archivos_ruta(rutas_eliminar)
            estrategia_marcador()

        elif opcion == "5":
            print("Saliendo del programa...")
            break  # ---------> Termina el bucle y no ejecuta nada

        else:
            print("Opción no válida, intenta de nuevo.")
            continue  # ---------> Vuelve a preguntar sin ejecutar nada

        # ---------> Pregunta solo después de estrategia_marcador
        if opcion in ["1", "2", "4"]:
            while True:
                respuesta = input("🛠️ ¿Ya terminaste? Escribe 'SI' para continuar, 'NO' para esperar o 'SALIR' para salir del programa: ").strip().upper()
                
                if respuesta == "SI":
                    break  # Sale del bucle si la respuesta es válida
                
                if respuesta == "SALIR":
                    print("🚪 Saliendo del programa... ¡Hasta luego!")
                    quit()  # Finaliza la ejecución
                
                print("⚠️ Respuesta no válida. Debes escribir 'SI', 'NO' o 'SALIR'. Intenta de nuevo.")


        cargar_vicidial()