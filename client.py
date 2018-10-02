# -*- coding: utf-8 -*-
import socket
import sys
import os

# armamos el socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# diccionario de servers
servers = dict()

if os.path.isfile(sys.argv[1]):
    print('lleizon')
else:
    i = 1
    while i < len(sys.argv):

        # nombre del server
        nombre = sys.argv[i]

        # direccion del server
        direccion = sys.argv[i + 1]

        # puerto (23 por defecto)
        puerto = 23

        # si se indica el puerto se modifica, ademas hay que avanzar un espacio extra
        if (i + 2 < len(sys.argv)):
            try:
                puerto = int(sys.argv[i + 2])
                i += 1
            except ValueError:
                pass

        i += 2

        # cada elemento del diccionario usa el nombre como llave y una tupla con la direccion y el puerto como valor
        servers[nombre] = direccion, puerto


# esto esta mal, no se como conectar varios, pero asi se itera sobre los servers
for nombre, datos in servers.items():
    direccion, puerto = datos
    print("Conectando a " + nombre + " en el puerto " + str(puerto))

    # se conecta
    clientsocket.connect((direccion, puerto))

    first_answer = clientsocket.recv(2048)
    print(first_answer.decode(), end='')


"""
# nombre del server
nombre = sys.argv[1]

puerto = 23

if len(sys.argv) == 3:
    # elejimos el puerto a conectar
    puerto = int(sys.argv[2])

print("Conectando a " + nombre + " en el puerto " + str(puerto))

# lo conectamos al puerto acordado
clientsocket.connect(('localhost', puerto))

first_answer = clientsocket.recv(2048)
print(first_answer.decode(), end='')

n = 0
while True:
    message = input()
    if message == 'exit':
        break
    clientsocket.send(message.encode())
    answer = clientsocket.recv(2048)
print(answer.decode(), end='')
"""
