"""
CREATED BY EMERSON AGUILAR CRUZ
"""

from read_pdf._cls_lector_pdf import LeerPdf

def main():

    ruta_pdf_dir = r"C:\Users\Emerson.Aguilar\Documents\git_hub\Axa\data\pdf"
    
    processor_lectura = LeerPdf(
        ruta_pdf_dir=ruta_pdf_dir,
    )

    try:
        processor_lectura.extraer_temporario_fecha_solicitud()
#        processor_lectura.load_data()
    except Exception as e:
        print(f"Error general: {e}")


if __name__ == '__main__':

    main()