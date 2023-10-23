# Proyecto 2: Ray Tracer
Objetivos:

El objetivo de éste proyecto es demostrar los conocimientos adquiridos durante la segunda parte del curso.

Los alumnos deben entregar un Ray Tracer simple que trate de recrear una escena/imagen escogida por el alumno por medio de figuras simples.


Objetivos cumplidos:

- 30 puntos máximos por complejidad de la escena.
  - Más de 10 figuras: 30 puntos
- 5 puntos por cada material que se aplique a una figura. Máximo de 4 materiales.
- 5 puntos por renderizar por lo menos una figura reflectiva.
- 5 puntos por renderizar por lo menos una figura refractiva.
- 5 puntos por implementar un Environment Map
- 20 puntos máximos por figuras geométricas distintas a las vistas en clase. Máximo de 2 figuras.
- 0 - 20 puntos según la estética de la escena.
- 0 - 10 puntos por la iluminación de la escena


## Inicialización
El Rasterizador puede ser ejecutado mediante la ejecución del archivo Main.py, dentro de una ventana de shell, navegar al directorio donde se encuentran los archivos y correr el siguiente comando:
  ```bash
    python3 Main.py
  ```  

## Resultado
Se tomo de inspiración la siguiente escena:
![Escena](/escena.jpg)
Esta escena muestra una pelota de rugby sobre un tee viendo hacia los postes H, además se puede observar una valla publicitaria en el fondo.
La escena se recreo en la siguiente imagen renderizada con el ray tracer trabajado:
![Resultado](/Resultado.png)

- Se utilizaron un total de 13 figuras
- Se utilizaron un total de 8 materiales
- Un anuncio publiciatario del fondo y una parte del tee tienen textura reflectiva
- Un anuncio publicitario del fondo tiene textura refractiva
- Se utiliza un Enviroment Map de un campo
- Se desarrollaron las figuras de esfera ovalada y cilindro para este proyecto
