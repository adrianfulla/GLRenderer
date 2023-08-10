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
printProgressBar(0, 6, prefix = 'Progreso: ', suffix = 'Completado: Iniciando', length = 50)

width = 500
height = 500


rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

printProgressBar(1, 6, prefix = 'Progreso: ', suffix = 'Completado: Cargando Modelo ', length = 50)

rend.glLoadModel("Models/cup.obj", "Models/cup.bmp",translate = (0, 0, -5),
                 rotate = (0, 0, 0),
                 scale = (1,1,1))

#Medium shot
rend.glLookAt(camPos = (0,2,0), eyePos= (0,0,-5))
printProgressBar(2, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando Medium Shot ', length = 50)
rend.glRender()
rend.glFinish("medium.bmp")

rend.glClear()

#Low angle
rend.glLookAt(camPos = (0,-1,0), eyePos= (0,2.5,-5))
printProgressBar(3, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando Low Angle    ', length = 50)
rend.glRender()
rend.glFinish("low.bmp")


rend.glClear()

#High angle
rend.glLookAt(camPos = (0,5,0), eyePos= (0,-2.5,-5))
printProgressBar(4, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando High Angle ', length = 50)
rend.glRender()
rend.glFinish("high.bmp")

rend.glClear()

#Dutch angle
rend.glClearModel()
rend.glLoadModel("Models/cup.obj", "Models/cup.bmp",translate = (0, 0, -5),
                 rotate = (0, 0, 1),
                 scale = (1,1,1))
rend.glLookAt(camPos = (-0.5,2,0), eyePos= (-0.2,0.4,-2))
printProgressBar(5, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando Dutch Angle ', length = 50)
rend.glRender()
rend.glFinish("dutch.bmp")

printProgressBar(6, 6, prefix = 'Progreso: ', suffix = 'Completado: Terminado              ', length = 50)
