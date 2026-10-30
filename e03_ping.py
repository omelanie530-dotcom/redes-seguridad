# platform indica el sistema operativo; subprocess ejecuta comandos del sistema
import platform
import subprocess

# Envía un solo ping y devuelve True si el host respondió
def hacer_ping(host):
    # Se usa -n en Windows y -c en Linux porque cada sistema operativo 
    # utiliza diferentes argumentos en su comando ping nativo.
    if platform.system().lower() == "windows":
        comando = ["ping", "-n", "1", "-w", "1000", host]
    else:
        comando = ["ping", "-c", "1", "-w", "1", host]
        
    try:
        # Ejecutamos el comando sin ocultar la salida para que puedas ver qué ocurre en la terminal
        resultado = subprocess.run(comando, timeout=5)
        
        # Código de retorno 0 significa que el ping tuvo éxito
        return resultado.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

# Programa principal
host = input("Host o IP a probar: ").strip()

if hacer_ping(host):
    print("\nResultado:", host, "responde")
else:
    print("\nResultado:", host, "no responde")

# Evita que la ventana de la terminal se cierre automáticamente
input("\nPresiona Enter para salir...")