import logging
import time
from djitellopy import Tello, BackgroundFrameRead


class TelloService:
    """
    A class that provides a high-level interface for controlling the Tello drone.

    Attributes:
        tello: An instance of the Tello class for low-level communication with the drone.

    Methods:
        connect: Establishes a connection with the Tello drone.
        set_speed: Sets the speed of the Tello drone.
        streamoff: Stops the video stream from the Tello drone.
        streamon: Starts the video stream from the Tello drone.
        get_frame_read: Returns an instance of BackgroundFrameRead for reading frames from the video stream.
        takeoff: Initiates the takeoff sequence of the Tello drone.
        land: Initiates the landing sequence of the Tello drone.
        send_rc_control: Sends RC control commands to the Tello drone for manual control.
        end: Closes the connection with the Tello drone.
    """

    def __init__(self, tello: Tello):
        self.tello = tello

    def connect(self):
        self.tello.connect()
        for second in range(3, 0, -1):
            logging.info(f"Connecting in {second}")
            time.sleep(1)

        # In case streaming is on. This happens when we quit this program with out the escape key.
        self.tello.streamoff()

        self.tello.streamon()

    def set_speed(self, speed):
        self.tello.set_speed(speed)

    def streamoff(self):
        self.tello.streamoff()

    def streamon(self):
        logging.info("Restarting video stream")
        time.sleep(1)
        self.streamoff()
        time.sleep(1)
        self.tello.streamon()
        logging.info("Video stream on")

    def get_frame_read(self) -> BackgroundFrameRead:
        return self.tello.get_frame_read()

    def takeoff(self):
        logging.info("Taking off...")
        self.tello.takeoff()

    def land(self):
        logging.info("Landing...")
        self.tello.land()

    def send_rc_control(
        self,
        left_right_velocity: int,
        for_back_velocity: int,
        up_down_velocity: int,
        yaw_velocity: int,
    ):
        self.tello.send_rc_control(
            left_right_velocity, for_back_velocity, up_down_velocity, yaw_velocity
        )

    def end(self):
        self.tello.end()
