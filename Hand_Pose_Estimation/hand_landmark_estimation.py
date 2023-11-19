import cv2
import numpy as np
import time

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

# define HandLandmarkers elements
model_path = 'C:\pywork\hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

'''
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    #Create a hand landmarker instance with the live stream mode:
    print('hand landmarker result: {}'.format(result))
'''

# define values for draw_landmarks_on_image
MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

def draw_landmarks_on_image(rgb_image, detection_result):
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
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
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
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)
    return annotated_image

# set option
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path, delegate=BaseOptions.Delegate.CPU),
    running_mode=VisionRunningMode.IMAGE)

# The landmarker is initialized
landmarker = HandLandmarker.create_from_options(options)

# define output point and key point(wrist, <finger>_tip, <finger>_PIP, <finger>_MCP)
position = [
    "0 - wrist",
    "1 - thumb_cmc", "2 - thumb_mcp", "3 - thumb_ip", "4 - thumb_tip",
    "5 - index_finger_mcp", "6 - index_finger_pip", "7 - index_finger_dip", "8 - index_finger_tip",
    "9 - middle_finger_mcp", "10 - middle_finger_pip", "11 - middle_finger_dip", "12 - middle_finger_tip",
    "13 - ring_finger_mcp", "14 - ring_finger_pip", "15 - ring_finger_dip", "16 - ring_finger_tip",
    "17 - pinky_finger_mcp", "18 - pinky_finger_pip", "19 - pinky_finger_dip", "20 - pinky_finger_tip"
]

# define x,y,z for saving key point
points = 21
x=[]
y=[]
z=[]

# define flags
written_flag = False

# define save_frames
save_frames = 0

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
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB,
                        data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    '''
    # Send live image data to perform hand landmarks detection.
    # The results are accessible via the `result_callback` provided in
    # the `HandLandmarkerOptions` object.
    # The hand landmarker must be created with the live stream mode.
    landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)
    '''
    hand_landmarker_result = landmarker.detect(mp_image)

    # show detection_result to visible
    annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), hand_landmarker_result)
    cv2.imshow("Result", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    # save key point at list if flag is True
    if written_flag == True:
        x.append([None] * points)
        y.append([None] * points)
        z.append([None] * points)
        for i in range(0,points,1):
            x[save_frames][i] = hand_landmarker_result.hand_landmarks[0][i].x
            y[save_frames][i] = hand_landmarker_result.hand_landmarks[0][i].y
            z[save_frames][i] = hand_landmarker_result.hand_landmarks[0][i].z
        save_frames += 1

    # show process time and fps
    process_time = time.time() - start_time
    FPS = 1 / process_time
    print(f"process_time = {process_time:.4f}s, FPS = {FPS:.2f}")

    # if pressed 'q', end capture
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        written_flag = not written_flag
        print(written_flag)

# show list
for row in range(0,save_frames,1):
    print(f"Frame{row}")
    for col in range(0,points,1):
        print(f"{position[col]} x={x[row][col]}, y={z[row][col]}, z={z[row][col]}")