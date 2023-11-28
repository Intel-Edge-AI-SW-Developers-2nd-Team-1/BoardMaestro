import math
import statistics


class HandPatternRecognition:
    '''
    Class that hand pattern recognition

    Instance :
        self.x, self.y, self.z:         int
        self.nodes:                     string list
        self.angle:                     float
        self.flags:                     int
        self.ptrn:                      int
        self.check_frames_len:          int
        self.check_frames_idx:          int
        self.check_frames_ptrn_list:    int list
        self.mode_value:                int

    Method :
        __init__():                     None
        set_3d_position():              None
        get_3d_len():                   float
        get_angle_from_lens():          float
        get_node_angle():               float
        get_current_pattern():          int
        check_switch_pattern():         int
    '''

    def __init__(self,  x, y, z, check_frames_len):
        '''Init value, nodes, flags'''
        self.x, self.y, self.z = x, y, z
        self.nodes = ["0 - index_angle", "1 - middle_angle", "2 - ring_angle", "3 - pinky_angle"]
        self.angles = [0, 0, 0, 0]
        self.flags = [0, 0, 0, 0]
        self.ptrn = 0
        self.check_frames_len = check_frames_len
        self.check_frames_idx = 0
        self.check_frames_ptrn_list = []
        self.mode_value = 0
        for i in range(0, self.check_frames_len, 1):
            self.check_frames_ptrn_list.append(0)

    def set_3d_position(self, x, y, z):
        '''
        call List Points for calculation

        input : each point x, y, z values
        output : None
        '''
        self.x, self.y, self.z = x, y, z

    def get_3d_len(self, p1, p2):
        '''
        calculate 3D points p1 and p2 distance

        input : p1 x, y, z values and p2 x, y, z values
        output : distance between each two nodes
        '''
        return math.sqrt((self.x[p1] - self.x[p2]) ** 2 + (self.y[p1] - self.y[p2]) ** 2 + (self.z[p1] - self.z[p2]) ** 2)

    def get_angle_from_lens(self, a, b, c):
        '''
        Calculate angle ACB

        input : length of a, b, c
        output : Angle of C
        '''
        return math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)) / 3.14 * 180

    def get_node_angle(self):
        """Calculate each nodes angle"""
        # check the point
        if len(self.x) == 0:
            print("Points are empty")
            return 0
        else:
            for i in range(0, len(self.nodes), 1):
                # calculating node index
                node_index = i*4+5

                # calculate lens for calculating angle
                a = self.get_3d_len(node_index, node_index + 1)
                b = self.get_3d_len(node_index + 3, node_index + 1)
                c = self.get_3d_len(node_index, node_index + 3)

                # calculate angle
                self.angles[i] = self.get_angle_from_lens(a, b, c)

    def get_current_pattern(self):
        '''
        Detect this frame Pattern

        input : none
        output : current action pattern
        '''
        # check the point
        if len(self.x) == 0:
            print("Points are empty")
            return 0

        else:
            self.ptrn = 0

            # detect finger status from angles
            for i in range(0, len(self.nodes), 1):
                if self.angles[i] > 150:
                    self.flags[i] = 1
                else:
                    self.flags[i] = 0
                # save finger status at ptrn
                self.ptrn += self.ptrn + self.flags[i]

            # return now pattern
            if self.ptrn == 8:
                # print("write")
                return 1
            elif self.ptrn == 1:
                # print("enter")
                return 2
            elif self.ptrn == 15:
                # print("easer")
                return 3
            else:
                # print("stop")
                return 0

    def check_switch_pattern(self):
        '''
        Check check_frames_len frames pattern and pick out mode pattern for avoiding scattering

        input : None
        output : mode pattern about current check_frames_len
        '''
        # calculate node angles from updated x, y, z points
        self.get_node_angle()

        # push ptrn_value in check_frames_ptrn_list
        self.check_frames_ptrn_list[self.check_frames_idx] = self.get_current_pattern()

        # find mode_value in check_frames_ptrn_list
        self.mode_value = statistics.mode(self.check_frames_ptrn_list)
        self.check_frames_idx = (self.check_frames_idx + 1) % self.check_frames_len

        return self.mode_value
