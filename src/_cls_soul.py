"""
CREATED BY Emerson Aguilar Cruz
"""
import os
import time
from pathlib import Path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from web_scraping._cls_webscraping import WebScraping_Chrome


mapping = {
"Primer Nombre": "Primer Nombre",
"Segundo Nombre": "Segundo Nombre",
"Primer Apellido": "Primer Apellido",
"Segundo Apellido": "Segundo Apellido",
"Tipo de documento": "Tipo de documento",
"No. Documento": "No. Documento",
"Teléfono": "Teléfono",
"Correo electrónico": "Correo electrónico",
"Fecha Nacimiento": "Fecha Nacimiento",
"Cod Municipio": "Cod Municipio",
"Departamento": "Departamento",
"Ciudades": "Ciudades",
"Cod Departamento": "Cod Departamento",
"Genero": "Genero",
"Dirección": "Dirección",
"Teléfono 2": "Teléfono 2",
"Teléfono 3": "Teléfono 3",
"Placa": "Placa",
"Fecha Fin vigencia Actual": "Fecha Fin vigencia Actual",
"Fecha Inicio Nueva Vigencia": "Fecha Inicio nueva vigencia",
"Modelo": "Modelo",
"Línea": "Línea",
"Cod Fasecolda": "Cod Fasecolda",
"suma aseguadora": "Suma aseguradora",
"Prima Plus": "Prima plus",
"Prima sin IVA Plus": "Prima sin Iva Plus",
"N° Temporario 1 plus": "N Temporario 1 plus",
"Prima Tradicional": "Prima TRADICIONAL",
"Prima sin IVA TRADICIONAL": "Prima Sin Iva TRADICIONAL",
"N° Temporario 1 TRADICIONAL": "N° Temporario 1 TRADICIONAL",
"Prima Autosuficiente": "Prima AUTOSUFICIENTE",
"Prima sin IVA AUTOSUFICIENTE": "Prima sin Iva AUTOSUFICIENTE",
"N° Temporario AUTOSUFICIENTE": "N Temporario AUTOSUFICIENTE",
"Prima con IVA Aseguradora Actual": "Prima con IVA Aseguradora Actual",
"Diferencia con la Aseguradora Actual": "Diferencia con la Aseguradora Actual",
"Clase de vehiculo": "Clase de vehículo",
"Servicio": "Servicio",
"Marca": "Marca",
"Aseguradora Actual": "Aseguradora Actual"

    }

