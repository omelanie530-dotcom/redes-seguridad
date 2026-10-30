import socket

# Puertos conocidos y el servicio que suele usarlos (incluyendo los 3 puertos adicionales solicitados: 8080, 5432 y 445)
PUERTOS = {
    21: "FTP", 
    22: "SSH", 
    23: "Telnet", 
    25: "SMTP", 
    53: "DNS",
    80: "HTTP", 
    110: "POP3", 
    143: "IMAP", 
    443: "HTTPS",
    445: "SMB",      # Puerto adicional solicitado (ejemplo)
    3306: "MySQL", 
    3389: "RDP",
    5432: "PostgreSQL", # Puerto adicional solicitado
    8080: "HTTP-Alt"    # Puerto adicional solicitado
}

# Intenta una conexión TCP; si se establece, el puerto está abierto
def puerto_abierto(host, puerto, espera=1.0):
    # SOCK_STREAM = TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Tiempo máximo de espera por puerto, para no quedar bloqueado en puertos filtrados
    s.settimeout(espera)
    try:
        # connect_ex devuelve 0 si conectó y un código de error si no, sin lanzar excepción
        return s.connect_ex((host, puerto)) == 0
    # El socket se cierra siempre
    finally:
        s.close()

# Programa principal
host = input("Host o IP a escanear: ").strip()
try:
    # Acepta IP o nombre de dominio; si es un nombre, lo traduce a IP
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print("No se pudo resolver", host)
    raise SystemExit(1)

print("Escaneando", ip)
# Se prueba cada puerto de la lista y se muestra una fila por resultado
for puerto, servicio in PUERTOS.items():
    estado = "ABIERTO" if puerto_abierto(ip, puerto) else "cerrado"
    print("{:>5} {:<8} {}".format(puerto, servicio, estado))