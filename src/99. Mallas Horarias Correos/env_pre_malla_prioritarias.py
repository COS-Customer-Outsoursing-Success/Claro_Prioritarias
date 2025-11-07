# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:40:10 2025

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
usuario_red = 'Emerson.Aguilar'

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
num_mes_sem_act = hoy.month
nom_mes_semana_act = hoy.strftime('%B').capitalize()
nom_mes_formateado_ruta_2 = f"{num_mes_sem_act}. {nom_mes_semana_act}"
ayer_dia = ayer.strftime("%d")
# ------------> Configuracion Outlook
outlook = win32com.client.Dispatch("Outlook.Application") # Aplicacion De Outlook Inicializada
# ------------> Destinarios
#Pruebas
#destinatario = ['crismar.quintero@groupcosbpo.com']
#copia = ['45639857@groupcosbpo.com']
destinatario = ['jose.pinto@groupcos.com.co', 'carol.cortes@groupcos.com.co', '4441832@groupcos.com.co', 'Yegnner.morales@groupcos.com.co', 'gina.perez@groupcos.com.co', 'ricardo.sanchez@groupcos.com.co', 'SoniaE.Moreno@groupcosbpo.com', 'alejandro.ariza@groupcos.com.co']
copia = ['Crismar.Quintero@groupcosbpo.com', 'raul.hernandezq@groupcosbpo.com', 'Andres.luna@groupcos.com.co' ]

# ------------> Configuracion Correo (Asunto, Cuerpo, Etc)
nom_informe = f'Pre Malla Horaria {nom_semana_formateado_ruta}'
campana = 'Claro Prioritarias'
asunto = 'Pre Malla Horaria Proxima Semana'
buen_dia = 'Buen Día,'
cuerpo_correo = f'Se realiza envió de {nom_informe} correspondiente a la campaña de {campana}. Recuerde que el detalle puede observarlo en el archivo adjunto. Por favor generar la validacion de la malla y realizar los ajutes pertinentes. Por favor garantizar La devolucion de la misma con los cambios pertientes para el dia viernes antes de las 14:00:00'
texto_adicional = 'Quedo atento a cualquier tipo de novedad que se tenga en relacion a lo enviado'

# ------------> Rutas Compartida
archivo_adjunto = rf'Z:\WORKFORCE\03. Mission\Emerson Aguilar\05.Mallas\{campana}\{anho_actual}\{nom_semana_formateado_ruta}\PV_{campana}_W{num_sem_siguiente}_(Del_{prim_dia_sem_siguiente_form}_al_{ulti_dia_sem_siguiente_form}_De_{nom_mes_semana_sigu})Pre_Malla.xlsb'
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