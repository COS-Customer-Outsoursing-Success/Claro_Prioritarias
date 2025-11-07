# -*- coding: utf-8 -*-
"""
@author: Emerson.Aguilar
"""

# -----------> USUARIO DE RED <-----------
usuario_red = 'emerson.aguilar'

import subprocess
import os
import time

ruta_dir_scripts = rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\scripts\01. Recuperacion\00. Propension'

scripts = [
    'sql_ejec_sps_propension.py',
    'process_borrar_archivos.py',
    'mlearning_regresion_logistica.py',
    'sql_ejec_sps_probabilidad.py'
    ]


def correr_scripts(ruta_dir_scripts,scripts):
    for script in scripts:
        script_path = os.path.join(ruta_dir_scripts, script)
        print(f"script {script} ejecutandose")
        try:
            subprocess.run(["Python", script_path], check=True)
            print(f"Finalizo ejecucion de script {script}")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar script {script} por erro {e}") 
            time.sleep(3)

    else:
            print(f"script {script} no se encuentra en la ruta {ruta_dir_scripts}")

if __name__ == "__main__":
    correr_scripts(ruta_dir_scripts, scripts)