
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *
# import copy

import ojb_3D_load

import numpy
from random import uniform, random, choice
import pygame
from pygame.locals import *

import sys
import time

from Shaders.Shaders import *
from Objects.BaseObjects import *
from Objects.Maze import *
from Objects.Dice import *
from Objects.Plane import *
from Objects.Orb import *
from Objects.Walls import *
# from Objects import *
# from Objects import Dice
from Assets.Texture import *
from Assets.Characters.Ogre.Ogre import *
from Matrices import *
from Camera import *

class GraphicsProgram3D:
    def __init__(self):
        self.view_width = 1200
        self.view_height = 800

        pygame.init() 
        pygame.display.set_mode((self.view_width,self.view_height), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        # Need to do this in display for looking around with camera
        # self.view_matrix = ViewMatrix()
        # Eye - center - up
        # self.view_matrix.look(Point(25, 10, 2), Point(25, 9, -4), Vector(0, 1, 0))
        # self.view_matrix.look(Point(2.5, 2, 2.5), Point(2.5, 2, 4.5), Vector(0, 1, 0))
        self.first_person_view = True
        self.v_key_pressed = False

        self.camera_to_wall_offset = 0.7
        self.fpCamera = Camera(Point(2.5, 2, 2.5), Point(2.5, 2, 4.5), Vector(0, 1, 0))
        self.followCamera = Camera(Point(2.5, 2, 2.5), Point(2.5, 2, 4.5), Vector(0, 1, 0))
        self.overviewCamera = Camera(Point(25.0, 30.0, 0.0), Point(25.0, 10.0, 10.0), Vector(0, 1, 0))
        # Maybe take this out?
        # self.shader.set_view_matrix(self.view_matrix.get_matrix())  # Get matrix and send to shader

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)

        self.fov = pi / 2
        # How close does my camera get? Set the near plane clipping (3rd param) as close to that as possible
        self.projection_matrix.set_perspective(self.fov, self.view_width / self.view_height, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # self.cube = Cube()
        self.cube = D2()
        self.sphere = Sphere()
        self.orb = Orb((0.0, 0.0)) # Generic orb for setting stuff
        # self.wall = Wall()
        self.dice = D2()
        # self.plane = Plane()
        self.plane = Plane()
        # self.ogre = Ogre()
        self.obj_model = ojb_3D_load.load_obj_file(sys.path[0] + "/MeshModelAddon/models", "simple_box.obj")
        self.ogre = ojb_3D_load.load_obj_file(sys.path[0] + "/Assets/Characters/Ogre", "ogre_posed.obj")


              # Matrix sizes
        self.wall_height = 3.0
        self.wall_thickness = 1.0
        self.h_wall_length = 6.0
        self.v_wall_length = 5.0
        self.h_wall = HorizontalWall(self.h_wall_length, self.wall_thickness, self.wall_height)
        self.v_wall = VerticalWall(self.v_wall_length, self.wall_thickness, self.wall_height)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False
        self.DOWN_key_down = False
        self.RIGHT_key_down = False
        self.LEFT_key_down = False
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.X_key_down = False
        self.C_key_down = False
        self.V_key_down = False
        self.N_key_down = False

        self.white_background = True


        # Actual player coordinates
        self.player_pos = Point(2.5, 1.0, 2.5)

        # X and Z values in a 10by10 grid
        self.player_pos_mod = [self.player_pos.x // 5, self.player_pos.z // 5]
        # Slighly different values to get proximity arrays
        self.player_pos_prev = [self.player_pos.x - 5 // 5, self.player_pos.z - 5 // 5]

  

        # For now, player is a box of sixe 2.0
        self.player_size = 2.0 # TODO is this used?

        # Plane sizes
        self.plane_size = 50.0
        self.plane_thickness = 1.0

        # Make new (random) maze
        self.maze = Maze(self.plane_size)

        # Get the closest walls to the player
        self.getProximityArray(True)

        # Set orbs in 10x10 grid (orb modulus position)
        self.omp = [(0,0),(2,4),(8,3),(6,7),(1,8)]
        self.show_orb = [True, True, True, True, True]

        # Calculates orb positions automatically from mod coords
        self.orb_pos = [Point(self.goc(self.omp[0][0]), 2.0, self.goc(self.omp[0][1])),
                        Point(self.goc(self.omp[1][0]), 2.0, self.goc(self.omp[1][1])),
                        Point(self.goc(self.omp[2][0]), 2.0, self.goc(self.omp[2][1])),
                        Point(self.goc(self.omp[3][0]), 2.0, self.goc(self.omp[3][1])),
                        Point(self.goc(self.omp[4][0]), 2.0, self.goc(self.omp[4][1]))]



        # print(self.maze.orb_positions)
        self.orb_pos2 = []
        for item in self.maze.orb_positions:
            self.orb_pos2.append(Orb(item))

        self.bricks = Texture("/Assets/Textures/Bricks/Bricks_Color.jpg", "/Assets/Textures/Bricks/Bricks_Roughness.jpg", "/Assets/Textures/Bricks/Bricks_Normal.jpg")
        # self.paving = Texture("PavingStones/PavingStones067_2K_Color.jpg", "PavingStones/PavingStones067_2K_AmbientOcclusion.jpg", "PavingStones/PavingStones067_2K_Normal.jpg")
        self.paving = Texture("/Assets/Textures/PavingStones2/PavingStones024_2K_Color.jpg", "/Assets/Textures/PavingStones2/PavingStones024_2K_Roughness.jpg", "/Assets/Textures/PavingStones2/PavingStones024_2K_Normal.jpg")
        self.ogre_texture = Texture("/Assets/Characters/Ogre/ogre_diffuse.jpg")


    # Returns actual coordinates from mod position
    def goc(self, val):
        return  val * 5 + 2.5

    def update(self):
        self.delta_time = self.clock.tick() / 1000.0
        self.angle += pi * self.delta_time

        self.checkOrbCollision()
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        # Moving the camera
        if self.W_key_down:
            # self.view_matrix.pitch(pi * self.delta_time)
            pass
        if self.S_key_down:
            # self.view_matrix.pitch(-pi * self.delta_time)
            pass
        if self.A_key_down:
            self.fpCamera.yaw(-pi * self.delta_time)
        if self.D_key_down:
            self.fpCamera.yaw(pi * self.delta_time)
        if self.X_key_down:
            self.fpCamera.yaw(pi * self.delta_time)
        if self.C_key_down:
            self.fpCamera.yaw(-pi * self.delta_time)

        # Main camera movements   
        if self.UP_key_down:
            self.fpCamera.slide(0, 0, -10 * self.delta_time)
            collisionHor, itemH = self.collisionDetectionHorizontal(self.fpCamera.eye)
            collisionVer, itemV = self.collisionDetectionVertical(self.fpCamera.eye)
            
            if collisionHor:
                if self.fpCamera.n.z < 0:
                    self.fpCamera.eye.z = itemH[1] - (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.z = itemH[1] + (self.wall_thickness / 2 + self.camera_to_wall_offset)

            if collisionVer:
                if self.fpCamera.n.x < 0:
                    self.fpCamera.eye.x = itemV[0] - (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.x = itemV[0] + (self.wall_thickness / 2 + self.camera_to_wall_offset)
            self.player_pos = self.fpCamera.eye
            self.update_player_pos_modulo()

        if self.DOWN_key_down:
            self.fpCamera.slide(0, 0, 10 * self.delta_time)
            collisionHor, itemH = self.collisionDetectionHorizontal(self.fpCamera.eye)
            collisionVer, itemV = self.collisionDetectionVertical(self.fpCamera.eye)
            if collisionHor:
                if self.fpCamera.n.z < 0:
                    self.fpCamera.eye.z = itemH[1] + (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.z = itemH[1] - (self.wall_thickness / 2 + self.camera_to_wall_offset)
            if collisionVer:
                if self.fpCamera.n.x < 0:
                        self.fpCamera.eye.x = itemV[0] + (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.x = itemV[0] - (self.wall_thickness / 2 + self.camera_to_wall_offset)
            self.player_pos = self.fpCamera.eye
            self.update_player_pos_modulo()

        if self.LEFT_key_down:
            self.fpCamera.slide(-10 * self.delta_time, 0, 0)
            collisionHor, itemH = self.collisionDetectionHorizontal(self.fpCamera.eye)
            collisionVer, itemV = self.collisionDetectionVertical(self.fpCamera.eye)
            if collisionHor:
                if self.fpCamera.u.z < 0:
                    self.fpCamera.eye.z = itemH[1] - (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.z = itemH[1] + (self.wall_thickness / 2 + self.camera_to_wall_offset)
            if collisionVer:
                if self.fpCamera.u.x < 0:
                    self.fpCamera.eye.x = itemV[0] - (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.x = itemV[0] + (self.wall_thickness / 2 + self.camera_to_wall_offset)
            self.player_pos = self.fpCamera.eye
            self.update_player_pos_modulo()
            
        if self.RIGHT_key_down:
            self.fpCamera.slide(10 * self.delta_time, 0, 0)
            collisionHor, itemH = self.collisionDetectionHorizontal(self.fpCamera.eye)
            collisionVer, itemV = self.collisionDetectionVertical(self.fpCamera.eye)
            if collisionHor:
                if self.fpCamera.u.z < 0:
                    self.fpCamera.eye.z = itemH[1] + (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.z = itemH[1] - (self.wall_thickness / 2 + self.camera_to_wall_offset)

            if collisionVer:
                if self.fpCamera.u.x < 0:
                    self.fpCamera.eye.x = itemV[0] + (self.wall_thickness / 2 + self.camera_to_wall_offset)
                else:
                    self.fpCamera.eye.x = itemV[0] - (self.wall_thickness / 2 + self.camera_to_wall_offset)
            self.player_pos = self.fpCamera.eye
            self.update_player_pos_modulo()
  

        # Zoom in and out
        if self.T_key_down:
            self.fov -= 0.25 * self.delta_time
        if self.G_key_down:
            self.fov += 0.25 * self.delta_time

        # Press for overview
        if self.V_key_down:
            if self.v_key_pressed == False:
                self.first_person_view = not self.first_person_view
            self.v_key_pressed = True
        else:
            self.v_key_pressed = False

        # Regenerate maze with orbs (new game)
        if self.N_key_down:
            self.maze = Maze(self.plane_size)
            self.getProximityArray(True)
            self.show_orb = [True, True, True, True, True]

    

    def update_player_pos_modulo(self):
        self.player_pos_mod[0] = self.player_pos.x // 5
        self.player_pos_mod[1] = self.player_pos.z // 5
        self.getProximityArray()

    # Using AABB to check for collision
    # Check collision detection for both H&V (unused as is)
    def collisionDetection(self, pos):
        for item in self.h_proxi:
            if abs(item[0] - pos.x) < (self.h_wall_length / 2 + self.player_size / 2):
                if abs(item[1] - pos.z) < (self.wall_thickness / 2 + self.player_size / 2):
                    return True

        for item in self.v_proxi:
            if abs(item[0] - pos.x) < (self.wall_thickness / 2 + self.player_size / 2):
                if abs(item[1] - pos.z) < (self.v_wall_length / 2 + self.player_size / 2):
                    return True
        return False

    # Check collision with horizontal walls
    def collisionDetectionHorizontal(self, pos):
        for item in self.h_proxi:
            if abs(item[0] - pos.x) < (self.h_wall_length / 2 + self.camera_to_wall_offset):
                if abs(item[1] - pos.z) < (self.wall_thickness / 2 + self.camera_to_wall_offset):
                    return True, item
        return False, (0.0, 0.0)

    # Check collision with vertical walls
    def collisionDetectionVertical(self, pos):
        for item in self.v_proxi:
            if abs(item[0] - pos.x) < (self.wall_thickness / 2 + self.camera_to_wall_offset):
                if abs(item[1] - pos.z) < (self.v_wall_length / 2 + self.camera_to_wall_offset):
                    return True, item
        return False, (0.0, 0.0)


    # Checks for orb collision if the player is within the
    # same tile (10x10) and only for that specific orb
    def checkOrbCollision(self):
        tuple_pos = tuple(self.player_pos_mod)
        if tuple_pos in self.omp:
            index = self.omp.index(tuple_pos)
            orb = self.orb_pos[index]
            dist = sqrt(pow(self.player_pos.x - orb.x, 2) + pow(self.player_pos.y - orb.y, 2) + pow(self.player_pos.z - orb.z, 2))
            if dist < 1.0:
                self.show_orb[index] = False

    # This array returns the walls closest to the player
    # Done so that we are not checking all walls on the board
    # when checking for collision
    def getProximityArray(self, initial=False):
        # If the player is within a new tile, get new walls
        if (self.player_pos_prev[0] != self.player_pos_mod[0]) or (self.player_pos_prev[1] != self.player_pos_mod[1]) or (initial == True):
            # Horizontal walls
            x = self.player_pos_mod[0]
            z = self.player_pos_mod[1]
            z_list = [z * 5, (z + 1) * 5]
            x_list = [((x-1) * 5) + 2.5, (x * 5) + 2.5, ((x+1) * 5) + 2.5] 
            h_proxi = []
            v_proxi = []
            for i in z_list:
                for j in x_list:
                    if (j, i) in self.maze.horizontal_line_array:
                        h_proxi.append((j, i))

            x_list = [x * 5, (x + 1) * 5]
            z_list = [((z-1) * 5) + 2.5, (z * 5) + 2.5, ((z+1) * 5) + 2.5] 
            for i in z_list:
                for j in x_list:
                    if (j, i) in self.maze.vertical_line_array:
                        v_proxi.append((j, i))
            # Update previous positions
            self.player_pos_prev[0] = x
            self.player_pos_prev[1] = z
            self.h_proxi = h_proxi
            self.v_proxi = v_proxi

    def display(self):
        # self.view_matrix = ViewMatrix()
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        # glDisable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        glViewport(0, 0, self.view_width, self.view_height)

        self.projection_matrix.set_perspective(self.fov, self.view_width / self.view_height, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # Set viewmatrix every single time to get a new matrix
        if self.first_person_view:
            self.shader.set_view_matrix(self.fpCamera.get_matrix())  # Get matrix and send to shader
        else:
            self.shader.set_view_matrix(self.overviewCamera.get_matrix())  # Get matrix and send to shader
        self.shader.set_eye_position(self.fpCamera.eye)    # Sets eye position as camera
        # self.shader.set_light_position(Point(10 * cos(self.angle), 1, 10 * sin(self.angle)))    # Lighsource turning


        # LIGHT
        # self.shader.set_light_position(self.fpCamera.eye)    # Sets lightsource as eye
        self.shader.set_light_position(Point(1.0, 20.0, 1.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(0.3, 0.3, 0.3)
        self.shader.set_light_ambient(0.3, 0.3, 0.3)
        # self.shader.set_light_diffuse(0.3, 0.3, 0.3)
        # self.shader.set_light_specular(0.4, 0.4, 0.4)
        # self.shader.set_light_ambient(0.1, 0.1, 0.1)

        # FOG
        self.shader.set_fog_color(1.0, 1.0, 1.0)
        self.shader.set_fog_start(2.0)
        self.shader.set_fog_end(50.0)

        # Sets current matrix as the identity matrix, used to reset.
        self.model_matrix.load_identity() 



        # # Set vertices for cubes
        # self.cube.set_vertices(self.shader)
        # # Player cube
        # if self.first_person_view == False:
        #     self.shader.set_material_diffuse(1.0, 1.0, 1.0) 
        #     self.shader.set_material_specular(1.0, 1.0, 1.0)
        #     self.model_matrix.push_matrix()
        #     self.model_matrix.add_translation(self.player_pos.x, 1.0, self.player_pos.z) 
        #     # self.model_matrix.add_translation(self.player_pos.x, self.player_pos.y, self.player_pos.z + 4) 
        #     self.model_matrix.add_scale(1.0, 1.0, 1.0)
        #     # self.model_matrix.add_rotate_y(90)
        #     # self.model_matrix.add_rotate_z(self.fpCamera.n.z)
        #     self.shader.set_model_matrix(self.model_matrix.matrix)
        #     self.cube.draw(self.shader)
        #     self.model_matrix.pop_matrix()




        self.set_textures(self.bricks)
        self.shader.set_has_texture(1)

        # # # Setting material for walls
        self.shader.set_material_ambient(Color(0.1, 0.1, 0.1))
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(1.0)
        # self.h_wall.set_vertices(self.shader)
        for item in self.maze.horizontal_line_array:
            # print("Horizontal: ", item)
            self.model_matrix.push_matrix() # Pushes a copy of the current matrix onto OpenGl's matrix stack. Calling transformation fuctions still affects the current matrix but has no effect on this copy
            self.model_matrix.add_translation(item[0], self.wall_height/2, item[1])
            # self.model_matrix.add_scale(0.8, 0.8, 0.8)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.h_wall.draw(self.shader)
            self.model_matrix.pop_matrix() # Pops the matrix off the top of the matrix stack and overwrites the current matrix with its values

        # self.v_wall.set_vertices(self.shader)
        for item in self.maze.vertical_line_array:
            self.model_matrix.push_matrix() # Pushes a copy of the current matrix onto OpenGl's matrix stack. Calling transformation fuctions still affects the current matrix but has no effect on this copy
            self.model_matrix.add_translation(item[0], self.wall_height/2, item[1])
            # self.model_matrix.add_scale(0.8, 0.8, 0.8)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.v_wall.draw(self.shader)
            self.model_matrix.pop_matrix() # Pops the matrix off the top of the matrix stack and overwrites the current matrix with its values


        # glActiveTexture(GL_TEXTURE0)
        # glBindTexture(GL_TEXTURE_2D, self.tex_id)

        # self.shader.set_diffuse_texture(self.tex_id)

        self.shader.set_has_texture(0)
        # self.orb.set_vertices(self.shader)
        for orb in self.orb_pos2:
            # self.orb_pos2[].set_vertices(self.shader)
            self.shader.set_orb_1_position(orb.position)
            self.shader.set_orb_1_diffuse(1.0, 0.0, 1.0)
            self.shader.set_orb_1_ambient(1.0, 0.0, 1.0)
            self.shader.set_orb_1_specular(1.0, 0.0, 1.0)
            self.shader.set_orb_1_attenuation(0.9, 0.9, 0.9)
            # print(orb)
            self.shader.set_material_ambient(Color(0.0, 0.0, 0.0))
            self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
            self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(orb.pos_x, 2.0, orb.pos_z)
            self.model_matrix.add_scale(0.2, 0.2, 0.2)
            # self.model_matrix.add_rotate_x(self.angle * 0.1)
            # self.model_matrix.add_rotate_z(self.angle * self.delta_time)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            orb.draw(self.shader)
            self.model_matrix.pop_matrix()


        # PLANE
        self.set_textures(self.paving)
        self.shader.set_has_texture(1)

        # self.plane.set_vertices(self.shader)
        self.shader.set_material_ambient(Color(1.0, 1.0, 1.0))
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(1)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(25.0, 0, 25.0) 
        self.model_matrix.add_scale(50.0, 0.8, 50.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.plane.draw(self.shader)
        self.model_matrix.pop_matrix()



        # self.shader.set_has_texture(1)
        # self.set_textures(self.ogre_texture)
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(2.0, 2.0, 2.0)
        # self.model_matrix.add_scale(1.0, 1.0, 1.0)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.ogre.draw(self.shader)
        # self.model_matrix.pop_matrix()

        self.shader.set_has_texture(1)
        # self.set_textures(self.ogre_texture)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(2.0, 0.2, 2.0)
        self.model_matrix.add_scale(1.0, 1.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model.draw(self.shader)
        self.model_matrix.pop_matrix()
        


        pygame.display.flip()

    # Helper function to set the textures for an object
    def set_textures(self, texture):
        # Diffuse texture
        glActiveTexture(GL_TEXTURE0)  
        glBindTexture(GL_TEXTURE_2D, texture.diffuse) # Will affect activetexture
        self.shader.set_diffuse_tex(0)

        if texture.specular:
        # Texture1  is specular
            glActiveTexture(GL_TEXTURE1)  
            glBindTexture(GL_TEXTURE_2D, texture.specular)
            self.shader.set_spec_tex(1)

        # Normal map
        if texture.normal:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D, texture.normal)
            self.shader.set_spec_tex(2)


    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_DOWN:
                        self.DOWN_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_t:
                        self.T_key_down = True
                    if event.key == K_g:
                        self.G_key_down = True
                    if event.key == K_x:
                        self.X_key_down = True
                    if event.key == K_c:
                        self.C_key_down = True
                    if event.key == K_v:
                        self.V_key_down = True
                    if event.key == K_n:
                        self.N_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_DOWN:
                        self.DOWN_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_t:
                        self.T_key_down = False
                    if event.key == K_g:
                        self.G_key_down = False
                    if event.key == K_x:
                        self.X_key_down = False
                    if event.key == K_c:
                        self.C_key_down = False
                    if event.key == K_v:
                        self.V_key_down = False
                    if event.key == K_n:
                        self.N_key_down = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    continue
                if event.type == pygame.MOUSEMOTION:
                    continue
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()