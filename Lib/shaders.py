"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Tarea 1 - Lines & Obj Models

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
from Lib.npPirata import multMV
def vertexShader(vertex, **kwargs):
     modelMatrix = kwargs["modelMatrix"]
     vt = [vertex[0], 
        vertex[1], 
        vertex[2], 
        1]
     vt = modelMatrix @ vt
     vt = [vt[0] / vt[3],
        vt[1] / vt[3],
        vt[2] / vt[3]]
     return vt

def fragmentShader(**kwargs):
    color = [1,1,1]
    return color