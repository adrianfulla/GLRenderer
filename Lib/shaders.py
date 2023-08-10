"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Tarea 3 - Camaras

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
def vertexShader(vertex, **kwargs):
     modelMatrix = kwargs["modelMatrix"]
     viewMatrix = kwargs["viewMatrix"]
     projectionMatrix = kwargs["projectionMatrix"]
     vpMatrix = kwargs["vpMatrix"]

     vts = [vertex[0],
          vertex[1],
          vertex[2],
          1]

     vt = vpMatrix * projectionMatrix * viewMatrix * modelMatrix  @ vts

     vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

     return vt

def fragmentShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1,1,1)

    return color