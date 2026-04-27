# Gesture Encrypt
Gesture Encrypt is a Python based tool for encrypting and decrypting files using gesture recognition supported by Google's 
MediaPipe, and OpenCV. 

**Be Aware:** This project exists sole as an education tool, and is a poor replacement for more secure methods of encrypting 
files. While fun, don't try using this for actually sensitive files as it doesn't generate anything more secure than a password 
you can make yourself.
# Getting Started
## Dependencies
- [Python](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide)
- MediaPipe supported model (Can be found from above link)
## Running
1. The project is intended to be ran in command prompt. The basic format is: `GestureEncrypt file.txt --output file.gesture`. 
To decrypt the format would be `GestureEncrypt file.gesture --output file.txt`. Files encrypted must be of extension `.gesture`, 
and decrypted files must have their original extension set manually.
2. Once ran a live video of your camera capture should appear. Any gestures recognized by the provided model will be 
recorded after a short delay as part of the gesture password. See your model's support gestures for information on that.
3. Press q when you have created a sufficiently long gesture password, or if the password would
be too long to continue adding more.
4. If successful the new file should be encrypted or decrypted, under a salted password including the gestures recorded.
# License
This project is licensed under the [MIT License](https://mit-license.org/). For more information see the attached link.