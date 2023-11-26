import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


class HandPoseEstimation:
    def __init__(self, model_path):
        '''
        init to use hand pose estimation
        :model_path: model_path must include .xml, .bin, .task, .json
        '''
        # define values for draw_landmarks_on_image
        self.MARGIN = 10  # pixels
        self.FONT_SIZE = 1
        self.FONT_THICKNESS = 1
        self.HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green

        # define HandLandmarkers elements
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        # set option
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path+'/hand_landmarker.task', delegate=BaseOptions.Delegate.CPU),
            running_mode=VisionRunningMode.IMAGE)

        # The landmarker is initialized
        self.landmarker = HandLandmarker.create_from_options(options)

    def get_hand_pose_result(self, frame, annotated_image_flag):
        '''
        Find the hand landmark detection results and visualize

        input : inference image and show flag
        output : detection result and annotated image
        '''
        # make frame to mediapipe image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
                        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        detection_result = self.landmarker.detect(mp_image)

        if annotated_image_flag is False:
            return detection_result

        else:
            hand_landmarks_list = detection_result.hand_landmarks
            handedness_list = detection_result.handedness
            annotated_image = np.copy(mp_image.numpy_view())

            # Loop through the detected hands to visualize.
            for idx in range(len(hand_landmarks_list)):
                hand_landmarks = hand_landmarks_list[idx]
                handedness = handedness_list[idx]

                # Draw the hand landmarks.
                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in
                    hand_landmarks])
                solutions.drawing_utils.draw_landmarks(
                    annotated_image,
                    hand_landmarks_proto,
                    solutions.hands.HAND_CONNECTIONS,
                    solutions.drawing_styles.get_default_hand_landmarks_style(),
                    solutions.drawing_styles.get_default_hand_connections_style())

                # Get the top left corner of the detected hand's bounding box.
                height, width, _ = annotated_image.shape
                x_coordinates = [landmark.x for landmark in hand_landmarks]
                y_coordinates = [landmark.y for landmark in hand_landmarks]
                text_x = int(min(x_coordinates) * width)
                text_y = int(min(y_coordinates) * height) - self.MARGIN

                # Draw handedness (left or right hand) on the image.
                cv2.putText(annotated_image, f"{handedness[0].category_name}",
                            (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                            self.FONT_SIZE, self.HANDEDNESS_TEXT_COLOR, self.FONT_THICKNESS, cv2.LINE_AA)

            # detect hand landmark and draw annotated_image
            return detection_result, annotated_image
