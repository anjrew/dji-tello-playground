from abc import ABC, abstractmethod
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


class XboxDPadKeys(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class XboxAxisKeys(Enum):
    LEFT_STICK_HORIZONTAL = 0
    LEFT_STICK_VERTICAL = 1
    LEFT_ANALOG_TRIGGER = 2
    RIGHT_STICK_HORIZONTAL = 3
    RIGHT_STICK_VERTICAL = 4
    RIGHT_ANALOG_TRIGGER = 5


@dataclass
class StickState:
    horizontal: float
    vertical: float


@dataclass
class XboxControllerAxesState:
    left_stick: StickState
    right_stick: StickState
    left_analog_trigger: float
    right_analog_trigger: float


class XboxButtonKeys(Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    VIEW = 6
    MENU = 7
    NA = 8
    LEFT_STICK = 9
    RIGHT_STICK = 10


@dataclass
class XboxControllerButtonPressedState:
    A: bool
    B: bool
    X: bool
    Y: bool
    LB: bool
    RB: bool
    VIEW: bool
    MENU: bool
    NA: bool
    LEFT_STICK: bool
    RIGHT_STICK: bool

    def get_pressed_buttons(self) -> List[str]:
        return [field.name for field in fields(self) if getattr(self, field.name)]


@dataclass
class XboxControllerDPadState:
    horizontal_right: int
    """If positive, the D-pad is pressed right, if negative, the D-pad is pressed left. If 0, the D-pad is not pressed"""
    vertical_up: int
    """If positive, the D-pad is pressed up, if negative, the D-pad is pressed down. If 0, the D-pad is not pressed"""

    def get_active(self) -> List[str]:
        return [field.name for field in fields(self) if getattr(self, field.name) != 0]


@dataclass
class XboxControllerState:
    """
    This state represents the desired state for the controller.
    """

    # The axis control range
    AXIS_MIN_VAL = -1
    AXIS_MAX_VAL = 1

    axes: XboxControllerAxesState
    buttons: XboxControllerButtonPressedState
    d_pad: XboxControllerDPadState

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
        self.validate_direction(
            "axes.left_analog_trigger", self.axes.left_analog_trigger
        )
        self.validate_direction(
            "axes.right_analog_trigger", self.axes.right_analog_trigger
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


class XboxController(ABC):
    @abstractmethod
    def get_state(self) -> XboxControllerState:
        """Gets the current controller state of the drone"""


class Xbox360PyGameJoystick(XboxController):
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
        LOGGER.info(f"detected joystick device: {name}")
        if "360" not in name or "xbox" not in name.lower():
            raise ValueError(
                f"Xbox controller not detected. Controller detected was {name}"
            )

        self.axis_states = [0.0 for i in range(self.joystick.get_numaxes())]
        self.button_states = [False for i in range(self.joystick.get_numbuttons())]
        self.axis_ids = {}
        self.button_ids = {}
        self.dead_zone = 0.07
        for i in range(self.joystick.get_numaxes()):
            self.axis_ids[i] = XboxAxisKeys(i)
        for i in range(self.joystick.get_numbuttons()):
            self.button_ids[i] = XboxButtonKeys(i)

    def get_state(self) -> XboxControllerState:
        self.pygame_connector.get_events()

        left_stick_horizontal = self.joystick.get_axis(
            XboxAxisKeys.LEFT_STICK_HORIZONTAL.value
        )
        left_stick_vertical = self.joystick.get_axis(
            XboxAxisKeys.LEFT_STICK_VERTICAL.value
        )
        right_stick_horizontal = self.joystick.get_axis(
            XboxAxisKeys.RIGHT_STICK_HORIZONTAL.value
        )
        right_stick_vertical = self.joystick.get_axis(
            XboxAxisKeys.RIGHT_STICK_VERTICAL.value
        )
        left_analog_trigger = self.joystick.get_axis(
            XboxAxisKeys.LEFT_ANALOG_TRIGGER.value
        )
        right_analog_trigger = self.joystick.get_axis(
            XboxAxisKeys.RIGHT_ANALOG_TRIGGER.value
        )

        if abs(left_stick_horizontal) < self.dead_zone:
            left_stick_horizontal = 0.0
        if abs(left_stick_vertical) < self.dead_zone:
            left_stick_vertical = 0.0
        if abs(right_stick_horizontal) < self.dead_zone:
            right_stick_horizontal = 0.0
        if abs(right_stick_vertical) < self.dead_zone:
            right_stick_vertical = 0.0
        if abs(left_analog_trigger) < self.dead_zone:
            left_analog_trigger = 0.0
        if abs(right_analog_trigger) < self.dead_zone:
            right_analog_trigger = 0.0

        axes = XboxControllerAxesState(
            left_stick=StickState(
                horizontal=left_stick_horizontal, vertical=left_stick_vertical
            ),
            right_stick=StickState(
                horizontal=right_stick_horizontal, vertical=right_stick_vertical
            ),
            left_analog_trigger=left_analog_trigger,
            right_analog_trigger=right_analog_trigger,
        )

        buttons = XboxControllerButtonPressedState(
            A=self.joystick.get_button(XboxButtonKeys.A.value),
            B=self.joystick.get_button(XboxButtonKeys.B.value),
            X=self.joystick.get_button(XboxButtonKeys.X.value),
            Y=self.joystick.get_button(XboxButtonKeys.Y.value),
            LB=self.joystick.get_button(XboxButtonKeys.LB.value),
            RB=self.joystick.get_button(XboxButtonKeys.RB.value),
            VIEW=self.joystick.get_button(XboxButtonKeys.VIEW.value),
            MENU=self.joystick.get_button(XboxButtonKeys.MENU.value),
            NA=self.joystick.get_button(XboxButtonKeys.NA.value),
            LEFT_STICK=self.joystick.get_button(XboxButtonKeys.LEFT_STICK.value),
            RIGHT_STICK=self.joystick.get_button(XboxButtonKeys.RIGHT_STICK.value),
        )

        # Retrieve the state of the D-pad buttons
        hat = self.joystick.get_hat(0)
        d_pad_state = XboxControllerDPadState(
            int(hat[XboxDPadKeys.HORIZONTAL.value]),
            int(hat[XboxDPadKeys.VERTICAL.value]),
        )

        pressed_button_ids = [
            button.value
            for button in XboxButtonKeys
            if self.joystick.get_button(button.value)
        ]
        pressed_buttons = [
            XboxButtonKeys(button_id) for button_id in pressed_button_ids
        ]

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            LOGGER.debug(f"Axes: {axes}")
            LOGGER.debug(f"Buttons: {buttons}")
            LOGGER.debug(
                f"Pressed Buttons: {[button.name for button in pressed_buttons]}"
            )

        return XboxControllerState(axes=axes, buttons=buttons, d_pad=d_pad_state)


if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    LOGGER.setLevel(log_level)
    pygame_connector = PyGameConnector()
    pygame_joystick = Xbox360PyGameJoystick(pygame_connector)

    while True:
        state = pygame_joystick.get_state()
        print("Current state")
        dict_state = state.to_dict()

        for k, v in dict_state.items():
            print(k, v)

        time.sleep(0.1)
