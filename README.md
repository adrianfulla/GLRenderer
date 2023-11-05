# Lab 4: Shaders II
Objetivos:

El objetivo de este laboratorio es que practiquen la creación de shaders (tanto Vertex como Fragment) en base a GLSL y para uso en un renderer hecho en OpenGL.

Para este lab, tienen que crear distintas variaciones de shaders y mostrar los resultados en un sólo modelo de su elección usando su renderer. Deben usar las teclas numéricas (1, 2, 3...) para cambiar la configuración de shaders durante la ejecución del programa. La nota de los criterios subjetivos dependerá de qué tan complejos e interesantes sean los shaders que implementen.

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
![Result]("/Result.jpg")
