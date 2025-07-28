"""
CREATED BY EMERSON AGUILAR CRUZ
"""
import os
from _cls_lector_pdf import LeerPdf

def main():

    ruta_pdf_dir = r"Z:\WORKFORCE\03. Mission\Emerson Aguilar\19. Axa\pdf"
    
    if not os.path.exists(ruta_pdf_dir):
        print(f"Directorio no encontrado: {ruta_pdf_dir}")
        return

    archivos_pdf = [
        os.path.join(ruta_pdf_dir, f) for f in os.listdir(ruta_pdf_dir) if f.lower().endswith(".pdf")
    ]

    if not archivos_pdf:
        print("No se encontraron archivos PDF en el directorio.")
        return

    processor_lectura = LeerPdf(
        rutas_pdf=archivos_pdf,
        ruta_pdf_dir=ruta_pdf_dir,
        archivos_pdf=archivos_pdf
    )

    try:
        processor_lectura.obtener_pdf()

        if processor_lectura.ruta_pdf:
            temporario, fecha_solicitud, fecha_vigencia = processor_lectura.extraer_temporario_fecha_solicitud()
            print("Temporario:", temporario)
            print("Fecha Solicitud:", fecha_solicitud)
            print("Fecha Vigencia:", fecha_vigencia)
    except Exception as e:
        print(f"Error general: {e}")


if __name__ == '__main__':

    main()