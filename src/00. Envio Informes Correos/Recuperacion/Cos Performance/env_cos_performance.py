# -*- coding: utf-8 -*-
"""
@author: Emerson.Aguilar
"""

import os
import win32com.client
from datetime import datetime, timedelta
import locale

#---------------------------------------------------------------------------------
# ------------> VARIABLES A CAMBIAR SEGUN CASO CORRESPONDAAAA --------------------
#---------------------------------------------------------------------------------

# ------------> Usuario Red
usuario_red = 'emerson.aguilar'

# Configuracion Leng
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# ------------> Formateo De Fechas

hoy = datetime.now()
hoy_formateada = hoy.strftime("%d-%m-%y")
ayer = hoy - timedelta(days=1)
ayer_form = ayer.strftime("%d-%m-%Y")
num_sem_actal = hoy.isocalendar()[1]
num_sem_siguiente = num_sem_actal + 1
dias_para_lunes = (hoy.weekday() - 0) % 7  # Días desde el lunes
prim_dia_sem_siguiente = hoy + timedelta(days=7 - dias_para_lunes)
prim_dia_sem_siguiente_form = prim_dia_sem_siguiente.strftime("%d")
ulti_dia_sem_siguiente = prim_dia_sem_siguiente + timedelta(days=6)
ulti_dia_sem_siguiente_form = ulti_dia_sem_siguiente.strftime("%d")
num_mes_sem_sigu = prim_dia_sem_siguiente.month
nom_mes_semana_sigu = prim_dia_sem_siguiente.strftime('%B').capitalize()
nom_mes_formateado_ruta = f"{num_mes_sem_sigu}. {nom_mes_semana_sigu}"
nom_semana_formateado_ruta = f"Semana {num_sem_siguiente}"
anho_actual = hoy.strftime("%Y")

# ------------> Configuracion Outlook
outlook = win32com.client.Dispatch("Outlook.Application") # Aplicacion De Outlook Inicializada
# ------------> Destinarios

destinatario = ['crismar.quintero@groupcosbpo.com']
copia = ['albeiro.hernandez@groupcosbpo.com']

# ------------> Configuracion Correo (Asunto, Cuerpo, Etc)

asunto = 'PRUEBAS ENVIO NUEVO'
buen_dia = 'Buen Día,'
cuerpo_correo = f'Se realiza envió de informe COS PERFORMANCE actualizado a corte del {ayer_form}. Se adjunta detalle para su validación'
texto_adicional = 'Quedo atento a cualquier tipo de novedad que se tenga en relacion a lo enviado'

# ------------> Rutas Compartida
ruta_imagen_1 = rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Correos\Cos Performance\Img\Ausentismo_Adherencia.png',
ruta_imagen_2 = rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Correos\Cos Performance\Img\Ocupacion_Utilizacion.png',
ruta_imagen_3 = rf'C:\Users\{usuario_red}\Documents\git_hub\Claro-Prioritarias\data\Correos\Cos Performance\Img\Comportamiento_Auxiliares.png'
archivo_adjunto = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\04.Informes\01. Cos Performance\01.Informe_Cos_Performance_Claro_Prioritarias_Buck.xlsx'
ruta_firma_img = rf'C:\Users\{usuario_red}\Pictures\Firma.PNG'

#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------V------------------------------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------> CODIGO NO TOCAR POR FAVOR GRACIAS <-----------
#-------------------------------------------------------------
#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------|------------------------------
#------------------------------V------------------------------

def enviar_correo(outlook):
    
    correo = outlook.CreateItem(0)
    # Asignación de destinatarios y copia
    correo.To = ";".join(destinatario) if isinstance(destinatario, list) else destinatario
    correo.CC = ";".join(copia) if isinstance(copia, list) else copia
    correo.Subject = asunto

    cuerpo_html = f"<p>{buen_dia}</p><p>{cuerpo_correo}</p>"
    
    if os.path.exists(ruta_imagen_1 ):
        cuerpo_html += f"<br><img src='cid:imagen_principal_1' width='1000' height='700'><br>"
        adjunto_imagen = correo.Attachments.Add(ruta_imagen_1 )
        adjunto_imagen.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "imagen_principal_1"
        )

    if os.path.exists(ruta_imagen_2 ):
        cuerpo_html += f"<br><img src='cid:imagen_principal_2' width='1000' height='700'><br>"
        adjunto_imagen = correo.Attachments.Add(ruta_imagen_2 )
        adjunto_imagen.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "imagen_principal_2"
        )
    if os.path.exists(ruta_imagen_3 ):
        cuerpo_html += f"<br><img src='cid:imagen_principal_3' width='1000' height='700'><br>"
        adjunto_imagen = correo.Attachments.Add(ruta_imagen_3 )
        adjunto_imagen.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "imagen_principal_3"
        )
        
    if os.path.exists(archivo_adjunto):
        correo.Attachments.Add(archivo_adjunto)
    else:
        print(f"⚠️ Advertencia: El archivo adjunto no se encuentra en la ruta {archivo_adjunto}")

    cuerpo_html += f"<br><p>{texto_adicional}</p>"

    if os.path.exists(ruta_firma_img):
        cuerpo_html += f"<br><img src='cid:imagen_firma' width='1000' height='700'><br>"
        adjunto_firma = correo.Attachments.Add(ruta_firma_img)
        adjunto_firma.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "imagen_firma"
        )

    correo.HTMLBody = cuerpo_html

    try:
        correo.Send()
        print(f"✅ Correo enviado con éxito a destinario 🧑‍💻{', '.join(destinatario)} dejando en copia 🧑‍💻{'. '.join(copia)}")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")

if __name__ == '__main__':
    enviar_correo(outlook)
