import logging
from services.tello_connector import TelloConnector

try:
    from tello_controller import TelloActionType, TelloControlState
except ModuleNotFoundError:
    from services.tello_controller import TelloActionType, TelloControlState


LOGGER = logging.getLogger(__name__)


class TelloCommandDispatcher:
    """
    A stateful class that dispatches commands to the Tello drone based on the control state.
    """

    speed_cm_s = 10
    "The speed of the Tello in cm/s. Default is 10 cm/s."

    def __init__(self, tello: TelloConnector):
        self.tello = tello
        self.tello.set_speed_cm_s(self.speed_cm_s)

    def _adjust_speed(self, delta: int) -> None:
        """
        Adjusts the speed of the Tello drone by the given delta.
        """
        self.speed_cm_s += delta
        self.tello.set_speed_cm_s(self.speed_cm_s)
        LOGGER.info(f"Speed adjusted to {self.speed_cm_s} cm/s")

    def increase_speed(self) -> None:
        """
        Increases the speed of the Tello drone by 10 cm/s.
        """
        self._adjust_speed(10)

    def decrease_speed(self) -> None:
        """
        Decreases the speed of the Tello drone by 10 cm/s.
        """
        self._adjust_speed(-10)

    def send_commands(self, control_state: TelloControlState):
        "Send the commands to the Tello based on the control state"

        self.tello.send_rc_control(
            control_state.right_velocity,
            control_state.forward_velocity,
            control_state.up_velocity,
            control_state.yaw_right_velocity,
        )

        # Process events
        for event in control_state.events:
            if event == TelloActionType.TAKEOFF:
                self.tello.take_off()
            elif event == TelloActionType.LAND:
                self.tello.land()
            elif event == TelloActionType.EMERGENCY_LAND:
                self.tello.emergency_stop()
            elif event == TelloActionType.INCREASE_SPEED_CM_S:
                self.increase_speed()
            elif event == TelloActionType.DECREASE_SPEED_CM_S:
                self.decrease_speed()
            elif event == TelloActionType.FLIP_FORWARD:
                self.tello.flip_forward()
            elif event == TelloActionType.FLIP_BACK:
                self.tello.flip_back()
            elif event == TelloActionType.FLIP_RIGHT:
                self.tello.flip_right()
            elif event == TelloActionType.FLIP_LEFT:
                self.tello.flip_left()
