import numpy as np
import glfw
from PyViscom.Shader import Shader
from PyViscom.Texture import Texture
from OpenGL.GL import *
import time
import cv2


class Canvas(object):
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.updateTex = False
        # Initialize the library
        if not glfw.init():
            return
        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(self.width, self.height, "DataVis Canvas", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # prepare buffer
        self.vertices = np.array([
            -1.0, 1.0, 0.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0, 0.0,
            1.0, 1.0, 0.0, 1.0, 1.0,
            1.0, -1.0, 0.0, 1.0, 0.0
        ], dtype=np.float32)
        self.shapeVAO = glGenVertexArrays(1)
        self.shapeVBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.shapeVBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.itemsize * len(self.vertices), self.vertices, GL_STATIC_DRAW)
        glBindVertexArray(self.shapeVAO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(12))
        glBindVertexArray(0)

        # prepare texture
        self.draw_buffer = np.zeros((height, width, 4), dtype=np.float32)
        self.texture = Texture()
        self.texture.set_texture("D:/hartwig/masterarbeit/multicalib/ulm/out_undist/01/0-0.jpg")

        # prepare shader
        self.shader = Shader()
        self.shader.set_shader(vert="canvas.vert", frag="canvas.frag")

    def draw(self):
        # Render here, e.g. using pyOpenGL
        if self.updateTex:
            self.texture.set_texture_from_buffer(self.draw_buffer)
            self.updateTex = False
        self.shader.use_shader()
        glActiveTexture(GL_TEXTURE0)
        self.texture.use_texture()
        glUniform1i(glGetUniformLocation(self.shader.programId, "draw_texture"), 0)
        glBindVertexArray(self.shapeVAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        # Swap front and back buffers
        glfw.swap_buffers(self.window)

        # Poll for and process events
        glfw.poll_events()

    def set_pixel(self, x, y, color):
        self.draw_buffer[y][x] = color
        self.updateTex = True

    def get_pixel(self, x, y):
        return self.draw_buffer[y][x]


if __name__ == '__main__':
    c = Canvas()
    while True:
        start = time.time()
        #for x in range(200, 600):
        #    for y in range(100, 500):
        #        c.set_pixel(x, y, (0.0, 0.0, 255.0, 255.0))
        c.draw()
        print(time.time() - start)
