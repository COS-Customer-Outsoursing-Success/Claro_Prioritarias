r"""
CREATED BY \\ EMERSON AGUILAR CRUZ \\
"""
# -----------> LIBRERIAS UTILIZADAS
import time
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# -----------> USUARIO DE RED
usuario_red = 'emerson.aguilar'

# -----------> Formateo De Fechas

fecha_actual = datetime.now().strftime("%Y-%m-%d")

# -----------> CREDENCIALES VICIDIAL
usuario_vicidial = '1031120694'
contrasena_vicidial = '103112069400'

# -----------> CHROME DRIVER
chrome_driver = rf'C:\Users\{usuario_red}\Documents\chromedriver.exe'

# -----------> RUTAS DE CARPETA COMPARTIDA
ruta_cargue_vicidial = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\19. Axa\Depuracion\listas_vicidial\cargar'

ruta_cargado_vicidial = rf'Z:\WORKFORCE\03. Mission\Emerson Aguilar\19. Axa\Depuracion\listas_vicidial\cargado\{fecha_actual}'

rutas_eliminar = [
                rf'C:\Users\{usuario_red}\Documents\git_hub\Axa\Falabela\data\img\cargue_listas'
                ]

# -----------> LISTAR ARCHIVOS EN RUTA
archivos = os.listdir(ruta_cargue_vicidial)

# -----------> FILTRAR ARCHIVOS XLSX
archivos_xlsx = [archivo for archivo in archivos if archivo.endswith(".xlsx")]

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
# -----------> \\CONFIGURACIONES DE VICIDIAL\\CONFIGURACIONES DE VICIDIAL\\ <-----------
# -----------> \\CONFIGURACIONES DE VICIDIAL\\CONFIGURACIONES DE VICIDIAL\\ <-----------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

# -----------> SERVIDOR VICIDIAL
servidor_vcdl = '172.70.7.37'

# -----------> DEJAR LISTA ACTIVA
activo = 'N'

# -----------> INDICATIVO PAIS 
indicativo_pais = '57 - COL'

# -----------> OPCION COPIAR
opcion_copiado = 'APPEND'

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
xpath_submit_cargar_final = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[45]/th/input[1]'
xpath_tabla_campos_personalizados = "/html/body/table[2]/tbody/tr/td/form/table/tbody/tr"
xpath_cargado_final = '/html/body/table[2]/tbody/tr/td/table/tbody/tr[9]/td/form/font'

# --------------------------------------------------------------------------------------------------
# -----------> COLUMNAS A UTILIZAR EN LA TRANSFORMACION DE DATOS PARA SUBIR EN VICIDIAL <-----------
# --------------------------------------------------------------------------------------------------
mapping = {
#    "VENDOR LEAD CODE:": '"COLOCAR_ACA"',
#    "SOURCE ID:": '"COLOCAR_ACA"',
    "PHONE NUMBER:": '"telefono"',
    "TITLE:": '"placa"',
    "FIRST NAME:": '"No_Documento"',
#    "MIDDLE INITIAL:": '"COLOCAR_ACA"',
#    "LAST NAME:": '"propietario_de_la_cuenta"',
    "ADDRESS1:": '"No_Documento"',
    "ADDRESS2:": '"placa"',
#    "ADDRESS3:": '"direccion"',
#    "CITY:": '"ciudad"',
#    "STATE:": '"ciudad"',
#    "PROVINCE:": '"ciudad"',
#    "POSTAL CODE:": '"ciudad"',
#    "COUNTRY CODE:": '"ciudad"',
#    "GENDER:": '"ciudad"',
#    "DATE OF BIRTH:": '"ciudad"',
    "EMAIL:": '"correo_electronico_corporativo"',
#    "PROVINCE:": '"ciudad"',
#    "PROVINCE:": '"ciudad"',
#    "PROVINCE:": '"ciudad"',
#    "PROVINCE:": '"ciudad"',
"TIPO DOCUMENTO:": '"Tipo_Documento"',
"DOCUMENTO:": '"Documento"',
"NOMBRE:": '"Nombre"',
"PLACA:": '"Placa"',
"ASEGURADORA ACTUAL:": '"Aseguradora_Actual"',
"MARCA:": '"Marca"',
"TELEFONO 1:": '"Telefono_1"',
"FECHA VIGENCIA:": '"Fecha_vigencia"',
"NO TEMPORARIO PLUS:": '"No_Temporario_Plus"',
"NO TEMPORARIO TRADICIONAL:": '"No_Temporario_Tradicional"',
"PRIMA TEMPORARIO PLUS:": '"Prima_Temporario_Plus"',
"PRIMASINIVA TEMPORARIO PLUS:": '"PrimaSinIVA_Temporario_Plus"',
"PRIMA TRADICIONAL:": '"Prima_Tradicional"',
"PRIMASINIVA TRADICIONAL:": '"PrimaSinIVA_Tradicional"',
"NO TEMPORARIO VIP:": '"No_Temporario_VIP"',
"PRIMA VIP:": '"Prima_VIP"',
"PRIMA SINI VA VIP:": '"Prima_SinI_VA_VIP"',
"TELFONO 2:": '"Telfono_2"',
"TELFONO 3:": '"Telfono_3"',
"SUMA ASEGURADA:": '"Suma_asegurada"',

}

