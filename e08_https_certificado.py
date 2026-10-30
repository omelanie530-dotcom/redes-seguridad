# Módulos para conexión, TLS (cifrado), medición de tiempo, pedidos web y fechas
import socket
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

# Solo el nombre del sitio, por ejemplo github.com
dominio = input("Dominio (sin https://): ").strip()
inicio = time.perf_counter()

try:
    # Pide la página principal por HTTPS; status es el código HTTP (200 = correcto)
    with urllib.request.urlopen("https://" + dominio, timeout=5) as r:
        codigo = r.status
# El servidor respondió con un código de error (404, 500...): también es una respuesta
except urllib.error.HTTPError as e:
    codigo = e.code
# No hubo conexión: DNS, red caída o certificado inválido
except OSError as e:
    print("No se pudo conectar:", e)
    raise SystemExit(1)

ns = (time.perf_counter() - inicio) * 1000
print("Código HTTP:", codigo)
print("Tiempo de respuesta: {:.0f} ms".format(ns))

# El contexto verifica el certificado con las autoridades confiables del sistema
contexto = ssl.create_default_context()

# Conexión TCP al puerto 443 y luego se negocia TLS sobre ella
with socket.create_connection((dominio, 443), timeout=5) as sock:
    with contexto.wrap_socket(sock, server_hostname=dominio) as s:
        # Diccionario con los datos del certificado del servidor
        cert = s.getpeercert()

# notAfter es la fecha de vencimiento, escrita como texto
vence = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
vence = vence.replace(tzinfo=timezone.utc)

# Días restantes hasta el vencimiento (negativo si ya venció)
dias = (vence - datetime.now(timezone.utc)).days
print("El certificado vence en", dias, "días")