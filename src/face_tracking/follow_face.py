"This Module is used to track a face in the frame and follow it with the drone."

import os
import sys
import time
import face_recognition
from djitellopy import Tello
import cv2


IMAGE_COMPRESSION = 4

# Create a Tello instance
tello = Tello()

# Connect to Tello
tello.connect()

tello.streamon()

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


while True:
    time.sleep(0.200)

    cam_output = tello.get_frame_read()

    frame = cam_output.frame

    if frame is not None:
        # Get the image height and width
        frame_height, frame_width, _ = frame.shape

        compressed_image = cv2.resize(
            frame,
            (
                int(frame_width / IMAGE_COMPRESSION),
                int(frame_height / IMAGE_COMPRESSION),
            ),
        )
