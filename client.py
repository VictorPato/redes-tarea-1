# -*- coding: utf-8 -*-
import socket
import sys
import os
import threading
import json

# Lock utilizado para sincronizar escritura
print_lock = threading.Lock()


# La clase socket_listener esta pensada para crear un thread por cada socket que le interesa escuchar al programa
# Hace uso de print_lock para sincronizar la escritura al output
class socket_listener(threading.Thread):
    def __init__(self, name, port=23, address='localhost'):
        threading.Thread.__init__(self)
        self.name = name
        self.port = port
        self.address = address
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # se pone el socket en modo timeout para que no se bloquee, permitiendo que itere al correr
        self.clientsocket.settimeout(0.1)
        self.should_run = True

    def run(self):
        self.clientsocket.connect((self.address, self.port))
        # recibe la primera respuesta
        # TODO: No se si imprimir la primera respuesta
        self.clientsocket.recv(4096)
        while self.should_run:
            answer = self.clientsocket.recv(4096)
            print_lock.acquire()
            # TODO: Considerando que es multiservidor, quizas queramos quitar el "user@CC4303 ~ $ " al final de la respuesta
            print(self.name + " en el puerto " + str(self.port) + " dice:")
            print(answer.decode())
            print_lock.release()

    def stop(self):
        self.should_run = False

# diccionario de servers
servers = dict()

if os.path.isfile(sys.argv[1]):

	# se cargan los datos
    with open(sys.argv[1]) as archivo:
    	data = json.load(archivo)

    for i in range(len(data)):

    	# nombre del server
        nombre = data[i]["nombre"]

        # direccion del server
        direccion = data[i]["direccion"]

        # puerto (23 por defecto)
        puerto = 23

        # si se indica el puerto se modifica
        try:
        	puerto = data[i]["puerto"]
        except KeyError:
        	pass

        # cada elemento del diccionario usa el nombre como llave y una tupla con la direccion y el puerto como valor
        servers[nombre] = direccion, puerto    

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

# lista de los threads por si fuera necesario usarlos
socket_threads = []

# se conecta a los servidores
for nombre, datos in servers.items():
    direccion, puerto = datos
    print("Conectando a " + nombre + " en el puerto " + str(puerto))
    new_thread = socket_listener(nombre, puerto, direccion)
    socket_threads.append(new_thread)
    # TODO: falta hacerles thread.start()

# comenzar los threads
for thread in socket_threads:
    print("Comenzando el thread "+ thread.name)
    thread.start()

# matar los threads
for thread in socket_threads:
    print("Matando el thread "+ thread.name)
    thread.stop()
    thread.join()
    print("El thread "+ thread.name + " murio")
    
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
<<<<<<< HEAD
print(answer.decode(), end='')
"""
