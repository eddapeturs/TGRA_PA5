
import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *

import numpy


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        length = self.__len__()
        # print("Lenght: ", length)
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class Material:
    def __init__(self, diffuse = None, specular = None, shininess = None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse == None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular == None else specular
        self.shininess = 1 if shininess == None else shininess
        

class Cube:
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

    def set_vertices(self, shader):
        # Normals and position read from arrays - vertex list opengl uses
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

    def draw(self, shader):
        # From the arrays, start from beginning and read the next 4 arrays
        # Read 3 and 3 values together, one vertice means 3 values. 
        # Indices 0, 4 means the indices he has made from our floating point array.
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)

class Sphere:
    # stack - latitude, slices - longitude
    def __init__(self, stacks = 12, slices = 24):
        vertex_array = []
        self.slices = slices

        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0


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

        # Optimization
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        vertex_array = None

    # def set_vertices(self, shader):
        # shader.set_position_attribute(self.vertex_array)
        # shader.set_normal_attribute(self.vertex_array)

    def draw(self, shader):
        shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0) # unbinding



class MeshModel:
    def __init__(self):
        self.vertex_arrays = dict()
        # self.index_arrays = dict()
        self.mesh_materials = dict() # Key table between mesh and materials
        self.materials = dict()
        self.vertex_counts = dict()
        self.vertex_buffer_ids = dict()

    def add_vertex(self, mesh_id, position, normal, uv = None):
        if mesh_id not in self.vertex_arrays:
            self.vertex_arrays[mesh_id] = []
            self.vertex_counts[mesh_id] = 0
        self.vertex_arrays[mesh_id] += [position.x, position.y, position.z, normal.x, normal.y, normal.z, uv.x, uv.y]
        self.vertex_counts[mesh_id] += 1
        # print("Mesh: ", self.vertex_arrays[mesh_id])

    def set_mesh_material(self, mesh_id, mat_id):
        self.mesh_materials[mesh_id] = mat_id

    def add_material(self, mat_id, mat):
        # print("Mat Id: ", mat_id)
        # print("Mat: ", mat.diffuse)
        self.materials[mat_id] = mat
    

    # Makes buffers for each of the mesh id
    def set_opengl_buffers(self):
        for mesh_id in self.mesh_materials.keys():
            self.vertex_buffer_ids[mesh_id] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_ids[mesh_id])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertex_arrays[mesh_id], dtype='float32'), GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)


    def draw(self, shader):
        for mesh_id, mesh_material in self.mesh_materials.items():
            material = self.materials[mesh_material]
            shader.set_material_diffuse(material.diffuse)
            shader.set_material_specular(material.specular)
            shader.set_material_shininess(material.shininess)
            shader.set_attribute_buffers_with_uv(self.vertex_buffer_ids[mesh_id])
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[mesh_id])
            glBindBuffer(GL_ARRAY_BUFFER, 0)