class FormulariosSoul():

    def __init__(self, usuario=None, contrasena=None, archivo_excel=None):

        self.current_folder = os.path.dirname(os.path.abspath(__file__))
        print(self.current_folder)

        self.project_root = os.path.dirname(self.current_folder)
        print(self.project_root)

        self.path_home = str(Path.home())
        self.driver_path = os.path.join(
            self.path_home,
            'Documents',
            'chromedriver.exe'
        )

        self.url = 'https://mysoul.groupcos.com/login'
        
        self.usuario = 'eaguilar84' # usuario
        self.contrasena = 'Bruno.1908+++++' # contrasena
        
        self.crm = 'CRM' # 'CRM2'
        self.nombre_formulario = 'AXA Falabella V2'
        
        self.ruta_formulario = os.path.join(self.project_root, 'data', 'upload_soul', 'Falabella')
        os.makedirs(self.ruta_formulario, exist_ok=True)

        for archivo in os.listdir(self.ruta_formulario):
            if archivo.lower().endswith(('.xlsx', '.xls')):
                self.archivo_excel = os.path.join(self.ruta_formulario, archivo )
                break

        else: 
            self.archivo_excel = None

    def buscar_formulario(self):

        try:
            driver = WebScraping_Chrome.Webdriver_ChrDP(self.driver_path)
            WebScraping_Chrome.WebScraping_Acces(driver, self.url)
            
            WebScraping_Chrome.WebScraping_WaitCSS(driver, 150, 'input[formcontrolname="user"]')
            WebScraping_Chrome.WebScraping_SendKeysCSS(driver, 'input[formcontrolname="user"]', self.usuario) 

            WebScraping_Chrome.WebScraping_WaitCSS(driver, 150, 'input[formcontrolname="password"]')
            WebScraping_Chrome.WebScraping_SendKeysCSS(driver, 'input[formcontrolname="password"]', self.contrasena) 
            time.sleep(1)

            WebScraping_Chrome.WebScraping_WaitCSS(driver, 150, 'button[type="submit"][color="primary"]')
            WebScraping_Chrome.WebScraping_ClickCSS(driver, 'button[type="submit"][color="primary"]')

            WebScraping_Chrome.WebScraping_WaitTextCSS(driver, 150, 'a.mat-list-item.mat-menu-trigger', 'Menú')
            WebScraping_Chrome.WebScraping_ClickByTextCSS(driver, 'a.mat-list-item.mat-menu-trigger', 'Menú')
            time.sleep(1)

            WebScraping_Chrome.WebScraping_WaitTextCSS(driver, 150, 'button.mat-focus-indicator[mat-menu-item]', 'Aplicaciones')
            WebScraping_Chrome.WebScraping_ClickByTextCSS(driver, 'button.mat-focus-indicator[mat-menu-item]', 'Aplicaciones')
            time.sleep(1)

            WebScraping_Chrome.WebScraping_WaitTextCSS(driver, 150, 'button.mat-focus-indicator[mat-menu-item]', self.crm)
            WebScraping_Chrome.WebScraping_ClickByTextCSS(driver, 'button.mat-focus-indicator[mat-menu-item]', self.crm)
            time.sleep(1)

            WebScraping_Chrome.WebScraping_WaitClickableCSS(driver, 150, 'a.mat-list-item.mat-focus-indicator')
            driver.refresh()
            
            WebScraping_Chrome.WebScraping_WaitClickableCSS(driver, 150, 'a.mat-list-item.mat-focus-indicator')
            WebScraping_Chrome.WebScraping_ClickByTextCSS(driver, 'a.mat-list-item.mat-focus-indicator', 'Formularios')
            time.sleep(1)

            WebScraping_Chrome.WebScraping_ScrollIntoViewCSS(driver, 'mat-select')
            WebScraping_Chrome.WebScraping_WaitClickableCSS(driver, 10, 'mat-select')
            WebScraping_Chrome.WebScraping_ClickCSS(driver, 'mat-select')
            time.sleep(1)

            WebScraping_Chrome.WebScraping_WaitClickableCSS(driver, 10, 'mat-option .mat-option-text')
            WebScraping_Chrome.WebScraping_ClickByTextCSS(driver, 'mat-option .mat-option-text', '100')
            time.sleep(1)

            WebScraping_Chrome.WebScraping_WaitCSS(driver, 150, 'input[formcontrolname="search"]')
            WebScraping_Chrome.WebScraping_SendKeysCSS(driver, 'input[formcontrolname="search"]', self.nombre_formulario)
            time.sleep(1)

        except Exception as e:
             print(f"Error: Error al buscar el formulario debido a {e}")
        
        self.driver = driver
        return self.driver
    
    def cargar_formulario(self):

        try:
            WebScraping_Chrome.WebScraping_WaitClickableCSS(self.driver, 150, 'button[aria-label="Toggle menu"]')
            WebScraping_Chrome.WebScraping_ClickCSS(self.driver, 'button[aria-label="Toggle menu"]')
            time.sleep(1)
        
            WebScraping_Chrome.WebScraping_WaitClickableCSS(self.driver, 150, 'button.mat-menu-item')
            WebScraping_Chrome.WebScraping_ClickByTextCSS(self.driver, 'button.mat-menu-item', 'Crear base de datos')
            time.sleep(1)

            file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
            file_input.send_keys(self.archivo_excel)
        
        except Exception as e:
            print(f"Error: Error al cargar el formulario debido a {e}")
        
        WebScraping_Chrome.WebScraping_WaitClickableCSS(self.driver, 150, 'div.row.col-8')
        rows = self.driver.find_elements(By.CSS_SELECTOR, 'div.row.col-8')

        for row in rows:
            label_text = None
            try:
                label_elem = row.find_element(By.CSS_SELECTOR, '.col-4 .box__white')
                label_text = label_elem.text.strip()

                if label_text in mapping:
                    try:
                        select_elem = row.find_element(By.CSS_SELECTOR, 'mat-select')
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", select_elem)
                        select_elem.click()
                        time.sleep(0.5)

                        option_text = mapping[label_text]
                        option_elem = self.driver.find_element(
                            By.XPATH,
                            f"//mat-option//span[normalize-space(text())='{option_text}']"
                        )
                        option_elem.click()
                        time.sleep(0.3)

                    except Exception as e:
                        print(f"Error: No se pudo seleccionar opción para '{label_text}': {e}")

                else:
                    print(f"Etiqueta '{label_text}' no está en el mapping, se omite.")

            except Exception as e:
                print(f"Error: Error procesando fila (etiqueta: {label_text}): {e}")
  
        WebScraping_Chrome.WebScraping_WaitCSS(self.driver, 150, 'button[type="submit"][color="primary"]')
        WebScraping_Chrome.WebScraping_ClickCSS(self.driver, 'button[type="submit"][color="primary"]')
        time.sleep(1)

        WebScraping_Chrome.WebScraping_WaitCSS(self.driver, 150, 'mat-radio-button[value="false"]')
        WebScraping_Chrome.WebScraping_ClickCSS(self.driver, 'mat-radio-button[value="false"]')
        time.sleep(1)

        WebScraping_Chrome.WebScraping_WaitCSS(self.driver, 10, 'button[type="submit"][color="primary"].continue-button')
        WebScraping_Chrome.WebScraping_ClickCSS(self.driver, 'button[type="submit"][color="primary"].continue-button')
        time.sleep(1)

        WebScraping_Chrome.WebScraping_WaitTextCSS(self.driver, 150, 'mat-radio-button .mat-radio-label-content', 'Reemplazar y actualizar')
        WebScraping_Chrome.WebScraping_ClickByTextCSS(self.driver, 'mat-radio-button .mat-radio-label-content', 'Reemplazar y actualizar')
        time.sleep(1)

        WebScraping_Chrome.WebScraping_WaitCSS(self.driver, 150, 'button[type="button"][color="primary"].continue-button')
        WebScraping_Chrome.WebScraping_ClickCSS(self.driver, 'button[type="button"][color="primary"].continue-button')
        time.sleep(1)

        WebScraping_Chrome.WebScraping_WaitTextCSS(self.driver, 150, 'button.swal2-confirm.swal2-styled', 'Aceptar')
        WebScraping_Chrome.WebScraping_ClickByTextCSS(self.driver, 'button.swal2-confirm.swal2-styled', 'Aceptar')
        time.sleep(1)

        WebScraping_Chrome.WebScraping_WaitTextCSS(self.driver, 700, 'button.swal2-confirm.swal2-styled', 'Aceptar')
        WebScraping_Chrome.WebScraping_ClickByTextCSS(self.driver, 'button.swal2-confirm.swal2-styled', 'Aceptar')
        time.sleep(1)
        print("Proceso SOUL Terminado")

if __name__ == '__main__':

    procesor = FormulariosSoul()
    procesor.buscar_formulario()
    procesor.cargar_formulario()