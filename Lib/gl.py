"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Proyecto 1: Rasterizer

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
from collections import namedtuple
from math import sin, cos, tan, pi
import Lib.notnumpy as nnp
from Lib.Model import Model
from Lib.texture import Texture
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
        self.activeTexture = None
        self.glViewPort(0,0,self.width,self.height)
        self.glCamMatrix()
        self.glProjectionMatrix()
        self.directionalLight = [-5,0,-7]
        self.background = None


    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)

    def glColor(self, r, g, b):
        self.currColor = color(r, g, b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

        self.zbuffer = [[float('inf') for y in range(self.height)]
                        for x in range(self.width)]
        
    def glClearModel(self):
        self.objects = []

    def glBackgroundTexture(self, filename):
        self.background = Texture(filename)
        
    def glClearBG(self):
        self.glClear()
        if self.background:
            for x in range(self.vpX, self.vpX + self.vpWidth + 1):
                for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                    u = (x - self.vpX) / self.vpWidth
                    v = (y - self.vpY) / self.vpHeight
                    
                    texColor = self.background.getColor(u, v)
                    if texColor:
                        self.glPoint(x,y, color(texColor[0], texColor[1], texColor[2]))
    
    def glPoint(self, x, y, clr=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[x][y] = clr or self.currColor

    def glTriangle(self, v0, v1, v2, clr=None):
        def paintFlatBottomTri(v0, v1, v2):
            try:
                m1 = (v1[0] - v0[0]) / (v1[1] - v0[1])
                m2 = (v2[0] - v0[0]) / (v2[1] - v0[1])
            except:
                pass
            else:
                x0, x1 = v1[0], v2[0]

                for y in range(v1[1], v0[1]):
                    self.glLine((x0, y), (x1, y))
                    x0 += m1
                    x1 += m2
        
        def paintFlatTopTri(v0, v1, v2):
            try:
                m1 = (v2[0] - v0[0]) / (v2[1] - v0[1])
                m2 = (v2[0] - v1[0]) / (v2[1] - v1[1])
            except:
                pass
            else:
                x0, x1 = v0[0], v1[0]

                for y in range(v0[1], v2[1], -1):
                    self.glLine((x0, y), (x1, y))
                    x0 -= m1
                    x1 -= m2

        if (v0[1] < v1[1]):
            v0, v1, = v1, v0
        if (v0[1] < v2[1]):
            v0, v2 = v2, v0
        if (v1[1] < v2[1]):
            v1, v2 = v2, v1
        
        if (v1[1] == v2[1]):
            paintFlatBottomTri(v0, v1, v2)
        elif (v0[1] == v1[1]):
            paintFlatTopTri(v0, v1, v2)
        else:
            v3 = [v0[0] + ((v1[1] - v0[1]) / (v2[1] - v0[1])) * (v2[0] - v0[0]), v1[1]]
            paintFlatBottomTri(v0, v1, v3)
            paintFlatTopTri(v1, v3, v2)

        self.glLine(v0, v1, clr or self.currColor)
        self.glLine(v1, v2, clr or self.currColor)
        self.glLine(v2, v0, clr or self.currColor)

    def glViewPort(self,x,y,width,height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height
        
        self.vpMatrix = nnp.Matrix([[self.vpWidth/2,0,0,self.vpX+self.vpWidth/2],
                                   [0,self.vpHeight/2,0,self.vpY+self.vpHeight/2],
                                   [0,0,0.5,0.5],
                                   [0,0,0,1]])
    
    def glCamMatrix(self, translate = (0,0,0), rotate = (0,0,0)):
        #Crea matrix de camara
        self.camMatrix = self.glModelMatrix(translate, rotate)
        
        #Matriz de vista es igual a la inversa de la camara
        self.viewMatrix = nnp.inv(self.camMatrix.mat)

    def glLookAt(self, camPos = (0,0,0), eyePos = (0,0,0)):
        worldUp = (0,1,0)
        self.eyePos = eyePos
        
        forward = nnp.sub(worldUp, eyePos)

        forward = nnp.divTF(forward, nnp.norm(forward))

        right = nnp.cross(worldUp, forward)
        right = nnp.divTF(right, nnp.norm(forward))

        up = nnp.cross(forward, right)
        up = nnp.divTF(up, nnp.norm(up))

        self.camMatrix = nnp.Matrix([[right[0],up[0],forward[0],camPos[0]],
                                    [right[1],up[1],forward[1],camPos[1]],
                                    [right[2],up[2],forward[2],camPos[2]],
                                    [0,0,0,1]])
        
        self.viewMatrix = nnp.Matrix(nnp.inv(self.camMatrix.mat))

    def glProjectionMatrix(self, fov = 60, n = 0.1, f = 1000):
        aspectRatio = self.vpWidth/self.vpHeight
        
        t = tan((fov*pi/180)/2)*n
        
        r = t*aspectRatio
        
        self.projectionMatrix = nnp.Matrix([[n/r,0,0,0],
                                           [0,n/t,0,0],
                                           [0,0,-(f+n)/(f-n),(-2*f*n)/(f-n)],
                                           [0,0,-1,0]])


    def glTriangleBC(self, verts, texCoords, normals, normalMap, mMatrix):
        A= verts[0]
        B= verts[1]
        C= verts[2]

        # Bounding box
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        # Para cada pixel dentro del bounding box
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                # Si el pixel est� dentro del FrameBuffer
                if (0 <= x < self.width) and (0 <= y < self.height):

                    P = (x,y)
                    bCoords = nnp.bcCoords(A, B, C, P)

                    # Si se obtienen coordenadas baric�ntricas v�lidas para este punto
                    if bCoords != None:

                        u, v, w = bCoords

                        # Se calcula el valor Z para este punto usando las coordenadas baric�ntricas
                        z = u * A[2] + v * B[2] + w * C[2]

                        # Si el valor de Z para este punto es menor que el valor guardado en el Z Buffer
                        if z < self.zbuffer[x][y]:
                            
                            # Guardamos este valor de Z en el Z Buffer
                            self.zbuffer[x][y] = z

                            # Si contamos un Fragment Shader, obtener el color de ah�.
                            # Sino, usar el color preestablecido.
                            if self.fragmentShader != None:
                                # Mandar los par�metros necesarios al shader
                                colorP = self.fragmentShader(texture = self.activeTexture,
                                                             normalMap = normalMap,
                                                             texCoords= texCoords,
                                                             normals= normals,
                                                             dLight= self.directionalLight,
                                                             bCoords= bCoords,
                                                             viewer = self.eyePos,
                                                             point = bCoords, 
                                                             modelMatrix = mMatrix,
                                                             background = self.background,
                                                             mapCoords = [x,y],
                                                             measures = [self.width, self.height])

                                if colorP:
                                    self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                                else:
                                    self.glPoint(x, y, color(0, 0, 0))
                                
                            else:
                                self.glPoint(x, y)


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

    def glLoadModel(self, filename, texName, normalMapName = None, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1), vertexShader = None, fragmentShader = None):
        model = Model(filename, normalMapName, translate,rotate, scale, 
                      (self.vertexShader if vertexShader is None else vertexShader), 
                      (self.fragmentShader if fragmentShader is None else fragmentShader))

        model.loadTexture(texName)

        self.objects.append(model)

    def glRender(self):
        tVerts = []
        tCoords = []
        tnormals = []

        for model in self.objects:
            self.activeTexture = model.texture
            self.vertexShader = model.vertexShader
            self.fragmentShader = model.fragmentShader
            mMatrix = self.glModelMatrix(model.translate, model.rotate, model.scale)

            for face in model.faces:
                vertCount = len(face)
                
                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]

                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]
                
                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix = mMatrix,
                                           viewMatrix = self.viewMatrix,
                                           projectionMatrix = self.projectionMatrix,
                                           vpMatrix = self.vpMatrix)
                    v1 = self.vertexShader(v1, modelMatrix = mMatrix,
                                           viewMatrix = self.viewMatrix,
                                           projectionMatrix = self.projectionMatrix,
                                           vpMatrix = self.vpMatrix)
                    v2 = self.vertexShader(v2, modelMatrix = mMatrix,
                                           viewMatrix = self.viewMatrix,
                                           projectionMatrix = self.projectionMatrix,
                                           vpMatrix = self.vpMatrix)
                    if vertCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix = mMatrix,
                                           viewMatrix = self.viewMatrix,
                                           projectionMatrix = self.projectionMatrix,
                                           vpMatrix = self.vpMatrix)
                
                tVerts.append(v0)
                tVerts.append(v1)
                tVerts.append(v2)
                if vertCount == 4:
                    tVerts.append(v0)
                    tVerts.append(v2)
                    tVerts.append(v3)

                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                if vertCount == 4:
                    vt3 = model.texcoords[face[3][1] - 1]
                
                tCoords.append(vt0)
                tCoords.append(vt1)
                tCoords.append(vt2)
                if vertCount == 4:
                    tCoords.append(vt0)
                    tCoords.append(vt2)
                    tCoords.append(vt3)

                v0 = model.normals[face[0][2] - 1]
                v1 = model.normals[face[1][2] - 1]
                v2 = model.normals[face[2][2] - 1]
                if vertCount == 4:
                    v3 = model.normals[face[3][2] - 1]

                tnormals.append(v0)
                tnormals.append(v1)
                tnormals.append(v2)
                if vertCount == 4:
                    tnormals.append(v0)
                    tnormals.append(v2)
                    tnormals.append(v3)
                    
                    
            primitives = self.glPrimitiveAssembly(tVerts, tCoords, tnormals)


            for prim in primitives:
                if (self.primitiveType == TRIANGLES):
                        self.glTriangleBC(prim[0], prim[1], prim[2], model.normalMap, mMatrix)

                
            
        

    def glAddVertices(self, vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)

    def glPrimitiveAssembly(self, tVerts, tTexCoords, tnormals):

        primitives = []

        if self.primitiveType == TRIANGLES:

            for i in range(0, len(tVerts), 3):
                verts = []
                # Verts
                verts.append( tVerts[i] )
                verts.append( tVerts[i + 1] )
                verts.append( tVerts[i + 2] )

                # TexCoords
                texCoords = []
                texCoords.append( tTexCoords[i] )
                texCoords.append( tTexCoords[i + 1] )
                texCoords.append( tTexCoords[i + 2] )

                #Normals
                normals = []
                normals.append(tnormals[i])
                normals.append(tnormals[i + 1])
                normals.append(tnormals[i + 2])

                triangle = [verts, texCoords, normals]
                primitives.append(triangle)

        return primitives

    def rotationMatCalc(self, t, w, a):
        rx = nnp.Matrix([[1, 0, 0, 0],
                [0, cos(t), -sin(t), 0],
                [0, sin(t), cos(t), 0],
                [0, 0, 0, 1]])
        ry = nnp.Matrix([[cos(w), 0, sin(w), 0],
                [0, 1, 0, 0],
                [-sin(w), 0, cos(w), 0],
                [0, 0, 0, 1]])
        rz = nnp.Matrix([[cos(a), -sin(a), 0, 0],
                [sin(a), cos(a), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
        temp = rx * ry
        return temp * rz

    def glModelMatrix(self, translate = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1)):
        translation = nnp.Matrix([[1, 0, 0, translate[0]],
                        [0, 1, 0, translate[1]],
                        [0, 0, 1, translate[2]],
                        [0, 0, 0, 1]])

        scaleMat = nnp.Matrix([[scale[0], 0, 0, 0],
                    [0, scale[1], 0, 0],
                    [0, 0, scale[2], 0],
                    [0, 0, 0, 1]])

        rotationMat = self.rotationMatCalc(rotation[0], rotation[1], rotation[2])

        temp = translation * rotationMat

        return temp * scaleMat 
    
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
