"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Lab 3: Ray-Intersect Algorithm, New Shapes

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
import pygame
from pygame.locals import * 
from Lib.rt import Raytracer
from Lib.figure import *
from Lib.lights import *
from Lib.materials import *

width = 516
height = 516

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.envMap = pygame.image.load("Res/City.jpg")
#skyTexture = pygame.image.load("Res/sky.jpg")
ballTexture = pygame.image.load("Res/ball_texture.png")
raytracer.rtClearColor(0.25,0.25,0.25)

blanco = Material(diffuse=(255,255,255), spec = 10, ks = 0.02)
# red = Material(diffuse=(255,0,0), spec = 10, ks = 0.02)
# oro = Material(diffuse=(206,163,96), spec = 256, ks = 0.2, matType=OPAQUE)
# haze = Material(diffuse=(95,75,139), spec = 32, ks = 0.1)
mirror = Material(diffuse=(200,200, 200), spec =64, ks = 0.02, matType=REFLECTIVE)
# sky = Material(spec=64, ks=0.1, texture=skyTexture, matType=REFLECTIVE)
# grass = Material(diffuse=(100,225,100), spec = 46, ks = 0.05)
glass =  Material(diffuse=(100,255, 255), spec =64, ior = 1.5, ks = 0.02, matType=TRANSPARENT)
# ball = Material(spec=50, ks=0.4, texture=ballTexture, matType=OPAQUE) 

objetos = [
            OvalSphere(position=(0,0,-6), radius=(2, 0.9, 1.0), material=blanco),
            # OvalSphere(position=(0,0,-6), radius=(2, 0.9, 1.0), material=mirror), #Material Reflectivo
            # OvalSphere(position=(0,0,-6), radius=(2, 0.9, 1.0), material=glass), #Material Transparente
            ]

luces = [
    AmbientLight(intensity=0.4, color=(1,0.8,1)),
    DirectionalLight(direction=(0,0,-1), intensity=0.2, color=(0.5,1,1)),
    PointLight(point=(-2,1,-4.5), intensity=1, color=(1,1,1))
]

for objeto in objetos:
    raytracer.scene.append(objeto)

for luz in luces:
    raytracer.lights.append(luz)
    
raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:",pygame.time.get_ticks()/1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning=False
    
                
pygame.quit()           