# -----------------------------------------------------------------------------------
# -----------> \\\\ CODIGO INICIA SIN VARIABLES EXPLICITAS DENTRO \\\\ <-----------
# -----------------------------------------------------------------------------------

configuracion_campanas = {
    "AXA_FAL2": {
        "campana_vicidial": "AXA_FAL2",
        "campaign_id": "AXA_FAL2 - 212",
        "numero_maximo_listas": 32768914
    },
    "AXA_FAL3": {
        "campana_vicidial": "AXA_FAL3",
        "campaign_id": "AXA_FAL3 - 212",
        "numero_maximo_listas": 35037827
    },
    "AXA_FAL4": {
        "campana_vicidial": "AXA_FAL3",
        "campaign_id": "AXA_FAL3 - 212",
        "numero_maximo_listas": 37306741
    },
    "AXA_FAL5": {
        "campana_vicidial": "AXA_FAL5",
        "campaign_id": "AXA_FAL5 - 212",
        "numero_maximo_listas": 39575654
    },
    "AXA_FAL6": {
        "campana_vicidial": "AXA_FAL6",
        "campaign_id": "AXA_FAL6 - 212",
        "numero_maximo_listas": 41844568
    },
    "AXA_FAL7": {
        "campana_vicidial": "AXA_FAL7",
        "campaign_id": "AXA_FAL7 - 212",
        "numero_maximo_listas": 44113481
    },
    "AXA_FAL8": {
        "campana_vicidial": "AXA_FAL8",
        "campaign_id": "AXA_FAL8 - 212",
        "numero_maximo_listas": 46382395
    },
    "AXA_FA10": {
        "campana_vicidial": "AXA_FA10",
        "campaign_id": "AXA_FA10 - 212",
        "numero_maximo_listas": 48651308
    },
    "AXA_FA11": {
        "campana_vicidial": "AXA_FA11",
        "campaign_id": "AXA_FA11 - 212",
        "numero_maximo_listas": 50920222
    },
    
    
}

# -----> LISTAR ARCHIVOS EN CARPETA
def lectura_nombres_archivos():
    try:
        archivos = os.listdir(ruta_cargue_vicidial)
        print(f"📁 Archivos encontrados en la ruta '{ruta_cargue_vicidial}': {archivos}")
    except FileNotFoundError:
        print(f"❌ Error: La ruta '{ruta_cargue_vicidial}' no existe.")
        exit()

# -----------> FILTRAR ARCHIVOS XLSX
archivos_xlsx = [archivo for archivo in archivos if archivo.endswith(".csv")]
print(f"📄 Archivos .xlsx encontrados: {archivos_xlsx}")

def eliminar_archivos_ruta():
    try:
        for ruta in rutas_eliminar:
            if os.path.exists(ruta):
                archivos = glob.glob(os.path.join(ruta, '*'))
                for archivo in archivos:
                    os.remove(archivo)
                    print(f'Archivo eliminado: {archivo}')
            else:
                print(f'Ruta no encontrada: {ruta}')
    except Exception as e:
        print(f'Error al eliminar archivos: {e}')

def configurar_chrome(driver_path):
    print("🌐 Configurando Chrome WebDriver...")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")

    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    print("✅ Chrome WebDriver configurado correctamente.")
    return driver

