import argparse
import os.path

import cv2

from FileHandler import FileHandler
from GestureEncryptor import GestureEncryptor
from GestureHandler import GestureHandler
from VideoStream import VideoStream

parser = argparse.ArgumentParser(
    prog="Gesture Encryptor",
    description="Encrypts and decrypts files as .gesture files by using hand gestures."
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

assert not os.path.isfile(output)
assert os.path.isfile(filename)

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