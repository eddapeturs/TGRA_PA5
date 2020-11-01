
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *
# import copy

import ojb_3D_load

import numpy
from random import uniform, random, choice, randint
import pygame
from pygame.locals import *

import sys
import time

from Shaders.Shaders import *
from Objects.BaseObjects import *
from Objects.Maze import *
from Objects.Plane import *
from Objects.Walls import *
from Objects.SkyBox import *
from Assets.Texture import *
# from Assets.Characters.Ogre.Ogre import *
from Matrices import *
from Camera import *
from Bezier import *

class GraphicsProgram3D:
    def __init__(self):
        self.view_width = 1200
        self.view_height = 800

        pygame.init() 
        pygame.display.set_mode((self.view_width,self.view_height), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()
        self.sky_shader = SkyShader()

        self.model_matrix = ModelMatrix()
        # Need to do this in display for looking around with camera
        # self.view_matrix = ViewMatrix()
        # Eye - center - up
        # self.view_matrix.look(Point(25, 10, 2), Point(25, 9, -4), Vector(0, 1, 0))
        # self.view_matrix.look(Point(2.5, 2, 2.5), Point(2.5, 2, 4.5), Vector(0, 1, 0))
        self.first_person_view = True
        self.follow_view = False
        self.over_view = False
        self.v_key_pressed = False

        self.camera_to_wall_offset = 0.7
        self.fpCamera = Camera(Point(2.5, 2, 2.5), Point(2.5, 2, 4.5), Vector(0, 1, 0))
        self.followCamera = Camera(Point(2.5, 2, 2.5), Point(2.5, 2, 4.5), Vector(0, 1, 0))
        self.followCamera.follow_look(self.fpCamera)
        self.overviewCamera = Camera(Point(25.0, 30.0, 0.0), Point(25.0, 10.0, 10.0), Vector(0, 1, 0))
        # Maybe take this out?
        # self.shader.set_view_matrix(self.view_matrix.get_matrix())  # Get matrix and send to shader

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)

        self.fov = pi / 2
        # How close does my camera get? Set the near plane clipping (3rd param) as close to that as possible
        self.projection_matrix.set_perspective(self.fov, self.view_width / self.view_height, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # Imported models
        self.obj_model = ojb_3D_load.load_obj_file(sys.path[0] + "/Objects/models", "simple_box.obj")
        self.orb = ojb_3D_load.load_obj_file(sys.path[0] + "/Objects/models", "smooth_sphere.obj")
        self.ogre = ojb_3D_load.load_obj_file(sys.path[0] + "/Objects/Ogre", "ogre_posed.obj")
        self.coin = ojb_3D_load.load_obj_file(sys.path[0] + "/Objects/Coin", "coin.obj")
        self.hero = ojb_3D_load.load_obj_file(sys.path[0] + "/Objects/Hero", "son_jow.obj")

        self.brick_texture = Texture("/Assets/Textures/Bricks/Bricks_Color.jpg", "/Assets/Textures/Bricks/Bricks_Roughness.jpg", "/Assets/Textures/Bricks/Bricks_Normal.jpg")
        # self.paving_texture = Texture("PavingStones/PavingStones067_2K_Color.jpg", "PavingStones/PavingStones067_2K_AmbientOcclusion.jpg", "PavingStones/PavingStones067_2K_Normal.jpg")
        self.paving_texture = Texture("/Assets/Textures/PavingStones2/PavingStones024_2K_Color.jpg", "/Assets/Textures/PavingStones2/PavingStones024_2K_Roughness.jpg", "/Assets/Textures/PavingStones2/PavingStones024_2K_Normal.jpg")
        self.ogre_texture = Texture("/Objects/Ogre/ogre_diffuse.jpg")
        self.skybox_texture = Texture("/Assets/Textures/Skybox/skybox_texture06.jpg")
        self.coin_texture = Texture("/Objects/Coin/coinlowpoly.png", None, "/Objects/Coin/COINNORMAL.png")
        self.hero_texture = Texture("/Objects/Hero/raydal_blond_tex.tga.png")

        self.sphere = Sphere()
        self.plane = Plane()
        self.skySphere = SkySphere()
        self.bezier = Bezier()

        self.wall_height = 4.0
        self.wall_thickness = 1.0
        self.h_wall_length = 6.0
        self.v_wall_length = 5.0
        self.h_wall = HorizontalWall(self.h_wall_length, self.wall_thickness, self.wall_height)
        self.v_wall = VerticalWall(self.v_wall_length, self.wall_thickness, self.wall_height)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0
        self.gameEnded = False

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

        self.white_background = False

        self.start_time = time.time()
        self.elapsed_time = 0.0


        # # Actual player coordinates
        self.player_pos = Point(2.5, 1.0, 2.5)

        # X and Z values in a 10by10 grid
        self.player_pos_mod = [self.player_pos.x // 5, self.player_pos.z // 5]
        # Slighly different values to get proximity arrays
        self.player_pos_prev = [self.player_pos.x - 5 // 5, self.player_pos.z - 5 // 5]

        # Plane sizes
        self.plane_size = 50.0
        self.plane_thickness = 1.0

        self.max_orbs = 8
        self.orb_time = 30.0
        self.games_won = 0

        self.regenerateGame()


    def regenerateGame(self):
        self.maze = Maze(self.plane_size)
        self.getProximityArray(True)

        self.max_orbs -= self.games_won
        if self.max_orbs <= 3:
            self.max_orbs = 3

        # Set orbs in 10x10 grid (orb modulus position)
        # self.omp = [(0,1),(2,4),(8,3),(6,7),(1,8),(9,9),(5,2)]
        self.omp = []
        for num in range(self.max_orbs):
            x = randint(1, 9)
            z = randint(1, 9)
            self.omp.append((x, z)) 

        self.show_orb = []
        # for item in self.omp:
        for num in range(self.max_orbs):
            self.show_orb.append(True)

        # Calculates orb positions automatically from mod coords
        self.orb_pos = []
        for item in self.omp:
            self.orb_pos.append(Point(self.get_orb_pos(item[0]), 2.0, self.get_orb_pos(item[1])))

        # for val in self.bezier_points:
        #     print("Bezier: {}".format(val))

        self.ogre_walls = self.maze.ogre_positions
        self.ogre_h_walls = []
        self.ogre_v_walls = []
        for position, direction in self.maze.ogre_positions.items():
            if direction in ["N", "S"]:
                self.ogre_h_walls.append(position)
            if direction in ["E", "W"]:
                self.ogre_v_walls.append(position)

        self.coin_positions = []
        for item in self.maze.coin_positions:
            self.coin_positions.append(Point(self.get_coin_pos(item[0]), 2.0, self.get_coin_pos(item[1])))

        self.bezier_points = []
        for pos in self.coin_positions:
            bezier_list = [
                Point(pos.x - 1.0, 1.0, pos.z),
                Point(pos.x, 3.0, pos.z - 1.0),
                Point(pos.x + 1, 1.0, pos.z),
                Point(pos.x, 3.0, pos.z + 1.0)
            ]
            self.bezier_points.append(bezier_list)


        self.show_coin = []
        for item in self.coin_positions:
            self.show_coin.append(True)

        self.coins_to_collect = len(self.coin_positions)
        self.coins_collected = 0

        self.gameEnded = False
        self.invisible = False
        self.timer = 0.0
        self.previous_time = 0


    # Returns actual coordinates from mod position
    def get_coin_pos(self, val):
        return  val * 5 + 2.5

    def get_orb_pos(self, val):
        return  val * 5 + 1.5

    def update(self):
        self.delta_time = self.clock.tick() / 1000.0
        self.angle += pi * self.delta_time
        self.elapsed_time += self.delta_time
        
        self.checkOrbCollision()
        self.checkCoinCollision()
        # if angle > 2 * pi:
        #     angle -= (2 * pi)
        if not self.gameEnded:
            if(self.timer > 0.0):
                self.timer -= self.delta_time
                if self.previous_time != int(self.timer):
                    print("Time left: {} seconds".format(int(self.timer)))
                    self.previous_time = int(self.timer)
                    if int(self.timer == 0):
                        print("Times up!")
            else:
                self.invisible = False

        # Moving the camera
        if self.W_key_down:
            # self.view_matrix.pitch(pi * self.delta_time)
            pass
        if self.S_key_down:
            # self.view_matrix.pitch(-pi * self.delta_time)
            pass
        if self.A_key_down:
            if not self.over_view:
                self.fpCamera.yaw(-pi * self.delta_time)
                self.followCamera.follow_look(self.fpCamera)

        if self.D_key_down:
            if not self.over_view:
                self.fpCamera.yaw(pi * self.delta_time)
                self.followCamera.follow_look(self.fpCamera)

        if self.X_key_down:
            if not self.over_view:
                self.fpCamera.yaw(pi * self.delta_time)
                self.followCamera.follow_look(self.fpCamera)
        if self.C_key_down:
            if not self.over_view:
                self.fpCamera.yaw(-pi * self.delta_time)
                self.followCamera.follow_look(self.fpCamera)

        # Main camera movements   
        if self.UP_key_down:
            if not self.over_view:
                self.fpCamera.slide(0, 0, -10 * self.delta_time)
                self.wall_collision(-1, 1, self.fpCamera.n)

        if self.DOWN_key_down:
            if not self.over_view:
                self.fpCamera.slide(0, 0, 10 * self.delta_time)
                self.wall_collision(1, -1, self.fpCamera.n)

        if self.LEFT_key_down:
            if not self.over_view:
                self.fpCamera.slide(-10 * self.delta_time, 0, 0)
                self.wall_collision(-1, 1, self.fpCamera.u)

        if self.RIGHT_key_down:
            if not self.over_view:
                self.fpCamera.slide(10 * self.delta_time, 0, 0)
                self.wall_collision(1, -1, self.fpCamera.u)


        # Zoom in and out
        if self.T_key_down:
            self.fov -= 0.25 * self.delta_time
        if self.G_key_down:
            self.fov += 0.25 * self.delta_time

        # Press for overview
        if self.V_key_down:
            if self.v_key_pressed == False:
                if self.first_person_view:
                    # self.first_person_view = not self.first_person_view
                    self.follow_view = True
                    self.first_person_view = False
                elif self.follow_view:
                    self.follow_view = False
                    self.over_view = True
                elif self.over_view:
                    self.first_person_view = True
                    self.over_view = False
            self.v_key_pressed = True
        else:
            self.v_key_pressed = False

        # Regenerate maze with orbs (new game)
        if self.N_key_down:
            self.regenerateGame()
            # self.maze = Maze(self.plane_size)
            # self.getProximityArray(True)
            # self.show_orb = []
            # for item in self.omp:
            #     self.show_orb.append(True)
            # self.show_orb = [True, True, True, True, True]

    def wall_collision(self, mult1, mult2, vec):
        offset1 = mult1 * (self.wall_thickness / 2 + self.camera_to_wall_offset)
        offset2 = mult2 * (self.wall_thickness / 2 + self.camera_to_wall_offset)
        collisionHor, itemH = self.collisionDetectionHorizontal(self.fpCamera.eye)
        collisionVer, itemV = self.collisionDetectionVertical(self.fpCamera.eye)
        ogreCollisionHor, itemOH = self.ogreCollisionHor(self.fpCamera.eye)
        ogreCollisionVer, itemOV = self.ogreCollisionVer(self.fpCamera.eye)
        if collisionHor:
            if vec.z < 0:
                self.fpCamera.eye.z = itemH[1] + offset1
            else:
                self.fpCamera.eye.z = itemH[1] + offset2
        if collisionVer:
            if vec.x < 0:
                self.fpCamera.eye.x = itemV[0] + offset1
            else:
                self.fpCamera.eye.x = itemV[0] + offset2
        if ogreCollisionHor:
            if vec.z < 0:
                self.fpCamera.eye.z = itemOH[1] + offset1
            else:
                self.fpCamera.eye.z = itemOH[1] + offset2
        if ogreCollisionVer:
            if vec.x < 0:
                self.fpCamera.eye.x = itemOV[0] + offset1
            else:
                self.fpCamera.eye.x = itemOV[0] + offset2
        self.player_pos = self.fpCamera.eye
        self.followCamera.follow_look(self.fpCamera)
        self.update_player_pos_modulo()

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

        
    def ogreCollisionHor(self, pos):
        '''Checks for horizontal ogre walls'''
        if self.invisible:              # Do not check collision if player is invisible
            return False, (0.0, 0.0)
        for item in self.ogre_h_walls:
            if abs(item[0] - pos.x) < (self.h_wall_length / 2 + self.camera_to_wall_offset):
                if abs(item[1] - pos.z) < (self.wall_thickness / 2 + self.camera_to_wall_offset):
                    return True, item
        return False, (0.0, 0.0)

    # Check collision with vertical walls
    def ogreCollisionVer(self, pos):
        '''Checks for vertical ogre walls'''
        if self.invisible:              # Do not check collision if player is invisible
            return False, (0.0, 0.0)
        for item in self.ogre_v_walls:
            if abs(item[0] - pos.x) < (self.wall_thickness / 2 + self.camera_to_wall_offset):
                if abs(item[1] - pos.z) < (self.v_wall_length / 2 + self.camera_to_wall_offset):
                    return True, item
        return False, (0.0, 0.0)
  

    def update_player_pos_modulo(self):
        '''Updates player in 10by10 grid'''
        self.player_pos_mod[0] = self.player_pos.x // 5
        self.player_pos_mod[1] = self.player_pos.z // 5
        self.getProximityArray()

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
                self.invisible = True
                self.timer = self.orb_time

    def checkCoinCollision(self):
        tuple_pos = tuple(self.player_pos_mod)
        if tuple_pos in self.maze.coin_positions:
            index = self.maze.coin_positions.index(tuple_pos)
            coin = self.coin_positions[index]
            dist = sqrt(pow(self.player_pos.x - coin.x, 2) + pow(self.player_pos.y - coin.y, 2) + pow(self.player_pos.z - coin.z, 2))
            if dist < 1.0:
                if self.show_coin[index]:
                    self.show_coin[index] = False
                    self.coins_collected += 1
                    print("Coins collected: {}/{}".format(self.coins_collected, self.coins_to_collect))
                    if self.coins_collected == self.coins_to_collect:
                        self.gameEnded = True
                        self.games_won += 1
                        print("YOU WIN! Awesome! Press N to play again.")

        #         self.invisible = True
        #         self.timer = 30.0


    def getProximityArray(self, initial=False):
        '''Returns array of walls closest to the player.'''
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

        glClear(GL_COLOR_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        glViewport(0, 0, self.view_width, self.view_height)

        self.projection_matrix.set_perspective(self.fov, self.view_width / self.view_height, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # Set viewmatrix every single time to get a new matrix
        if self.first_person_view:
            self.shader.set_view_matrix(self.fpCamera.get_matrix())         # Get matrix and send to shader
        elif self.follow_view:
            self.shader.set_view_matrix(self.followCamera.get_matrix())     # Get matrix and send to shader
        elif self.over_view:
            self.shader.set_view_matrix(self.overviewCamera.get_matrix())   # Get matrix and send to shader
        else:
            self.shader.set_view_matrix(self.fpCamera.get_matrix())         # FP default


        self.shader.set_eye_position(self.fpCamera.eye)    # Sets eye position as camera
        # self.shader.set_flash_light(self.fpCamera, 50.5)    # Sets eye position as camera
        self.shader.set_flash_light(self.fpCamera, 50.5, 0.9)    # Sets eye position as camera
        # self.shader.set_light_position(Point(10 * cos(self.angle), 1, 10 * sin(self.angle)))    # Lighsource turning


        # LIGHT
        self.shader.set_light_position(Point(self.fpCamera.eye.x, 5.0, self.fpCamera.eye.z))    # Sets lightsource as eye
        # self.shader.set_light_position(Point(1.0, 20.0, 1.0))
        self.shader.set_light_diffuse(0.6, 0.6, 0.6)
        self.shader.set_light_specular(0.4, 0.4, 0.4)
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

        # SKYSPHERE
        glDisable(GL_DEPTH_TEST)
        self.sky_shader.use()
        glActiveTexture(GL_TEXTURE0)  
        glBindTexture(GL_TEXTURE_2D, self.skybox_texture.diffuse) # Will affect activetexture
        self.sky_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sky_shader.set_view_matrix(self.fpCamera.get_matrix())
        self.sky_shader.set_diffuse_tex(0)
        self.sky_shader.set_opacity(1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.fpCamera.eye.x, self.fpCamera.eye.y, self.fpCamera.eye.z)
        self.model_matrix.add_scale(1.0, 1.0, 1.0)
        self.sky_shader.set_model_matrix(self.model_matrix.matrix)
        self.skySphere.draw(self.sky_shader)
        self.model_matrix.pop_matrix()
        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)
        self.shader.use()


        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_ambient(Color(0.2, 0.2, 0.2))
        self.shader.set_material_specular(Color(0.0, 0.0, 0.0))
        self.shader.set_has_texture(1, 0, 0)
        self.set_textures(self.ogre_texture)
        for ogre_pos, direction in self.maze.ogre_positions.items():
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(ogre_pos[0], 0.4, ogre_pos[1])
            if direction == "E":
                self.model_matrix.add_rotate_y(-90)
            if direction == "S":
                self.model_matrix.add_rotate_y(150)
            if direction == "W":
                self.model_matrix.add_rotate_y(90)
            # No need to rotate on N, already in correct pos
            self.model_matrix.add_scale(1.0, 1.0, 1.0)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.ogre.draw(self.shader)
            self.model_matrix.pop_matrix()
        
        self.shader.set_has_texture(1, 0, 1)
        self.set_textures(self.coin_texture)
        coin_y_pos = sin(time.time() * 0.5) + 2.0
        # self.orb.set_vertices(self.shader)


        for index, pos in enumerate(self.coin_positions):
            coin_pos_point = self.bezier.get_bezier_position(self.elapsed_time, self.bezier_points[index], 0.0, 3.0)
            if self.show_coin[index]:
                self.shader.set_material_ambient(Color(0.4, 0.4, 0.4))
                self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
                self.shader.set_material_specular(Color(0.4, 0.4, 0.4))
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(coin_pos_point.x, coin_pos_point.y, coin_pos_point.z)
                self.model_matrix.add_rotate_y(self.angle * 10.0)
                self.model_matrix.add_scale(0.2, 0.2, 0.2)
                self.shader.set_model_matrix(self.model_matrix.matrix)
                self.coin.draw(self.shader)
                self.model_matrix.pop_matrix()

        self.set_textures(self.brick_texture)
        self.shader.set_has_texture(1, 1, 1)

        # Setting material for walls
        self.shader.set_material_ambient(Color(0.1, 0.1, 0.1))
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_specular(Color(0.0, 0.0, 0.0))
        self.shader.set_material_shininess(0.2)

        self.model_matrix.load_identity()
        for item in self.maze.horizontal_line_array:
            self.model_matrix.push_matrix() # Pushes a copy of the current matrix onto OpenGl's matrix stack. Calling transformation fuctions still affects the current matrix but has no effect on this copy
            self.model_matrix.add_translation(item[0], self.wall_height/2, item[1])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.h_wall.draw(self.shader, self.maze.h_neigh_dict[item])
            self.model_matrix.pop_matrix() # Pops the matrix off the top of the matrix stack and overwrites the current matrix with its values

        for item in self.maze.vertical_line_array:
            self.model_matrix.push_matrix() # Pushes a copy of the current matrix onto OpenGl's matrix stack. Calling transformation fuctions still affects the current matrix but has no effect on this copy
            self.model_matrix.add_translation(item[0], self.wall_height/2, item[1])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.v_wall.draw(self.shader, self.maze.v_neigh_dict[item])
            self.model_matrix.pop_matrix() # Pops the matrix off the top of the matrix stack and overwrites the current matrix with its values

        # PLANE
        self.set_textures(self.paving_texture)
        self.shader.set_has_texture(1, 1, 0)

        # self.plane.set_vertices(self.shader)
        self.shader.set_material_ambient(Color(0.3, 0.3, 0.3))
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_specular(Color(0.3, 0.3, 0.3))
        self.shader.set_material_shininess(1)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(25.0, 0, 25.0) 
        self.model_matrix.add_scale(50.0, 0.8, 50.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.plane.draw(self.shader)
        self.model_matrix.pop_matrix()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
               # HERO
        if self.invisible:
            self.shader.set_opacity(0.1)
        if self.first_person_view == False:
            self.set_textures(self.hero_texture)
            self.shader.set_has_texture(1, 0, 0)
            self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0)) 
            self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
            self.model_matrix.push_matrix()
            self.model_matrix.load_identity()
            self.model_matrix.add_translation(self.player_pos.x, 1.0, self.player_pos.z) 
            self.model_matrix.add_scale(1.0, 1.0, 1.0)
            self.model_matrix.add_rotate_y(120)
            self.model_matrix.add_transformation(self.fpCamera.mm)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.hero.draw(self.shader)
            self.model_matrix.pop_matrix()
        # self.shader.set_opacity(1.0)


        self.shader.set_has_texture(0, 0, 0)
        self.shader.set_opacity(0.6)

        self.shader.set_orb_diffuse(0.0, 1.0, 1.0)
        self.shader.set_orb_ambient(0.0, 1.0, 1.0)
        self.shader.set_orb_specular(0.0, 1.0, 1.0)
        self.shader.set_orb_attenuation(5.0, 5.0, 5.0)
        self.shader.set_material_diffuse(Color(0.0, 1.0, 1.0))
        self.shader.set_material_specular(Color(0.0, 1.0, 1.0))

        orb_y_pos = sin(time.time() * 0.5) + 2.0
        for num in range(self.max_orbs):
            self.shader.set_orb_position(num, Point(self.orb_pos[num].x, orb_y_pos, self.orb_pos[num].z), int(self.show_orb[num]))
        for num in range(self.max_orbs, 8):
            self.shader.set_orb_position(num, Point(0.0, 0.0, 0.0), 0)

        for index, orb in enumerate(self.orb_pos):
            if self.show_orb[index]:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(orb.x, orb_y_pos, orb.z) 
                self.model_matrix.add_scale(0.2, 0.2, 0.2)
                self.shader.set_model_matrix(self.model_matrix.matrix)
                self.orb.draw(self.shader)
                self.model_matrix.pop_matrix()
        
        glDisable(GL_BLEND)

        self.shader.set_opacity(1)

        pygame.display.flip()

    # Helper function to set the textures for an object
    def set_textures(self, texture):
        # Diffuse texture
        glActiveTexture(GL_TEXTURE0)  
        glBindTexture(GL_TEXTURE_2D, texture.diffuse) # Will affect activetexture
        self.shader.set_diffuse_tex(0)

        # Texture1  is specular
        if texture.specular:
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