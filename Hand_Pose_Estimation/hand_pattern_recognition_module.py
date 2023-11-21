import math

class HandPatternRecognition:
    '''hand parttern recognition class'''
    def __init__(self,  x, y, z):
        '''init value, nodes, flags'''
        self.x, self.y, self.z = x, y, z
        self.nodes=["0 - index_angle", "1 - middle_angle", "2 - ring_angle", "3 - pinky_angle"]
        self.angles = [0,0,0,0]
        self.flags = [0,0,0,0]
        self.ptrn = 0

    def set3DPosition(self, x,y,z):
        '''call List Points for calculation'''
        self.x, self.y, self.z = x,y,z

    def get3DLen(self, p1, p2):
        '''calculate 3D points p1 and p2 distance '''
        return math.sqrt((self.x[p1] - self.x[p2]) ** 2 + (self.y[p1] - self.y[p2]) ** 2 + (self.z[p1] - self.z[p2]) ** 2)

    def getAnglefromLens(self, a, b, c):
        '''calculate angle p1-p3-p2'''
        return math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)) / 3.14 * 180

    def getNodesAngle(self):
        '''calculate each nodes angle'''
        # check the point
        if len(self.x) == 0:
            print("Points are empty")
            return 0
        else :
            for i in range(0,len(self.nodes),1):
                # calculating node index
                node_index = i*4+5

                # calculate lens for calculating angle
                a = self.get3DLen(node_index, node_index + 1)
                b = self.get3DLen(node_index + 3, node_index + 1)
                c = self.get3DLen(node_index, node_index + 3)

                # calculate angle
                self.angles[i]=self.getAnglefromLens(a,b,c)

    def getNowPattern(self):
        '''Detect this frame Pattern'''
        # check the point
        if len(self.x) == 0:
            print("Points are empty")
            return 0
        else:
            self.ptrn = 0

            # detect finger status from angles
            for i in range(0,len(self.nodes),1):
                if self.angles[i]>150:
                    self.flags[i] = 1
                else:
                    self.flags[i] = 0
                # save finger status at ptrn
                self.ptrn += self.ptrn + self.flags[i]

            #
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