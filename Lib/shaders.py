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

import Lib.notnumpy as nnp
import random

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
        color = texture.getColor(texCoords[0][0], texCoords[0][1])
    else:
        color = (1,1,1)

    return color

def diffuseShader(**kwargs):
    texture = kwargs["texture"]
    background = kwargs["background"]
    x, y = kwargs["mapCoords"]
    width, height = kwargs["measures"]
    nA, nB, nC= kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]


    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV) 

        if background is not None:
            bgColor = background.getColor(x/width, y/height)

            alpha = 0.2  
            
            r = (1 - alpha) * bgColor[0] + alpha * textureColor[0]
            g = (1 - alpha) * bgColor[1] + alpha * textureColor[1]
            b = (1 - alpha) * bgColor[2] + alpha * textureColor[2]
        else:
            r, g, b = textureColor
    
    else:
        r, g, b = 1.0, 1.0, 1.0  
        
    normal = nnp.Matrix([[u * nA[0] + v * nB[0] + w * nC[0]],
             [u * nA[1] + v * nB[1] + w * nC[1]],
             [u * nA[2] + v * nB[2] + w * nC[2]], [0]])
    
    normal = modelMatrix @ normal
    
    normal = [normal.mat[0][0],normal.mat[1][0],normal.mat[2][0]]
    
    negate_array = lambda arr: [-x for x in arr]

    intensity= nnp.dot_product(normal, negate_array(dLight))
    
    b *= intensity
    g *= intensity
    r *= intensity

    return max(min(r, 1.0), 0), max(min(g, 1.0), 0), max(min(b, 1.0), 0)
    
def gouradShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]

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

    normal = nnp.Matrix([[u * nA[0] + v * nB[0] + w * nC[0]],
             [u * nA[1] + v * nB[1] + w * nC[1]],
             [u * nA[2] + v * nB[2] + w * nC[2]], [0]])
    
    normal = modelMatrix @ normal
    
    normal = [normal.mat[0][0],normal.mat[1][0],normal.mat[2][0]]
    
    negate_array = lambda arr: [-x for x in arr]

    intensity= nnp.dot_product(normal, negate_array(dLight))
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    

    if intensity > 0:
        return [min(value, 1) for value in (r, g, b)]

    else:
        return [0,0,0]
    

def phongShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    viewer = kwargs["viewer"]  # View vector from the camera to the point
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]
    

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

    normal = nnp.Matrix([[u * nA[0] + v * nB[0] + w * nC[0]],
             [u * nA[1] + v * nB[1] + w * nC[1]],
             [u * nA[2] + v * nB[2] + w * nC[2]], [0]])
    
    normal = modelMatrix @ normal
    
    normal = [normal.mat[0][0],normal.mat[1][0],normal.mat[2][0]]
    
    # Ensure the normal is unit-length
    normal_len = nnp.norm(normal)
    if normal_len > 0:
        normal = [x / normal_len for x in normal]

    # Compute the reflection vector
    reflect = nnp.subtract(nnp.multiply(2 * nnp.dot_product(normal, dLight), normal), dLight)
    reflect_len = nnp.norm(reflect)
    if reflect_len > 0:
        reflect = [x / reflect_len for x in reflect]

    # Compute the view direction vector
    view = nnp.subtract(viewer, kwargs["point"])
    view_len = nnp.norm(view)
    if view_len > 0:
        view = [x / view_len for x in view]

    # Compute the specular factor
    spec = max(nnp.dot_product(reflect, view), 0) ** 100  # Adjust the power for the shininess
    
    # Compute the diffuse factor
    diff = max(nnp.dot_product(normal, dLight), 0)

    # Combine ambient, diffuse, and specular components
    r *= (0.1 + diff * 0.7 + spec * 0.2)
    g *= (0.1 + diff * 0.7 + spec * 0.2)
    b *= (0.1 + diff * 0.7 + spec * 0.2)

    return max(min(r, 1.0), 0), max(min(g, 1.0), 0), max(min(b, 1.0), 0)


def gradientShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]

    b= 1.0
    g= 1.0
    r= 1.0
    
    c1 = (0.5,0.4,0)
    c2 = (0.2,0,0.8)

    gColor = [u * c2[0] + v * c1[0] + w * c1[0],
             u * c2[1] + v * c1[1] + w * c1[1],
             u * c2[2] + v * c1[0] + w * c1[2]
    ]
    
    b *= gColor[2] 
    g *= gColor[1] 
    r *= gColor[0] 

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = nnp.Matrix([[u * nA[0] + v * nB[0] + w * nC[0]],
             [u * nA[1] + v * nB[1] + w * nC[1]],
             [u * nA[2] + v * nB[2] + w * nC[2]], [0]])
    
    normal = modelMatrix @ normal
    
    normal = [normal.mat[0][0],normal.mat[1][0],normal.mat[2][0]]
    
    negate_array = lambda arr: [-x for x in arr]

    intensity= nnp.dot_product(normal, negate_array(dLight))
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    

    if intensity > 0:
        return [min(value, 1) for value in (r, g, b)]

    else:
        return [0,0,0]


