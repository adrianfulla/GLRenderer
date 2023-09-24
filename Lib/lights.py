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
import Lib.notnumpy as nnp
from math import acos, asin

def reflectVector(normal, direction):
    reflect = 2*nnp.dot_product(normal, direction)
    reflect = nnp.multiply(reflect, normal)
    reflect = nnp.sub(reflect, direction)
    reflect = nnp.divTF(reflect , nnp.norm(reflect))
    
    return reflect

def totalInternalReflection(incident, normal, n1, n2):
    if n1 < n2:
        n1, n2 = n2, n1
        
    Ai = acos(nnp.dot_product(incident, normal))
    Ac = asin(n2/n1)
    
    return Ai >= Ac

def fresnel(n1, n2):
    Kr = ((n1**0.5 - n2**0.5)**2) / ((n1**0.5 + n2**0.5)**2)
    Kt = 1 - Kr
    
    return Kr, Kt

def refractVector(incident, normal ,n1, n2):
    #Snell's Law
    
    refract = nnp.multiply(nnp.dot_product(incident, normal), normal)
    refract = nnp.sub(incident, refract)
    refract = n1 * refract
    refract = refract / n2
    refract = refract / nnp.norm(refract)
    
    return refract

class Light(object):
    def __init__(self, intensity = 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType
    
    def getLightColor(self):
        return [self.color[0]*self.intensity,
                self.color[1]*self.intensity,
                self.color[2]*self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intercept, viewPos):
        return None
    

class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,0,0)):
        super().__init__(intensity,color,"Ambient")

class DirectionalLight(Light):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = nnp.divTF(direction, nnp.norm(direction))
        super().__init__(intensity,color,"Directional")
    
    def getDiffuseColor(self, intercept):
        
        dir =[(i*-1) for i in self.direction]
        
        intensity = nnp.dot_product(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks
        
        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir =[(i*-1) for i in self.direction]
        reflect = reflectVector(intercept.normal, dir)
        
        viewDir = nnp.sub(viewPos,intercept.point)
        viewDir = nnp.divTF(viewDir, nnp.norm(viewDir))
                
        #Cambia dependiendo de la superficie
        specIntensity = max(0, nnp.dot_product(viewDir, reflect))** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor

class PointLight(Light):
    def __init__(self, point = (0,0,0), intensity = 1, color = (1,1,1)):
        self.point = point
        super().__init__(intensity, color, "Point")
        
    def getDiffuseColor(self, intercept):
        dir = nnp.sub(self.point, intercept.point)
        R = nnp.norm(dir)
        dir = nnp.divTF(dir, R)
        
        intensity = nnp.dot_product(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.ks
        
        #Ley de cuadrados inversos
        #If = intensity/R**2
        #R: distancia del punto intercepto a la luz punto.
        
        if R!=0:
            intensity /= R**2
        intensity = max(0, min(1, intensity))

        
        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = nnp.sub(self.point, intercept.point)
        R = nnp.norm(dir)
        dir = nnp.divTF(dir, R)
        
        reflect = reflectVector(intercept.normal, dir)
        
        viewDir = nnp.sub(viewPos,intercept.point)
        viewDir = nnp.divTF(viewDir, nnp.norm(viewDir))
        
        #Cambia dependiendo de la superficie
        specIntensity = max(0, nnp.dot_product(viewDir, reflect))** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity
        
        if R!=0:
            specIntensity /= R**2
            
        specIntensity = max(0, min(1, specIntensity))
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor
        
        