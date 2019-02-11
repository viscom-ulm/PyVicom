import os
from OpenGL.GL import *


class Shader:
    def __init__(self):
        self.programId = -1

    def setShader(self, vert, frag):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        absolute_vertex_shader_path = os.path.join(dir_path, 'shader', vert)
        absolute_fragment_shader_path = os.path.join(dir_path, 'shader', frag)
        if os.path.isfile(absolute_vertex_shader_path) and os.path.isfile(absolute_fragment_shader_path):
            with open(absolute_vertex_shader_path, 'r') as vertex_shader:
                v = vertex_shader.read()
            with open(absolute_fragment_shader_path, 'r') as fragment_shader:
                f = fragment_shader.read()
        else:
            v = vert
            f = frag
        # // Vertex Shader
        vertex = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex, v)
        glCompileShader(vertex)
        success = glGetShaderiv(vertex, GL_COMPILE_STATUS)

        if not success:
            infoLog = glGetShaderInfoLog(vertex)
            print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + str(infoLog))

        # // Fragment  Shader
        fragment = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment, f)
        glCompileShader(fragment)
        success = glGetShaderiv(fragment, GL_COMPILE_STATUS)

        if not success:
            infoLog = glGetShaderInfoLog(fragment)
            print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + str( infoLog))

        # // Shader Program
        self.programId = glCreateProgram()
        glAttachShader(self.programId, vertex)
        glAttachShader(self.programId, fragment)
        glLinkProgram(self.programId)
        success = glGetProgramiv(self.programId, GL_LINK_STATUS)

        if not success:
            infoLog = glGetProgramInfoLog(self.programId)
            print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + str(infoLog))

        glDeleteShader(vertex)
        glDeleteShader(fragment)

    def useShader(self):
        glUseProgram(self.programId)
