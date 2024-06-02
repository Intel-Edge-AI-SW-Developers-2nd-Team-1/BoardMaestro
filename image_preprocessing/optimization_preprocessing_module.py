import cv2
import numpy as np

class optimization_preprocessing:
    def __init__(self, desired_width, desired_height):
        '''
        Proceed with initializing variables within the class.

        input : None
        output : None
        '''
        self.result_counter = 0
        self.result_image = []
        self.moving_buf = 5
        self.image_width = 640
        self.image_height = 480
        self.desired_width = desired_width
        self.desired_height = desired_height
        self.pretrained_model_resolution = 45
        for i in range(100):
            self.result_image.append(np.ones((self.desired_width, self.desired_height, 3), dtype=np.uint8)*255)

    def create_image_from_point(self, x, y, each_line_contain_points, line_thick):
        # move_avg_filter x, y points
        new_x = []
        new_y = []
        current_idx = 0
        moving_buf_half = int(self.moving_buf/2)
        for i in range(len(each_line_contain_points)):
            for j in range(current_idx, each_line_contain_points[i]):
                if j >= (moving_buf_half+current_idx) and j < (each_line_contain_points[i] - moving_buf_half):
                    sum_x = 0
                    sum_y = 0
                    for k in range(self.moving_buf):
                        sum_x += x[j - moving_buf_half + k]
                        sum_y += y[j - moving_buf_half + k]
                    new_x.append(int(sum_x/self.moving_buf))
                    new_y.append(int(sum_y/self.moving_buf))
                else:
                    new_x.append(x[j])
                    new_y.append(y[j])
            current_idx = each_line_contain_points[i]
        x = new_x
        y = new_y

        # find max_x, max_y, min_x, min_y
        max_x = 0
        max_y = 0
        min_x = 10000
        min_y = 10000
        points_total_number = len(x)

        for i in range(points_total_number):
            if max_x < x[i]:
                max_x  = x[i]
            if max_y < y[i]:
                max_y  = y[i]
            if min_x > x[i]:
                min_x  = x[i]
            if min_y > y[i]:
                min_y  = y[i]

        # make new points for roi image
        # find width, height about incomming points
        width = max_x - min_x
        height = max_y - min_y
        resize_rate = 1

        # move initial point to (0, 0)
        for i in range(points_total_number):
            x[i] = x[i] - min_x
            y[i] = y[i] - min_y

        if width < height:
            append_size = height - width
            append_size = append_size / 2
            resize_rate = self.pretrained_model_resolution / height

            # move x, y points for appending width & resizing
            for i in range(points_total_number):
                x[i] = int((x[i] + append_size) * resize_rate)
                y[i] = int(y[i] * resize_rate)
        
        else:
            append_size = width - height
            append_size = append_size / 2
            resize_rate = self.pretrained_model_resolution / width

            # move x, y points for appending width & resizing
            for i in range(points_total_number):
                x[i] = int(x[i] * resize_rate)
                y[i] = int((y[i] + append_size) * resize_rate)

        # create image
        self.result_image[self.result_counter] = self.draw_line_from_point(x, y, each_line_contain_points, self.result_image[self.result_counter], line_thick)
        self.result_image[self.result_counter] = cv2.flip(self.result_image[self.result_counter], 1)

        self.result_counter += 1
        return self.result_image[self.result_counter-1]
    
    def draw_line_from_point(self, x, y, each_line_contain_points, frame, line_thick):
        current_idx = 0
        for i in range(len(each_line_contain_points)):
            for j in range(current_idx, each_line_contain_points[i]-1):
                cv2.line(frame, (x[j], y[j]), (x[j+1], y[j+1]), (0,0,0), line_thick)
            current_idx = each_line_contain_points[i]
        return frame