import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarksConnections
from mediapipe.tasks.python.vision.drawing_utils import draw_landmarks

from GestureHandler import GestureHandler
from VideoStream import VideoStream

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

while True:
    image, imageRGB = videoStreamer.getCapture()

    mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    gestureResults = gestureHandler.getGestures(mpImage)

    if gestureResults.hand_landmarks:
        draw_landmarks(image, gestureResults.hand_landmarks[0], connections=HandLandmarksConnections.HAND_CONNECTIONS)

    cv2.imshow("Image", image)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break