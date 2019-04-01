import cv2
import os
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.EXT.texture_filter_anisotropic import *


class Texture:
    def __init__(self, texture_path='textures'):
        self.texID = -1
        self.width = None
        self.height = None
        self.texComponents = None

        self.anisoFilterLevel = None

        self.texType = None
        self.texInternalFormat = None
        self.texFormat = None
        self.texture_path = texture_path

    def get_tex_width(self):
        return int(self.width)

    def get_tex_height(self):
        return int(self.height)

    def set_texture_from_buffer(self, buffer):
        (self.height, self.width, self.texComponents) = buffer.shape
        self.texType = GL_TEXTURE_2D

        self.texID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        self.anisoFilterLevel = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, float(self.anisoFilterLevel))

        if buffer is not None:
            if self.texComponents == 1:
                self.texFormat = GL_RED
            elif self.texComponents == 3:
                self.texFormat = GL_RGB
            elif self.texComponents == 4:
                self.texFormat = GL_RGBA
            self.texInternalFormat = self.texFormat

            glTexImage2D(GL_TEXTURE_2D, 0, self.texInternalFormat, self.get_tex_width(), self.get_tex_height(), 0,
                         self.texFormat,
                         GL_FLOAT, buffer)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glGenerateMipmap(GL_TEXTURE_2D)
        else:
            print("TEXTURE FAILED - LOADING")
        glBindTexture(GL_TEXTURE_2D, 0)

    def set_texture(self, tex_path, flip=True):
        self.texType = GL_TEXTURE_2D
        tmp_path = self.absolute_dir(tex_path)

        buffer = self.load_data(tmp_path, np.float32, flip)
        self.set_texture_from_buffer(buffer)

    def absolute_dir(self, path):
        if os.path.isfile(path):
            return path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        absolute_texture_path = os.path.join(dir_path, self.texture_path, path)
        if os.path.isfile(absolute_texture_path):
            return absolute_texture_path
        else:
            print(path + " is not a valid texture path!")
            raise NameError(path + " is not a valid texture path!")

    def load_data(self, absolute_path, dtype=np.float32, flip=True):
        try:
            img_data = cv2.imread(absolute_path, cv2.IMREAD_COLOR)

            if flip:
                cv2.flip(img_data, 0, img_data)
            if img_data.shape[2] == 3:
                img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
            if img_data.shape[2] == 4:
                img_data = cv2.cvtColor(img_data, cv2.COLOR_BGRA2RGBA)
            img_data = img_data.astype(dtype) / 255.0
            return img_data
        except Exception as e:
            print("unable to load texture: " + absolute_path)
            print(e)

    def compute_tex_mipmap(self):
        glBindTexture(self.texType, self.texID)
        glGenerateMipmap(self.texType)

    def use_texture(self):
        glBindTexture(self.texType, self.texID)
