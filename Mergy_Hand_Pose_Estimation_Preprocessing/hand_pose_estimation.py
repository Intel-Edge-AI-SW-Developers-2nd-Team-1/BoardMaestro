import time
import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from hand_pattern_recognition_module import HandPatternRecognition
from hand_pose_estimation_show_module import HandPoseEstimationShow
from image_inferencing_module import ImageInferencing

from preprocessing_module import Preprocessing

# define HandLandmarkers elements
model_path = './models/hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# set option
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path, delegate=BaseOptions.Delegate.CPU),
    running_mode=VisionRunningMode.IMAGE)

# The landmarker is initialized
landmarker = HandLandmarker.create_from_options(options)

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

# define save_frames
save_frames = 0

# call HandPatternRecognition class
hpr = HandPatternRecognition(hprx, hpry, hprz)

# call preprocessing class
ppr = Preprocessing()

# call HandPoseEstimationShow class
hpes = HandPoseEstimationShow(points)

# call and set inferencing module
infer_model_path = './models'
input_shape = np.zeros((224, 224, 3))
infer = ImageInferencing(infer_model_path, 'CPU', input_shape)

# Use OpenCV’s VideoCapture to start capturing from the webcam.
cap = cv2.VideoCapture(0)

# Create a loop to read the latest frame from the camera using VideoCapture#read()
while True:
    # to calculate running time, save start time to start_time
    start_time = time.time()

    # read the frame from webcam
    ret, frame = cap.read()

    # check the frame
    if not ret:
        break

    # Convert the frame received from OpenCV to a MediaPipe’s Image object.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
                        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    hand_landmarker_result = landmarker.detect(mp_image)

    # show detection_result to visible
    annotated_image = hpes.draw_landmarks_on_image(mp_image.numpy_view(), hand_landmarker_result)
    cv2.imshow("Result", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    # if detect hand, start HandPatternRecognition
    if hand_landmarker_result.handedness.__len__() == 1:
        # save point to HandPatternRecognition
        for i in range(0, points, 1):
            hprx[i] = hand_landmarker_result.hand_landmarks[0][i].x
            hpry[i] = hand_landmarker_result.hand_landmarks[0][i].y
            hprz[i] = hand_landmarker_result.hand_landmarks[0][i].z
        hpr.set_3d_position(hprx, hpry, hprz)

        # calculate node angles
        hpr.get_node_angle()

        # detect ptrn
        now_pattern = hpr.get_current_pattern()

        # pick out mode pattern for avoiding scattering
        mode_pattern = hpr.check_switch_pattern(now_pattern)

        # status[0:stop, 1:write, 2:enter, 3:erase]
        if execute_flag is False and mode_pattern == 0:
            execute_flag = True
            print("stop")

        #  execute each status
        #  writing action
        if execute_flag is True and mode_pattern == 1:
            # saving points save in x,y
            x_8.append(hprx[8])
            y_8.append(hpry[8])
            save_frames += 1
            execute_flag = True

            # list_flag down
            list_flag = True

        # enter action 
        elif execute_flag is True and mode_pattern == 2:
            if list_flag is True:
                # make image
                ppr.get_current_excel(save_frames, x_8, y_8)
                ppr.get_current_image()
                save_frames = 0
                ppr.get_current_resize()
                x_8 = []
                y_8 = []

                # inferencing and make string
                string_image = cv2.imread(f'./Result/Result_{ppr.result_counter-1}.jpg')
                string_buf.append(f'{infer.get_inferencing_result(string_image)}')
                print(string_buf)

                print("enter")

                # execute_flag down
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
                print("erase list")
                execute_flag = False

                # list_flag down
                list_flag = False

            else:
                # erase picture or move index
                if ppr.result_counter != 0:
                    ppr.result_counter -= 1
                    del string_buf[ppr.result_counter]
                    print(string_buf)

                print("erase picture")
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
