# Lab 3: Ray-Intersect Algorithm, New Shapes
Objetivos:

- Que los alumnos renderizen una nueva figura a través del RayTracer simple que hemos estado trabajando.
Para éste lab, tienen que investigar e implementar el Ray Intersect Algorithm de una figura de su elección. La figura puede ser cualquiera de las siguientes opciones:

-- Triángulo (puede ser usado después para dibujar modelos)
-- OBBs (oriented bounding boxes)
-- Cilindro
-- Capsula
-- Toroide/dona
-- Esfera ovalada


Condiciones:

Para obtener la nota completa de ésta tarea deben entregar lo siguiente:

- Solamente es necesario elabrorar el algoritmo de una sola figura, pero están en libertad de elaborarlo para múltiples figuras.
- Para recibir la nota completa, en la imagen final la figura tiene que renderizarse tres veces con diferentes tamaños, posiciones y materiales (uno opaco, uno reflectivo y otro transparente) para demostrar que el algoritmo funciona correctamente.
- No usen las texturas compartidas en clase.
- Se les anima a que usen el Discord para discutir entre sus compañeros y compartir recursos de diferentes soluciones de algoritmos de intersección de rayos.
- Tienen que compartir en el canal ShowOff del Discord el resultado.
- En caso de que encuentren una solución usando herramientas de inteligencia artificial, adjunten con su entrega la conversación que tuvieron con el AI y una explicación de cómo lo aplicaron a su solución.


## Inicialización
El Rasterizador puede ser ejecutado mediante la ejecución del archivo Main.py, dentro de una ventana de shell, navegar al directorio donde se encuentran los archivos y correr el siguiente comando:
  ```bash
    python3 Main.py
  ```  

## Resultado
- Objeto con textura opaca:
 ![Alt text](/Opaque.png)
- Objeto con textura reflectiva:
 ![Alt text](/Mirror.png)
- Objeto con textura transparente:
 ![Alt text](/Transparent.png)

## Herramientas Externas
En este laboratorio se utilizo apoyo de la herramienta externa ChatGPT para crear una clase de figura que pueda modelar una esfera ovalada o un esferoide, esta se encuentra en el clase'''OvalSphere''' dentro de '''figure.py'''. La conversacion fue la siguiente: https://chat.openai.com/share/ba9ba7e4-b456-4853-864c-a01a613e5184

En la conversacion se le fue mostrando a ChatGPT como se generaban figuras en el rasterizador actual y en base a esto se le pidio que generara la clase para crear esferoides. El codigo funciona de la siguiente manera:
-Se crea la clase '''OvalSphere''' con los parametros de posicion, radio y material, la diferencia entre el radio de '''OvalSphere''' y de '''Sphere''' es que se pide una tupla de 3 elementos representando el radio en cada eje del esferoide.
-Cuando se realiza la funcion '''ray_intersect''' para el esferoide se normaliza tanto la longitud del punto a la posicion como la direccion por los radios. Luego se obtienen los coeficientes de la ecuacion cuadratica y se calcula el discriminante.
-Si el discriminante es menor que 0 entonces se retorna nulo ya que no hay interseccion con el objeto.
-En cambio, si el discriminante es mayor se procede a encontrar los puntos de interseccion y se determina si el esferoide esta frente a la camara, detras o en medio.
- Se obtiene el punto sumando el origen con la multiplicacion entre el punto de interseccion mas cercano y la direccion
- Luego se calcula la normal utilizando el punto y la posicion y se normaliza por los radios y luego se normaliza el vector.
-Por ultimo se calcula phi y theta utilizando las normales y con estos se encuentran los puntos uv para el mapa de texturas.
-Se retorna el Intercepto con la distancia al punto intercepto mas cercano, el punto, las normales, las uvs y el objeto propio.
