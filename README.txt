# Tarea 1 CC4303-Redes

Tarea 1 del curso de Redes.

## Integrantes

* Pedro Belmonte
* Víctor Garrido

## Cómo correr la tarea

La tarea fue resuelta en Python 3, para Ubuntu x64. A continuación se indica cómo correrla.

### Prerequisitos

Para correr la tarea solo se necesita tener Python 3 instalado y tener uno o más servers corriendo.

### Ejecución y parámetros

Hay dos maneras de correr el programa y darle los parámetros, en ambos casos se debe abrir una terminal e ir al directorio donde se encuentra client.py:

#### Entregar los parámetros por línea de comandos

El programa se debe correr con el comando


$ python3 client.py


Dándole los servidores como argumento en el formato <nombre direccion puerto ...>

Si, por ejemplo hay 3 servers corriendo en localhost (127.0.0.1) en los puertos 23, 2112 y 8001, se podría correr con el siguiente comando:


$ python3 client.py server1 localhost 23 server2 localhost 2112 server3 localhost 8001


Dado que el puerto por defecto es el 23 también se puede omitir el puerto y el programa asume que es el 23. Es decir, lo anterior es equivalente a


$ python3 client.py server1 localhost server2 localhost 2112 server3 localhost 8001


#### Entregar los parámetros a través de un json

En vez de pasarle los parámetros en la línea de comandos se puede crear un archivo json con el formato <"nombre": ...,
"dirección":...,"puerto":...>


[
	{
		"nombre": "server1",
		"direccion": "127.0.0.1"
	},
	{
		"nombre": "server2",
		"direccion": "127.0.0.1",
		"puerto": "2112"
	},
	{
		"nombre": "server3",
		"direccion": "127.0.0.1",
		"puerto": "8001"
	}
]


En el ejemplo anterior hay dos cosas que es importante notar:

* El nombre del puerto nuevamente es opcional, si no se indica se asume que es 23.
* Los parámetros se deben entregar (y el programa asume que así es) como strings, de la misma forma que sucede si se entregan por línea de comandos.

De esta forma, si por ejemplo el archivo se llama servers.json y se encuentra en el mismo directorio que client.py el comando para correrlo es


$ python3 client.py servers.json


## Uso

Después de correr el programa y conectarse a los servidores se pueden escribir comandos (ls, cat, echo, help o exit), indicando los servidores a los cuales se les hace el request, por ejemplo:


$ ls server1
$ echo hola mundo server1 server2
$ exit all


## Casos particulares

En el caso de tratar de conectarse a varios servidores y dar nombres duplicados, se acepta solo la primera conexión por cada nombre, y los siguientes intentos ser rechazan.

De la misma forma, si se trata de conectar a una dirección y puerto duplicados, se acepta solo el primer intento.
