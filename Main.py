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
import math
import random
from Lib.renderer import Renderer
from Lib.model import Model
from Lib.shaders import *
from Lib.obj import Obj


width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()


ambientSound = pygame.mixer.Sound("Res/Music/ambient.mp3")
shiftSound = pygame.mixer.Sound("Res/Music/shift.wav")
swooshSound = pygame.mixer.Sound("Res/Music/swoosh.wav")
thumpSound = pygame.mixer.Sound("Res/Music/thump.wav")

ambientSound.play(-1)

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)
drag = False
oldPosition = None
actualShader = 0


def loadModel(object):
    objData = []
    for face in object.faces:
        if len(face) == 3:
            for vertexInfo in face:
                vertexID, texcoordID, normalID = vertexInfo
                vertex = object.vertices[vertexID - 1]
                normals = object.normals[normalID - 1]
                uv = object.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objData.extend(vertex + uv + normals)
        elif len(face) == 4:
            for i in [0, 1, 2]:
                vertexInfo = face[i]
                vertexID, texcoordID, normalID = vertexInfo
                vertex = object.vertices[vertexID - 1]
                normals = object.normals[normalID - 1]
                uv = object.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objData.extend(vertex + uv + normals)
            for i in [0, 2, 3]:
                vertexInfo = face[i]
                vertexID, texcoordID, normalID = vertexInfo
                vertex = object.vertices[vertexID - 1]
                normals = object.normals[normalID - 1]
                uv = object.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objData.extend(vertex + uv + normals)
    return objData

def printMenu():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to the 3D model viewer! To see this menu again, press M.")
    print("We recommend you volume up your speakers to enjoy the experience!")

    print("\nModels available:")
    print("\t- A cute ducky plush (press 1)")
    print("\t- A cute litle octopus (press 2)")
    print("\t- A shiny diamond (press 3)")
    print("\t- A cute kitty plush (press 4)")
    print("\t\t* If you have the kitty on your screen, press 9 and 0 for a surprise!")

    print("\nShaders available:")
    print("\t- Original shader (press n)")
    print("\t- Party shader (press p)")
    print("\t- Sparkling shader (press s)")
    print("\t- Distorsioned shader (press d)")
    print("\t- Outline shader (press o)")
    print("\t\t* If you have a shader on your screen, press a for se the alternative version!")

    print("\nControls:")
    print("\t- Use the arrow keys to rotate the model")
    print("\t- Use the + and - keys to move the model closer or farther")
    print("\t- Use the mouse wheel to zoom in and out")
    print("\t- Use the mouse to rotate the camera around the model")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

obj = Obj("Res/Models/Penguin.obj")
objData = loadModel(obj)


model = Model(objData)
model.loadTexture("Res/Textures/Penguin.png")
model.position.z = -6
model.position.y = 0
model.scale = glm.vec3(1, 1, 1)
renderer.scene.append(model)
renderer.lightIntensity = 5.5
renderer.dirLight = glm.vec3(0.0, -1.0, -1.0)

movement_sensitive = 0.1
sens_x = 1
sens_y = 0.1
distance = abs(renderer.cameraPosition.z- model.position.z)
radius = distance
zoom_sensitive = 0.5
angle = 0.0


