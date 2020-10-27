
from OpenGL.GL import *
from OpenGL.GLU import *

from math import * # trigonometry

import sys

from Objects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/Shaders/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/Shaders/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))


        # Handles to use throughout the code
        # self.renderingProgramID = the ID of the shader program I am running
        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        # UV location
        self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        # self.colorLoc               = glGetUniformLocation(self.renderingProgramID, "u_color")
        # Orb property setting
        self.orb1PosLoc = glGetUniformLocation(self.renderingProgramID, "orb1.position")
        self.orb1AmbientLoc = glGetUniformLocation(self.renderingProgramID, "orb1.ambient")
        self.orb1DiffLoc = glGetUniformLocation(self.renderingProgramID, "orb1.diffuse")
        self.orb1SpecLoc = glGetUniformLocation(self.renderingProgramID, "orb1.specular")
        self.orb1Constant = glGetUniformLocation(self.renderingProgramID, "orb1.constant")
        self.orb1Linear = glGetUniformLocation(self.renderingProgramID, "orb1.linear")
        self.orb1Quadratic = glGetUniformLocation(self.renderingProgramID, "orb1.quadratic")

        self.orb2PosLoc = glGetUniformLocation(self.renderingProgramID, "orb2.position")
        self.orb2AmbientLoc = glGetUniformLocation(self.renderingProgramID, "orb2.ambient")
        self.orb2DiffLoc = glGetUniformLocation(self.renderingProgramID, "orb2.diffuse")
        self.orb2SpecLoc = glGetUniformLocation(self.renderingProgramID, "orb2.specular")
        self.orb2Constant = glGetUniformLocation(self.renderingProgramID, "orb2.constant")
        self.orb2Linear = glGetUniformLocation(self.renderingProgramID, "orb2.linear")
        self.orb2Quadratic = glGetUniformLocation(self.renderingProgramID, "orb2.quadratic")

        self.orb3PosLoc = glGetUniformLocation(self.renderingProgramID, "orb3.position")
        self.orb3AmbientLoc = glGetUniformLocation(self.renderingProgramID, "orb3.ambient")
        self.orb3DiffLoc = glGetUniformLocation(self.renderingProgramID, "orb3.diffuse")
        self.orb3SpecLoc = glGetUniformLocation(self.renderingProgramID, "orb3.specular")
        self.orb3Constant = glGetUniformLocation(self.renderingProgramID, "orb3.constant")
        self.orb3Linear = glGetUniformLocation(self.renderingProgramID, "orb3.linear")
        self.orb3Quadratic = glGetUniformLocation(self.renderingProgramID, "orb3.quadratic")

        self.orb4PosLoc = glGetUniformLocation(self.renderingProgramID, "orb4.position")
        self.orb4AmbientLoc = glGetUniformLocation(self.renderingProgramID, "orb4.ambient")
        self.orb4DiffLoc = glGetUniformLocation(self.renderingProgramID, "orb4.diffuse")
        self.orb4SpecLoc = glGetUniformLocation(self.renderingProgramID, "orb4.specular")
        self.orb4Constant = glGetUniformLocation(self.renderingProgramID, "orb4.constant")
        self.orb4Linear = glGetUniformLocation(self.renderingProgramID, "orb4.linear")
        self.orb4Quadratic = glGetUniformLocation(self.renderingProgramID, "orb4.quadratic")

        self.orb5PosLoc = glGetUniformLocation(self.renderingProgramID, "orb5.position")
        self.orb5AmbientLoc = glGetUniformLocation(self.renderingProgramID, "orb5.ambient")
        self.orb5DiffLoc = glGetUniformLocation(self.renderingProgramID, "orb5.diffuse")
        self.orb5SpecLoc = glGetUniformLocation(self.renderingProgramID, "orb5.specular")
        self.orb5Constant = glGetUniformLocation(self.renderingProgramID, "orb5.constant")
        self.orb5Linear = glGetUniformLocation(self.renderingProgramID, "orb5.linear")
        self.orb5Quadratic = glGetUniformLocation(self.renderingProgramID, "orb5.quadratic")

        self.lightPosLoc = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDiffLoc = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.lightAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_light_ambient")

        self.matAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_material.ambient")
        self.matDiffLoc = glGetUniformLocation(self.renderingProgramID, "u_material.diffuse")
        self.matSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_material.specular")
        self.matShineLoc = glGetUniformLocation(self.renderingProgramID, "u_material.shininess")

        # Texture 
        self.diffuseTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_diff_tex")
        # glUniform1f(self.diffuseTextureLoc, GL_TEXTURE0)
        self.specularTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_spec_tex")

        self.normalTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_norm_tex")
        # glUniform1f(self.diffuseTextureLoc, GL_TEXTURE1)
        self.hasTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_has_texture")


        # Fog
        self.fogColorLoc = glGetUniformLocation(self.renderingProgramID, "u_fog_color")
        self.fogStartLoc = glGetUniformLocation(self.renderingProgramID, "u_fog_start")
        self.fogEndLoc = glGetUniformLocation(self.renderingProgramID, "u_fog_end")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        # print(matrix_array)
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)


    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    # def set_solid_color(self, red, green, blue):
    #     glUniform4f(self.colorLoc, red, green, blue, 1.0)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_diffuse(self, red, green, blue):
        glUniform4f(self.lightDiffLoc, red, green, blue, 1.0)

    def set_light_specular(self, red, green, blue):
        glUniform4f(self.lightSpecLoc, red, green, blue, 1.0)

    def set_light_ambient(self, red, green, blue):
        glUniform4f(self.lightAmbientLoc, red, green, blue, 1.0)

    # Orb 1
    def set_orb_1_position(self, pos):
        glUniform4f(self.orb1PosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_orb_1_ambient(self, red, green, blue):
        glUniform4f(self.orb1AmbientLoc, red, green, blue, 1.0)

    def set_orb_1_diffuse(self, red, green, blue):
        glUniform4f(self.orb1DiffLoc, red, green, blue, 1.0)

    def set_orb_1_specular(self, red, green, blue):
        glUniform4f(self.orb1SpecLoc, red, green, blue, 1.0)

    def set_orb_1_attenuation(self, const, lin, quad):
        glUniform1f(self.orb1Constant, const)
        glUniform1f(self.orb1Linear, lin)
        glUniform1f(self.orb1Quadratic, quad)

    def set_orb_2_position(self, pos):
        glUniform4f(self.orb2PosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_orb_2_ambient(self, red, green, blue):
        glUniform4f(self.orb2AmbientLoc, red, green, blue, 1.0)

    def set_orb_2_diffuse(self, red, green, blue):
        glUniform4f(self.orb2DiffLoc, red, green, blue, 1.0)

    def set_orb_2_specular(self, red, green, blue):
        glUniform4f(self.orb2SpecLoc, red, green, blue, 1.0)

    def set_orb_2_attenuation(self, const, lin, quad):
        glUniform1f(self.orb2Constant, const)
        glUniform1f(self.orb2Linear, lin)
        glUniform1f(self.orb2Quadratic, quad)

    def set_orb_3_position(self, pos):
        glUniform4f(self.orb3PosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_orb_3_ambient(self, red, green, blue):
        glUniform4f(self.orb3AmbientLoc, red, green, blue, 1.0)

    def set_orb_3_diffuse(self, red, green, blue):
        glUniform4f(self.orb3DiffLoc, red, green, blue, 1.0)

    def set_orb_3_specular(self, red, green, blue):
        glUniform4f(self.orb3SpecLoc, red, green, blue, 1.0)

    def set_orb_3_attenuation(self, const, lin, quad):
        glUniform1f(self.orb3Constant, const)
        glUniform1f(self.orb3Linear, lin)
        glUniform1f(self.orb3Quadratic, quad)

    def set_orb_4_position(self, pos):
        glUniform4f(self.orb4PosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_orb_4_ambient(self, red, green, blue):
        glUniform4f(self.orb4AmbientLoc, red, green, blue, 1.0)

    def set_orb_4_diffuse(self, red, green, blue):
        glUniform4f(self.orb4DiffLoc, red, green, blue, 1.0)

    def set_orb_4_specular(self, red, green, blue):
        glUniform4f(self.orb4SpecLoc, red, green, blue, 1.0)

    def set_orb_4_attenuation(self, const, lin, quad):
        glUniform1f(self.orb4Constant, const)
        glUniform1f(self.orb4Linear, lin)
        glUniform1f(self.orb4Quadratic, quad)

    def set_orb_5_position(self, pos):
        glUniform4f(self.orb5PosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_orb_5_ambient(self, red, green, blue):
        glUniform4f(self.orb5AmbientLoc, red, green, blue, 1.0)

    def set_orb_5_diffuse(self, red, green, blue):
        glUniform4f(self.orb5DiffLoc, red, green, blue, 1.0)

    def set_orb_5_specular(self, red, green, blue):
        glUniform4f(self.orb5SpecLoc, red, green, blue, 1.0)

    def set_orb_5_attenuation(self, const, lin, quad):
        glUniform1f(self.orb5Constant, const)
        glUniform1f(self.orb5Linear, lin)
        glUniform1f(self.orb5Quadratic, quad)



    # Material - Could change and use color base type
    def set_material_ambient(self, color):
        glUniform4f(self.matAmbientLoc, color.r, color.g, color.b, 1.0)

    def set_material_diffuse(self, color):
        glUniform4f(self.matDiffLoc, color.r, color.g, color.b, 1.0)

    def set_material_specular(self, color):
        glUniform4f(self.matSpecLoc, color.r, color.b, color.g, 1.0)
        
    def set_material_shininess(self, shininess):
        glUniform1f(self.matShineLoc, shininess)
        # glUniform4f(self.matSpecLoc, red, green, blue, 1.0)

    # Currently not used
    def set_diffuse_texture(self, tex):
        glUniform1f(self.diffuseTextureLoc, tex)


    # Set vertex position and normal - DO NOT USE
    def set_position_attribute(self, vertex_array):
        # glUniform1i(self.hasTextureLoc, 1)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_position_attribute2(self, vertex_buffer_id):
        # glUniform1i(self.hasTextureLoc, 1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, None)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    # This works for sphere since position and normal are the same data
    # def set_attribute_buffers(self, position_buffer_id, normal_buffer_id):
    #     # Instead of array, send ID and bind to it (where daya exists)
    #     # glUniform1i(self.hasTextureLoc, 0)
    #     glBindBuffer(GL_ARRAY_BUFFER, position_buffer_id)
    #     glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, None)
    #     glBindBuffer(GL_ARRAY_BUFFER, normal_buffer_id)
    #     glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, None)

    # def set_attribute_buffers(self, vertex_buffer_id):
    #     # Instead of array, send ID and bind to it (where daya exists)
    #     # glUniform1i(self.hasTextureLoc, 0)
    #     glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
    #     glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, None)
    #     glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, None)

        
    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        # glUniform1i(self.hasTextureLoc, 0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        # x - x - x - x - STRIDES 
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))

    def set_attribute_buffers(self, vertex_buffer_id):
        # glUniform1i(self.hasTextureLoc, 0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

    # Texture coordinates 
    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    # Optimized
    def set_uv_attribute2(self, vertex_buffer_id):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_diffuse_tex(self, number):
        glUniform1i(self.diffuseTextureLoc, number)

    def set_spec_tex(self, number):
        glUniform1i(self.specularTextureLoc, number)

    def set_normal_tex(self, number):
        glUniform1i(self.normalTextureLoc, number)

    def set_has_texture(self, val):
        glUniform1i(self.hasTextureLoc, val)

    # Fog
    def set_fog_color(self, red, green, blue):
        glUniform4f(self.fogColorLoc, red, green, blue, 1.0)

    def set_fog_start(self, val):
        glUniform1f(self.fogStartLoc, val)

    def set_fog_end(self, val):
        glUniform1f(self.fogEndLoc, val)
