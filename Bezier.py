from Objects.BaseObjects import *
import math 

class Bezier:
    def __init__(self):
        self.endTime = 0.0
        self.startTime = 0.0
        # self.currentTime = 0.0


    def get_bezier_position(self, currentTime, ctrl_points, startTime=None, endTime=None):
        # print("TIME: ", time)
        # self.currentTime += 0.1
        bezier = Point(0.0, 0.0, 0.0)
            
        # t = currentTime - startTime / endTime - startTime
        # print("EndTime: ", endTime)
        currentTime %= endTime * 2
        t = (currentTime - startTime) / (endTime - startTime)
        if t >= 1.0:
            t = 1 - (t - 1)
        # print("Current time: ", currentTime)
        # print("t: ", t)
        mult_1 = pow((1-t), 3)
        mult_2 = 3 * pow((1-t), 2) * t
        mult_3 = 3 * (1-t) * pow(t, 2)
        mult_4 = pow(t, 3)
        # print("Mults: {}, {}, {}, {}".format(mult_1, mult_2, mult_3, mult_4))

        ctrl1 = ctrl_points[0]
        ctrl2 = ctrl_points[1]
        ctrl3 = ctrl_points[2]
        ctrl4 = ctrl_points[3]

        bezier.x = pow((1-t), 3) * ctrl1.x + 3 * pow((1-t), 2) * t * ctrl2.x + 3 * (1-t) * pow(t, 2) * ctrl3.x + pow(t, 3) * ctrl4.x
        bezier.y = pow((1-t), 3) * ctrl1.y + 3 * pow((1-t), 2) * t * ctrl2.y + 3 * (1-t) * pow(t, 2) * ctrl3.y + pow(t, 3) * ctrl4.y
        bezier.z = pow((1-t), 3) * ctrl1.z + 3 * pow((1-t), 2) * t * ctrl2.z + 3 * (1-t) * pow(t, 2) * ctrl3.z + pow(t, 3) * ctrl4.z


        # print("Bezier: ({},{},{})".format(bezier.x, bezier.y, bezier.z))

        return bezier