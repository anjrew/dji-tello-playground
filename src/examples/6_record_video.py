import time
from threading import Thread
from djitellopy import Tello
import cv2

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()


def video_recorder():

    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter(
        "video.avi", cv2.VideoWriter_fourcc(*"XVID"), 30, (width, height)
    )

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()


# Run the recorder in a separate thread, otherwise blocking options would prevent frames from getting added to the video
recorder = Thread(target=video_recorder)
recorder.start()

tello.takeoff()
tello.move_up(100)
tello.rotate_counter_clockwise(360)
tello.land()

keepRecording = False
recorder.join()
