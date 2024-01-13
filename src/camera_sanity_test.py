from djitellopy import Tello
import cv2


IMAGE_COMPRESSION = 4

# Create a Tello instance
tello = Tello()

# Connect to Tello
tello.connect()

tello.streamon()

try:
    while True:
        img = tello.get_frame_read().frame  #
        cv2.imshow("frame", img)
        cv2.waitKey(1)  #
except KeyboardInterrupt:
    exit(1)
finally:
    print("fin")
