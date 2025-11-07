# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:34:35 2024

@author: Emerson.Aguilar
"""

import os
import time
import subprocess

usuario_red = 'emerson.aguilar'

ruta_dir_scripts = rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\01. Recuperacion\02. Depure Proceso'

scripts = [
    "sql_ejec_sps_depurador_general.py",
    "clean_data_depurador_general_CAR.py"
        ]

def run_scripts(ruta_dir_scripts, scripts):
    for script in scripts:
        script_path = os.path.join(ruta_dir_scripts, script)
        if os.path.exists(script_path):
            print(f"ejecutando Script: {script}")
            try:
                subprocess.run(["python", script_path], check=True)
                print(f"Finalizó la ejecucion de {script}")
            except subprocess.CalledProcessError as e:
                print(f"Error al ejectuar {script}: {e}")
                time.sleep(3)
        else:
                print(f"el script {script} no existe")
run_scripts(ruta_dir_scripts, scripts)
