import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import GestureRecognizerOptions, HandLandmarkerOptions, HandLandmarker, \
    GestureRecognizer


class GestureHandler:
    landMarkerTaskPath = "hand_landmarker.task"
    gestureRecognizerTaskPath = "gesture_recognizer.task"

    VisionRunningMode = mp.tasks.vision.RunningMode

    def __init__(self):
        gestureOptions = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.gestureRecognizerTaskPath),
            running_mode=self.VisionRunningMode.IMAGE)

        landMarkerOptions = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.landMarkerTaskPath),
            running_mode=self.VisionRunningMode.IMAGE)

        self.landmarkRecognizer = HandLandmarker.create_from_options(landMarkerOptions)
        self.gestureRecognizer = GestureRecognizer.create_from_options(gestureOptions)

    def getLandmarks(self, image: mp.Image):
        return self.landmarkRecognizer.detect(image)

    def getGestures(self, image: mp.Image):
        return self.gestureRecognizer.recognize(image)

    def __del__(self):
        self.landmarkRecognizer.close()
        self.gestureRecognizer.close()