"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Rt1: Spheres, Material & Phong Shading

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
raytracer.rtClearColor(0.2109,0.30078,0.42578)

boton = Material(diffuse=(0.02734,0.02734,0.0351), spec = 5, ks = 0.02)
nariz = Material(diffuse=(0.9884,0.2305,0.2304), spec = 5, ks = 0.02)
cuerpo = Material(diffuse=(0.941,0.8867,0.789), spec = 5, ks = 0.02)
boca = Material(diffuse=(0.3594,0.2969,0.289), spec = 5, ks = 0.02)
ojo = Material(diffuse=(0.8398,0.7656,0.8008), spec = 9, ks = 0.02)

#Nieve
raytracer.scene.append(Sphere(position=(0,-1.2,-5), radius = 1.2, material = cuerpo))
raytracer.scene.append(Sphere(position=(0,0.55,-5), radius = 0.95, material = cuerpo))
raytracer.scene.append(Sphere(position=(0,1.94,-5), radius = 0.7, material = cuerpo))

#Ojos
raytracer.scene.append(Sphere(position=(0.145,2.04,-4.1), radius = 0.05, material = ojo))
raytracer.scene.append(Sphere(position=(-0.145,2.04,-4.1), radius = 0.05, material = ojo))
raytracer.scene.append(Sphere(position=(-0.145,1.98,-3.95), radius = 0.025, material = boton))
raytracer.scene.append(Sphere(position=(0.145,1.98,-3.95), radius = 0.025, material = boton))

#Nariz
raytracer.scene.append(Sphere(position=(0,1.75,-4), radius = 0.17, material = nariz))

#Boca
raytracer.scene.append(Sphere(position=(-0.35,1.54,-4.15), radius = 0.075, material = boca))
raytracer.scene.append(Sphere(position=(-0.13,1.49,-4.15), radius = 0.075, material = boca))
raytracer.scene.append(Sphere(position=(0.12,1.51,-4.15), radius = 0.075, material = boca))
raytracer.scene.append(Sphere(position=(0.35,1.55,-4.15), radius = 0.075, material = boca))

#Botones
raytracer.scene.append(Sphere(position=(0,-1,-4), radius = 0.35, material = boton))
raytracer.scene.append(Sphere(position=(0,0.15,-4), radius = 0.25, material = boton))
raytracer.scene.append(Sphere(position=(0,1,-4), radius = 0.15, material = boton))

#Luz
raytracer.lights.append(AmbientLight(intensity=0.05))
raytracer.lights.append(DirectionalLight(direction=(0.5,-1,-2), intensity=0.90))
raytracer.lights.append(PointLight(point=(2.5,0,-5), intensity=1, color= (0.8,0.9,1)))


isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning=False
    
    raytracer.rtClear()
    raytracer.rtRender()
    pygame.display.flip()
                
pygame.quit()           