"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Proyecto 2: Ray Tracer

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
import pygame
from pygame.locals import * 
from Lib.rt import Raytracer
from Lib.figure import *
from Lib.lights import *
from Lib.materials import *

width = 770
height = 512

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.envMap = pygame.image.load("Res/field.png")
ballTexture = pygame.image.load("Res/ball_texture.png")

raytracer.rtClearColor(0.25,0.25,0.25)

blanco = Material(diffuse=(255,255,255), spec = 10, ks = 0.02)
red = Material(diffuse=(255,0,0), spec = 10, ks = 0.02)
celeste = Material(diffuse=(157, 240,251), spec=10, ks=0.2)
mirror = Material(diffuse=(255,100, 100), spec =64, ks = 0.02, matType=REFLECTIVE)
glass =  Material(diffuse=(100,255, 255), spec =64, ior = 1.5, ks = 0.02, matType=TRANSPARENT)
ball = Material(spec=100, ks=1.5, texture=ballTexture, matType=OPAQUE)
cuero = Material(diffuse=(234,191,146), spec = 10, ks = 0.02)
negro = mirror = Material(diffuse=(100,100, 100), spec =70, ks = 0.05, matType=REFLECTIVE)

objetos = [
            
            OvalSphere(position=(-10,-5,-15), radius=(1.1, 2.0, 1.0), material=ball), #Pelota de rugby
            Cylinder(position=(-10.5,-7.5,-16), radius=0.4, height=0.5, material=cuero), #Tee cuero
            Cylinder(position=(-10.5,-8,-16), radius=0.5, height=0.8, material=negro), #Tee cuero
            AABB(position=(0,-14,-100), size=(175,5,1), material=blanco), #Valla publicitaria
            AABB(position=(50,-14,-99.99), size=(20,4,1), material=red), #Valla publicitaria, anuncio
            AABB(position=(-50,-14,-99.99), size=(20,4,1), material=red), #Valla publicitaria, anuncio
            AABB(position=(25,-14,-99.99), size=(15,4,1), material=glass), #Valla publicitaria, anuncio
            AABB(position=(0,-14,-99.99), size=(20,4,1), material=mirror), #Valla publicitaria, anuncio
            Cylinder(position=(-40,-16,-90), radius=1, height=8, material=celeste), #Poste izquierdo, parte inferior
            Cylinder(position=(-5,-16,-90), radius=1, height=8, material=celeste), #Poste derecho, parte inferior
            Cylinder(position=(-40,10,-90), radius=0.6, height=50, material=blanco), #Poste izquierdo, parte superior
            Cylinder(position=(-5,10,-90), radius=0.6, height=50, material=blanco), #Poste derecho, parte superior
            AABB(position=(-22.5,-5,-90), size=(35,1,1), material=blanco), #Poste perpendicular
            
            
            
            ]

luces = [
    AmbientLight(intensity=0.5, color=(1,1,1)),
    DirectionalLight(direction=(0,0.5,-1), intensity=0.8, color=(1,1,1)),

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