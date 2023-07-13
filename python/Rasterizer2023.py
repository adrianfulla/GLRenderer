from gl import Renderer, V2, color
import random

width = 1080
height = 1080

rend = Renderer(width,height)

rend.glClearColor(0, 0, 0)
rend.glClear()

#Dibuja un punto
""" rend.glColor(1,1,1)
rend.glPoint(250,250) """

#Dibuja una linea
""" rend.glColor(0.5, 0.9, 0.2)
rend.glLine(V2(0,0), V2(10, 250)) """

#Patron 1 (abajo hacia arriba, izquierda derecha)
""" for x in range(0, width, 25):
    rend.glLine(V2(0,0), V2(x, height - 1)) """

#Patron 2 (arriba hacia abajo, izquierda derecha)
""" for x in range(0, width, 25):
    rend.glColor(1, 0, 0)
    rend.glLine(V2(0,height - 1), V2(x, 0)) """

#Patron 3 (static)
""" for x in range(width):
    for y in range(height):
        if random.random() > 0.5:
            rend.glColor(1, 1, 1)
            rend.glPoint(x, y)
 """

#Patron 4 (Color static)
""" for x in range(width):
    for y in range(height):
        if random.random() > 0.5:
            rend.glPoint(x, y, color(random.random(),
                                     random.random(),
                                     random.random())) """

#Patron 5 (Estrellas)
for x in range(width):  
    for y in range(height):
        if random.random() > 0.995:
            size= random.randrange(0, 3)
            brigthness= random.random() / 2 + 0.5
            starColor= color(brigthness, brigthness, brigthness)

            if size== 0:
                rend.glPoint(x, y, starColor)

            elif size== 1:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x+1, y, starColor)
                rend.glPoint(x, y+1, starColor)
                rend.glPoint(x+1, y+1, starColor)

            elif size==2:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x+1, y, starColor)
                rend.glPoint(x, y+1, starColor)
                rend.glPoint(x+1, y+1, starColor)
                rend.glPoint(x+2, y, starColor)
                rend.glPoint(x, y+2, starColor)                
                rend.glPoint(x+2, y+2, starColor)

rend.glFinish("output.bmp")