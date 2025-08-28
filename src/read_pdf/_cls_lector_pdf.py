"""
CREATED BY EMERSON AGUILAR CRUZ
"""

import fitz  # PyMuPDF
import os
import shutil
import pandas as pd
from datetime import datetime
from conexiones_db._cls_sqlalchemy import MySQLConnector
from  load_data._cls_load_data import *
import json

class LeerPdf:

    def __init__(self, periodo=None):
        
        self.current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_root = os.path.dirname(self.current_folder)

        self.config_json_pdf = os.path.join(self.project_root, 'config', 'config_pdf.json')
        with open(self.config_json_pdf, 'r', encoding='utf-8') as json_pdf:
            config_pdf = json.load(json_pdf)

        print("\nCampañas disponibles:")
        for idx, camp in enumerate(config_pdf.keys(), start=1):
            print(f"{idx}: {camp}")

        while True:
            try:
                seleccion = int(input("Ingrese el número de la campaña: "))
                if 0 <= seleccion < len(config_pdf.keys()):
                    campana = list(config_pdf.keys())[seleccion - 1]
                    break
                else:
                    print("Índice fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Debes ingresar un número.")

        self.config_pdf = config_pdf[campana]


        self.mapeo_campos = {
            tuple(map(int, k.strip("()").split(","))): v
            for k, v in self.config_pdf["mapeo_campos"].items()
        }

        self.ruta_pdf_dir = os.path.join(self.project_root, 'data', 'pdf', 'nuevo', self.config_pdf['campana'])
        os.makedirs(self.ruta_pdf_dir, exist_ok=True)

        self.ruta_cargados = os.path.join(self.project_root, 'data', 'pdf', 'cargado', self.config_pdf['campana'])
        os.makedirs(self.ruta_cargados, exist_ok=True)

        self.archivos_pdf = []

        if self.ruta_pdf_dir and not self.archivos_pdf:
            self.archivos_pdf = [
                os.path.join(self.ruta_pdf_dir, f)
                for f in os.listdir(self.ruta_pdf_dir)
                if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(self.ruta_pdf_dir, f))
            ]

        if not self.archivos_pdf:
            print("No se encontraron archivos PDF en el directorio.")
            return

        self.ruta_pdf = None
        self.df = None
        self.periodo = periodo
        
        self.schema = self.config_pdf['schema']
        self.table =  self.config_pdf['table']
        self.engine = MySQLConnector().get_connection(database=self.schema)
        self.loader = MySQLLoader(self.engine, self.schema, self.table) 

    def imprimir_lineas_pdf(self):
        if not self.ruta_pdf:
            raise ValueError("No se ha seleccionado ningún PDF.")
        with fitz.open(self.ruta_pdf) as doc:
            for page_num, page in enumerate(doc, start=1):
                print(f"\nPágina {page_num}")
                lines = page.get_text().splitlines()
                for i, line in enumerate(lines):
                    print(f"{i:02d}: {line}")

    def obtener_pdf(self):
        pdf_validos = []

        for ruta in self.archivos_pdf:
            if os.path.exists(ruta) and ruta.lower().endswith('.pdf'):
                # mover cada PDF al directorio de cargados
                destino = os.path.join(self.ruta_cargados, os.path.basename(ruta))
                shutil.move(ruta, destino)
                pdf_validos.append(destino)
                print(f"PDF movido a: {destino}")
            else:
                print(f"Archivo no válido o no encontrado: {ruta}")

        if not pdf_validos:
            print("No se encontraron archivos PDF válidos.")
            return None

        # ahora devuelve la lista completa, no solo el primero
        return pdf_validos

    def obtener_informacion(self):

        if not self.ruta_pdf:
            raise ValueError("No se ha seleccionado ningún PDF.")
        
        data_extraida = {}

        with fitz.open(self.ruta_pdf) as doc:
            for pagina_num, pagina in enumerate(doc, start=1):
                lines = pagina.get_text().splitlines()
                for i, line in enumerate(lines):
                    clave = (pagina_num, i)
                    if clave in self.mapeo_campos:
                        campo = self.mapeo_campos[clave]
                        valor = line.strip()
                        data_extraida[campo] = valor
                        print(f"{pagina_num}:{i:02d} -> {campo} = {valor}")

        if data_extraida:
        
            self.df = pd.DataFrame([data_extraida])

            self.df['fecha_solicitud'] = (
            self.df['anho_solicitud'].astype(str) +
            self.df['mes_solicitud'].astype(str).str.zfill(2) +
            self.df['dia_solicitud'].astype(str).str.zfill(2)
            )

            self.df['fecha_solicitud'] = pd.to_datetime(self.df['fecha_solicitud'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
            
            self.df = self.df.drop(columns=["dia_solicitud", "mes_solicitud", "anho_solicitud"])
            
            self.df['periodo'] = self.periodo 

            self.df['fecha_cargue'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print("\nDataFrame generado:")
            print(self.df)
        else:
            print("No se encontró información según el mapeo.")

    def load_data(self):
        if self.df is None or self.df.empty:
            print("No hay datos para cargar.")
            return
        self.loader.upsert_into_table(self.df)
        print("Load Pdf Completado")