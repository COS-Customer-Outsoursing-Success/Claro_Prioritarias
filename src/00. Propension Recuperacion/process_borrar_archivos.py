# -*- coding: utf-8 -*-
"""
@author: emerson.aguilar
"""

# -----------> USUARIO DE RED <-----------
usuario_red = 'emerson.aguilar'

import os

class LimpiadorArchivos:
    def __init__(self, rutas_a_limpiar):
        # -------> Aseguramos que rutas_a_limpiar sea una lista
        if not isinstance(rutas_a_limpiar, list):
            raise ValueError("rutas_a_limpiar debe ser una lista de rutas.")
        self.rutas_a_limpiar = rutas_a_limpiar

    def eliminar_archivos_en_ruta(self, ruta):
        if not os.path.exists(ruta):
            print(f"La ruta {ruta} no existe.")
            return
        if not os.path.isdir(ruta):
            print(f"La ruta {ruta} no es un directorio.")
            return

        try:
            archivos = os.listdir(ruta)
            for archivo in archivos:
                ruta_completa = os.path.join(ruta, archivo)
                if os.path.isfile(ruta_completa): 
                    os.remove(ruta_completa)  
                    print(f"Archivo eliminado: {ruta_completa}")
        except PermissionError:
            print(f"Permiso denegado al intentar acceder a {ruta}.")
        except Exception as e:
            print(f"Error al eliminar archivos en {ruta}: {e}")

    def limpiar_rutas(self):
        for ruta in self.rutas_a_limpiar:
            self.eliminar_archivos_en_ruta(ruta)
        print(f"Proceso completado.Archivos Borrados de la ruta {ruta}")

if __name__ == "__main__":
    rutas_a_limpiar = [
        rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Propension\Coeficientes',
        rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Propension\Clasificacion'
        ]
    limpiador = LimpiadorArchivos(rutas_a_limpiar)
    limpiador.limpiar_rutas()
