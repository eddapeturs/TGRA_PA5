from OpenGL.GL import *
from OpenGL.GLU import *

class Dice:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,    # Floating point vertex 0,
                            -0.5, 0.5, -0.5,        # 1
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]

        # UV array goes in a circle from 0 to 1
        self.uv_array = [0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0,
                            0.0, 0.0,
                            0.0, 1.0,
                            1.0, 1.0,
                            1.0, 0.0]

    def set_vertices(self, shader):
        # Normals and position read from arrays - vertex list opengl uses
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        # From the arrays, start from beginning and read the next 4 arrays
        # Read 3 and 3 values together, one vertice means 3 values. 
        # Indices 0, 4 means the indices he has made from our floating point array.
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 20, 4)

class D2:
    def __init__(self):
        self.position_array = [ -0.5, -0.5, -0.5,    # Floating point vertex 0,
                                -0.5, 0.5, -0.5,        # 1
                                0.5, -0.5, -0.5,
                                0.5, 0.5, -0.5, #4
                                0.5, -0.5, -0.5,
                                0.5, 0.5, -0.5,
                                0.5, -0.5, 0.5,
                                0.5, 0.5, 0.5, #8
                                0.5, -0.5, 0.5,
                                0.5, 0.5, 0.5,
                                -0.5, -0.5, 0.5,
                                -0.5, 0.5, 0.5, #12
                                -0.5, -0.5, 0.5,
                                -0.5, 0.5, 0.5,
                                -0.5, -0.5, -0.5,
                                -0.5, 0.5, -0.5,
                                -0.5, 0.5, -0.5,
                                -0.5, 0.5, 0.5,
                                0.5, 0.5, -0.5,
                                0.5, 0.5, 0.5,
                                -0.5, -0.5, -0.5,
                                -0.5, -0.5, 0.5,
                                0.5, -0.5, -0.5,
                                0.5, -0.5, 0.5]
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
                            0.0, 1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,  
                           ]

        # UV array goes in a circle from 0 to 1
        self.uv_array = [   0.0, 0.33,
                            0.33, 0.33,
                            0.0, 0.67,
                            0.33, 0.67,

                            0.33, 0.33,
                            0.67, 0.33,
                            0.33, 0.67,
                            0.67, 0.67,

                            0.33, 0.0,
                            0.67, 0.0,
                            0.33, 0.33,
                            0.67, 0.33,

                            0.33, 0.67,
                            0.67, 0.67,
                            0.33, 1.0,
                            0.67, 1.0,

                            0.67, 0.0,
                            1.0, 0.0,
                            0.67, 0.33,
                            1.0, 0.33,

                            0.67, 0.33,
                            1.0, 0.33,
                            0.67, 0.67,
                            1.0, 0.67]

    def set_vertices(self, shader):
        # Normals and position read from arrays - vertex list opengl uses
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        # From the arrays, start from beginning and read the next 4 arrays
        # Read 3 and 3 values together, one vertice means 3 values. 
        # Indices 0, 4 means the indices he has made from our floating point array.
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
        glDrawArrays(GL_TRIANGLE_STRIP, 20, 4)