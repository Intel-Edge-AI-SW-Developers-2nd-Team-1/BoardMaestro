import cv2
import numpy as np
import sys
import os
import time
from openvino.runtime import Core

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from hand_pattern_recognition.hand_pattern_recognition_module import HandPatternRecognition
from ai_modeling.image_inferencing_module import ImageInferencing
from image_preprocessing.preprocessing_module import Preprocessing
from expression_calculating.calculator_module import Calculator

class HandPoseEstimation:
    def __init__(self, model_path):
        '''
        init to use hand pose estimation
        :model_path: model_path must include .xml, .bin
        '''
        # define values for draw_landmarks_on_image
        self.MARGIN = 10  # pixels
        self.FONT_SIZE = 1
        self.FONT_THICKNESS = 1
        self.HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green

        # OpenVINO Inference Engine 초기화
        self.ie = Core()
        self.model_xml = f"{model_path}/hand_landmark_FP32.xml"
        self.model_bin = f"{model_path}/hand_landmark_FP32.bin"
        self.model = self.ie.read_model(model=self.model_xml, weights=self.model_bin)
        self.compiled_model = self.ie.compile_model(model=self.model, device_name="CPU")

        # 입력 레이어와 출력 레이어 정보 추출
        self.input_layer = next(iter(self.compiled_model.inputs))
        self.output_layer = next(iter(self.compiled_model.outputs))

    def get_hand_pose_result(self, frame, annotated_image_flag):
        '''
        Find the hand landmark detection results and visualize

        input : inference image and show flag
        output : detection result and annotated image
        '''
        # 입력 프레임 전처리
        input_image = cv2.resize(frame, (self.input_layer.shape[2], self.input_layer.shape[3]))
        input_image = input_image.transpose((2, 0, 1))  # HWC to CHW
        input_image = np.expand_dims(input_image, axis=0)

        # 추론 수행
        results = self.compiled_model([input_image])[self.output_layer]
        landmarks = results.reshape(-1, 3)  # 결과를 3차원 배열로 변환 (각 랜드마크 포인트를 x, y, z로 변환)

        detection_result = landmarks

        if annotated_image_flag is False:
            return [detection_result, frame]

        else:
            annotated_image = frame.copy()

            # Loop through the detected hands to visualize.
            for landmark in landmarks:
                x = int(landmark[0] * frame.shape[1])
                y = int(landmark[1] * frame.shape[0])
                cv2.circle(annotated_image, (x, y), 5, (0, 255, 0), -1)

            return [detection_result, annotated_image]

def main():
    # define x,y,z for saving key point
    points = 21
    hprx = [0] * points
    hpry = [0] * points
    hprz = [0] * points

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
    model_path = '../ai_modeling/model'
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
        if hand_landmarker_result is not None and len(hand_landmarker_result) == points:
            # save point to HandPatternRecognition
            for i in range(points):
                hprx[i] = hand_landmarker_result[i][0]
                hpry[i] = hand_landmarker_result[i][1]
                hprz[i] = hand_landmarker_result[i][2]
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
        os._exit(1)

