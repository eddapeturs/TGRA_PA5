# import pygame
# import OpenGL
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
# import pywavefront

# class Ogre: 
#     def __init__(self):
#         self.scene = pywavefront.Wavefront('Assets/Characters/Ogre/ogre_posed.obj', collect_faces=True)

#         self.scene_box = (self.scene.vertices[0], self.scene.vertices[0])
#         for vertex in self.scene.vertices:
#             min_v = [min(self.scene_box[0][i], vertex[i]) for i in range(3)]
#             max_v = [max(self.scene_box[1][i], vertex[i]) for i in range(3)]
#             self.scene_box = (min_v, max_v)

#         self.scene_size     = [self.scene_box[1][i]-self.scene_box[0][i] for i in range(3)]
#         max_scene_size = max(self.scene_size)
#         scaled_size    = 5
#         self.scene_scale    = [scaled_size/max_scene_size for i in range(3)]
#         self.scene_trans    = [-(self.scene_box[1][i]+self.scene_box[0][i])/2 for i in range(3)]

#     def draw(self, shader):
#         glPushMatrix()
#         glScalef(*self.scene_scale)
#         glTranslatef(*self.scene_trans)

#         for mesh in self.scene.mesh_list:
#             glBegin(GL_TRIANGLES)
#             for face in mesh.faces:
#                 for vertex_i in face:
#                     glVertex3f(*self.scene.vertices[vertex_i])
#             glEnd()

#         glPopMatrix()

    
