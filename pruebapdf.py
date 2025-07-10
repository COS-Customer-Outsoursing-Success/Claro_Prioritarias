import fitz  # PyMuPDF
from datetime import datetime, timedelta

def extraer_datos(pdf_path):
    temporario = None
    fecha_solicitud = None

    with fitz.open(pdf_path) as doc:
        for page in doc:
            lines = [line.strip() for line in page.get_text().splitlines()]
            n = len(lines)

            # ---------- PRIMER INTENTO: ACCESO DIRECTO (posición fija) ----------
            try:
                if lines[6].isdigit():
                    temporario = lines[6]
                if lines[16].isdigit() and lines[17].isdigit() and lines[18].isdigit() and lines[19].upper() == "EXPEDICIÓN":
                    dia, mes, anio = lines[16], lines[17], lines[18]
                    fecha_solicitud_str = f"{anio}-{int(mes):02}-{int(dia):02}"
                    fecha_solicitud = datetime.strptime(fecha_solicitud_str, '%Y-%m-%d')
                    fecha_vigencia = fecha_solicitud + timedelta(days=1)
            except IndexError:
                pass  

            # ---------- RESPALDO: BÚSQUEDA DINÁMICA (por contenido) ----------
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

    return temporario, fecha_solicitud, fecha_vigencia

if __name__ == '__main__':
    pdf_path = r"Z:\WORKFORCE\03. Mission\Emerson Aguilar\19. Axa\pdf\27418911_19-06-2025 11-42-43-11919-06-2025 11-42-43-119.pdf"
    temporario, fecha_solicitud, fecha_vigencia = extraer_datos(pdf_path)
    print("Temporario:", temporario)
    print("Fecha_Solicitud:", fecha_solicitud)
    print("Fecha_Vigencia:", fecha_vigencia)

#%%

#def imprimir_lineas_pdf(pdf_path):
#    with fitz.open(pdf_path) as doc:
#        for page_num, page in enumerate(doc, start=1):
#            print(f"\n📄 Página {page_num}")
#            lines = page.get_text().splitlines()
#            for i, line in enumerate(lines):
#                print(f"{i:02d}: {line}")


#if __name__ == '__main__':
#    imprimir_lineas_pdf(pdf_path)
#    temporario, fecha_solicitud = extraer_datos(pdf_path)
#    print("Temporario:", temporario)
#    print("Fecha_Solicitud:", fecha_solicitud)
