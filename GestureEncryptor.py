import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarksConnections
from mediapipe.tasks.python.vision.drawing_utils import draw_landmarks

from FileHandler import FileHandler
from GestureHandler import GestureHandler
from VideoStream import VideoStream

FRAMES_TIL_ACCEPT = 30


class GestureEncryptor:
    def __init__(
            self, filename: str, output: str,
            videoStream: VideoStream, gesture: GestureHandler,
            fileHandler: FileHandler, salt: str = "", encryptOrDecrypt=True):
        self.filename = filename
        self.output = output
        self.encryptOrDecrypt = encryptOrDecrypt
        self.fileHandler = fileHandler
        self.videoStreamer = videoStream
        self.gestureHandler = gesture
        self.salt = salt

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

                    if len(currentInputs) >= 15:
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

        password = "".join(currentInputs)

        if self.encryptOrDecrypt:
            data = self.encrypt(password)
        else:
            data = self.decrypt(password)

        assert data

        self.writeOutput(data)

    def encrypt(self, password):
        return self.fileHandler.encrypt(self.filename, password)

    def decrypt(self, password):
        return self.fileHandler.decrypt(self.filename, password, self.salt)

    def getRender(self, image, landmarks, gesture):
        draw_landmarks(image, landmarks, connections=HandLandmarksConnections.HAND_CONNECTIONS)
        image = cv2.putText(image, gesture, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        return image

    def writeOutput(self, data: bytes):
        try:
            f = open(self.output, "bx")
            try:
                f.write(data)
            finally:
                f.close()
        except FileExistsError:
            print("Error: Output " + self.output + " cannot already exist!")

