# Proyecto 1: Rasterizer
El objetivo de éste proyecto es demostrar los conocimientos adquiridos durante la primera mitad del curso.

Los alumnos deben entregar un Rasterizador que lea archivos obj y realice un render a archivos bmp. Creen una escena cargando varios modelos que muestre lo que han aprendido.

La nota máxima es de 100 puntos. Se entregarán los siguientes puntos por cada uno de los objetivos que se cumplan. Pueden escoger los objetivos que quieran. No hay puntos extra.

- 10 puntos por cada modelo que se cargue y renderize. Máximo de 4 modelos:
-- Pueden poner los modelos que quieran, pero solo los primeros 4 valen puntos.
-- Cada modelo repetido se cuenta una sola vez.
-- Los modelos deben estar texturizados.
-- También deben estar coherentemente ubicados en el mundo (transformaciones).
- 0 - 10 puntos por cada combinación de shaders distintos que se aplique a un modelo. Máximo 4 shaders:
-- Aplicar el mismo shader a más de un modelo sólo les da puntos la primera vez.
-- El shader no debe ser trivial y debe ser significativamente distinto a los demás shaders en su escena.
-- Se da la puntuación del shader dependiendo de su complejidad.
- 15 puntos por implementar mapas normales o bump mapping:
-- Es suficiente con que lo apliquen a un solo modelo. No puede ser un modelo trivial.
- 0 - 10 puntos según la complejidad del modelo más complejo (10 es muy complejo, algo cómo un personaje, 0 es algo como un cubo o una pirámide).
- 0 - 20 puntos, criterio subjetivo según la estética y creatividad de la escena.


Para que un modelo cuente dentro del puntaje, debe de ser proyectado en perspectiva con respecto a una cámara. Ustedes pueden definir la posición de la cámara o de las luces que decida agregar. Pueden usar modelos que encuentren en internet, no necesitan hacerlos ustedes mismos. No usar modelos que se trabajaron en clase. Es necesario compartir el render final al canal del ShowOff del Discord de la clase.

## Inicialización

 El Rasterizador puede ser ejecutado mediante la ejecución del archivo ```Main.py```, dentro de una ventana de shell, navegar al directorio donde se encuentran los archivos y correr el siguiente comando:
  ```bash
    python3 Main.py
  ```
## Resultado
El resultado del programa es el archivo ```output.bmp```, al abrir este se obtendra una imagen de una plaza, especificamente la plaza del juego Cruelty Squad de Consumer Softproducts, en la plaza se encuentran 4 modelos, de derecha a izquierda se puede observar primero el modelo de un **puesto de comida** en el cuál todo es dorado y se encuentra con un **Phong Shader**, a la par se puede obsevar el modelo del **mercader** del puesto orgulloso de su tesoro, pero este se encuentra atacado por el **Glitch Vertex Shader** y el **Glitch Fragment Shader** los cuales lo distorcionan y alteran su imagen. En el techo se puede observar colgando la estatua de **David de Miguel Ángel**, esta tiene un **Gradient Shader** que combina una gradiente de colores con el sombreado Phong Shader. Por último pero no menos importante, se puede ver a la izquierda del mercader el modelo de un **toro**, esta bien si no se ve al inicio, eso es porque tiene un **Diffuser Shader** para esconderse en la plaza.

La inspiración para esta imagen fue el juego Cruelty Squad, específicamente la estética que busca ser bizarra y confusa al principio. 
