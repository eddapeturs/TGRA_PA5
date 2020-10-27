import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

class Ogre: 
    def __init__(self):
        self.scene = pywavefront.Wavefront('Assets/Characters/Ogre/ogre_posed.obj', collect_faces=True)

        self.scene_box = (self.scene.vertices[0], self.scene.vertices[0])
        for vertex in self.scene.vertices:
            min_v = [min(self.scene_box[0][i], vertex[i]) for i in range(3)]
            max_v = [max(self.scene_box[1][i], vertex[i]) for i in range(3)]
            self.scene_box = (min_v, max_v)

        self.scene_size     = [self.scene_box[1][i]-self.scene_box[0][i] for i in range(3)]
        max_scene_size = max(self.scene_size)
        scaled_size    = 5
        self.scene_scale    = [scaled_size/max_scene_size for i in range(3)]
        self.scene_trans    = [-(self.scene_box[1][i]+self.scene_box[0][i])/2 for i in range(3)]

    def draw(self, shader):
        glPushMatrix()
        glScalef(*self.scene_scale)
        glTranslatef(*self.scene_trans)

        for mesh in self.scene.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.scene.vertices[vertex_i])
            glEnd()

        glPopMatrix()

    
    # def set_vertices(self, shader):
        # Normals and position read from arrays - vertex list opengl uses
        # shader.set_position_attribute(self.scene.vertices)
        # shader.set_normal_attribute(self.normal_array)

    # def main():
    #         pygame.init()
    #         display = (800, 600)
    #         pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    #         gluPerspective(45, (display[0] / display[1]), 1, 500.0)
    #         glTranslatef(0.0, 0.0, -10)

    #         while True:
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     pygame.quit()
    #                     quit()

    #                 if event.type == pygame.KEYDOWN:
    #                     if event.key == pygame.K_LEFT:
    #                         glTranslatef(-0.5,0,0)
    #                     if event.key == pygame.K_RIGHT:
    #                         glTranslatef(0.5,0,0)
    #                     if event.key == pygame.K_UP:
    #                         glTranslatef(0,1,0)
    #                     if event.key == pygame.K_DOWN:
    #                         glTranslatef(0,-1,0)

    #             glRotatef(1, 5, 1, 1)
    #             glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #             glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #             Model()
    #             glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #             pygame.display.flip()
    #             pygame.time.wait(10)

    # main()