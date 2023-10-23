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
        l = nnp.subtract(orig, self.position) # Ensure l is float64
        l = nnp.divide(l, self.radii)  # Normalize by the radii
        direction = nnp.divide(direction, self.radii)  # Normalize the ray direction

        # Calculate the coefficients of the quadratic equation
        a = nnp.dot_product(direction, direction)
        b = 2.0 * nnp.dot_product(direction, l)
        c = nnp.dot_product(l, l) - 1.0  # The radii are normalized, so this is 1.0

        # Calculate the discriminant
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            # No intersection
            return None

        # Calculate the two solutions for t
        t1 = (-b + nnp.sqrt(discriminant)) / (2 * a)
        t2 = (-b - nnp.sqrt(discriminant)) / (2 * a)

        if t1 < 0 and t2 < 0:
            # Both intersections are behind the ray's origin
            return None

        # Use the nearest intersection point
        t = t1 if t1 < t2 else t2
        p = nnp.add(orig, nnp.multiply(t, direction))

        # Calculate the normal at the intersection point
        normal = nnp.subtract(p, self.position)
        normal = nnp.divide(normal, self.radii)  # Normalize by the radii

        # Normalize the normal vector
        normal = nnp.divTF(normal, np.linalg.norm(normal))

        # Calculate texture coordinates (u, v)
        phi = atan2(normal[1], normal[0])
        theta = acos(normal[2])
        u = 1 - (phi + pi) / (2 * pi)
        v = (theta + pi / 2) / pi

        return Intercept(distance=t, point=p, normal=normal, texcoords=(u, v), obj=self)

class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        self.radius = radius
        self.height = height
        super().__init__(position, material)
        
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        
        if dir[1] == 0:
            return None
        
        # Check if the ray intersects the top and bottom caps
        for y in [self.position[1] - self.height / 2, self.position[1] + self.height / 2]:
            t1 = (y - orig[1]) / dir[1]
            if t1 > 0:
                point = nnp.add(orig, nnp.multiply(t1, dir))
                if nnp.sqrt(point[0] ** 2 + point[2] ** 2) <= self.radius:
                    if t1 < t:
                        t = t1
                        normal = [0, 1 if y == self.position[1] + self.height / 2 else -1, 0]
                        intersect = Intercept(distance=t, point=point, normal=normal, texcoords=None, obj=self)
        
        # Check if the ray intersects the lateral surface
        a = dir[0] ** 2 + dir[2] ** 2
        b = 2 * (dir[0] * (orig[0] - self.position[0]) + dir[2] * (orig[2] - self.position[2]))
        c = (orig[0] - self.position[0]) ** 2 + (orig[2] - self.position[2]) ** 2 - self.radius ** 2
        discriminant = b ** 2 - 4 * a * c
        
        if discriminant >= 0:
            t2 = (-b - nnp.sqrt(discriminant)) / (2 * a)
            t3 = (-b + nnp.sqrt(discriminant)) / (2 * a)
            
            for t_val in [t2, t3]:
                if t_val > 0:
                    point = nnp.add(orig, nnp.multiply(t_val, dir))
                    if self.position[1] - self.height / 2 <= point[1] <= self.position[1] + self.height / 2:
                        if t_val < t:
                            t = t_val
                            normal = [point[0] - self.position[0], 0, point[2] - self.position[2]]
                            normal = nnp.divTF(normal, nnp.norm(normal))
                            intersect = Intercept(distance=t, point=point, normal=normal, texcoords=None, obj=self)
        
        if intersect is None:
            return None
        
        return intersect
