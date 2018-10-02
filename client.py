# -*- coding: utf-8 -*-
import socket
import sys

# armamos el socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# nombre del server
nombre = sys.argv[1]

puerto = 23

if len(sys.argv) == 3:
    # elejimos el puerto a conectar
    puerto = int(sys.argv[2])

print("Conectando a "+nombre+" en el puerto " + str(puerto))

# lo conectamos al puerto acordado
clientsocket.connect(('localhost', puerto))

first_answer = clientsocket.recv(2048)
print(first_answer.decode(), end='')

while True:
    message = input()
    clientsocket.send(message.encode())
    if message.strip() == 'exit':
        break
    answer = clientsocket.recv(2048)
    print(answer.decode(), end='')

