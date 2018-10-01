# -*- coding: utf-8 -*-
import socket
import sys

# armamos el socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# lo conectamos al puerto acordado
clientsocket.connect(('localhost', 8086))

# mandamos un mensajito
print "mandamos cositas..."
clientsocket.send('Holi c:')
print "enviado"