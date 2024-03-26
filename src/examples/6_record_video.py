import time
from threading import Thread
from typing import cast
from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()
keepRecording = True
tello.streamon()


frame_read = tello.get_frame_read()


def video_recorder():
    frame = cast(cv2.typing.MatLike, frame_read.frame)
    height, width, _ = frame.shape
    file_path = "video.mp4"
    fourcc = 0x00000021  # cv2.VideoWriter_fourcc(*"mp4v")
    fps = 30
    video = cv2.VideoWriter(file_path, fourcc, fps, (width, height), True)
    while keepRecording:
        print("Writing frame")
        video.write(frame)
        time.sleep(1 / 30)

    print("Finished recording")
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
