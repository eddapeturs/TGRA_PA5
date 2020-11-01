import numpy
from random import uniform, random, choice

class Maze:
    ''' Takes plane size and generates a random maze.'''
    def __init__(self, plane_size):
        self.plane_size = plane_size
        self.pos_x = 2.5
        self.pos_z = 2.5
        self.index_pos_x = 0
        self.index_pos_z = 0

        self.horizontal_line_array = []
        self.vertical_line_array = []

        self.max_coins = 7
        self.coin_count = 0
        self.last_deleted_wall = []
        self.coin_positions = []
        self.ogre_positions = dict()
        self.generate_new_maze()
        self.find_neighbours()

        # For testing:
        # self.horizontal_line_array = []
        # self.vertical_line_array = []

    def find_neighbours(self):
        '''Find the nearest neighbours of walls, so that we don't draw unneccessary sides'''
        self.v_neigh_dict = dict()
        for item in self.vertical_line_array:
            self.v_neigh_dict[item] = {
                "neg_z": (item[0], item[1] - 5.0) not in self.vertical_line_array
                          and (item[0] + 2.5, item[1] - 2.5) not in self.horizontal_line_array 
                          and (item[0] - 2.5, item[1] - 2.5) not in self.horizontal_line_array,
                "pos_z": (item[0], item[1] + 5.0) not in self.vertical_line_array
                          and (item[0] + 2.5, item[1] + 2.5) not in self.horizontal_line_array 
                          and (item[0] - 2.5, item[1] + 2.5) not in self.horizontal_line_array,
            } 
        self.h_neigh_dict = dict()
        for item in self.horizontal_line_array:
            self.h_neigh_dict[item] = {
                "pos_x": (item[0] + 5.0, item[1]) not in self.horizontal_line_array,
                "neg_x": (item[0] - 5.0, item[1]) not in self.horizontal_line_array
            }


    def get_available_moves(self, x, z):
        available_positions = []
        if x > 0:
            available_positions.append("W")
        if x < 9:
            available_positions.append("E")
        if z > 0:
            available_positions.append("N")
        if z < 9:
            available_positions.append("S")
        return available_positions

    def check_unvisited(self, curr_x, curr_z, available_moves):
        next_indices = []
        for item in available_moves:
            if item == "W":
                next_indices.append((curr_x - 1, curr_z))
            if item == "E":
                next_indices.append((curr_x + 1, curr_z))
            if item == "N":
                next_indices.append((curr_x, curr_z - 1))
            if item == "S":
                next_indices.append((curr_x, curr_z + 1))
        
        unvisited_indices = []
        for item in next_indices:
            if self.visited[item[1]][item[0]] == False:
                unvisited_indices.append(item)

        return unvisited_indices

    def delete_horizontal_wall(self, x, z):
        self.horizontal_line_array.remove((x, z))
        
    def delete_vertical_wall(self, x, z):
        self.vertical_line_array.remove((x, z))

    def move(self, index):
        if index[0] > self.index_pos_x:
            self.pos_x += 5.0
        if index[0] < self.index_pos_x:
            self.pos_x -= 5.0
        if index[1] > self.index_pos_z:
            self.pos_z += 5.0
        if index[1] < self.index_pos_z:
            self.pos_z -= 5.0

        self.index_pos_x = index[0]
        self.index_pos_z = index[1]


    def move_to_random(self, unvisited):
        self.previously_visited.append((self.index_pos_x, self.index_pos_z))
        move_to = choice(unvisited)
        tmp_pos_x = self.pos_x
        tmp_pos_z = self.pos_z
        if move_to[0] > self.index_pos_x:
            tmp_pos_x += 5.0
            self.last_deleted_wall = (self.pos_x + 2.5, self.pos_z)
            self.delete_vertical_wall(self.pos_x + 2.5, self.pos_z)
        if move_to[0] < self.index_pos_x:
            tmp_pos_x -= 5.0
            self.last_deleted_wall = (self.pos_x - 2.5, self.pos_z)
            self.delete_vertical_wall(self.pos_x - 2.5, self.pos_z)
        if move_to[1] > self.index_pos_z:
            tmp_pos_z += 5.0
            self.last_deleted_wall = (self.pos_x, self.pos_z + 2.5)
            self.delete_horizontal_wall(self.pos_x, self.pos_z + 2.5)
        if move_to[1] < self.index_pos_z:
            tmp_pos_z -= 5.0
            self.last_deleted_wall = (self.pos_x, self.pos_z - 2.5)
            self.delete_horizontal_wall(self.pos_x, self.pos_z - 2.5)
        self.pos_x = tmp_pos_x
        self.pos_z = tmp_pos_z
        
        self.index_pos_x = move_to[0]
        self.index_pos_z = move_to[1]

        self.visited[self.index_pos_z][self.index_pos_x] = True

    def generate_maze(self):
        avail = self.get_available_moves(self.index_pos_x, self.index_pos_z)
        unvisited = self.check_unvisited(self.index_pos_x, self.index_pos_z, avail)
        # If we come across a dead-end where all surrounding squares have been visited, drop an coin
        if unvisited == []:
            if self.coin_count <= self.max_coins:
                self.coin_positions.append((self.index_pos_x, self.index_pos_z))
                self.ogre_positions[self.last_deleted_wall] = self.get_ogre_direction(self.last_deleted_wall, (self.index_pos_x, self.index_pos_z))
                self.coin_count += 1
        while unvisited == []:
            index = self.previously_visited.pop()
            self.move(index)
            avail = self.get_available_moves(index[0], index[1])
            unvisited = self.check_unvisited(index[0], index[1], avail)
        self.move_to_random(unvisited)   

    def generate_new_maze(self):
        # self.horizontal_line_array = []
        for z in numpy.arange(0.0, self.plane_size + 5.0, 5.0):
            for x in numpy.arange(2.5, self.plane_size, 5.0):
                self.horizontal_line_array.append((x, z))

        # self.vertical_line_array = []
        for x in numpy.arange(0.0, self.plane_size + 5.0, 5.0):
            for z in numpy.arange(2.5, self.plane_size, 5.0):
                self.vertical_line_array.append((x, z))

        self.visited = []
        for i in range(0, 10):
            tmp_list = []
            for j in range(0, 10):
                tmp_list.append(False)
            self.visited.append(tmp_list)
        self.visited[self.index_pos_x][self.index_pos_z] = True
        self.previously_visited = [(0, 0)]

        # While a box is unvisited, generate the maze
        for line in self.visited:
            while False in line:
                self.generate_maze() 


    # Returns actual coordinates from mod position
    def goc(self, val):
        return val * 5 + 2.5

    def mod(self, val):
        return (val - 2.5) / 5

    def get_ogre_direction(self, ogre, coin):
        '''Get the direction the ogre is facing'''
        ogre_mod_x = self.mod(ogre[0])
        ogre_mod_z = self.mod(ogre[1])
        if ogre_mod_x < coin[0]:
            return "E"
        elif ogre_mod_x > coin[0]:
            return "W"
        elif ogre_mod_z < coin[1]:
            return "S"
        elif ogre_mod_z > coin[1]:
            return "N"