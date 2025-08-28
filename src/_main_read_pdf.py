"""
CREATED BY EMERSON AGUILAR CRUZ
"""

from read_pdf._cls_lector_pdf import LeerPdf

def main():
    try:
        periodo = ""
        while True:
            periodo = input("Escribe el periodo al cual corresponden los PDF (ej: 202508): ")
            if periodo.isdigit() and len(periodo) == 6:
                break
            else:
                print("Ingresa un periodo valido de 6 dígitos (ej: 202508).")

        processor_lectura = LeerPdf(periodo=periodo)

        pdfs_encontrados = processor_lectura.obtener_pdf()
        if not pdfs_encontrados:
            print("No se encontraron PDFs para procesar.")
            return 0

        for pdf in pdfs_encontrados:
            try:
                processor_lectura.ruta_pdf = pdf  # ----> Esto asigna el PDF actual
                print(f"\n>>> Procesando PDF: {pdf}")
                processor_lectura.obtener_informacion()
                processor_lectura.load_data()
            except Exception as e:
                print(f"Error procesando {pdf}: {e}")

        print("\nProceso finalizado correctamente")
        return 0

    except Exception as e:
        print(f"Error: Error general: {e}")
        return 1


if __name__ == '__main__':
    main()
