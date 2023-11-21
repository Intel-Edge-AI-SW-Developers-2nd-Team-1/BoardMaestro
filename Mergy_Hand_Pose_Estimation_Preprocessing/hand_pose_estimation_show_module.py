import cv2
import numpy as np

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

class HandPoseEstimationShow:
    def __init__(self, points):
        # define output point and key point(wrist, <finger>_tip, <finger>_PIP, <finger>_MCP)
        self.position = [
            "0 - wrist",
            "1 - thumb_cmc", "2 - thumb_mcp", "3 - thumb_ip", "4 - thumb_tip",
            "5 - index_finger_mcp", "6 - index_finger_pip", "7 - index_finger_dip", "8 - index_finger_tip",
            "9 - middle_finger_mcp", "10 - middle_finger_pip", "11 - middle_finger_dip", "12 - middle_finger_tip",
            "13 - ring_finger_mcp", "14 - ring_finger_pip", "15 - ring_finger_dip", "16 - ring_finger_tip",
            "17 - pinky_finger_mcp", "18 - pinky_finger_pip", "19 - pinky_finger_dip", "20 - pinky_finger_tip"
        ]

        self.points = points

        # define values for draw_landmarks_on_image
        self.MARGIN = 10  # pixels
        self.FONT_SIZE = 1
        self.FONT_THICKNESS = 1
        self.HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green

    def draw_landmarks_on_image(self, rgb_image, detection_result):
        '''to visualize the hand landmark detection results'''
        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness
        annotated_image = np.copy(rgb_image)

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
        return annotated_image

    def show_list(self, save_frames, x, y, z):
        '''Show List Function'''
        if save_frames == 0:
            print("List is empty")
            return 0
        # show each saved frame information
        for row in range(0, save_frames + 1, 1):
            print(f"Frame{row}")
            # show each positions, x,y,z value
            for col in range(0, self.points, 1):
                print(f"{self.position[col]} x={x[row][col]}, y={y[row][col]}, z={z[row][col]}")