import numpy as np
import glfw
from PyViscom.Shader import Shader
from PyViscom.Texture import Texture
from OpenGL.GL import *


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
        self.draw_buffer = np.zeros((height, width, 3), dtype=float)
        self.texture = Texture()
        self.texture.setTexture(self.draw_buffer)

        # prepare shader
        self.shader = Shader()
        self.shader.setShader(vert="canvas.vert", frag="canvas.frag")

    def draw(self):
        # Loop until the user closes the window
        while not glfw.window_should_close(self.window):
            # Render here, e.g. using pyOpenGL
            if self.updateTex:
                self.texture.setTexture(self.draw_buffer)
                self.updateTex = False
            self.shader.useShader()
            glActiveTexture(GL_TEXTURE0)
            self.texture.useTexture()
            glUniform1i(glGetUniformLocation(self.shader.programId, "draw_texture"), 0)
            glBindVertexArray(self.shapeVAO)
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()

    def set_pixel(self, x, y, color):
        self.draw_buffer[y][x] = color
        self.updateTex = True

    def get_pixel(self, x, y):
        return self.draw_buffer[y][x]


if __name__ == '__main__':
    c = Canvas()
    for x in range(200, 600):
        for y in range(100,500):
            c.set_pixel(x, y, (0.0, 0.0, 255.0))
    c.draw()
