import argparse

import cv2

from FileHandler import FileHandler
from GestureEncryptor import GestureEncryptor
from GestureHandler import GestureHandler
from VideoStream import VideoStream

parser = argparse.ArgumentParser(
    prog="Gesture Encryptor",
    description="Encrypts and decrypts files as .gesture by using hand gestures"
)

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