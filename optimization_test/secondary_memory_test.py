import cv2
import time
import numpy as np

import os

def main():
    #VideoCapture to start capturing from the webcam.
    cap = cv2.VideoCapture(0)

    # read the frame from webcam and define
    ret, frame = cap.read()
    frame_width = frame.shape[0]
    frame_height = frame.shape[1]
    
    # define 8_x,y,z for making image
    check_frame = 30
    point_num = 200
    point_num_half = 100
    x_8 = []
    y_8 = []

    for i in range(point_num_half):
        x_8.append(i)
        y_8.append(i)

    for i in range(point_num_half):
        x_8.append(i)
        y_8.append(point_num_half-i)

    save_image_list = []
    for i in range(check_frame):
        save_image_list.append(0)
    
    process_time = 0
    process_time_total = 0
    process_time_max = 0
    process_time_min = 1000
    counter = 0

    for i in range(check_frame):
        # to calculate running time, save start time to start_time
        start_time = time.time()
        counter += 1

        # read the frame from webcam
        ret, frame = cap.read()

        # show frame
        cv2.imshow("Result", frame)

        # calculate processing time on secondary memory
        process_time = (time.time() - start_time) * 1000
        process_time_total += process_time

        if(process_time < process_time_min):
            process_time_min = process_time
        
        if(process_time > process_time_max):
            process_time_max = process_time

        # if pressed 'q', end capture
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    process_time_total /= counter
    print(f"process_time_avg = {process_time_total:.4f}ms")
    print(f"process_time_min = {process_time_min:.4f}ms")
    print(f"process_time_max = {process_time_max:.4f}ms")

    process_time = 0
    process_time_total = 0
    process_time_max = 0
    process_time_min = 1000
    counter = 0

    for i in range(check_frame):
        # to calculate running time, save start time to start_time
        start_time = time.time()
        counter += 1

        # read the frame from webcam
        ret, frame = cap.read()

        # draw line
        for i in range(point_num-1):
            cv2.line(frame, (x_8[i]*5, y_8[i]*5), (x_8[i+1]*5, y_8[i+1]*5), (0,0,255), 2)
        

        # show frame
        cv2.imshow("Result", frame)

        # calculate processing time on secondary memory
        process_time = (time.time() - start_time) * 1000
        process_time_total += process_time

        if(process_time < process_time_min):
            process_time_min = process_time
        
        if(process_time > process_time_max):
            process_time_max = process_time
        
        # if pressed 'q', end capture
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    process_time_total /= counter
    print(f"process_time_avg on main memory = {process_time_total:.4f}ms")
    print(f"process_time_min on main memory = {process_time_min:.4f}ms")
    print(f"process_time_max on main memory = {process_time_max:.4f}ms")

    process_time = 0
    process_time_total = 0
    process_time_max = 0
    process_time_min = 1000
    counter = 0

    save_path = './test.jpg'
    for i in range(check_frame):
        # to calculate running time, save start time to start_time
        start_time = time.time()
        counter += 1

        # read the frame from webcam
        ret, frame = cap.read()

        # read and write image on secondary memory
        cv2.imwrite(save_path, frame)
        color_img = cv2.imread(save_path)
        for i in range(point_num-1):
            cv2.line(color_img, (x_8[i]*5, y_8[i]*5), (x_8[i+1]*5, y_8[i+1]*5), (0,0,255), 2)

        save_image_list[i] = color_img 
        cv2.imshow("Result", color_img)

        # calculate processing time on secondary memory
        process_time = (time.time() - start_time) * 1000
        process_time_total += process_time

        if(process_time < process_time_min):
            process_time_min = process_time
        
        if(process_time > process_time_max):
            process_time_max = process_time
        
        # if pressed 'q', end capture
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    process_time_total /= counter
    print(f"process_time_avg on secondary memory = {process_time_total:.4f}ms")
    print(f"process_time_min on secondary memory = {process_time_min:.4f}ms")
    print(f"process_time_max on secondary memory = {process_time_max:.4f}ms")

    cap.release()
    cv2.destroyAllWindows()

    cv2.imwrite(save_path, save_image_list[19])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
