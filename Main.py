"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Rt2: Opaque, Reflective & Refractive Materials

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
import pygame
from pygame.locals import * 
from Lib.rt import Raytracer
from Lib.figure import *
from Lib.lights import *
from Lib.materials import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.envMap = pygame.image.load("Res/parkinglot.bmp")
raytracer.rtClearColor(0.25,0.25,0.25)

blanco = Material(diffuse=(255,255,255), spec = 10, ks = 0.02)
oro = Material(diffuse=(206,163,96), spec = 256, ks = 0.2)
haze = Material(diffuse=(95,75,139), spec = 32, ks = 0.1)
mirror = Material(diffuse=(230,230, 230), spec =64, ks = 0.02, matType=REFLECTIVE)
bMirror = Material(diffuse=(100,100, 255), spec =32, ks = 0.02, matType=REFLECTIVE)


objetos = [
            Sphere(position=(1,1,-5), radius = 0.5, material = oro),
            Sphere(position=(-2,0,-7), radius = 2, material = mirror),
            Sphere(position=(0.5,-1,-5), radius = 0.3, material = haze),
            Sphere(position=(2,0,-7), radius = 2, material = bMirror),
            ]

luces = [
    AmbientLight(intensity=0.01),
    DirectionalLight(direction=(-1,-1,-1), intensity=0.70),
    PointLight(point=(1.5,0,-5), intensity=1, color= (1,0,1))
]

for objeto in objetos:
    raytracer.scene.append(objeto)

for luz in luces:
    raytracer.lights.append(luz)
    
raytracer.rtClear()
raytracer.rtRender()


isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning=False
    
                
pygame.quit()           