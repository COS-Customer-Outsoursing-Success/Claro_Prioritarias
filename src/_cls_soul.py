"""
CREATED BY Emerson Aguilar Cruz
"""
import os
import time
from pathlib import Path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from web_scraping._cls_webscraping import WebScraping_Chrome

class FormulariosSoul():

    def __init__(self, usuario=None, contrasena=None, archivo_excel=None):

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
        
        self.archivo_excel = archivo_excel

    
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

            WebScraping_Chrome.WebScraping_WaitCSS(self.driver, 10, 'input[accept*="application/vnd.ms-excel"]')
            elem = self.driver.find_element(By.CSS_SELECTOR, 'input[accept*="application/vnd.ms-excel"]')
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", elem)
            elem.send_keys(self.archivo_excel)
            time.sleep(20)

        except Exception as e:
            print(f"Error: Error al cargar el formulario debido a {e}")

if __name__ == '__main__':

    procesor = FormulariosSoul()
    procesor.buscar_formulario()
    procesor.cargar_formulario()