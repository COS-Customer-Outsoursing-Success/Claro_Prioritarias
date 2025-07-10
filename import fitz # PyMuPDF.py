import fitz  # PyMuPDF

pdf_path = r"Z:\WORKFORCE\03. Mission\Emerson Aguilar\19. Axa\pdf\27418911_19-06-2025 11-42-43-11919-06-2025 11-42-43-119.pdf"

def imprimir_lineas_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            print(f"\n📄 Página {page_num}")
            lines = page.get_text().splitlines()
            for i, line in enumerate(lines):
                print(f"{i:02d}: {line}")


if __name__ == '__main__':
    imprimir_lineas_pdf(pdf_path)
#    temporario, fecha_solicitud = extraer_datos(pdf_path)
#    print("Temporario:", temporario)
#    print("Fecha_Solicitud:", fecha_solicitud)
