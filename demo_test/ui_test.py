from concurrent.futures.thread import _worker
import cv2
import time
import numpy as np
#import bluetooth
import threading

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QFont

from hand_pose_estimation.hand_pose_estimation_module import HandPoseEstimation
from hand_pattern_recognition.hand_pattern_recognition_module import HandPatternRecognition
from ai_modeling.image_inferencing_module import ImageInferencing
from image_preprocessing.preprocessing_module import Preprocessing
from expression_calculating.calculator_module import Calculator
#from user_interface.ble_interface import BluetoothWorker

class App(QWidget):
    def __init__(self, w, h):
        super().__init__()
        self.title = 'Hand Draw Formula'
        self.left = 10
        self.top = 50
        self.width = w
        self.height = h
        self.initUI()

        # define x,y,z for saving key point
        self.points = 21
        self.hprx = []
        self.hpry = []
        self.hprz = []
        for i in range(0, self.points, 1):
            self.hprx.append(0)
            self.hpry.append(0)
            self.hprz.append(0)

        # define 8_x,y,z for making image
        self.x_8 = []
        self.y_8 = []

        # define flags and string_buf
        self.execute_flag = False
        self.list_flag = False
        self.string_buf = []
        self.start_time = 0

        # define save_frames
        self.save_frames = 0

        # call HandPoseEstimation
        model_path = './ai_modeling/model'
        self.hand_pose_estimation = HandPoseEstimation(model_path)

        # call HandPatternRecognition class
        self.hpr = HandPatternRecognition(self.hprx, self.hpry, self.hprz, 9)

        # call Calculator class
        self.calc = Calculator()
        
        # call preprocessing class
        desired_width = 150
        desired_height = 150
        self.preprocessing = Preprocessing(desired_width, desired_height)

        # call and set inferencing module
        input_shape = np.zeros((desired_width, desired_height, 3))
        self.infer = ImageInferencing(model_path, 'CPU', input_shape)

        self.cap = cv2.VideoCapture(0)

        # str save list
        self.str_buf = ""
        self.str = ""
        self.str2 = f'counter: {self.preprocessing.result_counter}'

        # read the frame from webcam and define
        _, frame = self.cap.read()
        self.frame_width = frame.shape[0]
        self.frame_height = frame.shape[1]

    
    def initUI(self):
        self.ratio_w, self.ratio_h = self.width / 1920, self.height / 1000
        
        #font size
        self.font_size = int(50 * self.ratio_w)
        
        #label(1~6)
        self.label1 = QLabel(self)
        self.label1.move(10, 10)
        self.label1.resize(int(1280 * self.ratio_w), int(960 * self.ratio_h))

        self.label2 = QLabel(self)
        self.label2.move(int(1350 * self.ratio_w), int(20 * self.ratio_h))
        self.label2.resize(int(450 * self.ratio_w), int(450 * self.ratio_h))

        self.label3 = QLabel('Current formula  ', self)
        self.label3.move(int(1350 * self.ratio_w), int(500 * self.ratio_h))
        self.label4 = QLabel('None                     ', self)
        self.label4.move(int(1350 * self.ratio_w), int(550 * self.ratio_h))
        self.label5 = QLabel('Result : ', self)
        self.label5.move(int(1350 * self.ratio_w), int(800 * self.ratio_h))
        self.label6 = QLabel('INVAILD                  ', self)
        self.label6.move(int(1350 * self.ratio_w), int(850 * self.ratio_h))

        self.set_font()


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_images)
        self.timer.start(10)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def set_font(self):
        font = QFont('Arial', self.font_size)  # 폰트 설정
        # 모든 라벨에 폰트 설정을 적용합니다.
        for label in [self.label1, self.label2, self.label3, self.label4, self.label5, self.label6]:
            label.setFont(font)

            
    def update_images(self):
        # to calculate running time, save start time to start_time
        start_time = time.time()

        # read the frame from webcam
        _, frame = self.cap.read()

        # detect hand landmark
        hand_landmarker_result, annotated_image = self.hand_pose_estimation.get_hand_pose_result(frame, True)
        annotated_image = cv2.resize(annotated_image,(int(1280 * self.ratio_w), int(960 * self.ratio_h)))

        # show detection_result to visible
        cv2.putText(annotated_image, self.str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
        cv2.putText(annotated_image, self.str2, (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)

        # Load images from file or camera
        h, w, c = annotated_image.shape
        img1 = QImage(annotated_image.data, w, h, w * c, QImage.Format_RGB888)
        pixmap1 = QPixmap.fromImage(img1)

        # if detect hand, start HandPatternRecognition
        if hand_landmarker_result.handedness.__len__() == 1:
            # save point to HandPatternRecognition
            for i in range(0, self.points, 1):
                self.hprx[i] = hand_landmarker_result.hand_landmarks[0][i].x
                self.hpry[i] = hand_landmarker_result.hand_landmarks[0][i].y
                self.hprz[i] = hand_landmarker_result.hand_landmarks[0][i].z
            self.hpr.set_3d_position(self.hprx, self.hpry, self.hprz)


            # pick out mode pattern for avoiding scattering
            mode_pattern = self.hpr.check_switch_pattern()

            # status[0:stop, 1:write, 2:enter, 3:erase]
            if mode_pattern == 0:
                self.execute_flag = True
                if self.str != "Stop mode":
                    self.str = "Stop mode"

            # execute each status
            # writing action
            if self.execute_flag is True and mode_pattern == 1:
                # saving points save in x, y
                self.x_8.append(self.hprx[8] * self.frame_height)
                self.y_8.append(self.hpry[8] * self.frame_width)
                self.save_frames += 1
                if self.str != "writing mode":
                    self.str = "writing mode"
                self.execute_flag = True

                # list_flag up
                self.list_flag = True

            # enter action
            elif self.execute_flag is True and mode_pattern == 2:
                if self.list_flag is True:
                    # list to image
                    self.preprocessing.get_current_image(self.x_8, self.y_8)
                    self.preprocessing.get_current_resize()
                    self.save_frames = 0
                    self.x_8 = []
                    self.y_8 = []
                    if self.str != "enter mode":
                        self.str = "enter mode"
                    try:
                        self.str2 = f'counter: {self.preprocessing.result_counter}'
                    except Exception:
                        print("Error : fail to acesse preprocess")

                    # inferencing and make string
                    string_image = cv2.imread(f'./demo_test/Result/Result_{self.preprocessing.result_counter - 1}.jpg')
                    self.string_buf.append(f'{self.infer.get_inferencing_result(string_image, False)}')
                    self.str_buf = "".join(self.string_buf)
                    print(self.str_buf)
                    print(self.calc.eval_proc(self.str_buf))

                    self.execute_flag = False

                    # list_flag down
                    self.list_flag = False

                else:
                    print("List is empty. Please draw number or sign")
                    self.execute_flag = False

            # erase action
            elif self.execute_flag is True and mode_pattern == 3:
                if self.list_flag is True:
                    # erase list
                    self.x_8 = []
                    self.y_8 = []
                    self.save_frames = 0
                    if self.str != "erase list":
                        self.str = "erase list"
                    self.execute_flag = False

                    # list_flag down
                    self.list_flag = False

                else:

                    # erase picture or move index
                    if self.preprocessing.result_counter != 0:
                        self.preprocessing.result_counter -= 1
                        del self.string_buf[self.preprocessing.result_counter]
                        self.str_buf = "".join(self.string_buf)
                        print(self.str_buf)
                        print(self.calc.eval_proc(self.str_buf))

                    if self.str != "erase picture":
                        self.str = "erase picture"
                    self.str2 = f'counter: {self.preprocessing.result_counter}'

                    self.execute_flag = False

        if self.preprocessing.result_counter == 0:
            img3 = cv2.imread('./demo_test/intel_logo.png')
            convert_img = cv2.resize(img3,(int(450 * self.ratio_w),int(450 * self.ratio_h)))
            convert_img = cv2.cvtColor(convert_img,cv2.COLOR_BGR2RGB)
            h, w, c = convert_img.shape
            img2 = QImage(convert_img.data, w, h, w * c, QImage.Format_RGB888)
        else:
            show_img = cv2.imread(f'./demo_test/Result/Result_{self.preprocessing.result_counter-1}.jpg')
            show_new_img = cv2.resize(show_img,(int(450 * self.ratio_w), int(450 * self.ratio_h)))
            h, w, c = show_new_img.shape
            img2 = QImage(show_new_img.data, w, h, w * c, QImage.Format_RGB888)
        pixmap2 = QPixmap.fromImage(img2)

        # Update labels with new images
        self.label1.setPixmap(pixmap1)
        self.label2.setPixmap(pixmap2)

        # Update label with new text
        self.label4.setText(self.str_buf)
        if self.calc.eval_proc(self.str_buf) == 'INVALID':
            self.label6.setText(self.calc.eval_proc(self.str_buf))
        else:
            self.label6.setText(str(self.calc.eval_proc(self.str_buf)))

        #self.worker.callstring(self.str_buf)  # BluetoothWorker 클래스의 callstring 메소드 호출하여 str_buf 전달
        # show process time and fps
        process_time = time.time() - start_time
        FPS = 1 / process_time
        print(f"process_time = {process_time:.4f}s, FPS = {FPS:.2f}")
    
    def close_windows(self):
        self.cap.release()
        self.socket.close()
        cv2.destoryAllWindows()

main = QApplication(sys.argv)
main_rect = main.desktop().screenGeometry()
width, height = main_rect.width(), main_rect.height()
ex = App(width, height)
ex.close_windows
sys.exit(main.exec_())


'''
img = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
h, w, c = img.shape
q_img = QImage(img.data, w, h, w * c, QImage.Format_RGB888)
# QImage를 QPixmap으로 변환
pixmap = QPixmap.fromImage(q_img)
'''
