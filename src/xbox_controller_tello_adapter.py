from typing import List

from joysticks.pygame_connector import PyGameConnector
from joysticks.xbox_controller import XboxPyGameController

from services.tello_controller import (
    TelloActionType,
    TelloControlState,
    TelloController,
)
from test_utils import run_adapter_test


class XboxTelloControlAdapter(TelloController):

    def __init__(self, controller: XboxPyGameController):
        self.xbox_controller = controller

    def t(self, controller_axis_value: float) -> int:
        "Transform the controller axis value to the tello control value"
        return int(controller_axis_value * 100)

    def get_state(self) -> TelloControlState:
        controller_state = self.xbox_controller.get_state()

        pressed_buttons = controller_state.buttons.get_pressed_buttons()
        d_pad = controller_state.d_pad

        events: List[TelloActionType] = []
        if "Y" in pressed_buttons:
            events.append(TelloActionType.TAKEOFF)
        if "A" in pressed_buttons:
            events.append(TelloActionType.LAND)
        if "B" in pressed_buttons:
            events.append(TelloActionType.EMERGENCY_LAND)

        if d_pad.vertical_up == 1:
            events.append(TelloActionType.FLIP_FORWARD)
        if d_pad.vertical_up == -1:
            events.append(TelloActionType.FLIP_BACK)
        if d_pad.horizontal_right == -1:
            events.append(TelloActionType.FLIP_LEFT)
        if d_pad.horizontal_right == 1:
            events.append(TelloActionType.FLIP_RIGHT)

        if "RB" in pressed_buttons:
            events.append(TelloActionType.INCREASE_SPEED_CM_S)
        if "LB" in pressed_buttons:
            events.append(TelloActionType.DECREASE_SPEED_CM_S)

        t = self.t

        return TelloControlState(
            forward_velocity=t(-controller_state.axes.left_stick.vertical_down),
            right_velocity=t(controller_state.axes.left_stick.horizontal_right),
            up_velocity=t(-controller_state.axes.right_stick.vertical_down),
            yaw_right_velocity=t(controller_state.axes.right_stick.horizontal_right),
            events=events,
        )


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    controller = XboxPyGameController(pygame_connector)
    tello_control = XboxTelloControlAdapter(controller)
    run_adapter_test(tello_control)
