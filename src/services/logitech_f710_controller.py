from dataclasses import asdict, dataclass, fields
import time
import logging
from typing import List

try:
    from pygame_connector import PyGameConnector
except ModuleNotFoundError:
    from services.pygame_connector import PyGameConnector

LOGGER = logging.getLogger(__name__)

from enum import Enum


class DPadKeys(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class AxisKeys(Enum):
    LEFT_STICK_HORIZONTAL = 0
    LEFT_STICK_VERTICAL = 1
    RIGHT_STICK_HORIZONTAL = 2
    RIGHT_STICK_VERTICAL = 3


@dataclass
class StickState:
    horizontal: float
    vertical: float


@dataclass
class ControllerAxesState:
    left_stick: StickState
    right_stick: StickState


class ButtonKeys(Enum):
    A = 1
    B = 2
    X = 0
    Y = 3
    LB = 4
    RB = 5
    Back = 8
    Start = 9
    LeftTrigger = 6
    RightTrigger = 7
    LEFT_STICK = 10
    RIGHT_STICK = 11


@dataclass
class ControllerButtonPressedState:
    A: bool
    B: bool
    X: bool
    Y: bool
    LB: bool
    RB: bool
    Back: bool
    Start: bool
    LEFT_STICK: bool
    RIGHT_STICK: bool
    Left_trigger: bool
    RightTrigger: bool

    def get_pressed_buttons(self) -> List[str]:
        return [field.name for field in fields(self) if getattr(self, field.name)]


@dataclass
class ControllerDPadState:
    horizontal_right: int
    """If positive, the D-pad is pressed right, if negative, the D-pad is pressed left. If 0, the D-pad is not pressed"""
    vertical_up: int
    """If positive, the D-pad is pressed up, if negative, the D-pad is pressed down. If 0, the D-pad is not pressed"""

    def get_active(self) -> List[str]:
        return [field.name for field in fields(self) if getattr(self, field.name) != 0]


@dataclass
class LogitechF710ControllerState:
    """
    This state represents the desired state for the controller.
    """

    # The axis control range
    AXIS_MIN_VAL = -1
    AXIS_MAX_VAL = 1

    axes: ControllerAxesState
    buttons: ControllerButtonPressedState
    d_pad: ControllerDPadState

    def __post_init__(self):
        self.validate_direction(
            "axes.left_stick.horizontal", self.axes.left_stick.horizontal
        )
        self.validate_direction(
            "axes.left_stick.vertical", self.axes.left_stick.vertical
        )
        self.validate_direction(
            "axes.right_stick.horizontal", self.axes.right_stick.horizontal
        )
        self.validate_direction(
            "axes.right_stick.vertical", self.axes.right_stick.vertical
        )

    def validate_direction(self, attribute_name: str, value: float):
        if not isinstance(value, float):
            raise ValueError(
                f"{attribute_name} value needs to be an float. Got {type(value)}"
            )
        if not (self.AXIS_MIN_VAL <= value <= self.AXIS_MAX_VAL):
            raise ValueError(
                f"Value {value} for attribute '{attribute_name}' is not in the range [{self.AXIS_MIN_VAL}, {self.AXIS_MAX_VAL}]"
            )

    def to_dict(self):
        return asdict(self)


class LogitechF710Joystick:
    """
    The controller works on two main principles
        - That the axes act like a stream of data and are constant
        - The buttons are event based as in only when a button is pressed is the button acknowledged.
            The release of the button is not acknowledged directly but can be inferred
    """

    def __init__(self, pygame_connector: PyGameConnector, joystick_id: int = 0):
        self.pygame_connector = pygame_connector
        pygame_connector.init_joystick()
        self.joystick = pygame_connector.create_joystick(joystick_id)
        self.joystick.init()

        name = self.joystick.get_name()
        LOGGER.info(f"Detected joystick device: {name}")
        controller_type = "logitech"
        if controller_type not in name.lower():
            raise ValueError(
                f"{controller_type.capitalize()} controller not detected. Controller detected was {name}"
            )

        num_axes = self.joystick.get_numaxes()
        num_buttons = self.joystick.get_numbuttons()
        self.axis_states = [0.0 for i in range(num_axes)]
        self.button_states = [False for i in range(num_buttons)]
        self.axis_ids = {}
        self.button_ids = {}
        self.dead_zone = 0.07
        for i in range(num_axes):
            self.axis_ids[i] = AxisKeys(i)
        for i in range(num_buttons):
            self.button_ids[i] = ButtonKeys(i)

    def get_state(self) -> LogitechF710ControllerState:
        self.pygame_connector.get_events()

        left_stick_horizontal = self.joystick.get_axis(
            AxisKeys.LEFT_STICK_HORIZONTAL.value
        )
        left_stick_vertical = self.joystick.get_axis(AxisKeys.LEFT_STICK_VERTICAL.value)
        right_stick_horizontal = self.joystick.get_axis(
            AxisKeys.RIGHT_STICK_HORIZONTAL.value
        )
        right_stick_vertical = self.joystick.get_axis(
            AxisKeys.RIGHT_STICK_VERTICAL.value
        )

        if abs(left_stick_horizontal) < self.dead_zone:
            left_stick_horizontal = 0.0
        if abs(left_stick_vertical) < self.dead_zone:
            left_stick_vertical = 0.0
        if abs(right_stick_horizontal) < self.dead_zone:
            right_stick_horizontal = 0.0
        if abs(right_stick_vertical) < self.dead_zone:
            right_stick_vertical = 0.0

        axes = ControllerAxesState(
            left_stick=StickState(
                horizontal=left_stick_horizontal, vertical=left_stick_vertical
            ),
            right_stick=StickState(
                horizontal=right_stick_horizontal, vertical=right_stick_vertical
            ),
        )

        buttons = ControllerButtonPressedState(
            A=self.joystick.get_button(ButtonKeys.A.value),
            B=self.joystick.get_button(ButtonKeys.B.value),
            X=self.joystick.get_button(ButtonKeys.X.value),
            Y=self.joystick.get_button(ButtonKeys.Y.value),
            LB=self.joystick.get_button(ButtonKeys.LB.value),
            RB=self.joystick.get_button(ButtonKeys.RB.value),
            LEFT_STICK=self.joystick.get_button(ButtonKeys.LEFT_STICK.value),
            RIGHT_STICK=self.joystick.get_button(ButtonKeys.RIGHT_STICK.value),
            Start=self.joystick.get_button(ButtonKeys.Start.value),
            Back=self.joystick.get_button(ButtonKeys.Back.value),
            Left_trigger=self.joystick.get_button(ButtonKeys.LeftTrigger.value),
            RightTrigger=self.joystick.get_button(ButtonKeys.RightTrigger.value),
        )

        # Retrieve the state of the D-pad buttons
        hat = self.joystick.get_hat(0)
        d_pad_state = ControllerDPadState(
            int(hat[DPadKeys.HORIZONTAL.value]),
            int(hat[DPadKeys.VERTICAL.value]),
        )

        print("Current state")
        print(axes)
        print(self.joystick.get_numbuttons(), self.joystick)
        print(d_pad_state)

        pressed_button_ids = [
            button.value
            for button in ButtonKeys
            if self.joystick.get_button(button.value)
        ]
        pressed_buttons = [ButtonKeys(button_id) for button_id in pressed_button_ids]

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            LOGGER.debug(f"Axes: {axes}")
            LOGGER.debug(f"Buttons: {buttons}")
            LOGGER.debug(
                f"Pressed Buttons: {[button.name for button in pressed_buttons]}"
            )

        return LogitechF710ControllerState(
            axes=axes, buttons=buttons, d_pad=d_pad_state
        )


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    pygame_joystick = LogitechF710Joystick(pygame_connector)
    LOGGER.setLevel("DEBUG")
    while True:
        state = pygame_joystick.get_state()
        print("Current state")
        dict_state = state.to_dict()

        for k, v in dict_state.items():
            print(k, v)

        time.sleep(0.1)
