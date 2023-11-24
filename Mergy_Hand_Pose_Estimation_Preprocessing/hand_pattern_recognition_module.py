import math
import statistics


class HandPatternRecognition:
    '''Hand pattern recognition class.'''
    def __init__(self,  x, y, z):
        '''init value, nodes, flags'''
        self.x, self.y, self.z = x, y, z
        self.nodes = ["0 - index_angle", "1 - middle_angle", "2 - ring_angle", "3 - pinky_angle"]
        self.angles = [0, 0, 0, 0]
        self.flags = [0, 0, 0, 0]
        self.ptrn = 0
        self.check_frames_len = 11
        self.check_frames_idx = 0
        self.check_frames_ptrn_list = []
        self.mode_value = 0
        for i in range(0, self.check_frames_len, 1):
            self.check_frames_ptrn_list.append(0)

    def set_3d_position(self, x, y, z):
        ''' call List Points for calculation'''
        self.x, self.y, self.z = x, y, z

    def get_3d_len(self, p1, p2):
        '''calculate 3D points p1 and p2 distance '''
        return math.sqrt((self.x[p1] - self.x[p2]) ** 2 + \
                         (self.y[p1] - self.y[p2]) ** 2 + (self.z[p1] - self.z[p2]) ** 2)

    def get_angle_from_lens(self, a, b, c):
        '''calculate angle ACB'''
        return math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)) / 3.14 * 180

    def get_node_angle(self):
        '''calculate each nodes angle'''
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
        '''Detect this frame Pattern'''
        # check the point
        if len(self.x) == 0:
            print("Points are empty")
            return 0

        else:
            self.ptrn = 0

            # detect finger status from angles
            for i in range(0, len(self.nodes), 1):
                if self.angles[i] > 160:
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

    def check_switch_pattern(self, value):
        '''check 9 frames pattern and pick out mode pattern for avoiding scattering'''
        # push ptrn_value in check_frames_ptrn_list
        self.check_frames_ptrn_list[self.check_frames_idx] = value

        # find mode_value in check_frames_ptrn_list
        self.mode_value = statistics.mode(self.check_frames_ptrn_list)
        self.check_frames_idx = (self.check_frames_idx + 1) % self.check_frames_len

        return self.mode_value
