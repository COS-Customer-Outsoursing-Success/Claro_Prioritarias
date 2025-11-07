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
"""
# -----------> USUARIO DE RED <-----------
usuario_red = 'crismar.quintero'

# -----------> LIBRERIAS UTILIZADAS
import os
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# -------- CONFIGURACIÓN --------
ruta_cargue_vicidial = r"Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\03.Tercer_Anillo_Reversion\Procesos\01. Depuracion_Rever\Cargar Vicidial\Pendientes"
ruta_destino_base = r"Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\03.Tercer_Anillo_Reversion\Procesos\01. Depuracion_Rever\Cargar Vicidial\Cargues"
chromedriver_path = r"C:\Users\crismar.quintero\Documents\chromedriver-win64\chromedriver.exe"
url_vicidial = "http://tuvicidial.local"

# -------- BUSCAR ARCHIVO --------
hoy = datetime.now().strftime("%Y-%m-%d")
archivos = [f for f in os.listdir(ruta_cargue_vicidial) if f.endswith(".xlsx")]

if not archivos:
    print("❌ No se encontró ningún archivo en la carpeta de cargue.")
    exit()

nombre_archivo_cargue = archivos[0]
ruta_archivo_cargue = os.path.join(ruta_cargue_vicidial, nombre_archivo_cargue)

print(datetime.now().strftime("%Y-%m-%d"))
print(f"📂 Nombre del archivo encontrado: {nombre_archivo_cargue}")

# -------- CONFIGURAR CHROME --------
service = Service(chromedriver_path)
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # silenciar logs molestos
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

try:
    # -------- ABRIR VICIDIAL --------
    driver.get(url_vicidial)
    print("✅ Página cargada correctamente.")

    # -------- EJEMPLO: CARGAR LISTA --------
    # Aquí deberías poner los XPATHs correctos según tu HTML
    max_list = 59610  # deberías calcularlo en tu lógica real
    xpath_lista_id = "/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/form/center/table/tbody/tr[1]/td[2]/input"
    campo_lista = wait.until(EC.presence_of_element_located((By.XPATH, xpath_lista_id)))
    campo_lista.send_keys(str(max_list + 1))
    print(f"✅ Campo {xpath_lista_id} llenado con: {max_list+1}")

    # -------- MAPPING DE CAMPOS --------
    mapping = {
        "VENDOR LEAD CODE:": "phone",
        "SOURCE ID:": "phone",
        "PHONE NUMBER:": "phone",
        "NOMBRE:": "nombre_cliente",
        "TELE NUMB:": "phone",
        "IDENTIFICACION:": "identificacion",
        "REGION UBICACION:": "region",
        "CORREOEMAIL:": "email",
        "DIRECCION:": "direccion",
        "CIUDAD UBICACION:": "ciudad",
    }

    # Extendido para evitar ⚠️
    mapping.update({
        "TITLE:": "",
        "FIRST NAME:": "nombre_cliente",
        "MIDDLE INITIAL:": "",
        "LAST NAME:": "nombre_cliente",
        "ADDRESS1:": "direccion",
        "ADDRESS2:": "",
        "ADDRESS3:": "",
        "CITY:": "ciudad",
        "STATE:": "region",
        "PROVINCE:": "region",
        "POSTAL CODE:": "",
        "COUNTRY CODE:": "",
        "GENDER:": "",
        "DATE OF BIRTH:": "",
        "ALT PHONE:": "phone",
        "EMAIL:": "email",
        "SECURITY PHRASE:": "",
        "COMMENTS:": "",
        "RANK:": "",
        "OWNER:": ""
    })

    # -------- TABLA DE ASIGNACIÓN --------
    xpath_tabla = "/html/body/center/table[2]/tbody/tr/td/table/tbody"  # cambia según tu HTML real
    tabla = wait.until(EC.presence_of_element_located((By.XPATH, xpath_tabla)))
    filas = tabla.find_elements(By.TAG_NAME, "tr")
    print(f"✅ Tabla encontrada. Total filas: {len(filas)}")

    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if len(celdas) < 2:
            continue

        clave = celdas[0].text.strip()
        select_element = celdas[1].find_element(By.TAG_NAME, "select")
        valor = mapping.get(clave, "")

        try:
            if valor:
                select = Select(select_element)
                select.select_by_visible_text(valor)
                print(f"✅ {clave} asignado a \"{valor}\"")
            else:
                print(f"⚠️ {clave}: sin mapping (dejado vacío)")
        except Exception as e:
            print(f"❌ {clave}: error {e}")

    # -------- BOTÓN SUBMIT --------
    try:
        xpath_boton = "/html/body/center/table[3]/tbody/tr/td/form/input[1]"  # cambia al real
        boton_submit = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_boton)))
        boton_submit.click()
        print("✅ Botón de envío clickeado.")
    except Exception as e:
        print(f"⚠️ No se pudo hacer click en submit: {e}")

except Exception as e:
    print(f"❌ Error en el proceso: {e}")

finally:
    driver.quit()
    print("✅ Navegador cerrado.")

    # -------- MOVER ARCHIVO --------
    ruta_destino = os.path.join(ruta_destino_base, hoy)
    os.makedirs(ruta_destino, exist_ok=True)
    shutil.move(ruta_archivo_cargue, os.path.join(ruta_destino, nombre_archivo_cargue))
    print(f"📂 Archivo movido a {ruta_destino}")
