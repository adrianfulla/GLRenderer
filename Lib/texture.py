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
from struct import unpack

class Texture(object):
    def __init__(self, filename):
        with open(filename, "rb") as image:
            image.seek(10)
            headerSize = unpack('=l', image.read(4))[0]

            image.seek(18)
            self.width = unpack('=l', image.read(4))[0]
            self.height = unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            self.pixels = []

            for y in range(self.height):
                pixelRow = []
                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    pixelRow.append([r, g, b])
                self.pixels.append(pixelRow)
    
    def getColor(self, u, v):
        if (0 <= u < 1) and (0 <= v < 1):
            return self.pixels[int(v * self.height)][int(u * self.width)]
        else:
            return (0,0,0)