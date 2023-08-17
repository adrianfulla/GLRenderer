# Lab 2 - Shaders
El objetivo de este laboratorio, es que practiquen crear shaders interesantes utilizando los parámetros que tienen ya a su disposición.

Para éste lab, tienen que crear tres shaders diferentes y mostrar sus resultados usando su Rasterizador. La nota de los criterios subjetivos dependera de qué tan complejo e interesante sea el shader que implementen. Usen su creatividad y habilidades matemáticas/artísticas para crear sus shaders. Pueden agregar o implementar el uso de diferentes tipos de iluminación, texturas múltiples, argumentos del shader, etc.

Puntos:

- [Criterio subjetivo] 40 puntos por hacer la implementación de un shader de su elección o inventado por usted.
- [Criterio subjetivo] 40 puntos por hacer la implementación de un shader de su elección o inventado por usted.
- [Criterio subjetivo] 40 puntos por hacer la implementación de un shader de su elección o inventado por usted.

Tomen en cuenta las siguientes condiciones:

- La nota máxima es 100.
- Utilicen modelos y texturas de su elección, no el usado en clase.
- Se les anima a que usen el Discord para discutir entre sus compañeros diferentes soluciones soluciones de shaders, ejemplos o recursos que hayan encontrado.
- Tienen que compartir en el canal ShowOff del Discord por lo menos uno de los resultados de sus shaders.
- En su entrega, pueden mostrar sus Shaders restultantes ya sea en un solo FrameBuffer o en tres FrameBuffers diferentes.
- En caso de que encuentren una solución usando herramientas de inteligencia artificial, adjunten con su entrega la conversación que tuvieron con el AI y una explicación de cómo lo aplicaron a su solución.
- Tiene que haber una primera entrega para el final del día de clases que se asignó esta actividad con suficiente trabajo hecho (por lo menos un shader propio terminado). Sin esta primera entrega, la actividad se calificará al 50% de la nota. Sin embargo, a lo largo de la semana aún tendrán oportunidad de hacer múltiples entregas en caso de que sepan como mejorar lo que tiene.

## Inicialización

 El Rasterizador puede ser ejecutado mediante la ejecución del archivo ```Main.py```, dentro de una ventana de shell, navegar al directorio donde se encuentran los archivos y correr el siguiente comando:
  ```bash
    python3 Main.py
  ```
## Resultado
Al ejecutar el progama se deben obtener los siguientes cuatro archivos:
- ```GouradShader.bmp```
- ```PhongShader.bmp```
- ```GradientShader.bmp```
- ```GlitchShader.bmp```

Cada uno de estos corresponde a uno de los shaders implementados en este laboratorio, siendo el GouradShader el implementado en clase y se puede utilizar como punto de comparación con los demas.

## Herramientas Externas

En este laboratorio se utilizo el apoyo de la herramienta externa ChatGPT para crear una algoritmo que generará el ```Phong Shader``` en base al algoritmo creado para generar el ```Gourad Shader```. La conversación fue la siguiente: https://chat.openai.com/share/8bb3be52-93f1-46a2-9c9c-884f52f379e7

Se dio como referencia el algoritmo de Gourad Shader y se pidio que se implementara un Phong Shader. Este shader fue desarrollado por Bui Tuong Phong en la Universidad de Utah en 1973 y consiste en mejorar el Gourad shader teniendo una mejor aproximación a la sombra de una superficie suave. Utilizá un modelo de reflexión para generar reflejos especulares. Además utilizá el punto de la cámara para ajustar la reflexión que se genera en base al punto de luz.

Este algoritmo fue además utilizado para generar el ```glitchFragmentShader``` utilizado en el ```GlitchShader``` ya que este combina el uso de un vertex shader para crear las "anomalias" en los vertices con un fragment shader que genera descoloración en cada pixel.
