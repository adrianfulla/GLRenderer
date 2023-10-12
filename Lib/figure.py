"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Rt3: Planes, Disks and Cubes

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
import Lib.notnumpy as nnp
from math import tan, pi, atan2, acos
import numpy as np

class Intercept(object):
    def __init__(self, distance, point, normal, texcoords, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
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
        
    def ray_intersect(self, orig, direction):
        l = nnp.sub(self.position, orig)
        lengthL = nnp.norm(l)
        tca = nnp.dot_product(l,direction)
        
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
        
        p = nnp.add(orig,nnp.multiply(t0, direction))
        normal = nnp.sub(p,self.position)
        normal = nnp.divTF(normal, nnp.norm(normal))
        
        u = atan2(normal[2], normal[0]) / (2 * pi) + 0.5
        v = acos(normal[1]) / pi
        
        return Intercept(distance = t0,
                         point = p,
                         normal = normal,
                         texcoords=(u, v),
                         obj = self)
        
class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = nnp.divTF(normal,nnp.norm(normal))
        super().__init__(position, material)
        
    def ray_intersect(self, orig, dir):
        denom = nnp.dot_product(dir, self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = nnp.dot_product(nnp.sub(self.position, orig), self.normal)
        t = num / denom
        
        if t < 0:
            return None
        
        P = nnp.add(orig, nnp.multiply(t, dir))
        
        return Intercept(distance= t,
                         point= P,
                         normal= self.normal,
                         texcoords= None,
                         obj= self)
            
class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)
        
    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)
        
        if planeIntersect is None:
            return None
        
        contactDist = nnp.sub(planeIntersect.point, self.position)
        
        contactDist = nnp.norm(contactDist)
        
        if contactDist > self.radius:
            return None
        
        return Intercept(distance= planeIntersect.distance,
                         point= planeIntersect.point,
                         normal= self.normal,
                         texcoords= None,
                         obj= self)
        
        
class AABB(Shape):
    def __init__(self, position, size,material):
        self.size = size
        super().__init__(position, material)
        
        self.planes = [Plane(nnp.add(self.position, (-size[0] / 2, 0,0)),(-1,0,0), material ),
                       Plane(nnp.add(self.position, (size[0] / 2, 0,0)),(1,0,0), material ),
                       Plane(nnp.add(self.position, (0, -size[1] / 2,0)),(0,-1,0), material ),
                       Plane(nnp.add(self.position, (0, size[1] / 2,0)),(0,1,0), material ),
                       Plane(nnp.add(self.position, (0, 0,-size[2] / 2)),(0,0,-1), material ),
                       Plane(nnp.add(self.position, (0, 0,size[2] / 2)),(0,0,1), material )]
        
        #Bounds
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]
        
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (0.001 + size[i]/2)
            self.boundsMax[i] = self.position[i] + (0.001 + size[i]/2)
            
    def ray_intersect(self, orig, dir):
       # super().ray_intersect(orig, dir)
        intersect = None
        t = float('inf')
        
        u = 0
        v = 0
        
        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig, dir)
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0] <= planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect
                                
                                if abs(plane.normal[0]) > 0:
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[1]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[2]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
        if intersect is None:
            return None
        
        return Intercept(distance= t,
                         point= intersect.point,
                         normal= intersect.normal,
                         texcoords= (u,v),
                         obj= self) 


class OvalSphere(Shape):
    def __init__(self,position,radius,material):
        self.radii = radius
        super().__init__(position,material)
        
    def ray_intersect(self, orig, direction):
        # Transform the ray to local coordinates
        l = np.array(np.subtract(orig, self.position), dtype=np.float64)  # Ensure l is float64
        self.radii = np.array(self.radii, dtype=np.float64)
        l /= self.radii  # Normalize by the radii
        direction /= self.radii  # Normalize the ray direction

        # Calculate the coefficients of the quadratic equation
        a = np.dot(direction, direction)
        b = 2.0 * np.dot(direction, l)
        c = np.dot(l, l) - 1.0  # The radii are normalized, so this is 1.0

        # Calculate the discriminant
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            # No intersection
            return None

        # Calculate the two solutions for t
        t1 = (-b + np.sqrt(discriminant)) / (2 * a)
        t2 = (-b - np.sqrt(discriminant)) / (2 * a)

        if t1 < 0 and t2 < 0:
            # Both intersections are behind the ray's origin
            return None

        # Use the nearest intersection point
        t = t1 if t1 < t2 else t2
        p = np.add(orig, np.multiply(t, direction))

        # Calculate the normal at the intersection point
        normal = np.subtract(p, self.position)
        normal /= self.radii  # Normalize by the radii

        # Normalize the normal vector
        normal /= np.linalg.norm(normal)
        normal *= -1

        # Calculate texture coordinates (u, v)
        phi = np.arctan2(normal[1], normal[0])
        theta = np.arccos(normal[2])
        u = 1 - (phi + np.pi) / (2 * np.pi)
        v = (theta + np.pi / 2) / np.pi

        return Intercept(distance=t, point=p, normal=normal, texcoords=(u, v), obj=self)