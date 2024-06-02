import cv2
import time
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from hand_pose_estimation.hand_pose_estimation_module import HandPoseEstimation
from hand_pattern_recognition.hand_pattern_recognition_module import HandPatternRecognition
from ai_modeling.image_inferencing_module import ImageInferencing
from image_preprocessing.preprocessing_module import Preprocessing
from expression_calculating.calculator_module import Calculator
from optimization_preprocessing_module import optimization_preprocessing

def main():
    # define x,y,z for saving key point
    points = 21
    hprx = []
    hpry = []
    hprz = []
    for i in range(0, points, 1):
        hprx.append(0)
        hpry.append(0)
        hprz.append(0)

    # define x,y,each_line_contain_points for making image
    x_8 = []
    y_8 = []
    each_line_contain_points = []
    
    # define flags and string_buf
    each_line_contain_points_flag = False
    execute_flag = False
    list_flag = False
    string_buf = []
    start_time = 0

    # define save_frames
    save_frames = 0

    # call HandPoseEstimation
    model_path = '../ai_modeling/model'
    hand_pose_estimation = HandPoseEstimation(model_path)

    # call HandPatternRecognition class
    hpr = HandPatternRecognition(hprx, hpry, hprz, 9)

    # call Calculator class
    calc = Calculator()

    # call preprocessing class
    desired_width = 45
    desired_height = 45
    preprocessing = Preprocessing(desired_width, desired_height)
    opti_preprocessing = optimization_preprocessing(desired_width, desired_height)

    # call and set inferencing module
    input_shape = np.zeros((desired_width, desired_height, 3))
    infer = ImageInferencing(model_path, 'CPU', input_shape)

    # Use OpenCV’s VideoCapture to start capturing from the webcam.
    cap = cv2.VideoCapture(0)

    # str save list
    str_buf = ""
    str = ""
    str2 = f'counter: {opti_preprocessing.result_counter}'

    # read the frame from webcam and define
    ret, frame = cap.read()
    frame_width = frame.shape[0]
    frame_height = frame.shape[1]

    # check time value
    frame_read_time = 0
    hand_pose_estimation_time = 0
    preprocessing_time = 0
    inference_time = 0

    # Create a loop to read the latest frame from the camera using VideoCapture#read()
    while True:
        if time.time() - start_time < 0.04:
            continue
        # to calculate running time, save start time to start_time
        start_time = time.time()

        # read the frame from webcam
        ret, frame = cap.read()

        # check the frame
        if not ret:
            break
        
        # check time
        frame_read_time = (time.time() - start_time) * 1000
        start_time = time.time()

        # detect hand landmark
        hand_landmarker_result, annotated_image = hand_pose_estimation.get_hand_pose_result(frame, True)

        # show detection_result to visible
        cv2.putText(annotated_image, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
        cv2.putText(annotated_image, str2, (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)
        cv2.imshow("Result", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

        # if detect hand, start HandPatternRecognition
        if hand_landmarker_result.handedness.__len__() == 1:
            # save point to HandPatternRecognition
            for i in range(0, points, 1):
                hprx[i] = hand_landmarker_result.hand_landmarks[0][i].x
                hpry[i] = hand_landmarker_result.hand_landmarks[0][i].y
                hprz[i] = hand_landmarker_result.hand_landmarks[0][i].z
            hpr.set_3d_position(hprx, hpry, hprz)

            # pick out mode pattern for avoiding scattering
            mode_pattern = hpr.check_switch_pattern()

            # check time
            hand_pose_estimation_time = (time.time() - start_time) * 1000

            # status[0:stop, 1:write, 2:enter, 3:erase]
            if mode_pattern == 0:
                execute_flag = True
                if str != "Stop mode":
                    str = "Stop mode"
                
                # save each_line_contain_points
                if each_line_contain_points_flag == True:
                    each_line_contain_points_flag = False
                    each_line_contain_points.append(len(x_8))

            # execute each status
            # writing action
            if execute_flag is True and mode_pattern == 1:
                # saving points save in x, y
                x_8.append(hprx[8] * frame_height)
                y_8.append(hpry[8] * frame_width)
                save_frames += 1
                if str != "writing mode":
                    str = "writing mode"
            
                # list_flag up
                each_line_contain_points_flag = True
                execute_flag = True
                list_flag = True

            # enter action
            elif execute_flag is True and mode_pattern == 2:
                if list_flag is True:
                    start_time = time.time()

                    each_line_contain_points.append(len(x_8))

                    # list to image
                    opti_preprocessing.create_image_from_point(x_8, y_8, each_line_contain_points, 1)

                    # initialize value for next image
                    save_frames = 0
                    x_8 = []
                    y_8 = []
                    each_line_contain_points = []

                    if str != "enter mode":
                        str = "enter mode"
                    str2 = f'counter: {opti_preprocessing.result_counter}'

                    # check time
                    preprocessing_time = (time.time() - start_time) * 1000
                    start_time = time.time()

                    # inferencing and make string
                    string_image = opti_preprocessing.result_image[opti_preprocessing.result_counter - 1]
                    cv2.imwrite('number.png', string_image)
                    cv2.imshow(f'draw_img{opti_preprocessing.result_counter-1}',string_image)
                    string_buf.append(f'{infer.get_inferencing_result(string_image, False)}')
                    str_buf = "".join(string_buf)
                    print(str_buf)
                    print(calc.eval_proc(str_buf))

                    inference_time = (time.time() - start_time) * 1000
                    print(f"frame_read_time = {frame_read_time:.4f}ms")
                    print(f"hand_pose_estimation_time = {hand_pose_estimation_time:.4f}ms")
                    print(f"preprocessing_time = {preprocessing_time:.4f}ms")
                    print(f"inference_time = {inference_time:.4f}ms")

                    # flag down
                    each_line_contain_points_flag = False
                    execute_flag = False
                    list_flag = False

                else:
                    print("List is empty. Please draw number or sign")
                    execute_flag = False

            # erase action
            elif execute_flag is True and mode_pattern == 3:
                if list_flag is True:
                    # erase list
                    x_8 = []
                    y_8 = []
                    each_line_contain_points = []
                    save_frames = 0
                    if str != "erase list":
                        str = "erase list"
                    
                    # flag down
                    each_line_contain_points_flag = False
                    execute_flag = False
                    list_flag = False

                else:
                    # erase picture or move index
                    if opti_preprocessing.result_counter != 0:
                        opti_preprocessing.result_counter -= 1
                        opti_preprocessing.result_image[opti_preprocessing.result_counter] = np.ones((desired_width, desired_height, 3), dtype=np.uint8)*255
                        del string_buf[opti_preprocessing.result_counter]
                        str_buf = "".join(string_buf)
                        print(str_buf)
                        print(calc.eval_proc(str_buf))

                    if str != "erase picture":
                        str = "erase picture"
                    str2 = f'counter: {opti_preprocessing.result_counter}'

                    # flag down
                    each_line_contain_points_flag = False
                    execute_flag = False
                    list_flag = False

        # show process time and fps
        process_time = time.time() - start_time
        FPS = 1 / process_time
        # print(f"process_time = {process_time:.4f}s, FPS = {FPS:.2f}")

        # if pressed 'q', end capture
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
