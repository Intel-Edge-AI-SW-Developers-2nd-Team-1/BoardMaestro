import time
import cv2
import numpy as np
from optimization_preprocessing_module import optimization_preprocessing

width = 45
height = 45
preprocessing = optimization_preprocessing(width, height)

x_8 = []
y_8 = []
each_line_contain_points = []

# create list about 1
for i in range(20):
    x_8.append(200)
    y_8.append(100+i*10)
each_line_contain_points.append(len(x_8))

frame = np.ones((600, 600, 3), dtype=np.uint8)*255

# to calculate running time, save start time to start_time
start_time = time.time()

# create image about 1
cv2.imshow("Result1", preprocessing.draw_line_from_point(x_8, y_8, each_line_contain_points, frame, 2))
cv2.imshow("Result2", preprocessing.create_image_from_point(x_8, y_8, each_line_contain_points, 1))

# calculate processing time
process_time = (time.time() - start_time) * 1000
print(f"process_time = {process_time:.4f}ms")
cv2.waitKey(0)

# create list about +
x_8 = []
y_8 = []
each_line_contain_points = []
for i in range(20):
    x_8.append(200)
    y_8.append(100+i*10)
each_line_contain_points.append(len(x_8))

for i in range(20):
    x_8.append(100+i*10)
    y_8.append(200)
each_line_contain_points.append(len(x_8))

frame = np.ones((600, 600, 3), dtype=np.uint8)*255

# to calculate running time, save start time to start_time
start_time = time.time()

# create image about +
cv2.imshow("Result1", preprocessing.draw_line_from_point(x_8, y_8, each_line_contain_points, frame, 2))
cv2.imshow("Result2", preprocessing.create_image_from_point(x_8, y_8, each_line_contain_points, 1))

# calculate processing time
process_time = (time.time() - start_time) * 1000
print(f"process_time = {process_time:.4f}ms")
cv2.waitKey(0)

# create list about \
x_8 = []
y_8 = []
each_line_contain_points = []
for i in range(20):
    x_8.append(200+i)
    y_8.append(100+i*10)
each_line_contain_points.append(len(x_8))

frame = np.ones((600, 600, 3), dtype=np.uint8)*255

# to calculate running time, save start time to start_time
start_time = time.time()

# create image about +
cv2.imshow("Result1", preprocessing.draw_line_from_point(x_8, y_8, each_line_contain_points, frame, 2))
cv2.imshow("Result2", preprocessing.create_image_from_point(x_8, y_8, each_line_contain_points, 1))

# calculate processing time
process_time = (time.time() - start_time) * 1000
print(f"process_time = {process_time:.4f}ms")
cv2.waitKey(0)
cv2.destroyAllWindows()


