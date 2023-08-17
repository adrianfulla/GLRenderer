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
rend.fragmentShader = shaders.gouradShader

printProgressBar(1, 6, prefix = 'Progreso: ', suffix = 'Completado: Cargando Modelo ', length = 50)

rend.glLoadModel("Models/cup.obj", "Models/cup.bmp",translate = (0, 1, -2),
                 rotate = (-1, 5, 0),
                 scale = (1,1,1))

rend.glLookAt(camPos = (0,2,0), eyePos= (0,0,-5))
printProgressBar(2, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando Gourud Shader ', length = 50)

rend.glRender()
rend.glFinish("GourudShader.bmp")
rend.glClear()

printProgressBar(3, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando Phong Shader ', length = 50)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.phongShader

rend.glRender()
rend.glFinish("PhongShader.bmp")
rend.glClear()

printProgressBar(4, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando Gradient Shader ', length = 50)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.gradientShader

rend.glRender()
rend.glFinish("GradientShader.bmp")
rend.glClear()

printProgressBar(5, 6, prefix = 'Progreso: ', suffix = 'Completado: Generando Glitch Shader ', length = 50)
rend.vertexShader = shaders.glitchVertexShader
rend.fragmentShader = shaders.glitchFragmentShader

rend.glRender()
rend.glFinish("GlitchShader.bmp")
rend.glClear()

printProgressBar(6, 6, prefix = 'Progreso: ', suffix = 'Completado: Terminado                    ', length = 50)
    