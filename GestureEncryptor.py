import argparse

import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarksConnections
from mediapipe.tasks.python.vision.drawing_utils import draw_landmarks

from GestureHandler import GestureHandler
from VideoStream import VideoStream

FRAMES_TIL_ACCEPT = 30


class GestureEncryptor:
    def __init__(self, filename, videoStream, gesture, encryptOrDecrypt=True):
        self.filename = filename
        self.encryptOrDecrypt = encryptOrDecrypt
        self.videoStreamer = videoStream
        self.gestureHandler = gesture

    def start(self):
        currentInputs = []
        currentGesture = None

        frameDelay = 0

        while True:
            image, imageRGB = self.videoStreamer.getCapture()

            mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=imageRGB)

            gestureResults = self.gestureHandler.getGestures(mpImage)

            gestureType = gestureResults.gestures[0][0].category_name if len(gestureResults.gestures) > 0 else None
            if gestureType and gestureType != "None":
                if FRAMES_TIL_ACCEPT <= frameDelay:
                    currentInputs.append(gestureType)

                    frameDelay = 0
                    currentGesture = None

                if currentGesture == gestureType:
                    frameDelay += 1
                else:
                    currentGesture = gestureType
                    frameDelay = 0
            else:
                currentGesture = None
                frameDelay = 0

            if gestureResults.hand_landmarks:
                self.render(image, gestureResults.hand_landmarks[0], gestureType)

            if cv2.waitKey(1) & 0xff == ord("q"):
                break

    def render(self, image, landmarks, gesture):
        draw_landmarks(image, landmarks, connections=HandLandmarksConnections.HAND_CONNECTIONS)
        image = cv2.putText(image, gesture, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.imshow("Image", image)


parser = argparse.ArgumentParser(
    prog="Gesture Encryptor",
    description="Encrypts and decrypts files as .gesture by using hand gestures"
)

parser.add_argument("filename")
parser.add_argument("--encrypt", action="store_true")
parser.add_argument("--decrypt", action="store_true")

args = parser.parse_args()

filename = args.filename
encrypt = args.encrypt
decrypt = args.decrypt

if encrypt and decrypt:
    raise Exception("Can't both be encrypting and decrypting!")

vidCapture = cv2.VideoCapture(0)

videoStreamer = VideoStream(vidCapture)
gestureHandler = GestureHandler()

gestureEncryptor = GestureEncryptor(
    filename=filename,
    encryptOrDecrypt=True,
    videoStream=videoStreamer,
    gesture=gestureHandler)

gestureEncryptor.start()