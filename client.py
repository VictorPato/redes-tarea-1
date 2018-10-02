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
        self.should_run = True

    def print_to_console(self, to_print):
        print_lock.acquire()
        print("-------" + self.name + " en el puerto " + str(self.port) + " dice:")
        print(to_print.decode())
        print("--------- Fin mensaje de " + self.name)
        print_lock.release()

    def run(self):
        self.clientsocket.connect((self.address, self.port))
        # recibe la primera respuesta
        self.print_to_console(self.clientsocket.recv(4096))
        while self.should_run:
            answer = self.clientsocket.recv(4096)
            if len(answer) == 0:
                break
            self.print_to_console(self.clientsocket.recv(4096))

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
            puerto = int(data[i]["puerto"])
        except KeyError:
            pass

        # se crea el thread
        new_thread = socket_listener(nombre, puerto, direccion)

        # se agrega el server al diccionario, usando el nombre como llave y el thread como valor
        servers[nombre] = new_thread

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
        if i + 2 < len(sys.argv):
            try:
                puerto = int(sys.argv[i + 2])
                i += 1
            except ValueError:
                pass

        i += 2

        # se crea el thread
        new_thread = socket_listener(nombre, puerto, direccion)

        # se agrega el server al diccionario, usando el nombre como llave y el thread como valor
        servers[nombre] = new_thread

# comenzar los threads
for server, thread in servers.items():
    print("Comenzando el thread " + thread.name)
    thread.start()

while True:
    message = input()
    message_parts = message.split()
    comando = message_parts[0]
    if message_parts[1] == 'all':
        for server, thread in servers.items():
            thread.clientsocket.send(comando.encode())

# matar los threads
for thread in socket_threads:
    print("Matando el thread " + thread.name)
    thread.stop()
    thread.join()
    print("El thread " + thread.name + " murio")
