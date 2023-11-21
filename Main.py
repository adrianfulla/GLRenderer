"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Proyecto 3: OpenGL

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
import pygame
import glm
from pygame.locals import *
import time
from Lib.renderer import Renderer
from Lib.model import Model
from Lib.shaders import *
from Lib.obj import Obj

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

printProgressBar(0, 4, prefix = 'Progreso: ', suffix = 'Completado: Iniciando', length = 50)

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

printProgressBar(1, 4, prefix = 'Progreso: ', suffix = 'Completado: Creacion de ambiente    ', length = 50)

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

obj = Obj("Res/Models/cup.obj")
objData = []
for face in obj.faces:
    if len(face) == 3:
        for vertexInfo in face:
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
    elif len(face) == 4:
        for i in [0, 1, 2]:
            vertexInfo = face[i]
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
        for i in [0, 2, 3]:
            vertexInfo = face[i]
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)

printProgressBar(2, 4, prefix = 'Progreso: ', suffix = 'Completado: Creacion de modelo   ', length = 50)

model = Model(objData)
model.loadTexture("Res/Textures/cup.bmp")
model.position.z = -6
model.position.y = 0
model.scale = glm.vec3(1, 1, 1)
renderer.scene.append(model)
renderer.lightIntensity = 5.5
renderer.dirLight = glm.vec3(0.0, -1.0, -1.0)

printProgressBar(3, 4, prefix = 'Progreso: ', suffix = 'Completado: Cargado de modelo    ', length = 50)

printProgressBar(4, 4, prefix = 'Progreso: ', suffix = 'Completado: Terminado          ', length = 50)

isRunning = True
current_time = time.time()
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        renderer.clearColor[0] += deltaTime
    if keys[K_LEFT]:
        renderer.clearColor[0] -= deltaTime
    if keys[K_UP]:
        renderer.clearColor[1] += deltaTime
    if keys[K_DOWN]:
        renderer.clearColor[1] -= deltaTime
    if keys[K_SPACE]:
        renderer.clearColor[2] += deltaTime
    if keys[K_LSHIFT]:
        renderer.clearColor[2] -= deltaTime

    if keys[K_d]:
        model.rotation.y += deltaTime * 50
    if keys[K_a]:
        model.rotation.y -= deltaTime * 50
    if keys[K_w]:
        model.rotation.x += deltaTime * 50
    if keys[K_s]:
        model.rotation.x -= deltaTime * 50


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_1:
                print("Original")
                renderer.setShader(vertex_shader, fragment_shader)
            if event.key == pygame.K_2:
                print("Gourad")
                renderer.setShader(vertex_shader, gourad_fragment_shader)
            if event.key == pygame.K_3:
                print("Cell")
                renderer.setShader(vertex_shader, cell_fragment_shader)
            if event.key == pygame.K_4:
                print("Multicolor")
                renderer.setShader(vertex_shader, multicolor_fragment_shader)
            if event.key == pygame.K_5:
                print("Candy Cane")
                renderer.setShader(vertex_shader, candy_cane_fragment_shader)
            if event.key == pygame.K_6:
                print("Glitch Effect")
                renderer.setShader(glitch_vertex_shader, fragment_shader)
            if event.key == pygame.K_7:
                print("Color Shift Effect")
                renderer.setShader(vertex_shader, color_shift_fragment_shader)
            if event.key == pygame.K_8:
                print("Moving Effect")
                renderer.setShader(moving_vertex_shader, gourad_fragment_shader)

    renderer.render()
    pygame.display.flip()

pygame.quit()
