from math import * # trigonometry
from Objects.BaseObjects import *

class Camera:
    def __init__(self, eye, center, up):
        # self.eye = Point(0, 0, 0)  # Local coordinates of our camera
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)
        self.eye = eye                  # Point of origin in coordinate frame (where we should be at)
        self.n = (eye - center)         # Should be directed backwards from us
        self.n.normalize()
        self.u = up.cross(self.n)
        self.u.normalize()
        self.v = self.n.cross(self.u)               # We know this will be normalized

        self.center = center
        self.up = up

        # self.dir = self.u + self.n
        # self.dir.normalize()


    def look(self, eye, center, up):
        self.eye = eye                  # Point of origin in coordinate frame (where we should be at)
        self.n = (eye - center)         # Should be directed backwards from us
        self.n.normalize()
        self.u = up.cross(self.n)
        self.u.normalize()
        self.v = self.n.cross(self.u)               # We know this will be normalized

        self.center = center
        self.up = up

        # self.dir = self.u + self.n
        # self.dir.normalize()


       # Relative movements to camera
    def slide(self, del_u, del_v, del_n):
        # self.eye += self.u * del_u + self.v * del_v + self.n * del_n
        # tmp_y = self.eye.y
        self.eye += self.u * del_u + self.v * del_v + self.n * del_n

        # self.dir = self.u + self.n
        # self.dir.normalize()
        # self.eye.y = tmp_y


    def roll(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_u = self.u * c + self.v * s
        self.v = self.u * -s + self.v * c 
        self.u = tmp_u

    def yaw(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_u = self.u * c + self.n * s
        self.n = self.u * -s + self.n * c 
        self.u = tmp_u


    def pitch(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_u = self.u * c + self.v * s
        self.v = self.u * -s + self.v * c 
        self.u = tmp_u


    # Takes whatever eye, u, v and n values we have at this current point to build an array
    # Inverse of how we build the model matrix
    def get_matrix(self):
        minusEye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0,        0,        0,        1]
