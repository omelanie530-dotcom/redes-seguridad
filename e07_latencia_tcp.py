# statistics calcula el promedio; time mide los intervalos
import socket
import statistics
import time

host = input("Host: ").strip()
puerto = int(input("Puerto (ej. 443): "))

# Cantidad de pruebas a realizar (Modificado a 20 según el punto 3 de la consigna)
intentos = 20

# Aquí se guardan los tiempos de las conexiones exitosas
tiempos = []
perdidos = 0

# En cada intento se mide cuánto tarda en establecerse la conexión TCP
for i in range(intentos):
    inicio = time.perf_counter()
    try:
        # create_connection resuelve el nombre y conecta; si falla lanza OSError
        with socket.create_connection((host, puerto), timeout=2):
            ms = (time.perf_counter() - inicio) * 1000
            tiempos.append(ms)
            print("Intento {}: {:.1f} ms".format(i + 1, ms))
    # Sin respuesta o conexión rechazada: se cuenta como intento perdido
    except OSError:
        perdidos += 1
        print("Intento {}: sin respuesta".format(i + 1))
    
    # Pausa corta entre intentos
    time.sleep(0.5)

# Si todos los intentos fallaron no hay tiempos para calcular
if tiempos:
    print("Mín {:.1f} ms  Máx {:.1f} ms  Prom {:.1f} ms".format(
        min(tiempos), max(tiempos), statistics.mean(tiempos)
    ))

# Porcentaje de intentos sin respuesta
print("Pérdida: {:.0f}%".format(perdidos / intentos * 100))