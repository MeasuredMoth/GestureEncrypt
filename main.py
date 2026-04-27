import argparse
import os.path

import cv2

import cv2

from FileHandler import FileHandler
from GestureEncryptor import GestureEncryptor
from GestureHandler import GestureHandler
from VideoStream import VideoStream

parser = argparse.ArgumentParser(
    prog="Gesture Encryptor",
    description="Encrypts and decrypts files as .gesture files by using hand gestures."
)

assert os.path.isfile("gesture_recognizer.task"), "No model task detected. Must be named \"gesture_recognizer.task\""

parser.add_argument("filename")
parser.add_argument("--output")
parser.add_argument("--decrypt", action="store_true")
parser.add_argument("--salt")

args = parser.parse_args()

filename = args.filename
output = args.output
decrypt = args.decrypt
salt = args.salt

if decrypt:
    assert ".gesture" in filename
    assert salt
else:
    assert ".gesture" in output

assert not os.path.isfile(output), f"{output} cannot already exist for output!"
assert os.path.isfile(filename), f"{filename} was not found as input"

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
    fileHandler=fileHandler,
    salt=salt)

gestureEncryptor.start()