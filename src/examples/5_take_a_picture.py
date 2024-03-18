import os
import cv2
import numpy as np
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

os.makedirs("../artifacts", exist_ok=True)

cv2.imwrite("../artifacts/picture.png", np.array(frame_read.frame))

tello.land()
