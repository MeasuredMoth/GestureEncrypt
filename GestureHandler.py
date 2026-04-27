import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import GestureRecognizerOptions, GestureRecognizer


class GestureHandler:
    gestureRecognizerTaskPath = "gesture_recognizer.task"

    VisionRunningMode = mp.tasks.vision.RunningMode

    def __init__(self):
        gestureOptions = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.gestureRecognizerTaskPath),
            running_mode=self.VisionRunningMode.IMAGE)

        self.gestureRecognizer = GestureRecognizer.create_from_options(gestureOptions)

    def getGestures(self, image: mp.Image):
        return self.gestureRecognizer.recognize(image)

    def __del__(self):
        self.gestureRecognizer.close()