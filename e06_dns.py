# socket incluye las funciones de resolución de nombres; time permite medir la demora
import socket
import time

nombre = input("Dominio a resolver: ").strip()
# Se toma la hora antes de consultar al servidor DNS
inicio = time.perf_counter()
try:
    # Devuelve (nombre canónico, lista de alias, lista de IP)
    canonico, alias, ips = socket.gethostbyname_ex(nombre)
# gaierror ocurre cuando el nombre no existe o no hay servidor DNS disponible
except socket.gaierror:
    print("No se pudo resolver", nombre)
    raise SystemExit(1)

# Tiempo transcurrido, pasado a milisegundos
ms = (time.perf_counter() - inicio) * 1000

print("Nombre canónico:", canonico)
for ip in ips:
    print("IP:", ip)
print("Tiempo de resolución: {:.1f} ms".format(ms))

try:
    # Resolución inversa: de IP a nombre (registro PTR). Puede no existir
    print("Resolución inversa:", socket.gethostbyaddr(ips[0])[0])
# herror indica que esa IP no tiene registro inverso
except socket.herror:
    print("Resolución inversa: sin registro")