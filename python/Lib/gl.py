"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Tarea 1 - Lines & Obj Models

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
from collections import namedtuple
from math import sin, cos, radians
import Lib.notnumpy as nnp
from Lib.Model import Model
from Lib.Types import char, word, dword

V3 = namedtuple('V3', ['x', 'y', 'z'])
TRIANGLES = 3


def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClearColor(0, 0, 0)
        self.glClear()
        self.glColor(1, 1, 1)
        self.primitiveType = TRIANGLES
        self.vertexBuffer = []
        self.vertexShader = None
        self.fragmentShader = None
        self.objects = []

    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)

    def glColor(self, r, g, b):
        self.currColor = color(r, g, b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

    def glPoint(self, x, y, clr=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[x][y] = clr or self.currColor

    def glTriangle(self, v0, v1, v2, clr=None):
        self.glLine(v0, v1, clr or self.currColor)
        self.glLine(v1, v2, clr or self.currColor)
        self.glLine(v2, v0, clr or self.currColor)

    def glLine(self, v0, v1, clr=None):
        # Bresenham line algorith
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        if x0 == x1 and y1 == y0:  # Si los vertices son el mismo, dibuja un punto
            self.glPoint(x0, y0)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:  # Si la pendiente es mayor a 1 o menor a -1
            # Intercambio de valores
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:  # Si la linea va de derecha a izquierda, se intercambian valores para dibujarlos de izquierda a derecha
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0.0
        limit = 0.5

        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:  # Dibujar de manera vertical
                self.glPoint(y, x, clr or self.currColor)

            else:  # Dibujar de manera horizontal
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:  # Dibujando de abajo para arriba
                    y += 1

                else:  # Dibujando de arriba para abajo
                    y -= 1

                limit += 1

    def glLoadModel(self, filename, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        self.objects.append(Model(filename, translate, rotate, scale))

    def glRender(self):

        transformedVerts = []
        for model in self.objects:
            mm = self.glModelMatrix(model.translate, model.rotate, model.scale)

        for face in model.faces:
            vertCount = len(face)

            v0 = model.vertices[face[0][0] - 1]
            v1 = model.vertices[face[1][0] - 1]
            v2 = model.vertices[face[2][0] - 1]

            if vertCount == 4:
                v3 = model.vertices[face[3][0] - 1]

            if self.vertexShader:
                v0 = self.vertexShader(v0, modelMatrix=mm)
                v1 = self.vertexShader(v1, modelMatrix=mm)
                v2 = self.vertexShader(v2, modelMatrix=mm)
                if vertCount == 4:
                    v3 = self.vertexShader(v3, modelMatrix=mm)

            transformedVerts.append(v0)
            transformedVerts.append(v1)
            transformedVerts.append(v2)
            if vertCount == 4:
                transformedVerts.append(v0)
                transformedVerts.append(v2)
                transformedVerts.append(v3)

        primitives = self.glPrimitiveAssembly(transformedVerts)

        if self.fragmentShader:
            primsColor = self.fragmentShader()

            primColor = color(primsColor[0], primsColor[1], primsColor[2])
        else:
            primColor = self.currColor

        for primitive in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(primitive[0], primitive[1], primitive[2], primColor)

    def glAddVertices(self, vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)

    def glPrimitiveAssembly(self, tVerts):

        primitives = []

        if self.primitiveType == TRIANGLES:
            print(len(tVerts))
            if len(tVerts) % 3 == 0:
                for i in range(0, len(tVerts), 3):
                    triangle = [tVerts[i], tVerts[i + 1], tVerts[i + 2]]
                    primitives.append(triangle)

        return primitives

    def glModelMatrix(self, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        translation = nnp.Matrix([[1, 0, 0, translate[0]],
                                  [0, 1, 0, translate[1]],
                                  [0, 0, 1, translate[2]],
                                  [0, 0, 0, 1]])
        scale = nnp.Matrix([[scale[0], 0, 0, 0],
                            [0, scale[1], 0, 0],
                            [0, 0, scale[2], 0],
                            [0, 0, 0, 1]])
        rotateX = nnp.Matrix([[1, 0, 0, 0],
                              [0, cos(rotate[0]), -sin(rotate[0]), 0],
                              [0, sin(rotate[0]), cos(rotate[0]), 0],
                              [0, 0, 0, 1]])
        rotateY = nnp.Matrix([[cos(rotate[1]), 0, sin(rotate[1]), 0],
                              [0, 1, 0, 0],
                              [-sin(rotate[1]), 0, cos(rotate[1]), 0],
                              [0, 0, 0, 1]])
        rotateZ = nnp.Matrix([[cos(rotate[2]), -sin(rotate[2]), 0, 0],
                              [sin(rotate[2]), cos(rotate[2]), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        rotation = rotateX * rotateY * rotateZ

        self.modelMatrix = translation * rotation * scale
        return self.modelMatrix
    
    def glBuildPoly(self, vertices, clr = None):
        for i in range(len(vertices)):
            if i < (len(vertices) - 1):
                self.glLine(vertices[i], vertices[i+1], clr)
            else:
                self.glLine(vertices[i], vertices[0], clr)
            
    def insidePolygon(self, x, y, polygon):
        n = len(polygon)
        odd_nodes = False
        j = n - 1

        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]

            if yi < y and yj >= y or yj < y and yi >= y:
                if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                    odd_nodes = not odd_nodes

            j = i

        return odd_nodes
    
    
    def glPaintPoly(self, vertices, clr = None):
        bountyBox = [[vertices[0][0],vertices[0][1]],[vertices[0][0],vertices[0][1]]]
        for vert in vertices:
            if vert[0] < bountyBox[0][0]:
                bountyBox[0][0] = vert[0]
            elif vert[0] > bountyBox[1][0]:
                bountyBox[1][0] = vert[0]
            if vert[1] < bountyBox[0][1]:
                bountyBox[0][1] = vert[1]
            elif vert[1] > bountyBox[1][1]:
                bountyBox[1][1] = vert[1]
        
        for x in range(bountyBox[0][0], bountyBox[1][0]):
            for y in range(bountyBox[0][1], bountyBox[1][1]):
                if self.insidePolygon(x, y, vertices):
                    self.glPoint(x, y, clr)
                
                
    
    
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
