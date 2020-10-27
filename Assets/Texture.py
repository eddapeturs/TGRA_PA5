from OpenGL.GL import *
from OpenGL.GLU import *

import sys
import pygame
from pygame.locals import *

class Texture:
    def __init__(self, diff, spec=None, norm=None):
        self.diffuse = self.load_texture(diff)
        self.specular = self.load_texture(spec) if spec else None
        self.normal = self.load_texture(norm) if spec else None
    

    # Returns IDs for textures
    def load_texture(self, path_string):
        surface = pygame.image.load(sys.path[0] + path_string)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)   #  Make room in gl for texture and return id
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # Will affect active texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id