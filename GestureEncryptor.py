import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarksConnections
from mediapipe.tasks.python.vision.drawing_utils import draw_landmarks

from GestureHandler import GestureHandler
from VideoStream import VideoStream

vidCapture = cv2.VideoCapture(0)

videoStreamer = VideoStream(vidCapture)
gestureHandler = GestureHandler()

while True:
    image, imageRGB = videoStreamer.getCapture()

    mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    gestureResults = gestureHandler.getGestures(mpImage)

    if gestureResults.hand_landmarks:
        draw_landmarks(image, gestureResults.hand_landmarks[0], connections=HandLandmarksConnections.HAND_CONNECTIONS)

    cv2.imshow("Image", image)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break