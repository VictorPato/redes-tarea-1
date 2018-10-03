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

    def print_to_console(self, to_print):
        print_lock.acquire()
        print("<<<<< " + self.name + " en el puerto " + str(self.port) + " dice:")
        print(to_print.decode())
        print("Fin mensaje de " + self.name + " >>>>>\n")
        print_lock.release()

    def run(self):
        # recibe la primera respuesta
        self.print_to_console(self.clientsocket.recv(4096))
        # recibe el resto de las respuestas hasta que muera la conexion
        while True:
            answer = self.clientsocket.recv(4096)
            if len(answer) == 0:
                break
            self.print_to_console(answer)


# diccionario de servers
servers = dict()
# lista de threads
socket_threads = []


# trata de crear un thread. si lo logra, lo agrega al diccionario de servers y lista de threads
def try_create_thread(nombre, puerto, direccion):
    new_thread = socket_listener(nombre, puerto, direccion)
    try:
        new_thread.clientsocket.connect((direccion, puerto))
        servers[nombre] = new_thread
        socket_threads.append(new_thread)
        print("Conectado a " + nombre)
    except ConnectionRefusedError:
        print("Error en conexion a " + nombre)


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
        try_create_thread(nombre, puerto, direccion)

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
        try_create_thread(nombre, puerto, direccion)

for thrd in socket_threads:
    thrd.start()

try:
    # ciclo para enviar comandos
    while len(servers) > 0:
        # se separa la parte del input que es comando y cual son los servers
        message = input("")
        message_parts = message.split()
        i = 0
        target_is_all = False
        for part in message_parts:
            if part == 'all':
                target_is_all = True
                break
            if part in servers:
                break
            i += 1
        if i == len(message_parts):
            print("No se ingreso  ningun servidor de destino")
            continue
        command = ' '.join(message_parts[:i])
        if target_is_all:
            servers_to_send = list(servers.keys())
        else:
            servers_to_send = message_parts[i:]
        # se envia el comando a todos los servers destino
        for srv in servers_to_send:
            servers[srv].clientsocket.send(command.encode())
        # si se hizo exit, se quitan servidores del diccionario
        if command == 'exit':
            for srv in servers_to_send:
                servers.pop(srv)
    print("Se cerraron todos los servidores")
except KeyboardInterrupt:
    print("\nCerrando conexiones")
    servers_to_send = list(servers.keys())
    for srv in servers_to_send:
        servers[srv].clientsocket.send("exit".encode())

# matar los threads
for thread in socket_threads:
    thread.join()
