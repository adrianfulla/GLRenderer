"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Rt1: Spheres, Material & Phong Shading

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
class Material(object):
    def __init__(self, diffuse=(1,1,1), spec = 1.0, ks = 0.0):
        self.diffuse = diffuse
        self.spec= spec
        self.ks = ks
        