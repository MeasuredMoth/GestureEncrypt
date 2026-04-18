import argparse

import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarksConnections
from mediapipe.tasks.python.vision.drawing_utils import draw_landmarks

from FileHandler import FileHandler
from GestureHandler import GestureHandler
from VideoStream import VideoStream

FRAMES_TIL_ACCEPT = 30


class GestureEncryptor:
    def __init__(self, filename, output, videoStream, gesture, fileHandler, encryptOrDecrypt=True):
        self.filename = filename
        self.output = output
        self.encryptOrDecrypt = encryptOrDecrypt
        self.fileHandler = fileHandler
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
                    print(f"Added {gestureType} to inputs, now is {currentInputs}")
                    if len(currentInputs) >= 3:
                        break

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
                image = self.getRender(image, gestureResults.hand_landmarks[0], gestureType)

            cv2.imshow("Image", image)

            if cv2.waitKey(1) & 0xff == ord("q"):
                break

        assert currentInputs, "Cannot have an empty set of inputs!"

        input = "".join(currentInputs)

        if self.encryptOrDecrypt:
            data = self.encrypt(input=input)
            assert data
        else:
            data = self.decrypt(input=input)
            assert data

        with open(self.output, "wb") as f:
            f.write(data)
            f.close()

    def encrypt(self, input):
        return self.fileHandler.encrypt(self.filename, input)

    def decrypt(self, input):
        return self.fileHandler.decrypt(self.filename, input)

    def getRender(self, image, landmarks, gesture):
        draw_landmarks(image, landmarks, connections=HandLandmarksConnections.HAND_CONNECTIONS)
        image = cv2.putText(image, gesture, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        return image

parser = argparse.ArgumentParser(
    prog="Gesture Encryptor",
    description="Encrypts and decrypts files as .gesture by using hand gestures"
)

parser.add_argument("filename")
parser.add_argument("--output")
parser.add_argument("--decrypt", action="store_true")

args = parser.parse_args()

filename = args.filename
output = args.output
decrypt = args.decrypt

if decrypt:
    assert ".gesture" in filename
else:
    assert ".gesture" in output

vidCapture = cv2.VideoCapture(0)

videoStreamer = VideoStream(vidCapture)
gestureHandler = GestureHandler()
fileHandler = FileHandler()

gestureEncryptor = GestureEncryptor(
    filename=filename,
    output=output,
    encryptOrDecrypt=not decrypt,
    videoStream=videoStreamer,
    gesture=gestureHandler,
    fileHandler=fileHandler)

gestureEncryptor.start()
