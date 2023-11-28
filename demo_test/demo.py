import cv2
import time
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from hand_pose_estimation.hand_pose_estimation_module import HandPoseEstimation
from hand_pose_estimation.hand_pattern_recognition_module import HandPatternRecognition
from ai_modeling.image_inferencing_module import ImageInferencing
from image_preprocessing.preprocessing_module import Preprocessing
from expression_calculating.calculator_module import Calculator

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

    # define 8_x,y,z for making image
    x_8 = []
    y_8 = []

    # define flags and string_buf
    execute_flag = False
    list_flag = False
    string_buf = []
    start_time = 0

    # define save_frames
    save_frames = 0

    # call HandPoseEstimation
    model_path = '../model'
    hand_pose_estimation = HandPoseEstimation(model_path)

    # call HandPatternRecognition class
    hpr = HandPatternRecognition(hprx, hpry, hprz, 9)

    # call Calculator class
    calc = Calculator()

    # call preprocessing class
    desired_width = 150
    desired_height = 150
    preprocessing = Preprocessing(desired_width, desired_height)

    # call and set inferencing module
    input_shape = np.zeros((desired_width, desired_height, 3))
    infer = ImageInferencing(model_path, 'CPU', input_shape)

    # Use OpenCV’s VideoCapture to start capturing from the webcam.
    cap = cv2.VideoCapture(0)

    # str save list
    str_buf = ""
    str = ""
    str2 = f'counter: {preprocessing.result_counter}'

    # read the frame from webcam and define
    ret, frame = cap.read()
    frame_width = frame.shape[0]
    frame_height = frame.shape[1]

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

            # status[0:stop, 1:write, 2:enter, 3:erase]
            if mode_pattern == 0:
                execute_flag = True
                if str != "Stop mode":
                    str = "Stop mode"

            # execute each status
            # writing action
            if execute_flag is True and mode_pattern == 1:
                # saving points save in x, y
                x_8.append(hprx[8] * frame_height)
                y_8.append(hpry[8] * frame_width)
                save_frames += 1
                if str != "writing mode":
                    str = "writing mode"
                execute_flag = True

                # list_flag up
                list_flag = True

            # enter action
            elif execute_flag is True and mode_pattern == 2:
                if list_flag is True:
                    # list to image
                    preprocessing.get_current_image(x_8, y_8)
                    preprocessing.get_current_resize()
                    save_frames = 0
                    x_8 = []
                    y_8 = []
                    if str != "enter mode":
                        str = "enter mode"
                    str2 = f'counter: {preprocessing.result_counter}'

                    # inferencing and make string
                    string_image = cv2.imread(f'./Result/Result_{preprocessing.result_counter - 1}.jpg')
                    string_buf.append(f'{infer.get_inferencing_result(string_image, False)}')
                    str_buf = "".join(string_buf)
                    print(str_buf)
                    print(calc.eval_proc(str_buf))

                    execute_flag = False

                    # list_flag down
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
                    save_frames = 0
                    if str != "erase list":
                        str = "erase list"
                    execute_flag = False

                    # list_flag down
                    list_flag = False

                else:
                    # erase picture or move index
                    if preprocessing.result_counter != 0:
                        preprocessing.result_counter -= 1
                        del string_buf[preprocessing.result_counter]
                        str_buf = "".join(string_buf)
                        print(str_buf)
                        print(calc.eval_proc(str_buf))

                    if str != "erase picture":
                        str = "erase picture"
                    str2 = f'counter: {preprocessing.result_counter}'

                    execute_flag = False

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
