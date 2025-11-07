# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:25:08 2025
--- Regresion Logistica ---
@author: emerson.aguilar
"""

# Librerías necesariass
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os

# Configuración de conexión a la base de datos
usuario = os.getenv('DB_USER', 'emersonaguilar0694')  # Usa variables de entorno para mayor seguridad
contrasena = os.getenv('DB_PASS', 'gBXJ,!cW!4yUqPIlTKA8')
host = '172.70.7.61'
base_de_datos = 'bbdd_cos_bog_claro_tercer_anillo'
cadena_de_conexion = f'mysql+pymysql://{usuario}:{contrasena}@{host}/{base_de_datos}'
engine = create_engine(cadena_de_conexion)
tabla_resultado = 'tb_variable_coeficiente'

# Ruta para guardar los archivos de salida
ruta_propension = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\02.Tercer Anillo\Propension\Coeficientes'
ruta_propensioon = r'Z:\WORKFORCE\03. Mission\Emerson Aguilar\01.Claro\02.Claro Prioritarias\02.Tercer Anillo\Propension\Clasificacion'

# Fecha actual

fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Lista de variables objetivo
variable_objeto = [
    'Efectividad',
    'Contacto'
]

def borrar_registros_tabla(tabla_resultado):
    """Borrar registros antiguos en la tabla especificada."""
    try:
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM {tabla_resultado}"))
            conn.execute(text("COMMIT"))
            print(f"Datos borrados de la tabla '{tabla_resultado}'")
    except SQLAlchemyError as e:
        print(f"Error al borrar datos debido a '{e}'")

def preprocesar_datos(df):
    """Limpiar y preprocesar los datos antes del modelado."""
    # Eliminar filas con valores nulos
    df = df.dropna()

    X = pd.get_dummies(df[['tipcliente', 'canal', 'zona', 'municipio', 'genero', 'edadmora', 'cargofijomensual', 'ciclo']])
    return X

def variables_objeto(variable_objeto):
    """Procesar cada variable objetivo."""
    id_incremental = 1
    for var in variable_objeto:
        print(f"Procesando modelo para la variable objetivo: {var}")
        
        # Query dinámica para seleccionar la variable objetivo
        query = f"""
        SELECT 
        tipo_cliente AS tipcliente,
        canal,
        zona,
        municipio,
        genero,
        edad_mora AS edadmora,
        cfm_con_imp AS cargofijomensual,
        ciclo,
        {var}
        FROM bbdd_cos_bog_claro_tercer_anillo.tb_dts_final
        """
        
        try:
            # Leer los datos desde la base de datos
            df = pd.read_sql(query, engine)
        except SQLAlchemyError as e:
            print(f"Error al leer datos desde SQL para la variable {var}: {e}")
            continue
        
        # Preprocesar los datos es decir convertir variables categóricas en dummy (¿ Que es dummy?)
        X = pd.get_dummies(df[['tipcliente', 'canal', 'zona', 'municipio', 'genero', 'edadmora', 'cargofijomensual', 'ciclo']])

        y = df[var]
        
        # Asegurar que las filas de X y Y coincidan en cantidades
        X, y = X.align(df[var], join='inner', axis=0)

        # Dividir los datos en entrenamiento y prueba con estratificación
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        except ValueError as e:
            print(f"Error en la división de los datos para la variable {var}: {e}")
            continue
        
        # Ajustar el modelo de regresión logística
        model = LogisticRegression(max_iter=500)
        model.fit(X_train, y_train)

        # Obtener el intercepto y los coeficientes
        intercepto = model.intercept_[0]
        coeficientes = model.coef_[0]

        # Crear un DataFrame con los coeficientes y las variables
        coef_df = pd.DataFrame({
            'variable': X.columns,
            'coeficiente': coeficientes
        })

        # Separar 'tipo_variable' y 'descripcion_variable'
        coef_df[['tipo_variable', 'descripcion_variable']] = coef_df['variable'].str.split('_', n=1, expand=True)

        # Agregar el intercepto al DataFrame
        intercepto_df = pd.DataFrame({
            'variable': ['Intercepto'], 
            'coeficiente': [intercepto],
            'tipo_variable': ['Intercepto'], 
            'descripcion_variable': [None]
        })
        coef_df = pd.concat([coef_df, intercepto_df], ignore_index=True)

        # Agregar columnas adicionales para SQL
        coef_df['id'] = range(id_incremental, id_incremental + len(coef_df))
        id_incremental += len(coef_df)
        coef_df['variable_objetivo'] = var
        coef_df['fecha_procesamiento'] = fecha_actual

        # Guardar los coeficientes en un archivo Excel
        output_path = os.path.join(ruta_propension, f"coeficientes_modelo_{var}.xlsx")
        try:
            coef_df.to_excel(output_path, index=False)
            print(f"Modelo para {var} procesado y guardado en: {output_path}")
        except Exception as e:
            print(f"Error al guardar el archivo Excel para la variable {var}: {e}")

        # Subir resultados a SQL
        subir_sql(coef_df, tabla_resultado)

        # Evaluar el modelo
        y_pred = model.predict(X_test)
        print(f"Reporte de clasificación para {var}:")
        report = classification_report(y_test, y_pred, output_dict=True)  # Genera un diccionario
        print(report)
        
        # Convertir el reporte a un DataFrame
        report_df = pd.DataFrame(report).transpose()
        
        # Guardar el reporte como archivo Excel
        guardar_clasificacion = os.path.join(ruta_propensioon, f"reporte_clasificacion_{var}.xlsx")
        try:
            report_df.to_excel(guardar_clasificacion, index=True)
            print(f"Reporte de clasificación {var} guardado correctamente en {guardar_clasificacion}")
        except Exception as e:
            print(f"Error al guardar clasificación debido a: {e}")
                    
    print("Proceso completado para todas las variables objetivo.")

def subir_sql(df, tabla_resultado):
    """Subir resultados a SQL."""
    try:
        with engine.connect() as conn:
            df.to_sql(tabla_resultado, con=conn, if_exists='append', index=False)
            print(f"Datos insertados en la tabla {tabla_resultado}")
    except SQLAlchemyError as e:
        print(f"Error al insertar datos debido a: {e}")

if __name__ == '__main__':
    borrar_registros_tabla(tabla_resultado)
    variables_objeto(variable_objeto)