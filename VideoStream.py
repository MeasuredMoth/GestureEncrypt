import cv2
from cv2 import VideoCapture


class VideoStream:

    def __init__(self, videoCapture: VideoCapture):
        self.videoCapture = videoCapture

    def getCapture(self):
        success, image = self.videoCapture.read()

        assert success, "Unable to read capture info!"

        image = cv2.flip(image, 1)
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image, imageRGB

    def __del__(self):
        self.videoCapture.release()
        self.videoCapture = None
