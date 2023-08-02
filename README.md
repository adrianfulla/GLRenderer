# Tarea1-Graficos
El objetivo de esta fase inicial del Rasterizador es que puedan cargar un modelo 3D básico y dibujarlo en un archivo BMP, usando solamente líneas e implementando una matriz de objeto básica (solamente Traslación y Escala).

Para obtener la nota completa de ésta tarea deben entregar lo siguiente:

<li>Código fuente capaz de crear un BMP y dibujar en él.</li>
<li>Código fuente capaz de cargar un archivo .obj de su elección (no puede ser el usado en clase).</li>
<li>El OBJ debe ser dibujado usando líneas para visualizar cada uno de los polígonos del modelo 3D.</li>
El modelo debe ser cargado en el centro de la pantalla y debe ser completamente visible (no muy pequeño que no se distinga, y no muy grande que se salga de la pantalla).

## Inicialización

 El Rasterizador puede ser ejecutado de dos maneras, la primera siendo mediante la ejecución del archivo ```Main.exe```, es posible que al intentar ejecutar este archivo se obtenga un mensaje de advertencia por parte de software de antivirus, prometo que no tiene nada malo, es debido al metodo de compilación que se encuentra marcado como potencial virus. 
La segunda manera de ejecutar el Rasterizador es mediante la ejecución del archivo ```Main.py```, dentro de una ventana de shell, navegar al directorio donde se encuentran los archivos y correr el siguiente comando:
  ```bash
    python3 Main.py
  ```  
Esta segunda manera es la indicada para computadoras que no corran Windows como sistema operativo o no se desee ejecutar el .exe. Se necesita tener python3 instalado.

## Resultado
Al ejecutar el progama se debe obtener un archivo llamado ```output.bmp``` la cual tendra un tamaño de 2160x3860px con la imagen de un toro vista desde una perspectiva superior creada completamente con triangulos.
