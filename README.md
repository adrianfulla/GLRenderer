# Proyecto 3: OpenGL
## Objetivos:

El objetivo de éste proyecto es demostrar los conocimientos adquiridos a lo largo del semestre.

Los alumnos deben entregar un visualizador de modelos creado en base al renderer de OpenGL que se trabajó en clase.

La nota máxima es de 100 puntos. Se entregarán los siguientes puntos por cada uno de los objetivos que se cumplan. Pueden escoger los objetivos que quieran. No hay puntos extra.

### Objetivos cumplidos:
- 4 modelos
- 5 puntos, movimiento circular al rededor del modelo, enfocado siempre en el modelo.
- 5 puntos, movimiento de la cámara hacia arriba y hacia abajo, pero siempre enfocado en el modelo. Tiene que tener un límite.
- 5 puntos, Zoom In y Zoom out de la cámara, con un límite de cuanto se puede acercar o cuanto se puede alejar.
    - Se puede realizar con la rueda del mouse
- 0 - 30 puntos según uso creativo de shaders (iluminación compleja, usar input para variar algún valor dentro del shader, uso de mapas normales, toon shading, etc...)
    - 2 vertex shaders y sus variantes
    - 2 fragment shaders y sus variantes
- 0 - 20 puntos según características extras que el alumno agregue al programa (menús, música o efectos de sonido, imagen de fondo, etc)
    - Menu
    - Musica de ambiente
    - Efectos de sonido al cambiar modelo o shaders
    - Opcion para aleatorizacion de shaders

## Requisitos
- Python 32 bits, versión [3.11.6](https://www.python.org/ftp/python/3.11.6/python-3.11.6.exe)
- Modulo Pip de Python de 32 bits

Generalmente el modulo Pip se incluye al instalar cualquier versión de Python

## Setup
La ejecución del programa requiere la creación de un ambiente virtual de python en 32 bits para poder ser ejecutado, para esto se debe asegurar que
la maquina en la que se desea correr el programa tiene una versión de Python de 32 bits y el modulo Pip que sirve para instalar librerias de Python.

Una vez verificado que la maquina tiene una versión de Python de 32 bits con Pip se pueden empezar a descargar las librerias necesarias.

### Virtualenv
La primer libreria necesaria es Virtualenv, con esta crearemos un ambiente virtual sobre el cual se ejecutará el programa
```bash
    C:\direccion\al\python\32bits\python.exe -m pip install virtualenv
  ```
Una vez instalada la libreria se procede a crear el ambiente virtual, para esto nos dirigiremos al directorio donde se encuentra el repositorio y ejecutaremos el siguiente comando:
```bash
    C:\direcion\repositorio\GLRenderer C:\direccion\al\python\32bits\python.exe -m virtualenv myenv
  ```
```bash
    C:\direcion\repositorio\GLRenderer myenv/scripts/activate
  ```
### Librerias
Esto activará el ambiente virtual y procedemos a instalar las siguientes librerias, para esto utilizaremos el archivo ```requirements.txt``` que incluye las librerias necesarias y sus versiones
```bash
    C:\direcion\repositorio\GLRenderer C:\direccion\al\python\32bits\python.exe -m pip install -r requirements.txt
  ```

## Inicialización
Una vez terminado el setup podemos proceder a ejecutar el archivo ```Main.py``` que empezará el rasterizador:
  ```bash
    C:\direcion\repositorio\GLRenderer C:\direccion\al\python\32bits\python.exe Main.py
  ```  

## Resultado
[Video en YouTube](https://youtu.be/urnLFOPvQyg)

