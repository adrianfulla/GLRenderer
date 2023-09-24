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

class Intercept(object):
    def __init__(self, distance, point, normal, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.obj = obj

class Shape(object):
    def __init__(self,position,material):
        self.position = position
        self.material = material

    def ray_intersect(self,orig,dir):
        return None

class Sphere(Shape):
    def __init__(self,position,radius,material):
        self.radius = radius
        super().__init__(position,material)
        
    def ray_intersect(self, orig, dir):
        l = nnp.sub(self.position, orig)
        lengthL = nnp.norm(l)
        tca = nnp.dot_product(l,dir)
        
        d = (lengthL**2 - tca**2)**0.5
        if d > self.radius:
            return None
        
        thc = (self.radius**2 - d**2)**0.5
        t0 = tca - thc
        t1 = tca + thc
        
        if t0<0:
            t0 = t1
        if t0<0:
            return None
        
        p = nnp.add(orig,nnp.multiply(t0, dir))
        normal = nnp.sub(p,self.position)
        normal = nnp.divTF(normal, nnp.norm(normal))
        
        return Intercept(distance = t0,
                         point = p,
                         normal = normal,
                         obj = self)
        