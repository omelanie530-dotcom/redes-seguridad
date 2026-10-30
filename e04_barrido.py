import ipaddress
import platform
import subprocess
# ThreadPoolExecutor ejecuta varias tareas a la vez en hilos: un barrido uno por uno sería muy lento
from concurrent.futures import ThreadPoolExecutor

# Devuelve True si el host respondió al ping
def hacer_ping(host):
    host = str(host)
    if platform.system().lower() == "windows":
        comando = ["ping", "-n", "1", "-w", "1000", host]
    else:
        comando = ["ping", "-c", "1", "-w", "1", host]
    try:
        r = subprocess.run(comando, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=5)
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

entrada = input("Red a barrer (ej. 192.168.10.0/24): ")
# Red completa a explorar
red = ipaddress.ip_network(entrada, strict=False)

# Se limita el tamaño para no lanzar miles de pings por error
if red.num_addresses > 1024:
    print("Red demasiado grande para esta práctica (máximo /22)")
    raise SystemExit(1)

# hosts() entrega solo las direcciones útiles, sin red ni broadcast
hosts = list(red.hosts())

# NOTA (Punto 3): Comparación de rendimiento de hilos:
# - Con 1 hilo (max_workers=1): El barrido es secuencial. Al esperar el timeout 
#   de cada IP inactiva, una subred /24 (254 IPs) puede tardar varios minutos (aprox. 4 a 5 minutos).
# - Con 50 hilos (max_workers=50): Las peticiones se ejecutan en paralelo, 
#   reduciendo el tiempo total del barrido a tan solo unos pocos segundos (aprox. 5 a 10 segundos).
with ThreadPoolExecutor(max_workers=50) as executor:
    resultados = list(executor.map(hacer_ping, hosts))

# Se queda con los hosts cuyo resultado fue True
vivos = [h for h, ok in zip(hosts, resultados) if ok]

# Resumen del barrido
print("Hosts activos:", len(vivos), "de", len(hosts))
for h in vivos:
    print(" ", h)
    