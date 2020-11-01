
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
        # self.orb1PosLoc = glGetUniformLocation(self.renderingProgramID, "u_orb1_pos")
        # self.orb2PosLoc = glGetUniformLocation(self.renderingProgramID, "u_orb2_pos")
        # self.orb3PosLoc = glGetUniformLocation(self.renderingProgramID, "u_orb3_pos")
        # self.orb4PosLoc = glGetUniformLocation(self.renderingProgramID, "u_orb4_pos")
        # self.orb5PosLoc = glGetUniformLocation(self.renderingProgramID, "u_orb5_pos")
        # self.orb6PosLoc = glGetUniformLocation(self.renderingProgramID, "u_orb6_pos")
        # self.orb7PosLoc = glGetUniformLocation(self.renderingProgramID, "u_orb7_pos")

        self.orbPosLoc = []
        self.orbVisibleLoc = []
        for num in range(8):
            self.orbPosLoc.append(glGetUniformLocation(self.renderingProgramID, "u_orb" + str(num + 1) + "_pos"))
            self.orbVisibleLoc.append(glGetUniformLocation(self.renderingProgramID, "u_orb" + str(num + 1) + "_visible"))
            

        # self.orb1VisibleLoc = glGetUniformLocation(self.renderingProgramID, "u_orb1_visible")
        # self.orb2VisibleLoc = glGetUniformLocation(self.renderingProgramID, "u_orb2_visible")
        # self.orb3VisibleLoc = glGetUniformLocation(self.renderingProgramID, "u_orb3_visible")
        # self.orb4VisibleLoc = glGetUniformLocation(self.renderingProgramID, "u_orb4_visible")
        # self.orb5VisibleLoc = glGetUniformLocation(self.renderingProgramID, "u_orb5_visible")
        # self.orb6VisibleLoc = glGetUniformLocation(self.renderingProgramID, "u_orb6_visible")
        # self.orb7VisibleLoc = glGetUniformLocation(self.renderingProgramID, "u_orb7_visible")

        # self.orbPosLoc = glGetUniformLocation(self.renderingProgramID, "orb.position")
        self.orbAmbientLoc = glGetUniformLocation(self.renderingProgramID, "orb.ambient")
        self.orbDiffLoc = glGetUniformLocation(self.renderingProgramID, "orb.diffuse")
        self.orbSpecLoc = glGetUniformLocation(self.renderingProgramID, "orb.specular")
        self.orbConstant = glGetUniformLocation(self.renderingProgramID, "orb.constant")
        self.orbLinear = glGetUniformLocation(self.renderingProgramID, "orb.linear")
        self.orbQuadratic = glGetUniformLocation(self.renderingProgramID, "orb.quadratic")

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
        self.hasDiffLoc = glGetUniformLocation(self.renderingProgramID, "u_has_diffuse")
        self.hasSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_has_specular")
        self.hasNormLoc = glGetUniformLocation(self.renderingProgramID, "u_has_normal")


        # Fog
        self.fogColorLoc = glGetUniformLocation(self.renderingProgramID, "u_fog_color")
        self.fogStartLoc = glGetUniformLocation(self.renderingProgramID, "u_fog_start")
        self.fogEndLoc = glGetUniformLocation(self.renderingProgramID, "u_fog_end")

        # self.noOfOrbsLoc = glGetUniformLocation(self.renderingProgramID, "u_no_of_orbs")
        self.flashPosLoc = glGetUniformLocation(self.renderingProgramID, "u_flash.position")
        self.flashDirLoc = glGetUniformLocation(self.renderingProgramID, "u_flash.direction")
        self.flashCOLoc = glGetUniformLocation(self.renderingProgramID, "u_flash.cutoff")
        self.flashAttenuationLoc = glGetUniformLocation(self.renderingProgramID, "u_flash.attenuation")

        self.opacityLoc = glGetUniformLocation(self.renderingProgramID, "u_opacity")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_flash_light(self, camera, angle, attenuation):
        glUniform4f(self.flashPosLoc, camera.eye.x, camera.eye.y, camera.eye.z, 1.0)
        glUniform4f(self.flashDirLoc, camera.n.x, camera.n.y, camera.n.z, 0.0)
        # print("Rad: ", cos(radians(angle)))
        glUniform1f(self.flashCOLoc, cos(radians(angle)))
        glUniform1f(self.flashAttenuationLoc, attenuation)
        # lightingShader.setFloat("light.cutOff", glm::cos(glm::radians(12.5f)));

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

    # General orb setters
    def set_orb_position(self, pos):
        glUniform4f(self.orbPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_orb_ambient(self, red, green, blue):
        glUniform4f(self.orbAmbientLoc, red, green, blue, 1.0)

    def set_orb_diffuse(self, red, green, blue):
        glUniform4f(self.orbDiffLoc, red, green, blue, 1.0)

    def set_orb_specular(self, red, green, blue):
        glUniform4f(self.orbSpecLoc, red, green, blue, 1.0)

    def set_orb_attenuation(self, const, lin, quad):
        glUniform1f(self.orbConstant, const)
        glUniform1f(self.orbLinear, lin)
        glUniform1f(self.orbQuadratic, quad)


    def set_orb_position(self, orbNum, pos, visible):
        glUniform4f(self.orbPosLoc[orbNum], pos.x, pos.y, pos.z, 1.0)
        glUniform1i(self.orbVisibleLoc[orbNum], visible)
    # Orb 1
    # def set_orb_1_position(self, pos, visible):
    #     glUniform4f(self.orb1PosLoc, pos.x, pos.y, pos.z, 1.0)
    #     glUniform1i(self.orb1VisibleLoc, visible)

    # def set_orb_2_position(self, pos, visible):
    #     glUniform4f(self.orb2PosLoc, pos.x, pos.y, pos.z, 1.0)
    #     glUniform1i(self.orb2VisibleLoc, visible)

    # def set_orb_3_position(self, pos, visible):
    #     glUniform4f(self.orb3PosLoc, pos.x, pos.y, pos.z, 1.0)
    #     glUniform1i(self.orb3VisibleLoc, visible)

    # def set_orb_4_position(self, pos, visible):
    #     glUniform4f(self.orb4PosLoc, pos.x, pos.y, pos.z, 1.0)
    #     glUniform1i(self.orb4VisibleLoc, visible)

    # def set_orb_5_position(self, pos, visible):
    #     glUniform4f(self.orb5PosLoc, pos.x, pos.y, pos.z, 1.0)
    #     glUniform1i(self.orb5VisibleLoc, visible)

    # def set_orb_6_position(self, pos, visible):
    #     glUniform4f(self.orb6PosLoc, pos.x, pos.y, pos.z, 1.0)
    #     glUniform1i(self.orb6VisibleLoc, visible)

    # def set_orb_7_position(self, pos, visible):
    #     glUniform4f(self.orb7PosLoc, pos.x, pos.y, pos.z, 1.0)
    #     glUniform1i(self.orb7VisibleLoc, visible)

    def set_orb_ambient(self, red, green, blue):
        glUniform4f(self.orbAmbientLoc, red, green, blue, 1.0)

    def set_orb_diffuse(self, red, green, blue):
        glUniform4f(self.orbDiffLoc, red, green, blue, 1.0)

    def set_orb_specular(self, red, green, blue):
        glUniform4f(self.orbSpecLoc, red, green, blue, 1.0)

    def set_orb_attenuation(self, const, lin, quad):
        glUniform1f(self.orbConstant, const)
        glUniform1f(self.orbLinear, lin)
        glUniform1f(self.orbQuadratic, quad)

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


    # Set textures
    def set_has_texture(self, diff, spec, norm):
        glUniform1i(self.hasDiffLoc, diff)
        glUniform1i(self.hasSpecLoc, spec)
        glUniform1i(self.hasNormLoc, norm)

    # Fog
    def set_fog_color(self, red, green, blue):
        glUniform4f(self.fogColorLoc, red, green, blue, 1.0)

    def set_fog_start(self, val):
        glUniform1f(self.fogStartLoc, val)

    def set_fog_end(self, val):
        glUniform1f(self.fogEndLoc, val)

    def set_opacity(self, val):
        glUniform1f(self.opacityLoc, val)

    # def set_no_of_orbs(self, val):
    #     glUniform1f(self.noOfOrbsLoc, val)


class SkyShader:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/Shaders/skyShader.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/Shaders/skyShader.frag")
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


    #     # Texture 
        self.diffuseTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_diff_tex")
        self.opacityLoc = glGetUniformLocation(self.renderingProgramID, "u_opacity")


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

    # Currently not used
    def set_diffuse_texture(self, tex):
        glUniform1f(self.diffuseTextureLoc, tex)


    # Set vertex position and normal - DO NOT USE
    def set_position_attribute(self, vertex_array):
        # glUniform1i(self.hasTextureLoc, 1)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)
        
    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        # glUniform1i(self.hasTextureLoc, 0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        # x - x - x - x - STRIDES 
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))

    # Texture coordinates 
    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_diffuse_tex(self, number):
        glUniform1i(self.diffuseTextureLoc, number)

    def set_opacity(self, val):
        glUniform1f(self.opacityLoc, val)