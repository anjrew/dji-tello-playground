import logging
import time
from djitellopy import Tello, BackgroundFrameRead

LOGGER = logging.getLogger(__name__)


class TelloConnector:
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
            LOGGER.info(f"Connecting in {second}")
            time.sleep(1)

        LOGGER.debug("Connected to Tello")

    def streamoff(self):
        self.tello.streamoff()
        LOGGER.debug("Video stream off")

    def streamon(self):
        LOGGER.info("Restarting video stream")
        time.sleep(1)
        self.streamoff()
        time.sleep(1)
        self.tello.streamon()
        LOGGER.info("Video stream on")

    def get_frame_read(self) -> BackgroundFrameRead:
        LOGGER.debug("Getting frame read")
        return self.tello.get_frame_read()

    def take_off(self):
        LOGGER.info("Taking off...")
        self.tello.takeoff()

    def land(self):
        LOGGER.info("Landing...")
        self.tello.land()

    def send_rc_control(
        self,
        left_right_velocity: int,
        for_back_velocity: int,
        up_down_velocity: int,
        yaw_velocity: int,
    ):
        LOGGER.debug(
            f"Sending RC control: {left_right_velocity}, {for_back_velocity}, {up_down_velocity}, {yaw_velocity}"
        )
        self.tello.send_rc_control(
            left_right_velocity, for_back_velocity, up_down_velocity, yaw_velocity
        )

    def emergency_stop(self) -> None:
        self.tello.emergency()

    def set_speed_cm_s(self, cm_s: int) -> None:
        """Set speed to x cm/s.
        Arguments:
            x: 10-100
        """
        self.tello.set_speed(cm_s)

    def end(self) -> None:
        LOGGER.debug("Ending Tello service")
        self.tello.end()

    def flip_forward(self) -> None:
        self.tello.flip_forward()

    def flip_back(self) -> None:
        self.tello.flip_back()

    def flip_left(self) -> None:
        self.tello.flip_left()

    def flip_right(self) -> None:
        self.tello.flip_right()
