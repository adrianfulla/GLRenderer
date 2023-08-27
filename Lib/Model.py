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
from Lib.obj import Obj
from Lib.texture import Texture
class Model(object):
    def __init__(self, filename, normalMapName, translate=(0, 0, 0), 
                 rotate=(0, 0, 0), scale=(1, 1, 1), vertexShader = None, fragmentShader = None):
        self.model = Obj(filename)

        self.vertices = self.model.vertices
        self.texcoords = self.model.texcoords
        self.normals = self.model.normals
        self.faces = self.model.faces
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        self.vertexShader = vertexShader
        self.fragmentShader = fragmentShader
        self.normalMap = normalMapName
        
        if normalMapName:
          self.loadNormalMap(normalMapName)

    def loadTexture(self, texName):
      self.texture = Texture(texName)
      
    def loadNormalMap(self, normalMapName):
      self.normalMap = Texture(normalMapName)
      
    
