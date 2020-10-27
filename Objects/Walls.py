from OpenGL.GL import *
from OpenGL.GLU import *

import numpy

class VerticalWall:
    def __init__(self, length=None, width=None, height=None):
        self.width = width
        self.length = length
        self.height = height

        half_width = width / 2.0
        half_length = length / 2.0
        half_height = height / 2.0

        self.position_array = [ # Short side 1
                                -half_width, -half_height, -half_length,    # Floating point vertex 0,
                                -half_width, half_height, -half_length,        # 1
                                half_width, -half_height, -half_length,
                                half_width, half_height, -half_length, #4

                                half_width, -half_height, -half_length,
                                half_width, half_height, -half_length,
                                half_width, -half_height, half_length,
                                half_width, half_height, half_length, #8

                                # Short side 2
                                half_width, -half_height, half_length,
                                half_width, half_height, half_length,
                                -half_width, -half_height, half_length,
                                -half_width, half_height, half_length, #12

                                -half_width, -half_height, half_length,
                                -half_width, half_height, half_length,
                                -half_width, -half_height, -half_length,
                                -half_width, half_height, -half_length,

                                # Top
                                -half_width, half_height, -half_length,
                                -half_width, half_height, half_length,
                                half_width, half_height, -half_length,
                                half_width, half_height, half_length,
                                ]

        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,

                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,

                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,

                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,

                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0
                           ]

        # UV array goes in a circle from 0 to 1
        self.uv_array = [   
                            0.0, 0.0,  # Short side 1
                            0.0, half_height,
                            half_width, 0.0,
                            half_width, half_height,

                            0.0, 0.0,
                            0.0, half_height,
                            half_length, 0.0,
                            half_length, half_height,
                            
                            0.0, 0.0,  # Short side 1
                            0.0, half_height,
                            half_width, 0.0,
                            half_width, half_height,

                            0.0, 0.0,
                            0.0, half_height,
                            half_length, 0.0,
                            half_length, half_height,

                            # FIX! Not correct mapping
                            0.0, 0.0,
                            0.0, half_width,
                            half_length, 0.0,
                            half_length, half_width,

                            ]
        arr = []
        counter = 0
        print("LEN: ", len(self.normal_array))
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
        # From the arrays, start from beginning and read the next 4 arrays
        # Read 3 and 3 values together, one vertice means 3 values. 
        # Indices 0, 4 means the indices he has made from our floating point array.
        shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4) # Small side
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 4) # Long side
        glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
        # glDrawArrays(GL_TRIANGLE_STRIP, 20, 4)
        glBindBuffer(GL_ARRAY_BUFFER, 0) # unbinding


class HorizontalWall:
    def __init__(self, length=None, width=None, height=None):
        self.width = width
        self.length = length
        self.height = height

        half_width = width / 2.0
        half_length = length / 2.0
        half_height = height / 2.0

        self.position_array = [ # Long side1
                                -half_length, -half_height, -half_width,
                                -half_length, half_height, -half_width,
                                half_length, -half_height, -half_width,
                                half_length, half_height, -half_width,

                                half_length, -half_height, -half_width,
                                half_length, half_height, -half_width,
                                half_length, -half_height, half_width,
                                half_length, half_height, half_width, #8

                                # Short side 2
                                half_length, -half_height, half_width,
                                half_length, half_height, half_width,
                                -half_length, -half_height, half_width,
                                -half_length, half_height, half_width, #12

                                -half_length, -half_height, half_width,
                                -half_length, half_height, half_width,
                                -half_length, -half_height, -half_width,
                                -half_length, half_height, -half_width,
                                # Top
                                -half_length, half_height, -half_width,
                                -half_length, half_height, half_width,
                                half_length, half_height, -half_width,
                                half_length, half_height, half_width,
                                ]

        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,

                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,

                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,

                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,

                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0
                           ]

        # UV array goes in a circle from 0 to 1
        self.uv_array = [   
                            0.0, 0.0,
                            0.0, half_height,
                            half_length, 0.0,
                            half_length, half_height,

                            0.0, 0.0,  # Short side 1
                            0.0, half_height,
                            half_width, 0.0,
                            half_width, half_height,

                            0.0, 0.0,
                            0.0, half_height,
                            half_length, 0.0,
                            half_length, half_height,

                            0.0, 0.0,  # Short side 2
                            0.0, half_height,
                            half_width, 0.0,
                            half_width, half_height,


                            # FIX! Not correct mapping
                            # 0.0, 0.0,  # Short side 2
                            # 0.0, half_height,
                            # half_width, 0.0,
                            # half_width, half_height,
                            0.0, 0.0,
                            0.0, half_length,
                            half_width, 0.0,
                            half_width, half_length,
                            ]

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
        # From the arrays, start from beginning and read the next 4 arrays
        # Read 3 and 3 values together, one vertice means 3 values. 
        # Indices 0, 4 means the indices he has made from our floating point array.
        shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4) # Small side
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 4) # Long side
        glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
        glBindBuffer(GL_ARRAY_BUFFER, 0) # unbinding