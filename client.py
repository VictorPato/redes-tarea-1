# -*- coding: utf-8 -*-
import socket
import sys

# armamos el socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# elejimos el puerto a conectar
puerto = int(input("puerto: "))

# lo conectamos al puerto acordado
clientsocket.connect(('localhost', puerto))
first_answer = clientsocket.recv(2048)

print("first answer:\n" + first_answer.decode(), end='')
while True:
    message = input()
    clientsocket.send(message.encode())
    answer = clientsocket.recv(2048)
    print(answer.decode(), end='')