def glitchVertexShader(vertex, **kwargs):
     modelMatrix = kwargs["modelMatrix"]
     viewMatrix = kwargs["viewMatrix"]
     projectionMatrix = kwargs["projectionMatrix"]
     vpMatrix = kwargs["vpMatrix"]
     
     glitchOffset = random.uniform(-0.1, 0.1)

     vts = [vertex[0] + glitchOffset,
          vertex[1] + glitchOffset,
          vertex[2] ,
          1]

     vt = vpMatrix * projectionMatrix * viewMatrix * modelMatrix  @ vts

     vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

     return vt
 
def glitchFragmentShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    viewer = kwargs["viewer"]  
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]
    
    
    glitchOffset = [random.uniform(0.0, 1.0) for _ in range(3)]
    

    b = 1.0 * glitchOffset[0]
    g = 1.0 * glitchOffset[1]
    r = 1.0 * glitchOffset[2]

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        textureColor = texture.getColor(tU, tV)   
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = nnp.Matrix([[u * nA[0] + v * nB[0] + w * nC[0]],
             [u * nA[1] + v * nB[1] + w * nC[1]],
             [u * nA[2] + v * nB[2] + w * nC[2]], [0]])
    
    normal = modelMatrix @ normal
    
    normal = [normal.mat[0][0],normal.mat[1][0],normal.mat[2][0]]
    
    # Ensure the normal is unit-length
    normal_len = nnp.norm(normal)
    if normal_len > 0:
        normal = [x / normal_len for x in normal]

    # Compute the reflection vector
    reflect = nnp.subtract(nnp.multiply(2 * nnp.dot_product(normal, dLight), normal), dLight)
    reflect_len = nnp.norm(reflect)
    if reflect_len > 0:
        reflect = [x / reflect_len for x in reflect]

    # Compute the view direction vector
    view = nnp.subtract(viewer, kwargs["point"])
    view_len = nnp.norm(view)
    if view_len > 0:
        view = [x / view_len for x in view]

    # Compute the specular factor
    spec = max(nnp.dot_product(reflect, view), 0) ** 100  # Adjust the power for the shininess
    
    # Compute the diffuse factor
    diff = max(nnp.dot_product(normal, dLight), 0)

    # Combine ambient, diffuse, and specular components
    r *= (0.1 + diff * 0.7 + spec * 0.2)
    g *= (0.1 + diff * 0.7 + spec * 0.2)
    b *= (0.1 + diff * 0.7 + spec * 0.2)

    return max(min(r, 1.0), 0), max(min(g, 1.0), 0), max(min(b, 1.0), 0)


def normalMapShader(**kwargs):
    dLight = kwargs["dLight"]
    normalMap = kwargs["normalMap"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]
    tangent = kwargs["tangent"]
    
    b=1.0
    g=1.0
    r=1.0
    
    tU = u*tA[0] + v*tB[0] + w*tC[0]
    tV = u*tA[1] + v*tB[1] + w*tC[1]
    
    if texture != None:
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2],
              0]
    
    normal = modelMatrix @ normal
    normal = normal.tolist()[0]
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = nnp.array(dLight)
    
    if normalMap:
        texNormal= normalMap.getColor(tU, tV)
        texNormal = [texNormal[0]*2-1, texNormal[1]*2-1, texNormal[2]*2-1]
        texNormal = texNormal / nnp.linalg.norm(texNormal)
        
        bitangent = nnp.cross(normal, tangent)
        bitangent = bitangent / nnp.linalg.norm(bitangent)
        
        tangent = nnp.cross(normal, bitangent)
        tangent = tangent / nnp.linalg.norm(tangent)
        
        tangentMatrix = nnp.Matrix([[tangent[0],bitangent[0],normal[0]],
                                  [tangent[1],bitangent[1],normal[1]],
                                  [tangent[2],bitangent[2],normal[2]]])
        
        texNormal = tangentMatrix @ texNormal
        texNormal = texNormal.tolist()[0]
        texNormal = texNormal / nnp.linalg.norm(texNormal)
        
        intensity = intensity = nnp.dot(texNormal, -dLight)
        
    else:
        intensity = nnp.dot(normal, -dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    if b>=1.0:b=1.0
    if g>=1.0:g=1.0
    if r>=1.0:r=1.0
    
    if intensity > 0:
        return r,g,b
    else:
        return [0,0,0]