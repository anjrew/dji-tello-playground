import os
import cv2
import numpy as np
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

# The folder where the images will be stored
artifact_folder_path = "../artifacts/images"

os.makedirs(artifact_folder_path, exist_ok=True)

cv2.imwrite(f"{artifact_folder_path}/picture.png", np.array(frame_read.frame))

tello.land()
