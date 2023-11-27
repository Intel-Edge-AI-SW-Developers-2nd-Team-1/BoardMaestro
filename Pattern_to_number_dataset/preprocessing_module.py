import cv2
import math
import matplotlib.pyplot as plt


class Preprocessing:
    '''
    Class that help Image preprocessing and Camera real-time processing.

    Instance : 
        self.result_counter:                        int
        self.image_width:                           int
        self.image_height:                          int
        self.top_pad:                               int
        self.bottom_pad:                            int
        self.left_pad:                              int
        self.right_pad:                             int
        self.desired_width:                         int
        self.desired_height:                        int

    Method :
        __init__():                                 None
        get_current_calculate_distance():           None
        get_current_image():                        None
        get_current_roi():                          float
        get_current_resize():                       None
        get_current_padding():                      float
    '''

    def __init__(self, desired_width, desired_height):
        '''
        Proceed with initializing variables within the class.

        input : None
        output : None
        '''
        self.result_counter = 0
        self.image_width = 640
        self.image_height = 480
        self.desired_width = desired_width
        self.desired_height = desired_height

    def get_current_calculate_distance(self, point1, point2):
        '''
        Node values of two points in the list

        input :  point1,point2 (Node point)
        output : Distance between each two nodes
        '''
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def get_current_image(self, x_8, y_8):
        '''
        Through plot, the points of each node are averaged according to the chunk and connected to form an image.

        input :  x_list, y_list 
        output : None
        '''
        chunk_size = 3
        start_idx = 0
        avg_points = []
        threshold_distance = 80
        num_points = len(x_8)
        while start_idx < num_points:
            end_idx = min(start_idx + chunk_size, num_points)
            chunk_x = x_8[start_idx:end_idx]
            chunk_y = y_8[start_idx:end_idx]
            avg_x = sum(chunk_x) / len(chunk_x)
            avg_y = sum(chunk_y) / len(chunk_y)
            avg_points.append((avg_x, avg_y))
            start_idx += chunk_size
        plt.figure(figsize=(8, 6))
        plt.xlim(0, 640)
        plt.ylim(0, 480)
        plt.axis('square')
        for i in range(len(avg_points) - 4):
            distance = self.get_current_calculate_distance(avg_points[i], avg_points[i + 1])
            if distance <= threshold_distance:
                plt.scatter(avg_points[i][0], avg_points[i][1], color='white', marker='o', s=100)
                plt.plot([avg_points[i][0], avg_points[i + 1][0]], [avg_points[i][1], avg_points[i + 1][1]],
                         color='black', linewidth=6)
        plt.scatter(avg_points[-1][0], avg_points[-1][1], color='white', marker='o', s=100)
        plt.axis('off')
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        plt.savefig('number.png', bbox_inches='tight', pad_inches=0)
        plt.close()

    def get_current_roi(self, binary_image):
        '''
        Detect specific ROI

        input : binary image
        output : x_min ,y_min ,width, height for Roi
        '''
        x_min = float('inf')
        x_max = float('-inf')
        y_min = float('inf')
        y_max = float('-inf')
        height, width = binary_image.shape[:2]
        for i in range(width):
            for j in range(height):
                if binary_image[j][i] == 255:
                    if i < x_min:
                        x_min = i
                    if i > x_max:
                        x_max = i
                    if j < y_min:
                        y_min = j
                    if j > y_max:
                        y_max = j
        roi = binary_image[y_min:y_max, x_min:x_max]
        return x_min, y_min, x_max - x_min, y_max - y_min, roi

    def get_current_resize(self):
        '''
        Resize image for models

        input : None
        output : None
        '''
        color_img = cv2.imread('number.png')
        binary_img = cv2.imread('number.png', cv2.IMREAD_GRAYSCALE)
        binary_img_inverted = cv2.bitwise_not(binary_img)
        x, y, w, h, black_roi = self.get_current_roi(binary_img_inverted)
        original_roi = color_img[y:y + h, x:x + w]
        if(w >= h):
            padding_size = int((w-h)/2)
            padded_image_white_bg = self.get_current_padding(original_roi, padding_size, padding_size, 0,0) 
        else:
            padding_size = int((h-w)/2)
            padded_image_white_bg = self.get_current_padding(original_roi, 0, 0, padding_size,padding_size)
        resized_roi = cv2.resize(padded_image_white_bg, (self.desired_width, self.desired_height))
        save_path = f'./Result/Result_{self.result_counter}.jpg'
        cv2.imwrite(save_path, resized_roi)
        self.result_counter += 1

    def get_current_padding(self, image, top, bottom, left, right):
        '''
        Padding image for models

        input : image size, top size, bottom size, left size, right size
        output : padded image
        '''
        padded_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        return padded_image
