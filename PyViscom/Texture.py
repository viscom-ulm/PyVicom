from OpenGL.GL import *
from OpenGL.GL.EXT.texture_filter_anisotropic import *

class Texture:
    def __init__(self):
        self.texID = -1
        self.width = None
        self.height = None
        self.texComponents = None

        self.anisoFilterLevel = None

        self.texType = None
        self.texInternalFormat = None
        self.texFormat = None
        self.channels = None

    def getTexWidth(self):
        return int(self.width)

    def getTexHeight(self):
        return int(self.height)

    def setTexture(self, buffer):
        (self.height, self.width, self.channels) = buffer.shape
        self.texType = GL_TEXTURE_2D

        self.texID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        self.anisoFilterLevel = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, float(self.anisoFilterLevel))

        self.texInternalFormat = GL_RGB32F
        self.texFormat = GL_RGB


        glTexImage2D(GL_TEXTURE_2D, 0, self.texInternalFormat, self.getTexWidth(), self.getTexHeight(), 0,
                     self.texFormat,
                     GL_FLOAT, buffer)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

    def computeTexMipmap(self):
        glBindTexture(self.texType, self.texID)
        glGenerateMipmap(self.texType)

    def useTexture(self):
        glBindTexture(self.texType, self.texID)
