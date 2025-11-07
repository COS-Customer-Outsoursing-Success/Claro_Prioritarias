import pandas as pd
from sqlalchemy import create_engine

usuario = 'emersonaguilar0694'
contrasena = 'gBXJ,!cW!4yUqPIlTKA8'
host = '172.70.7.61'
base_de_datos = 'bbdd_cos_bog_claro_tercer_anillo'
cadena_de_conexion = f'mysql+pymysql://{usuario}:{contrasena}@{host}/{base_de_datos}'
engine = create_engine(cadena_de_conexion)
nombre_tabla = 'tb_campaing_id_3anillo'


ruta = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\02.Tercer Anillo\campaign_id.xlsx'

df = pd.read_excel(ruta)
print(df.columns)
print(df.dtypes)

df.to_sql(nombre_tabla,engine,if_exists='append',index=False)
print("Datos Subidos Correctamente")