"""
CREATED BY EMERSON AGUILAR CRUZ
"""

import fitz  # PyMuPDF
import os
import pandas as pd
from datetime import datetime, timedelta
from conexiones_db._cls_sqlalchemy import MySQLConnector
from  load_data._cls_load_data import *

class LeerPdf:

    def __init__(self, ruta_pdf_dir=None, archivos_pdf=None, schema=None, table=None):

        self.ruta_pdf_dir = ruta_pdf_dir 
        self.archivos_pdf = archivos_pdf or []

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

        self.schema = "bbdd_cos_bog_grupo_axa"
        self.table =  "tb_asignacion_falabella_v2_temporarios"
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
                pdf_validos.append(ruta)
            else:
                print(f"Archivo no válido o no encontrado: {ruta}")

        if not pdf_validos:
            print("No se encontraron archivos PDF válidos.")
            return None

        if len(pdf_validos) == 1:
            self.ruta_pdf = pdf_validos[0]
            print(f"\nSe encontró un solo archivo PDF. Seleccionado automáticamente: {self.ruta_pdf}")
            return self.ruta_pdf

        print("\nArchivos PDF encontrados:")
        for idx, ruta in enumerate(pdf_validos):
            print(f"{idx}: {ruta}")

        while True:
            try:
                seleccion = int(input("Ingrese el número del archivo PDF a tratar: "))
                if 0 <= seleccion < len(pdf_validos):
                    self.ruta_pdf = pdf_validos[seleccion]
                    print(f"\nSeleccionaste: {self.ruta_pdf}")
                    return self.ruta_pdf
                else:
                    print("Índice fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Debes ingresar un número.")

    def extraer_temporario_fecha_solicitud(self):

        self.obtener_pdf()

        if not self.ruta_pdf:
            raise ValueError("No se ha seleccionado ningún PDF.")
        
        temporario = None
        fecha_solicitud = None
        fecha_vigencia = None

        with fitz.open(self.ruta_pdf) as doc:
            for page in doc:
                lines = [line.strip() for line in page.get_text().splitlines()]
                n = len(lines)

                try:
                    if lines[6].isdigit():
                        temporario = lines[6]
                    if (
                        lines[16].isdigit()
                        and lines[17].isdigit()
                        and lines[18].isdigit()
                        and lines[19].upper() == "EXPEDICIÓN"
                    ):
                        dia, mes, anio = lines[16], lines[17], lines[18]
                        fecha_solicitud_str = f"{anio}-{int(mes):02}-{int(dia):02}"
                        fecha_solicitud = datetime.strptime(fecha_solicitud_str, '%Y-%m-%d')
                        fecha_vigencia = fecha_solicitud + timedelta(days=1)

                except IndexError:
                    pass

                if not temporario:
                    for i, line in enumerate(lines):
                        if "TEMPORARIO" in line.upper() and i + 1 < n:
                            if lines[i + 1].isdigit():
                                temporario = lines[i + 1]
                                break

                if not fecha_solicitud:
                    for i in range(n - 3):
                        if (
                            lines[i].isdigit()
                            and lines[i + 1].isdigit()
                            and lines[i + 2].isdigit()
                            and lines[i + 3].upper() == "EXPEDICIÓN"
                        ):
                            dia, mes, anio = lines[i], lines[i + 1], lines[i + 2]
                            fecha_solicitud_str = f"{anio}-{int(mes):02}-{int(dia):02}"
                            fecha_solicitud = datetime.strptime(fecha_solicitud_str, '%Y-%m-%d')
                            fecha_vigencia = fecha_solicitud + timedelta(days=1)
                            break
                
                
                if temporario and fecha_solicitud and fecha_vigencia:
                    break
                
        temporario_3 = temporario[:3] if temporario else None

        print("Temporario Completo:", temporario)        
        print("Temporario 3 Dijitos:", temporario_3)
        print("Fecha Solicitud:", fecha_solicitud)
        print("Fecha Vigencia:", fecha_vigencia)

        
        self.df = pd.DataFrame([{

            "temporario": temporario_3,
            "fecha_solicitud": fecha_solicitud,
            "fecha_vigencia": fecha_vigencia 
        }])
        
        while True:

            periodo = input("Colocar periodo del pdf elegido ej: 202504: ")
            if periodo.isdigit() and len (periodo) == 6:
                self.df["periodo"] = periodo
                break
            else: 
                print("Formato de periodo invalido. Tiene que ser un numero de 6 dijitos ej: 202507")

        print("------------- Data Final -------------:")
        print(self.df)

        return self.df

    def load_data(self):
        if self.df is None or self.df.empty:
            print("No hay datos para cargar.")
            return
        self.loader.upsert_into_table(self.df)
        print("Load Pdf Completado")