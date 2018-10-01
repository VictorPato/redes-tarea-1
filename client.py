# -*- coding: utf-8 -*-
import socket
import sys

# armamos el socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# nombre del server
nombre = sys.argv[1]

# elejimos el puerto a conectar
puerto = int(sys.argv[2])

# lo conectamos al puerto acordado
clientsocket.connect(('localhost', puerto))
print("Conectando a "+nombre+" en el puerto " + str(puerto))
first_answer = clientsocket.recv(2048)

print(first_answer.decode(), end='')

while True:
    message = input()
    if message.strip() == 'exit':
        break
    clientsocket.send(message.encode())
    answer = clientsocket.recv(2048)
    print(answer.decode(), end='')

