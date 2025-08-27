import paramiko
import subprocess
import zipfile
import os
import socket

def procesar_archivo_falabella():
    # CONFIGURACIÓN SFTP
    servidor = "172.17.8.199"
    puerto = 22
    usuario = "laura.castrob"
    password = "KgkY9f8jX4e6"
    ruta_remota = "/Entrada/Autos Falabella"
    archivo_pgp = "FALABELLA CALL VIP-VIP_3_75198.zip.pgp"
    
    # RUTA DE DESTINO
    directorio_destino = r"C:\Users\emerson.aguilar\Documents\git_hub\Axa\data\pdf"
    
    # Crear directorio si no existe
    os.makedirs(directorio_destino, exist_ok=True)
    
    # Variables para conexión
    ssh = None
    sftp = None
    
    try:
        # 1. Crear cliente SSH con configuraciones adicionales
        print(f"Conectando SFTP a: {servidor}:{puerto}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Probar conectividad básica primero
        print("Probando conectividad...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        resultado = sock.connect_ex((servidor, puerto))
        sock.close()
        
        if resultado != 0:
            print(f"No se puede conectar al servidor {servidor}:{puerto}")
            return
        
        print("Conectividad OK, intentando SSH...")
        
        # Conectar con parámetros específicos
        ssh.connect(
            hostname=servidor, 
            port=puerto, 
            username=usuario, 
            password=password,
            timeout=30,
            auth_timeout=30,
            banner_timeout=30,
            look_for_keys=False,  # No usar claves SSH, solo password
            allow_agent=False     # No usar SSH agent
        )
        
        print("Conexión SSH exitosa!")
        
        # Abrir canal SFTP
        sftp = ssh.open_sftp()
        print("Canal SFTP abierto!")
        
        # Intentar navegar al directorio (con manejo de errores)
        try:
            print(f"Navegando a: {ruta_remota}")
            sftp.chdir(ruta_remota)
            directorio_actual = sftp.getcwd()
            print(f"Directorio actual: {directorio_actual}")
        except IOError as e:
            print(f"Error navegando al directorio {ruta_remota}: {e}")
            # Intentar con ruta completa
            print("Intentando con ruta completa...")
            
        # Listar archivos
        try:
            archivos = sftp.listdir('.')
            print(f"Archivos encontrados: {archivos}")
        except Exception as e:
            print(f"Error listando archivos: {e}")
            # Intentar listar directorio raíz
            archivos = sftp.listdir('/')
            print(f"Archivos en directorio raíz: {archivos}")
        
        # Verificar si el archivo existe (intentar ambas formas)
        archivo_encontrado = False
        archivo_remoto = None
        
        if archivo_pgp in archivos:
            archivo_encontrado = True
            archivo_remoto = archivo_pgp
        else:
            # Intentar con ruta completa
            archivo_completo = f"{ruta_remota}/{archivo_pgp}"
            try:
                # Verificar si existe con stat
                sftp.stat(archivo_completo)
                archivo_encontrado = True
                archivo_remoto = archivo_completo
                print(f"Archivo encontrado con ruta completa: {archivo_completo}")
            except IOError:
                print(f"ADVERTENCIA: {archivo_pgp} no encontrado")
                print(f"Archivos disponibles en directorio actual: {archivos}")
        
        if not archivo_encontrado:
            print("No se pudo encontrar el archivo. Terminando.")
            return
        
        # Descargar archivo
        archivo_local_pgp = os.path.join(directorio_destino, archivo_pgp)
        print(f"Descargando {archivo_remoto} a {archivo_local_pgp}...")
        
        sftp.get(archivo_remoto, archivo_local_pgp)
        print("Descarga completada!")
        
        # Verificar que el archivo se descargó
        if os.path.exists(archivo_local_pgp):
            tamaño = os.path.getsize(archivo_local_pgp)
            print(f"Archivo descargado: {tamaño} bytes")
        else:
            print("Error: El archivo no se descargó correctamente")
            return
        
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
        # Cerrar conexiones
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
    
    # 2. Descifrar con GPG (solo si la descarga fue exitosa)
    try:
        print("Descifrando archivo PGP...")
        archivo_zip = archivo_pgp.replace('.pgp', '')
        archivo_local_zip = os.path.join(directorio_destino, archivo_zip)
        
        resultado = subprocess.run([
            'gpg', '--batch', '--yes', '--quiet',
            '--output', archivo_local_zip,
            '--decrypt', archivo_local_pgp
        ], capture_output=True, text=True)
        
        if resultado.returncode != 0:
            print(f"Error descifrando: {resultado.stderr}")
            print("Verifica que tengas la clave privada en Kleopatra")
            print("Comando GPG que falló:")
            print(f"gpg --output {archivo_local_zip} --decrypt {archivo_local_pgp}")
            return
        
        print("Descifrado exitoso!")
        
    except FileNotFoundError:
        print("Error: GPG no encontrado. Verifica que Kleopatra/GPG esté instalado")
        return
    except Exception as e:
        print(f"Error en descifrado: {e}")
        return
    
    # 3. Extraer ZIP
    try:
        print(f"Extrayendo PDFs en: {directorio_destino}")
        with zipfile.ZipFile(archivo_local_zip, 'r') as zip_ref:
            zip_ref.extractall(directorio_destino)
        
        print("Extracción completada!")
        
        # 4. Limpiar archivos temporales
        os.remove(archivo_local_pgp)
        os.remove(archivo_local_zip)
        
        print(f"¡Completado! Los PDFs están ahora en: {directorio_destino}")
        
        # Mostrar archivos extraídos
        archivos_pdf = [f for f in os.listdir(directorio_destino) if f.endswith('.pdf')]
        print(f"PDFs extraídos: {len(archivos_pdf)} archivos")
        for pdf in archivos_pdf:
            print(f"  - {pdf}")
        
    except zipfile.BadZipFile:
        print("Error: El archivo descifrado no es un ZIP válido")
    except Exception as e:
        print(f"Error extrayendo ZIP: {e}")

# Ejecutar
if __name__ == "__main__":
    procesar_archivo_falabella()