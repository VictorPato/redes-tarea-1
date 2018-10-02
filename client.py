# -*- coding: utf-8 -*-
import socket
import sys
import os
import threading

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
        if i + 2 < len(sys.argv):
            try:
                puerto = int(sys.argv[i + 2])
                i += 1
            except ValueError:
                pass

        i += 2

        # cada elemento del diccionario usa el nombre como llave y una tupla con la direccion y el puerto como valor
        servers[nombre] = direccion, puerto

# lista de los threads
socket_threads = []

# se conecta a los servidores
for nombre, datos in servers.items():
    direccion, puerto = datos
    print("Conectando a " + nombre + " en el puerto " + str(puerto))
    new_thread = socket_listener(nombre, puerto, direccion)
    socket_threads.append(new_thread)

# comenzar los threads
for thread in socket_threads:
    print("Comenzando el thread " + thread.name)
    thread.start()

while True:
    message = input()
    message_parts = message.split()
    comando = message_parts[0]
    if message_parts[1] == 'all':
        for nombre, datos in servers.items():
            pass



# matar los threads
for thread in socket_threads:
    print("Matando el thread " + thread.name)
    thread.stop()
    thread.join()
    print("El thread " + thread.name + " murio")

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
