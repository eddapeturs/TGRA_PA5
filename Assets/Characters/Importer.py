import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

scene = pywavefront.Wavefront('ogre_posed.obj', collect_faces=True)