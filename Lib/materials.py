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

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse=(255,255,255), spec = 1.0, ks = 0.0, ior = 1.0,texture = None,matType = OPAQUE):
        self.diffuse = [i / 255 for i in diffuse]
        self.spec= spec
        self.ks = ks
        self.ior = ior
        self.texture = texture
        self.matType = matType
        