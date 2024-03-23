import os
import sys
import time
import face_recognition
from djitellopy import Tello
import cv2


IMAGE_COMPRESSION = 4


script_path = os.path.abspath(sys.argv[0])
script_dir = os.path.dirname(script_path)
file_path = script_dir + "/face_to_track.jpeg"

raw_image = cv2.imread(file_path)

convert_color = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)

face_encodings = face_recognition.face_encodings(convert_color)


print("Starting flying in ...")
for i in range(5, 0, -1):
    print(i)
    time.sleep(1)


compressed_image = cv2.resize(
    frame,
    (
        int(frame_width / IMAGE_COMPRESSION),
        int(frame_height / IMAGE_COMPRESSION),
    ),
)
