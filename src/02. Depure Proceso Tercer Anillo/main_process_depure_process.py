# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:21:54 2024

@author: Emerson.Aguilar
"""

import os
import subprocess
import time

ruta_dir_scripts = r'C:\Users\Emerson.Aguilar\.spyder-py3\01.Campanas\02.Claro - Prioritarias\02.Reversion_Movil\depure_proceso'

scripts = [
    'web_exporte_marcaciones_rever.py',
    'ejec_sp_01_marcaciones_desgloce_dts_today.py',
    'ejec_sp_depurador_desgloce_today.py'
    ]

def correr_scripts(ruta_dir_scripts, scripts):
    for script in scripts:
        script_path = os.path.join(ruta_dir_scripts, script)
        print(f"script {script} ejecutandose")
        try:
            subprocess.run(["Python", script_path], check=True)
            print(f"Finalizo ejecucion de script {script}")
        except subprocess.CalledProcessError as e:
            print(f"error al ejecutar script {script} por {e}")
            time.sleep(3)
    else: 
             print(f"script {script} no se encuentra en {ruta_dir_scripts}")

correr_scripts(ruta_dir_scripts, scripts)