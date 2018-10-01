# -*- coding: utf-8 -*-
import socket


# armamos el socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# lo conectamos al server
serversocket.bind(('localhost', 8086))

# hacemos que sea un server socket y le decimos que tenga a lo mas 5 conexiones
serversocket.listen(5)

# nos quedamos esperando como buen server
while True:
    # sacamos los datitos de la conexion entrante (objeto, direccion)
    connection, address = serversocket.accept()
    # sacamos los datos. Aca 64 es el tamaño máximo del buffer
    buf = connection.recv(64)
    if len(buf) > 0:
        # mostramos lo que nos llegó y salimos del loop
        print buf
        break