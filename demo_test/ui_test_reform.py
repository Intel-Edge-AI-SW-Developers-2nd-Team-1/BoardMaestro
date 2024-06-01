from concurrent.futures.thread import _worker
import cv2
import time
import numpy as np
import threading
from collections import namedtuple
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QFont

from tools import mediapipe_utils as mpu
from tools.FPS import FPS, now
from hand_pose_estimation.hand_pose_estimation_module import HandPoseEstimation
from hand_pose_estimation.hand_tracker_module import HandTracker
from hand_pattern_recognition.hand_pattern_recognition_module import HandPatternRecognition
from ai_modeling.image_inferencing_module import ImageInferencing
from image_preprocessing.preprocessing_module import Preprocessing
from expression_calculating.calculator_module import Calculator

class App(QWidget):
    def __init__(self, w, h):
        super().__init__()
        self.title = 'Hand Draw Formula'
        self.left = 10
        self.top = 50
        self.width = w
        self.height = h

        self.cap = cv2.VideoCapture(0)

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
        model_path = 'ai_modeling/model'
        #self.hpe = HandPoseEstimation(model_path)
        self.ht = HandTracker( input_src='0',
                               pd_device='CPU',
                               pd_score_thresh=0.5, pd_nms_thresh=0.3,
                               use_lm=True,
                               lm_device='CPU',
                               lm_score_threshold=0.3,
                               use_gesture=False,
                               crop=True)
 
        self.fps = FPS(mean_nb_frames=30)
        
        self.nb_pd_inferences = 0
        self.nb_lm_inferences = 0
        self.glob_pd_rtrip_time = 0
        self.glob_lm_rtrip_time = 0

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

        # str save list
        self.str_buf = ""
        self.str = ""
        self.str2 = f'counter: {self.preprocessing.result_counter}'

        # read the frame from webcam and define
        #_, frame = self.cap.read()
        #self.frame_width = frame.shape[0]
        #self.frame_height = frame.shape[1]

    
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
        self.timer.start(5)

        # Print some stats
        #print(f"# palm detection inferences : {nb_pd_inferences}")
        #print(f"# hand landmark inferences  : {nb_lm_inferences}")
        #print(f"Palm detection round trip   : {glob_pd_rtrip_time/nb_pd_inferences*1000:.1f} ms")
        #print(f"Hand landmark round trip    : {glob_lm_rtrip_time/nb_lm_inferences*1000:.1f} ms")    
        
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
        #_, frame = self.cap.read()
        
        self.fps.update()

        ret, frame = self.cap.read()
        if not ret:
            print("[GUI] Could Not read frame...")
            self.timer.stop()
            return
        
        # detect hand landmark
        #hand_landmarker_result, annotated_image = self.hpe.get_hand_pose_result(frame, True)
 
        frame_nn = frame.copy()

        self.height, self.width = frame.shape[:2]
        #if self.ht.crop:
        self.ht.frame_size = min(self.height, self.width)
        dx = (self.width - self.ht.frame_size) // 2
        dy = (self.height - self.ht.frame_size) // 2
        resized_frame = frame[dy:dy+self.ht.frame_size, dx:dx+self.ht.frame_size]
        #else:
        #    self.ht.frame_size = max(self.height, self.width)
        #    pad_h = int((self.ht.frame_size - self.height) / 2)
        #    pad_w = int((self.ht.frame_size - self.width) / 2)
        #    frame = cv2.copyMakeBorder(frame, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_CONSTANT)

        # Resize image to NN square input shape
        frame_nn = cv2.resize(resized_frame, (self.ht.pd_w, self.ht.pd_h), interpolation=cv2.INTER_AREA)
        
        # Transpose hxwx3 -> 1x3xhxw
        frame_nn = np.transpose(frame_nn, (2,0,1))[None,]
        annotated_frame = resized_frame.copy()

        # Get palm detection
        self.pd_rtrip_time = now()
        inference = self.ht.pd_exec_net([frame_nn])
        self.glob_pd_rtrip_time += now() - self.pd_rtrip_time
        self.ht.pd_postprocess(inference)
        self.ht.pd_render(annotated_frame)
        self.nb_pd_inferences += 1
 
        self.handedness = 0

        # Hand landmarks
        for i, r in enumerate(self.ht.regions):
            frame_nn = mpu.warp_rect_img(r.rect_points, resized_frame, self.ht.lm_w, self.ht.lm_h)
            # Transpose hxwx3 -> 1x3xhxw
            frame_nn = np.transpose(frame_nn, (2,0,1))[None,]
            # Get hand landmarks
            lm_rtrip_time = now()
            inference = self.ht.lm_exec_net([frame_nn])
            self.glob_lm_rtrip_time += now() - lm_rtrip_time
            self.nb_lm_inferences += 1
            self.ht.lm_postprocess(r, inference)
            self.ht.lm_render(annotated_frame, r)
            if r.lm_score > self.ht.lm_score_threshold:
                self.handedness += 1

                #print(f"[HandPoseEstm] Landmarks: {r.landmarks}")

        #print(f"[HandPoseEstm] lm_pass_count: {self.lm_pass_count}")

        #if not self.ht.crop:
            #annotated_frame = annotated_frame[pad_h:pad_h+self.height, pad_w:pad_w+self.width]

        #cv2.imshow("video", annotated_frame)

        # if detect hand, start HandPatternRecognition
        if self.handedness > 0:
            # save point to HandPatternRecognition
            for i, r in enumerate(self.ht.regions):
                src = np.array([(0, 0), (1, 0), (1, 1)], dtype=np.float32)
                dst = np.array([ (x, y) for x,y in r.rect_points[1:]], dtype=np.float32)
                mat = cv2.getAffineTransform(src, dst)
                lm_xy = np.expand_dims(np.array([(l[0], l[1]) for l in r.landmarks]), axis=0)
                lm_xy = np.squeeze(cv2.transform(lm_xy, mat)).astype(np.int32)
                #print(f"[HandPtrnRecog] lm_xyz: {lm_xyz}")
                #lm_xyz = np.squeeze(cv2.transform(lm_xyz, mat)).astype(np.float32)
                for j in range(self.points):
                    self.hprx[j], self.hpry[j] = (lm_xy[j][0] + 1) / self.width, (lm_xy[j][1] + 1) / self.height
            #print(f"[HandPtrnRecog] hprx: {self.hprx}")
            #print(f"[HandPtrnRecog] hpry: {self.hpry}")
            #print(f"[HandPtrnRecog] hprz: {self.hprz}")
            
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
                self.x_8.append(self.hprx[8] * self.width)
                self.y_8.append(self.hpry[8] * self.height)
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
                        print("Error : fail to access preprocess")

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

        
        # Load images from file or camera
        annotated_frame = cv2.resize(annotated_frame,(int(1280 * self.ratio_w), int(960 * self.ratio_h)))
        self.fps.display(annotated_frame, orig=(int((1280 * 0.72) * self.ratio_w), 50), color=(240,180,100))
        
        # show detection_result to visible
        cv2.putText(annotated_frame, self.str, (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)
        cv2.putText(annotated_frame, self.str2, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)

        h, w, c = annotated_frame.shape
        img1 = QImage(annotated_frame.data, w, h, w * c, QImage.Format_BGR888)
        pixmap1 = QPixmap.fromImage(img1)
        
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
        #process_time = time.time() - start_time
        #FPS = 1 / process_time
        #print(f"process_time = {process_time:.4f}s, FPS = {FPS:.2f}")
     
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
             self.timer.stop()
             return
        elif key == 32:
            # Pause on space bar
            cv2.waitKey(0)
        elif key == ord('1'):
            self.ht.show_pd_box = not self.ht.show_pd_box
        elif key == ord('2'):
            self.ht.show_pd_kps = not self.ht.show_pd_kps
        elif key == ord('3'):
            self.ht.show_rot_rect = not self.ht.show_rot_rect
        elif key == ord('4'):
            self.ht.show_landmarks = not self.ht.show_landmarks
        elif key == ord('5'):
            self.ht.show_handedness = not self.ht.show_handedness
        elif key == ord('6'):
            self.ht.show_scores = not self.ht.show_scores
        elif key == ord('7'):
            self.ht.show_gesture = not self.ht.show_gesture

    def close_windows(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
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
