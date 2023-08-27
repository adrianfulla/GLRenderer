"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Proyecto 1: Rasterizer

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

width = 1000
height = 602

rend = Renderer(width, height)
printProgressBar(1, 6, prefix = 'Progreso: ', suffix = 'Completado: Background ', length = 50)
rend.glBackgroundTexture("Models/Plaza.bmp")
rend.glClearBG()

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.gouradShader

printProgressBar(2, 6, prefix = 'Progreso: ', suffix = 'Completado: Cargando Modelos ', length = 50)

rend.glLoadModel("Models/statue.obj", "Models/cup.bmp", normalMapName=None,translate = (-1.3, 0.8, -8),
                 rotate = (-0.28, 0, 3.1),
                 scale = (0.3,0.3,0.3), vertexShader=shaders.vertexShader, 
                 fragmentShader= shaders.gradientShader) 


rend.glLoadModel("Models/bull.obj", "Models/gold.bmp", normalMapName=None,translate = (-2, -1.5, -5),
                 rotate = (-0.5, 0, 0),
                 scale = (0.5,0.5,0.5), vertexShader=shaders.vertexShader, 
                 fragmentShader= shaders.diffuseShader)


rend.glLoadModel("Models/merchant.obj", "Models/basket.bmp", normalMapName=None,translate = (0, -2.4, -6.5),
                 rotate = (-0.5, 0, -0.02),
                 scale = (0.75,0.75,0.75), vertexShader=shaders.glitchVertexShader, 
                 fragmentShader= shaders.glitchFragmentShader)   

rend.glLoadModel("Models/stall2.obj", "Models/gold.bmp", normalMapName="Models/stall_normals.bmp",translate = (2, -2.5, -7),
                 rotate = (-0.5, -2.7, -0.02),
                 scale = (1,1,1), vertexShader=shaders.vertexShader, 
                 fragmentShader= shaders.phongShader) 

printProgressBar(3, 6, prefix = 'Progreso: ', suffix = 'Completado: Iniciando Render', length = 50)

rend.glLookAt(camPos = (0,2,0), eyePos= (0,0,-5))

printProgressBar(4, 6, prefix = 'Progreso: ', suffix = 'Completado: Renderizando      ', length = 50)

rend.glRender()
printProgressBar(5, 6, prefix = 'Progreso: ', suffix = 'Completado: Creando Output.bmp', length = 50)
rend.glFinish("output.bmp")
rend.glClear()

printProgressBar(6, 6, prefix = 'Progreso: ', suffix = 'Completado: Terminado                    ', length = 50)
    