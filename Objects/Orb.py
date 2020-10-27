
from OpenGL.GL import *
from math import *
from .BaseObjects import *
import numpy

class Orb:
    # stack - latitude, slices - longitude
    def __init__(self, position, stacks = 12, slices = 24):
        self.pos_x = self.get_orb_coordinates(position[0])
        self.pos_y = 2.0
        self.pos_z = self.get_orb_coordinates(position[1])

        self.position = Point(self.pos_x, self.pos_y, self.pos_z)

        self.vertex_array = []
        self.normal_array = []
        self.slices = slices

        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        vertex_array = []


        # for stack_count in range(stacks):
        #     stack_angle = stack_count * stack_interval
        #     for slice_count in range(slices + 1):
        #         slice_angle = slice_count * slice_interval
        #         self.vertex_array.append(sin(stack_angle) * cos(slice_angle))
        #         self.vertex_array.append(cos(stack_angle))
        #         self.vertex_array.append(sin(stack_angle) * sin(slice_angle))
        #         self.vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
        #         self.vertex_array.append(cos(stack_angle + stack_interval))
        #         self.vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

        #         # Flipping normals to get a light effect
        #         self.normal_array.append(-(sin(stack_angle) * cos(slice_angle)))
        #         self.normal_array.append(-(cos(stack_angle)))
        #         self.normal_array.append(-(sin(stack_angle) * sin(slice_angle)))
        #         self.normal_array.append(-(sin(stack_angle + stack_interval) * cos(slice_angle)))
        #         self.normal_array.append(-(cos(stack_angle + stack_interval)))
        #         self.normal_array.append(-(sin(stack_angle + stack_interval) * sin(slice_angle)))

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                for _ in range(2):
                    vertex_array.append(sin(stack_angle) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle))
                    vertex_array.append(sin(stack_angle) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append(stack_count / stack_interval)

                for _ in range(2):
                    vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle + stack_interval))
                    vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append((stack_count + 1) / stack_interval)

                self.vertex_count += 2

        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        vertex_array = None

    # def set_vertices(self, shader):
    #     shader.set_position_attribute(self.vertex_array)
    #     # shader.set_normal_attribute(self.vertex_array)
    #     shader.set_normal_attribute(self.normal_array)
    #     shader.set_uv_attribute(self.vertex_array)

    def draw(self, shader):
        shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0) # unbinding

    def get_orb_coordinates(self, val):
        return  val * 5 + 2.5