isRunning = True
current_time = time.time()
printMenu()
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()
    
    renderer.cameraPosition.x = math.sin(math.radians(angle)) * radius + model.position.x
    renderer.cameraPosition.z = math.cos(math.radians(angle)) * radius + model.position.z

    if keys[K_RIGHT]:
        model.rotation.y += deltaTime * 50
    if keys[K_LEFT]:
        model.rotation.y -= deltaTime * 50
    if keys[K_UP]:
        if (model.rotation.x <= 45):
            model.rotation.x += deltaTime * 50
    if keys[K_DOWN]:
        if (model.rotation.x >= -100):
            model.rotation.x -= deltaTime * 50
    if keys[K_PLUS]:
        if (model.position.z <= 0):
            model.position.z += 0.1
    if keys[K_MINUS]:
        if (model.position.z >= -10):
            model.position.z -= 0.1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_q:
                actualShader = 0
                print("Original")
                swooshSound.play()
                renderer.setShader(vertex_shader, fragment_shader)
            if event.key == pygame.K_w:
                actualShader = 1
                print("Candy Cane")
                swooshSound.play()
                renderer.setShader(vertex_shader, candy_cane_fragment_shader)
            if event.key == pygame.K_e:
                actualShader = 2
                print("Moving Effect")
                swooshSound.play()
                renderer.setShader(moving_vertex_shader, gourad_fragment_shader)
            if event.key == pygame.K_r:
                actualShader = 3
                print("Glitch Effect")
                swooshSound.play()
                renderer.setShader(glitch_vertex_shader, fragment_shader)
            if event.key == pygame.K_t:
                actualShader = 4
                print("Color Shift Effect")
                swooshSound.play()
                renderer.setShader(vertex_shader, color_shift_fragment_shader)
            if event.key == pygame.K_a:
                if (actualShader == 1):
                    print("Candy Cane alternative shader")
                    swooshSound.play()
                    renderer.setShader(vertex_shader, candy_cane_alt_fragment_shader)
                if (actualShader == 2):
                    print("Moving effect alternative shader")
                    swooshSound.play()
                    renderer.setShader(moving_vertex_alt_shader, fragment_shader)
                if (actualShader == 3):
                    print("Glitch effect alternative shader")
                    swooshSound.play()
                    renderer.setShader(glitch_alt_vertex_shader, fragment_shader)
                if (actualShader == 4):
                    print("Color Shift alternative shader")
                    swooshSound.play()
                    renderer.setShader(vertex_shader, color_shift_alt_fragment_shader)
            if event.key == pygame.K_b:
                random.seed(int(time.time()))
                randFragment = random.randint(1, 5)
                randVertex = random.randint(1, 5)
                if randFragment == 1:
                    fragment = fragment_shader
                    print("Original fragment shader")
                elif randFragment == 2:
                    fragment = candy_cane_fragment_shader
                    print("Candy Cane")
                elif randFragment == 3:
                    fragment = color_shift_fragment_shader
                    print("Color Shift Effect")
                elif randFragment == 4:
                    fragment = candy_cane_alt_fragment_shader
                    print("Alt Candy Cane")
                elif randFragment == 5:
                    fragment = color_shift_alt_fragment_shader
                    print("Alt Color Shift Effect")
                
                if randVertex == 1:
                    vertex = vertex_shader
                    print("Original vertex shader")
                elif randVertex == 2:
                    vertex = glitch_vertex_shader
                    print("Glitch effect shader")
                elif randVertex == 3:
                    vertex = moving_vertex_shader
                    print("Moving effect shader")
                elif randVertex == 4:
                    vertex = glitch_alt_vertex_shader
                    print("Glitch effect alternative shader")
                elif randVertex == 5:
                    vertex = moving_vertex_alt_shader
                    print("Moving effect alternative shader")
                
                swooshSound.play()
                renderer.setShader(vertex, fragment)
                
            if event.key == pygame.K_1:
                print("A bull has appeared!")
                thumpSound.play()
                renderer.scene.clear()
                obj = Obj("Res/models/bull.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Res/Textures/gold.bmp")
                model.position.z = -7
                model.position.y = -2
                model.position.x = -0.3
                model.rotation.y = 90
                model.scale = glm.vec3(1.20, 1.20, 1.20)
                renderer.scene.append(model)
                
            if event.key == pygame.K_2:
                print("The penguin returns!")
                shiftSound.play()
                renderer.scene.clear()
                obj = Obj("Res/Models/Penguin.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Res/Textures/Penguin.png")
                model.position.z = -3
                model.position.y = 0
                model.position.x = 0
                model.rotation.y = 0
                model.scale = glm.vec3(0.5, 0.5, 0.5)
                renderer.scene.append(model)
                
            if event.key == pygame.K_3:
                print("Class time, statue is here!")
                shiftSound.play()
                renderer.scene.clear()
                obj = Obj("Res/Models/statue.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Res/Textures/gold.bmp")
                model.position.z = -10
                model.position.y = 0
                model.position.x = 4
                model.rotation.y = 0
                model.scale = glm.vec3(1, 1, 1)
                renderer.scene.append(model)
            if event.key == pygame.K_4:
                print("Ominous cup")
                shiftSound.play()
                renderer.scene.clear()
                obj = Obj("Res/Models/cup.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Res/Textures/cup.bmp")
                model.position.z = -6
                model.position.y = 0
                model.position.x = 0
                model.rotation.y = 0
                model.scale = glm.vec3(1, 1, 1)
                renderer.scene.append(model)
        
        elif event.type == pygame.MOUSEWHEEL:
            if (model.position.z <= 0) and (model.position.z >= -10):
                model.position.z += (0.1 * event.y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                drag = True
                oldPosition = pygame.mouse.get_pos()

            elif event.button == 4:
                if radius > distance * 0.5:
                    radius -= zoom_sensitive             

            elif event.button == 5:
                if radius < distance * 1.5:
                    radius += zoom_sensitive
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                drag = True
                oldPosition = pygame.mouse.get_pos()

            elif event.button == 4:
                if radius > distance * 0.5:
                    radius -= zoom_sensitive             

            elif event.button == 5:
                if radius < distance * 1.5:
                    radius += zoom_sensitive

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                drag = False

        elif event.type == pygame.MOUSEMOTION:
            if drag:
                new_position = pygame.mouse.get_pos()
                deltax = new_position[0] - oldPosition[0]
                deltay = new_position[1] - oldPosition[1]
                angle += deltax * -sens_x

                if angle > 360:
                    angle = 0

                if distance > renderer.cameraPosition.y + deltay * -sens_y and distance * -1.5 < renderer.cameraPosition.y + deltay * -sens_y:
                    renderer.cameraPosition.y += deltay * -sens_y

                oldPosition = new_position



    renderer.updateViewMatrix()
    renderer.render()
    pygame.display.flip()

pygame.quit()
