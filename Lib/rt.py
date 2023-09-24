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
from math import tan, pi
import random
from Lib.materials import *
from Lib.lights import *
import Lib.notnumpy as nnp
import pygame


MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect() 
        
        self.scene = []
        self.lights = []
        
        self.camPosition = [0,0,0]
        
        self.rtViewport(0, 0, self.width, self.height)
        self.rtProyection()
        
        self.rtClearColor(0,0,0)
        self.rtColor(1,1,1)
        self.rtClear()
        
        self.envMap = None
        
    
    def rtViewport(self,posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height
    
    def rtProyection(self,fov=60,n=0.1):
        aspectRatio = self.vpWidth/self.vpHeight
        self.nearPlane = n
        self.topEdge = tan((fov*pi/180)/2)*self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio
       
    def rtClearColor(self, r, g, b):
        self.clearColor = (r*255,g*255,b*255)
    
    def rtClear(self):
        self.screen.fill((self.clearColor))
    
    def rtColor(self,r,g,b):
        self.currentColor = (r*255,g*255,b*255)
    
    def rtPoint(self,x,y,color = None):
        y = self.height - y
        
        if (0<=x<self.width) and (0<=y<self.height):
            if color != None:
                color = (int(color[0]*255),
                         int(color[1]*255),
                         int(color[2]*255))
                
                self.screen.set_at((x,y), color)
            else:
                self.screen.set_at((x,y), self.currentColor)
    
    def rtCastRay(self,orig,dir,sceneObj = None, recursion = 0):
        if recursion >= MAX_RECURSION_DEPTH:
            return None
       
        depth = float('inf')
        intercept = None
        hit = None
        
        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(orig, dir)
                if intercept != None:
                        
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        return hit
    
    def rtRayColor(self, intercept, rayDirection, recursion = 0):
        if intercept != None:
            #Phong Reflection Model
            #LightColor = AmbientIntensity + DiffuseIntensity + SpecularIntensity
            #FinalColor = SurfaceColor * LightColor
            
            material = intercept.obj.material
            finalColor = [0,0,0]
            surfaceColor = material.diffuse
            ambientColor = [0,0,0]
            diffuseColor = [0,0,0]
            specularColor = [0,0,0]
            reflectColor = [0,0,0]
            
            if material.matType == OPAQUE:
                
                
                for light in self.lights:
                    if light.lightType == "Ambient":
                        ambientColor = [(ambientColor[i]+light.getLightColor()[i]) for i in range(3)]
                    
                    else:
                        lightDir = None
                        if light.lightType == "Directional":
                            lightDir = [(i*-1) for i in light.direction]
                        elif light.lightType == "Point":
                            lightDir = nnp.sub(light.point, intercept.point)
                            lightDir = nnp.divTF(lightDir, nnp.norm(lightDir))
                            
                        shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                        
                        if shadowIntersect==None:
                            diffuseColor = [(diffuseColor[i]+light.getDiffuseColor(intercept)[i]) for i in range(3)]
                            specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
                
            elif material.matType == REFLECTIVE:
                reflect = reflectVector(intercept.normal, nnp.multiply(-1, rayDirection))
                reflectIntercept = self.rtCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
                reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)
                
                for light in self.lights:
                    if light.lightType != "Ambient":
                        lightDir = None
                        if light.lightType == "Directional":
                            lightDir = [(i*-1) for i in light.direction]
                        elif light.lightType == "Point":
                            lightDir = nnp.sub(light.point, intercept.point)
                            lightDir = nnp.divTF(lightDir, nnp.norm(lightDir))
                            
                        shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                        
                        if shadowIntersect==None:
                            specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
                
                
            lightColor = [(ambientColor[i]+diffuseColor[i]+specularColor[i] + reflectColor[i]) for i in range(3)]  
            finalColor = [min(1,surfaceColor[i]*lightColor[i])for i in range(3)]
            return finalColor     
        else:
            return [i /255 for i in self.clearColor]
    
    def rtRender(self):
        indexes = [(i, j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indexes)
        for i, j in indexes:
            x = i + self.vpX
            y = j + self.vpY
            if (0<=x<self.width) and (0<=y<self.height):
                pX = ((x+0.5-self.vpX)/self.vpWidth)*2-1
                pY = ((y+0.5-self.vpY)/self.vpHeight)*2-1
                
                pX*=self.rightEdge
                pY*=self.topEdge
                
                direction = (pX,pY,-self.nearPlane)
                direction = nnp.divTF(direction, nnp.norm(direction))
                
                intercept = self.rtCastRay(self.camPosition, direction)
                
                    
                self.rtPoint(x,y,self.rtRayColor(intercept, direction))
                pygame.display.flip() 
                    