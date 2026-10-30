import socket
def ip_local():
    s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8",80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close() 
nombre = socket.gethostname()
print(f"{nombre}:{ip_local()}")