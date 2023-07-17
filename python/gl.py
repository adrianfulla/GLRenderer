import struct
from collections import namedtuple
import numpy as np
from obj import Obj

V2= namedtuple('V2', ['x', 'y'])
V3= namedtuple('V3', ['x', 'y','z'])

POINTS = 0
LINES = 1
TRIANGLES = 2
SQUARES = 3

def char(c):
    #1 byte
    return struct.pack('=c',c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h',w)

def dword(d):
    #4 bytes      
    return struct.pack('=l',d)

def color(r,g,b):
    return bytes([int(b*255),int(g*255),int(r*255)])

class Model(object):
    def __init__(self,filename, translate =(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        self.model = Obj(filename)
        
        self.vertices = self.model.vertices
        self.texcoords = self.model.texcoords
        self.normals = self.model.normals
        self.faces = self.model.faces
        self.translate = translate
        self.rotate = rotate
        self.scale = scale

class Renderer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.glClearColor(0,0,0)
        self.glClear()

        self.glColor(1, 1, 1)
         
        self.primitiveType = TRIANGLES
        self.vertexBuffer = [ ]
        self.vertexShader = None
        self.fragmentShader = None
        self.objects = [ ]
        
    def glClearColor(self,r,g,b):
        self.clearColor = color(r,g,b)

    def glColor(self,r,g,b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

    def glPoint(self,x,y,clr=None):
        if 0<=x<self.width and 0<=y<self.height:
            self.pixels[x][y] = clr or self.currColor
            
    def glTriangle(self,v0,v1,v2, clr=None):
        self.glLine(v0,v1, clr or self.currColor)
        self.glLine(v1,v2, clr or self.currColor)
        self.glLine(v2,v0, clr or self.currColor)

    def glLine(self, v0, v1, clr= None):
        #Bresenham line algorith
        #y= mx + b
        
        """ m= (v1.y - v0.y) / (v1.x - v0.x)
        y= v0.y

        for x in range(v0.x, v1.x + 1):
            self.glPoint(x, int(y))
            y += m """
            
        x0 = int(v0[0])
        x1 = int(v1[0])        
        y0 = int(v0[1])
        y1 = int(v1[1])

        if x0 == x1 and y1 == y0: #Si los vertices son el mismo, dibuja un punto
            self.glPoint(x0, y0)

            return 
        
        dx= abs(x1 - x0)
        dy= abs(y1 - y0)

        steep= dy > dx

        if steep: #Si la pendiente es mayor a 1 o menor a -1
            #Intercambio de valores
            x0, y0 = y0, x0
            x1, y1= y1, x1

        if x0 > x1: #Si la linea va de derecha a izquierda, se intercambian valores para dibujarlos de izquierda a derecha
            x0, x1= x1, x0
            y0, y1= y1, y0

        dx= abs(x1 - x0)
        dy= abs(y1 - y0)


        offset= 0
        limit= 0.5

        m = dy / dx
        y = y0
        
        for x in range(x0, x1 + 1):
            if steep: #Dibujar de manera vertical
                self.glPoint(y, x, clr or self.currColor)

            else: #Dibujar de manera horizontal
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1: #Dibujando de abajo para arriba
                    y += 1
                
                else: #Dibujando de arriba para abajo
                    y -= 1

                limit += 1
                        
                
    def glLoadModel(self, filename, translate = (0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        self.objects.append( Model(filename, translate, rotate, scale))

    def glRender(self):
        
        transformedVerts = []
        for model in self.objects:
            modelMatrix = self.glModelMatrix(model.translate, model.scale)
            
        for face in model.faces:
            vertCount = len(face)
            v0 = model.vertices[face[0][0] - 1]
            v1 = model.vertices[face[1][0] - 1]
            v2 = model.vertices[face[2][0] - 1]
            
            if  vertCount == 4:
                v3 = model.vertices[ face[3][0] - 1]
                
            if self.vertexShader:
                v0 = self.vertexShader(v0,modelMatrix = modelMatrix)
                v1 = self.vertexShader(v1,modelMatrix = modelMatrix)
                v2 = self.vertexShader(v2,modelMatrix = modelMatrix)
                if  vertCount == 4:
                    v3 = self.vertexShader(v3,modelMatrix = modelMatrix)
            transformedVerts.append(v0)
            transformedVerts.append(v1)
            transformedVerts.append(v2)
            if  vertCount == 4:
                transformedVerts.append(v0)
                transformedVerts.append(v2)
                transformedVerts.append(v3)
            
        
        #Vertex shader
        
#         transformedVerts = [ ]
#         for vert in self.vertexBuffer:
#             if self.vertexShader:
#                 transformedVerts.append(self.vertexShader(vert, modelMatrix = self.modelMatrix))
#             else:
#                 transformedVerts.append(vert)
#                 
        primitives = self.glPrimitiveAssembly(transformedVerts)
        
        if self.fragmentShader:
            primsColor = self.fragmentShader()
            
            primColor = color(primsColor[0], primsColor[1], primsColor[2])
        else:
            primColor = self.currColor
        
        for primitive in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(primitive[0], primitive[1], primitive[2],primColor)
        
        
    def glAddVertices(self,vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)
            
    def glPrimitiveAssembly(self, tVerts):
        
        primitives = [ ]
        
        if self.primitiveType == TRIANGLES:
            for i in range(0,len(tVerts),3):
                triangle = [ ]
                triangle.append(tVerts[i])
                triangle.append(tVerts[i+1])
                triangle.append(tVerts[i+2])
                primitives.append(triangle)            
               
        return primitives
    
    def glModelMatrix(self, translate = (0,0,0), scale = (1,1,1)):
        translation = np.matrix([[1,0,0,translate[0]],
                                 [0,1,0,translate[1]],
                                 [0,0,1,translate[2]],
                                 [0,0,0,1]])
        scale = np.matrix([[scale[0],0,0,0],
                          [0,scale[1],0,0],
                          [0,0,scale[2],0],
                          [0,0,0,1]])
        
        self.modelMatrix =  translation * scale
        return self.modelMatrix
    
    def glFinish(self,filename):
        with open(filename,"wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])