def cargar_vicidial():

    print("Eliminando imagenes en ruta cargar")
    eliminar_archivos_ruta()
    
    if not archivos_xlsx:
        print("⚠️ No se encontró ningún archivo .xlsx en la carpeta")
        return

    for nombre_archivo_cargue in archivos_xlsx:
        print(f"\n📦 Procesando archivo: {nombre_archivo_cargue}")
        ruta_archivo_cargue = os.path.join(ruta_cargue_vicidial, nombre_archivo_cargue)
        driver = configurar_chrome(chrome_driver)

        try:
            nombre_archivo = nombre_archivo_cargue.split('-')[0].strip()
            if nombre_archivo not in configuracion_campanas:
                nombre_archivo = nombre_archivo_cargue.split(' -')[0].strip()

            if nombre_archivo in configuracion_campanas:
                config = configuracion_campanas[nombre_archivo]
                campana_vicidial = config["campana_vicidial"]
                campaign_id = config["campaign_id"]
                numero_maximo_listas = config["numero_maximo_listas"]
                link_vicidial = rf"http://{usuario_vicidial}:{contrasena_vicidial}@{servidor_vcdl}/vicidial/admin.php?ADD=34&campaign_id={campana_vicidial}"

                print(f"🎯 Configuración obtenida para campaña: {campana_vicidial}")
                print(f"🔗 Abriendo Vicidial: {link_vicidial}")
                driver.get(link_vicidial)
                print("✅ Página cargada correctamente.")
            else:
                print(f"❌ Campaña no encontrada para el archivo: {nombre_archivo}")
                driver.quit()
                continue

            wait = WebDriverWait(driver, 60)
            print("⏳ Esperando lista de cargue existente...")
            element = wait.until(EC.presence_of_element_located((By.ID, "last_list_statuses")))
            values = element.get_attribute("value").split('|')
            list_numbers = [int(val) for i, val in enumerate(values) if i % 2 == 0 and val.isdigit()]
            if not list_numbers:
                raise ValueError("No se encontraron números en la lista de cargue.")

            max_list = max(list_numbers)
            print(f"🔢 Lista de cargue más alta detectada: {max_list}")

            if max_list >= numero_maximo_listas:
                for _ in range(7):
                    print("⚠️ Advertencia: El número de lista excede el máximo asignado. Validar con telecomunicaciones.")
                driver.quit()
                continue

            print("📝 Creando nueva lista...")
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_boton_listas))).click()
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_crear_lista))).click()
            time.sleep(2)

            campos = [
                (xpath_lista_id, max_list+1),
                (xpath_name, f"{max_list+1} - {campana_vicidial}"),
                (xpath_list_description, f"{max_list+1} - {campana_vicidial}"),
                (xpath_campaign, campaign_id),
                (xpath_active, activo)
            ]
            for xpath, valor in campos:
                print(f"✍️ Llenando campo {xpath} con valor: {valor}")
                campo = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                campo.send_keys(valor)
                time.sleep(1)

            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_submit_crear))).click()
            print("📋 Lista creada exitosamente.")
            time.sleep(1)
            
            print("Copiando campos personalizados")
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
            
            print("📁 Iniciando carga de archivo...")
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cargar_contactos))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_adjuntar_archivo))).send_keys(ruta_archivo_cargue)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_list_id_cargar))).send_keys(f"{max_list+1} - {max_list+1} - {campana_vicidial}")
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_indicativo_pais))).send_keys(indicativo_pais)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_plantilla_personalizado))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_submit_enviar_contactos))).click()

            print("🧬 Esperando tabla de campos personalizados...")
            tabla = WebDriverWait(driver, 600).until(
                EC.presence_of_element_located((By.XPATH, xpath_tabla_campos_personalizados))
            )
            print("✅ Tabla encontrada.")
            
            time.sleep(3)
            
            filas = driver.find_elements(By.XPATH, "//tr[@bgcolor='#69D3E0']")
            print(f"📊 Total de filas de campos personalizados encontradas: {len(filas)}")

            for i, fila in enumerate(filas):
                columnas = fila.find_elements(By.TAG_NAME, "td")
                if len(columnas) < 2:
                    continue

                clave = columnas[0].text.strip()

                try:
                    select_element = columnas[1].find_element(By.TAG_NAME, "select")
                    if clave in mapping:
                        valor_a_seleccionar = mapping[clave]
                        select_element.send_keys(valor_a_seleccionar)
                        print(f'✅ {clave} asignado a {valor_a_seleccionar}')
                    else:
                        print(f'⚠️ {clave} no está en el mapping, se deja vacío.')
                except Exception as e:
                    print(f'❌ Error en asignación del campo {clave}: {e}')

            print("📤 Enviando para el cargue final...")
            boton_submit_cargar_final = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, xpath_submit_cargar_final))
            )
            boton_submit_cargar_final.click()

            time.sleep(1)
            
            print("⏳ Esperando finalización de carga...")
            boton_cargado = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.XPATH, xpath_cargado_final))
            )
            boton_cargado.click()
            print("✅ Lista Cargada Sin Problema")

            ruta_imagen = rf'C:\Users\{usuario_red}\Documents\git_hub\Axa\Falabela\data\img\cargue_listas\{nombre_archivo_cargue}.png'

            imagen = driver.get_screenshot_as_file(ruta_imagen)
            print(f"📸 Captura guardada en: {ruta_imagen}")

        except Exception as e:
            print(f"❌ Error general durante el proceso: {e}")

        time.sleep(5)

        try:
            print("📁 Moviendo archivo procesado a la carpeta de 'Cargados'...")
            if not os.path.exists(ruta_cargado_vicidial):
                os.makedirs(ruta_cargado_vicidial)
                print(f"📂 Carpeta {ruta_cargado_vicidial} creada.")

            nueva_ruta = os.path.join(ruta_cargado_vicidial, nombre_archivo_cargue)
            if not os.path.exists(nueva_ruta):
                os.rename(ruta_archivo_cargue, nueva_ruta)
                print(f"✅ Archivo {nombre_archivo_cargue} movido a {nueva_ruta}")
            else:
                print(f"⚠️ El archivo {nombre_archivo_cargue} ya existe en la carpeta de cargados.")

        except Exception as e:
            print(f"❌ Error al mover el archivo: {e}")
        finally:
            print("🚪 Cerrando navegador.")
            driver.quit()

if __name__ == '__main__':
    cargar_vicidial()