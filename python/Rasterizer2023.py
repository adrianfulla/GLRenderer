from /Lib/gl import Renderer
import /Lib/shaders

width = 2160
height = 3840

rend = Renderer(width, height)

rend.glClearColor(0, 0, 0)
rend.glClear()

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel("Bull.obj", translate=(width / 2, height/1.8, 0), rotate=(0, 0, 0), scale=(12, 12, 0))

rend.glRender()

rend.glFinish("output.bmp")

rend.glClear()

