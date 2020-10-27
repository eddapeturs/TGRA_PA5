from OpenGL.GL import *
from OpenGL.GLU import *

import numpy

class Plane:
    def __init__(self):
        self.position_array = [ -0.5, 0.5, -0.5,
                                -0.5, 0.5, 0.5,
                                0.5, 0.5, -0.5,
                                0.5, 0.5, 0.5]

        self.normal_array = [0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,]
                            
        self.uv_array = [0.0, 0.0,
                        0.0, 15.0,
                        15.0, 0.0,
                        15.0, 15.0]

        arr = []
        counter = 0
        for i in range(0, len(self.position_array), 3):
            arr.extend(self.position_array[i:i+3])
            arr.extend(self.normal_array[i:i+3])
            arr.extend(self.uv_array[counter:counter+2])
            counter += 2

        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(arr, dtype='float32'), GL_STATIC_DRAW)
        arr = None

    # def set_vertices(self, shader):
    #     # Normals and position read from arrays - vertex list opengl uses
    #     shader.set_position_attribute(self.position_array)
    #     shader.set_normal_attribute(self.normal_array)
    #     shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindBuffer(GL_ARRAY_BUFFER, 0) # unbinding
