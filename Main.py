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
from Lib.gl import Renderer, color
import Lib.shaders as shaders

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

print("Creando output.bmp")
#printProgressBar(0, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)

width = 960
height = 540

#printProgressBar(1, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)
rend = Renderer(width, height)
#printProgressBar(2, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

#printProgressBar(3, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)

rend.glLoadModel("Models/cup.obj", "Models/wall.bmp",translate = (0, 0, -5),
                 rotate = (0, 0, 0),
                 scale = (0.5,0.5,0.5))


#printProgressBar(4, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)
rend.glRender()

#printProgressBar(5, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)
rend.glFinish("output.bmp")

#printProgressBar(6, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)