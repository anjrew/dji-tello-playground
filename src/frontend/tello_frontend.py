from dataclasses import dataclass, field
import math
import cv2
from tello_service import TelloService
from tello_controller import Controller, TelloActionType, TelloControlEvent


@dataclass
class VehicleState:
    left_right_velocity: float = 0
    forward_backward_velocity: float = 0
    up_down_velocity: float = 0
    yaw_velocity: float = 0


@dataclass
class FrontEndState:
    control: VehicleState = field(default_factory=VehicleState)
    send_rc_control: bool = False
    speed_factor: float = 10


class FrontEnd:
    def __init__(self, controller: Controller, tello_service: TelloService):
        self.controller = controller
        self.tello_service = tello_service
        self.state = FrontEndState()

    def run(self, max_iterations=math.inf):
        self.tello_service.connect()
        self.tello_service.streamon()

        frame_read = self.tello_service.get_frame_read()
        iteration = 0
        while iteration < max_iterations:
            action = self.controller.get_action()
            if action:
                self._update_tello(action)

            if frame_read.stopped:
                frame_read.stop()
                break

            frame = frame_read.frame
            if frame is not None:
                cv2.imshow("Tello Stream", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break
            iteration += 1

        self.tello_service.end()

    def takeoff(self):
        self.tello_service.takeoff()
        self.state.send_rc_control = True

    def land(self):
        self.tello_service.land()
        self.state.send_rc_control = False

    def _update_tello(self, event: TelloControlEvent):
        if event.action == TelloActionType.TAKEOFF:
            self.takeoff()
            return
        if not self.state.send_rc_control:
            return
        if event.action == TelloActionType.LAND:
            self.land()
            return

        self._update_control_state(event)
        control_state = self.state.control

        self.tello_service.send_rc_control(
            round(control_state.left_right_velocity * self.state.speed_factor),
            round(control_state.forward_backward_velocity * self.state.speed_factor),
            round(control_state.up_down_velocity * self.state.speed_factor),
            round(control_state.yaw_velocity * self.state.speed_factor),
        )

    def _apply_speed_factor(self, intensity: float) -> int:
        """Apply a speed factor to an intensity value between 1 and 0

        Args:
            intensity (int): A value between 1 and 0

        Returns:
            int: the speed to send to the Tello
        """
        return round(intensity * self.state.speed_factor)

    def _update_control_state(self, event: TelloControlEvent) -> None:
        control_state = self.state.control
        if event.action == TelloActionType.SET_LEFT_VELOCITY:
            control_state.left_right_velocity = -event.intensity
        elif event.action == TelloActionType.SET_RIGHT_VELOCITY:
            control_state.left_right_velocity = event.intensity
        elif event.action == TelloActionType.SET_FORWARD_VELOCITY:
            control_state.forward_backward_velocity = event.intensity
        elif event.action == TelloActionType.SET_BACKWARD_VELOCITY:
            control_state.forward_backward_velocity = -event.intensity
        elif event.action == TelloActionType.SET_UP_VELOCITY:
            control_state.up_down_velocity = event.intensity
        elif event.action == TelloActionType.SET_DOWN_VELOCITY:
            control_state.up_down_velocity = -event.intensity
        elif event.action == TelloActionType.SET_YAW_CLOCKWISE_VELOCITY:
            control_state.yaw_velocity = event.intensity
        elif event.action == TelloActionType.SET_YAW_COUNTER_CLOCKWISE_VELOCITY:
            control_state.yaw_velocity = event.intensity
        else:
            raise ValueError(f"Unknown Tello action: {event.action}")