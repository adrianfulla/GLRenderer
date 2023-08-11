"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Tarea 3 - Camaras

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""

import Lib.notnumpy as nnp
import numpy 

def vertexShader(vertex, **kwargs):
     modelMatrix = kwargs["modelMatrix"]
     viewMatrix = kwargs["viewMatrix"]
     projectionMatrix = kwargs["projectionMatrix"]
     vpMatrix = kwargs["vpMatrix"]

     vts = [vertex[0],
          vertex[1],
          vertex[2],
          1]

     vt = vpMatrix * projectionMatrix * viewMatrix * modelMatrix  @ vts

     vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

     return vt

def fragmentShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1,1,1)

    return color

def flatShader(**kwargs):
    dLight = kwargs["dLight"]
    normal= kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    """dLight= np.array(dLight)"""
    normal = nnp.Matrix(normal)
    dLight = nnp.Matrix(dLight)
    intensity= nnp.dot_product(normal, -dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]
    
def gouradShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]
    
    negate_array = lambda arr: [-x for x in arr]

    intensity= nnp.dot_product(normal, negate_array(dLight))
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]
    

def phongShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    viewer = kwargs["viewer"]  # View vector from the camera to the point
    u, v, w = kwargs["bCoords"]
    

    b = 1.0
    g = 1.0
    r = 1.0

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    # Ensure the normal is unit-length
    normal_len = numpy.linalg.norm(normal)
    if normal_len > 0:
        normal = [x / normal_len for x in normal]

    # Compute the reflection vector
    reflect = numpy.subtract(numpy.multiply(2 * numpy.dot(normal, dLight), normal), dLight)
    reflect_len = numpy.linalg.norm(reflect)
    if reflect_len > 0:
        reflect = [x / reflect_len for x in reflect]

    # Compute the view direction vector
    view = numpy.subtract(viewer, 
                          numpy.array(kwargs["point"]))
    view_len = numpy.linalg.norm(view)
    if view_len > 0:
        view = [x / view_len for x in view]

    # Compute the specular factor
    spec = max(numpy.dot(reflect, view), 0) ** 100  # Adjust the power for the shininess
    
    # Compute the diffuse factor
    diff = max(numpy.dot(normal, dLight), 0)

    # Combine ambient, diffuse, and specular components
    r *= (0.1 + diff * 0.7 + spec * 0.2)
    g *= (0.1 + diff * 0.7 + spec * 0.2)
    b *= (0.1 + diff * 0.7 + spec * 0.2)

    return max(min(r, 1.0), 0), max(min(g, 1.0), 0), max(min(b, 1.0), 0)