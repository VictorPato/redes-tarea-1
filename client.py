# -*- coding: utf-8 -*-
import socket
import sys
import threading

# Lock utilizado para sincronizar escritura
print_lock = threading.Lock()


# La clase socket_listener esta pensada para crear un thread por cada socket que le interesa escuchar al programa
# Hace uso de print_lock para sincronizar la escritura al output
class socket_listener(threading.Thread):
    def __init__(self, threadID, name, port=23, address='localhost'):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port
        self.address = address
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.clientsocket.connect((self.address, self.port))
        # recibe la primera respuesta
        # TODO: No se si imprimir la primera respuesta
        self.clientsocket.recv(4096)
        while True:
            answer = self.clientsocket.recv(4096)
            print_lock.acquire()
            # TODO: Considerando que es multiservidor, quizas queramos quitar el "user@CC4303 ~ $ " al final de la respuesta
            print(self.name + " en el puerto " + str(self.port) + " dice:")
            print(answer.decode())
            print_lock.release()


# armamos el socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
