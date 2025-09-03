"""""
Created By Emerson Aguilar Cruz
"""""

import os
import sys

current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_folder)
sys.path.append(current_folder)

from arbol_tipificacion._cls_load_arbol_tipificacion import LoadArbolTipificacion
    
def main():
       
       
    
    schema = 'bbdd_cos_bog_grupo_axa'
#    table = 'tb_arb_tipificacion_v2'
#    archivo_excel = os.path.join(project_root, 'data', 'arbol_tipificacion')
    table = 'tb_arb_tipificacion_soul_v2'
    archivo_excel = os.path.join(project_root, 'data', 'arbol_tipificacion_soul')    
    
#    schema =  "bbdd_cos_bog_colsubsidio_atraccion"
#    table = 'tb_arbol_tipificacion_soul_dts'
#    archivo_excel = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\19. Axa\arbol_soul'

    
    # -- Inicializador de clases -- 
    processor_arbol = LoadArbolTipificacion(
        schema = schema, 
        table = table,
        archivo_excel=archivo_excel,

    )

    try:
        processor_arbol.main()
    except Exception as e:
        print(f"Error en el proceso principal: {str(e)}")

if __name__ == '__main__':

    main()