import paramiko  # Librería para conexiones SSH/SFTP
import subprocess  # Para ejecutar comandos del sistema (GPG)
import zipfile  # Para extraer archivos ZIP
import os  # Para operaciones del sistema de archivos
import socket  # Para verificar conectividad de red

def procesar_archivo_falabella():
    """
    Función principal que descarga, descifra y extrae archivos PDF desde un servidor SFTP.
    Proceso completo:
    1. Se conecta a servidor SFTP
    2. Descarga archivo PGP encriptado
    3. Lo descifra usando GPG
    4. Extrae los PDFs del archivo ZIP resultante
    """
    
    # ========== CONFIGURACIÓN DE CONEXIÓN SFTP ==========
    servidor = "172.17.8.199"  # IP del servidor SFTP de Falabella
    puerto = 22  # Puerto estándar SSH/SFTP
    usuario = "laura.castrob"  # Nombre de usuario para autenticación
    password = "KgkY9f8jX4e6"  # Contraseña del usuario
    ruta_remota = "/Entrada/Autos Falabella"  # Directorio en el servidor donde están los archivos
    archivo_pgp = "FALABELLA CALL VIP-VIP_3_75198.zip.pgp"  # Nombre del archivo a descargar
    
    # ========== CONFIGURACIÓN LOCAL ==========
    directorio_destino = r"C:\Users\emerson.aguilar\Documents\git_hub\Axa\data\pdf"  # Carpeta local donde guardar PDFs
    
    # Crear el directorio de destino si no existe
    os.makedirs(directorio_destino, exist_ok=True)
    
    # Variables para manejar las conexiones SSH/SFTP
    ssh = None  # Cliente SSH principal
    sftp = None  # Canal SFTP para transferencia de archivos
    
    try:
        # ========== ESTABLECER CONEXIÓN SFTP ==========
        print(f"Conectando SFTP a: {servidor}:{puerto}")
        
        # Crear cliente SSH con política de aceptar cualquier host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Acepta hosts desconocidos automáticamente
        
        # ========== VERIFICAR CONECTIVIDAD BÁSICA ==========
        print("Probando conectividad...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear socket TCP
        sock.settimeout(10)  # Timeout de 10 segundos
        resultado = sock.connect_ex((servidor, puerto))  # Intentar conexión básica
        sock.close()  # Cerrar socket de prueba
        
        # Si no se puede conectar al servidor, terminar
        if resultado != 0:
            print(f"No se puede conectar al servidor {servidor}:{puerto}")
            return
        
        print("Conectividad OK, intentando SSH...")
        
        # ========== ESTABLECER CONEXIÓN SSH COMPLETA ==========
        ssh.connect(
            hostname=servidor, 
            port=puerto, 
            username=usuario, 
            password=password,
            timeout=30,  # Timeout general de conexión
            auth_timeout=30,  # Timeout para autenticación
            banner_timeout=30,  # Timeout para recibir banner SSH
            look_for_keys=False,  # No buscar claves SSH locales
            allow_agent=False     # No usar SSH agent
        )
        
        print("Conexión SSH exitosa!")
        
        # Abrir canal SFTP para transferencia de archivos
        sftp = ssh.open_sftp()
        print("Canal SFTP abierto!")
        
        # ========== NAVEGAR AL DIRECTORIO REMOTO ==========
        try:
            print(f"Navegando a: {ruta_remota}")
            sftp.chdir(ruta_remota)  # Cambiar al directorio objetivo
            directorio_actual = sftp.getcwd()  # Obtener directorio actual
            print(f"Directorio actual: {directorio_actual}")
        except IOError as e:
            print(f"Error navegando al directorio {ruta_remota}: {e}")
            print("Intentando con ruta completa...")
            
        # ========== LISTAR ARCHIVOS EN EL DIRECTORIO ==========
        try:
            archivos = sftp.listdir('.')  # Listar archivos en directorio actual
            print(f"Archivos encontrados: {archivos}")
        except Exception as e:
            print(f"Error listando archivos: {e}")
            # Si falla, intentar listar el directorio raíz
            archivos = sftp.listdir('/')
            print(f"Archivos en directorio raíz: {archivos}")
        
        # ========== BUSCAR EL ARCHIVO OBJETIVO ==========
        archivo_encontrado = False
        archivo_remoto = None
        
        # Verificar si el archivo está en la lista de archivos del directorio
        if archivo_pgp in archivos:
            archivo_encontrado = True
            archivo_remoto = archivo_pgp
        else:
            # Intentar con la ruta completa
            archivo_completo = f"{ruta_remota}/{archivo_pgp}"
            try:
                sftp.stat(archivo_completo)  # Verificar si existe el archivo
                archivo_encontrado = True
                archivo_remoto = archivo_completo
                print(f"Archivo encontrado con ruta completa: {archivo_completo}")
            except IOError:
                print(f"ADVERTENCIA: {archivo_pgp} no encontrado")
                print(f"Archivos disponibles en directorio actual: {archivos}")
        
        # Si no se encuentra el archivo, terminar el proceso
        if not archivo_encontrado:
            print("No se pudo encontrar el archivo. Terminando.")
            return
        
        # ========== DESCARGAR ARCHIVO PGP ==========
        archivo_local_pgp = os.path.join(directorio_destino, archivo_pgp)  # Ruta local completa
        print(f"Descargando {archivo_remoto} a {archivo_local_pgp}...")
        
        sftp.get(archivo_remoto, archivo_local_pgp)  # Descargar archivo del servidor
        print("Descarga completada!")
        
        # Verificar que el archivo se descargó correctamente
        if os.path.exists(archivo_local_pgp):
            tamaño = os.path.getsize(archivo_local_pgp)
            print(f"Archivo descargado: {tamaño} bytes")
        else:
            print("Error: El archivo no se descargó correctamente")
            return
        
    # ========== MANEJO DE ERRORES DE CONEXIÓN ==========
    except paramiko.AuthenticationException:
        print("Error de autenticación - Verifica usuario y contraseña")
        return
    except paramiko.SSHException as e:
        print(f"Error SSH: {e}")
        print("Posibles causas:")
        print("- Servidor SSH no disponible")
        print("- Configuración de SSH incorrecta")
        print("- Firewall bloqueando conexión")
        return
    except socket.timeout:
        print("Timeout de conexión - El servidor no responde")
        return
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return
    finally:
        # ========== CERRAR CONEXIONES ==========
        # Siempre cerrar las conexiones, sin importar si hubo errores
        if sftp:
            sftp.close()  # Cerrar canal SFTP
        if ssh:
            ssh.close()  # Cerrar conexión SSH
    
    # ========== DESCIFRAR ARCHIVO PGP USANDO GPG ==========
    try:
        print("Descifrando archivo PGP...")
        
        # Crear nombre del archivo ZIP (quitando extensión .pgp)
        archivo_zip = archivo_pgp.replace('.pgp', '')
        archivo_local_zip = os.path.join(directorio_destino, archivo_zip)
        
        # Ejecutar comando GPG para descifrar el archivo
        resultado = subprocess.run([
            'gpg',  # Comando GPG
            '--batch',  # Modo no interactivo
            '--yes',  # Responder "sí" automáticamente a preguntas
            '--quiet',  # Modo silencioso
            '--output', archivo_local_zip,  # Archivo de salida
            '--decrypt', archivo_local_pgp  # Archivo a descifrar
        ], capture_output=True, text=True)  # Capturar salida del comando
        
        # Verificar si el descifrado fue exitoso
        if resultado.returncode != 0:
            print(f"Error descifrando: {resultado.stderr}")
            print("Verifica que tengas la clave privada en Kleopatra")
            print("Comando GPG que falló:")
            print(f"gpg --output {archivo_local_zip} --decrypt {archivo_local_pgp}")
            return
        
        print("Descifrado exitoso!")
        
    # ========== MANEJO DE ERRORES DE DESCIFRADO ==========
    except FileNotFoundError:
        print("Error: GPG no encontrado. Verifica que Kleopatra/GPG esté instalado")
        return
    except Exception as e:
        print(f"Error en descifrado: {e}")
        return
    
    # ========== EXTRAER PDFS DEL ARCHIVO ZIP ==========
    try:
        print(f"Extrayendo PDFs en: {directorio_destino}")
        
        # Abrir y extraer el archivo ZIP
        with zipfile.ZipFile(archivo_local_zip, 'r') as zip_ref:
            zip_ref.extractall(directorio_destino)  # Extraer todos los archivos
        
        print("Extracción completada!")
        
        # ========== LIMPIAR ARCHIVOS TEMPORALES ==========
        # Eliminar archivo PGP original (ya no se necesita)
        os.remove(archivo_local_pgp)
        # Eliminar archivo ZIP descifrado (ya no se necesita)
        os.remove(archivo_local_zip)
        
        # ========== MOSTRAR RESULTADOS FINALES ==========
        print(f"¡Completado! Los PDFs están ahora en: {directorio_destino}")
        
        # Listar todos los archivos PDF extraídos
        archivos_pdf = [f for f in os.listdir(directorio_destino) if f.endswith('.pdf')]
        print(f"PDFs extraídos: {len(archivos_pdf)} archivos")
        for pdf in archivos_pdf:
            print(f"  - {pdf}")
        
    # ========== MANEJO DE ERRORES DE EXTRACCIÓN ==========
    except zipfile.BadZipFile:
        print("Error: El archivo descifrado no es un ZIP válido")
    except Exception as e:
        print(f"Error extrayendo ZIP: {e}")

# ========== PUNTO DE ENTRADA DEL PROGRAMA ==========
if __name__ == "__main__":
    """
    Punto de entrada: ejecuta la función principal solo si el script
    se ejecuta directamente (no si se importa como módulo)
    """
    procesar_archivo_falabella()