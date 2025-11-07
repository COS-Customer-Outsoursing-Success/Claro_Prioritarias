# -*- coding: utf-8 -*-
"""
@author: Emerson.Aguilar
"""
import os
import time
import subprocess

usuario_red = 'Emerson.Aguilar'
ruta_dir_scripts = rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\scripts\04. Correos\00. Envio Informes\Recuperacion\Cos Performance'

scripts = [
    "xlsx_export_img.py",
    "env_cos_performance.py"
          ]

def correr_scripts(scripts):
    for script in scripts:
        script_path = os.path.join(ruta_dir_scripts, script)
        if os.path.exists(script_path):
            print(f"Ejecutando script {script}")
            try:
                subprocess.run(["python", script_path], check=True)
                print(f"Finalizo Ejecucion Script {script}")
            except Exception as e:
                print(f"Error Con La ejecucion debido a {e}")
                time.sleep(3)
        else:
                print(f"Error Script {script} no se encuentra")
if __name__ == '__main__':
    correr_scripts(scripts)
