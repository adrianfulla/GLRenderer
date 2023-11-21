"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Proyecto 3: OpenGL

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""

class Obj(object):
    def __init__(self, filename):
        with open(filename,"r") as file:
            self.lines = file.read().splitlines()
        
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
            except:
                continue
        
            if prefix =="v": #Vertices
               self.vertices.append(list(map(float, list(filter(None,value.split(" "))))))
            elif prefix =="vt": #Texture coordinates
               self.texcoords.append(list(map(float, list(filter(None,value.split(" "))))))
            elif prefix =="vn": #Normals
               self.normals.append(list(map(float, list(filter(None,value.split(" "))))))
            elif prefix == "f": #Faces
                self.faces.append([list(map(int, list(filter(None,vert.split("/"))))) for vert in list(filter(None,value.split(" ")))])
                