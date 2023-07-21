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

# def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     filledLength = int(length * iteration // total)
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
#     # Print New Line on Complete
#     if iteration == total: 
#         print()

print("Creando output.bmp")
# printProgressBar(0, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)

width = 1000
height = 1000
# printProgressBar(1, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)
rend = Renderer(width, height)
# printProgressBar(2, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader
# printProgressBar(3, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)

p1 = [[165, 380], [185, 360], [180, 330], [207, 345], [233, 330], [230, 360], [250, 380], [220, 385], [205, 410], [193, 383]] 
p2 = [[321, 335], [288, 286], [339, 251], [374, 302]]
p3 = [[377, 249], [411, 197], [436, 249]]
p4 = [[413, 177], [448, 159], [502, 88], [553, 53], [535, 36], [676, 37], [660, 52],
[750, 145], [761, 179], [672, 192], [659, 214], [615, 214], [632, 230], [580, 230],
[597, 215], [552, 214], [517, 144], [466, 180]]
p5 = [[682, 175], [708, 120], [735, 148], [739, 170]]


# printProgressBar(4, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)

# printProgressBar(5, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)

# printProgressBar(6, 6, prefix = 'Progreso: ', suffix = 'Completado', length = 50)

rend.glBuildPoly(p1)
rend.glPaintPoly(p1)


rend.glBuildPoly(p2)
rend.glPaintPoly(p2, color(1,0,0))


rend.glBuildPoly(p3)
rend.glPaintPoly(p3, color(0,1,0))



rend.glBuildPoly(p4)
rend.glPaintPoly(p4, color(0,0,1))




rend.glBuildPoly(p5, rend.clearColor)
rend.glPaintPoly(p5, rend.clearColor)


rend.glFinish("output.bmp")

