from typing import List

try:
    from services.xbox_360_controller import XboxButtonKeys, Xbox360PyGameJoystick
    from tello_controller import TelloActionType, TelloControlState, TelloController
except ModuleNotFoundError:
    from services.xbox_360_controller import (
        XboxButtonKeys,
        Xbox360PyGameJoystick,
    )
    from services.tello_controller import (
        TelloActionType,
        TelloControlState,
        TelloController,
    )


class XboxTelloControlAdapter(TelloController):

    def __init__(self, controller: Xbox360PyGameJoystick):
        self.xbox_controller = controller

    def t(self, controller_axis_value: float) -> int:
        "Transform the controller axis value to the tello control value"
        return int(controller_axis_value * 100)

    def get_state(self) -> TelloControlState:
        controller_state = self.xbox_controller.get_state()

        pressed_buttons = controller_state.buttons.get_pressed_buttons()
        d_pad = controller_state.d_pad

        events: List[TelloActionType] = []
        if XboxButtonKeys.Y.name in pressed_buttons:
            events.append(TelloActionType.TAKEOFF)
        if XboxButtonKeys.A.name in pressed_buttons:
            events.append(TelloActionType.LAND)
        if XboxButtonKeys.B.name in pressed_buttons:
            events.append(TelloActionType.EMERGENCY_LAND)

        if d_pad.vertical_up == 1:
            events.append(TelloActionType.INCREASE_SPEED_CM_S)
        if d_pad.vertical_up == -1:
            events.append(TelloActionType.DECREASE_SPEED_CM_S)

        t = self.t

        return TelloControlState(
            forward_velocity=t(-controller_state.axes.left_stick.vertical),
            right_velocity=t(controller_state.axes.left_stick.horizontal),
            up_velocity=t(-controller_state.axes.right_stick.vertical),
            yaw_right_velocity=t(controller_state.axes.right_stick.horizontal),
            events=events,
        )
