"""
This module contains the implementation of a General "Xbox Wireless" controller.
https://www.amazon.de/-/en/gp/product/B07SDFLVKD/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1
.. image:: docs/images/xbox_pad.jpeg
   :alt: General Xbox Wireless Controller
   :width: 400px
   :align: center
It provides classes for handling the controller's axes, buttons, and D-pad state.
The `Controller` abstract base class defines the interface for getting the current controller state.
The `XboxPyGameJoystick` class is a concrete implementation of the `Controller` interface using the PyGame library.
"""

from dataclasses import dataclass, fields
from typing import List
from enum import Enum
import logging
import time
import sys

try:
    from joysticks.pygame_connector import PyGameConnector
    from joysticks.game_controller import (
        Controller,
        ControllerAxesState,
        ControllerDPadState,
        ControllerState,
        StickState,
        ControllerButtonPressedState,
    )
except ModuleNotFoundError:
    from pygame_connector import PyGameConnector
    from game_controller import (
        Controller,
        ControllerAxesState,
        ControllerDPadState,
        ControllerState,
        StickState,
        ControllerButtonPressedState,
    )


LOGGER = logging.getLogger(__name__)


class ButtonKeys(Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 9
    RB = 10
    VIEW = 4
    MENU = 6
    NA = 15
    LEFT_STICK = 7
    RIGHT_STICK = 8
    D_PAD_UP = 11
    D_PAD_DOWN = 12
    D_PAD_LEFT = 13
    D_PAD_RIGHT = 14


class AxisKeys(Enum):
    LEFT_STICK_HORIZONTAL = 0
    LEFT_STICK_VERTICAL = 1
    LEFT_ANALOG_TRIGGER = 4
    RIGHT_STICK_HORIZONTAL = 2
    RIGHT_STICK_VERTICAL = 3
    RIGHT_ANALOG_TRIGGER = 5


# Button keys that are not assigned to any button on the controller
VOID_BUTTONS = [5]


@dataclass
class ButtonPressedState(ControllerButtonPressedState):
    A: bool
    B: bool
    X: bool
    Y: bool
    LB: bool
    RB: bool
    VIEW: bool
    MENU: bool
    SHARE: bool
    LEFT_STICK: bool
    RIGHT_STICK: bool

    def get_pressed_buttons(self) -> List[str]:
        return [field.name for field in fields(self) if getattr(self, field.name)]


class XboxPyGameJoystick(Controller):
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

        if sys.platform == "darwin":
            LOGGER.info("Running on macOS")
            if name != "Xbox Series X Controller":
                raise ValueError(
                    f"Xbox controller not detected. Controller detected was {name}"
                )
        elif sys.platform.startswith("linux"):
            if "360" not in name or "xbox" not in name.lower():
                raise ValueError(
                    f"Xbox controller not detected. Controller detected was {name}"
                )
        else:
            raise ValueError(
                f"Xbox controller not detected. Controller detected was {name}"
            )

        self.axis_states = [0.0] * self.joystick.get_numaxes()
        self.button_states = [False] * self.joystick.get_numbuttons()
        self.axis_ids = {}
        self.button_ids = {}
        self.dead_zone = 0.07
        for i in range(self.joystick.get_numaxes()):
            self.axis_ids[i] = AxisKeys(i)
        mapped_buttons = filter(
            lambda x: x not in VOID_BUTTONS, range(self.joystick.get_numbuttons())
        )
        for i in mapped_buttons:
            self.button_ids[i] = ButtonKeys(i)

    def get_state(self) -> ControllerState:
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
        left_analog_trigger = self.joystick.get_axis(AxisKeys.LEFT_ANALOG_TRIGGER.value)
        right_analog_trigger = self.joystick.get_axis(
            AxisKeys.RIGHT_ANALOG_TRIGGER.value
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

        axes = ControllerAxesState(
            left_stick=StickState(
                horizontal=left_stick_horizontal, vertical=left_stick_vertical
            ),
            right_stick=StickState(
                horizontal=right_stick_horizontal, vertical=right_stick_vertical
            ),
            left_analog_trigger=left_analog_trigger,
            right_analog_trigger=right_analog_trigger,
        )

        buttons = ButtonPressedState(
            A=self.joystick.get_button(ButtonKeys.A.value),
            B=self.joystick.get_button(ButtonKeys.B.value),
            X=self.joystick.get_button(ButtonKeys.X.value),
            Y=self.joystick.get_button(ButtonKeys.Y.value),
            LB=self.joystick.get_button(ButtonKeys.LB.value),
            RB=self.joystick.get_button(ButtonKeys.RB.value),
            VIEW=self.joystick.get_button(ButtonKeys.VIEW.value),
            MENU=self.joystick.get_button(ButtonKeys.MENU.value),
            SHARE=self.joystick.get_button(ButtonKeys.NA.value),
            LEFT_STICK=self.joystick.get_button(ButtonKeys.LEFT_STICK.value),
            RIGHT_STICK=self.joystick.get_button(ButtonKeys.RIGHT_STICK.value),
        )

        right = self.joystick.get_button(ButtonKeys.D_PAD_RIGHT.value)
        left = self.joystick.get_button(ButtonKeys.D_PAD_LEFT.value)
        up = self.joystick.get_button(ButtonKeys.D_PAD_UP.value)
        down = self.joystick.get_button(ButtonKeys.D_PAD_DOWN.value)

        d_pad_state = ControllerDPadState(
            horizontal_right=1 if right else -1 if left else 0,
            vertical_up=1 if up else -1 if down else 0,
        )

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

        return ControllerState(axes=axes, buttons=buttons, d_pad=d_pad_state)


if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    LOGGER.setLevel(log_level)
    pygame_connector = PyGameConnector()
    pygame_joystick = XboxPyGameJoystick(pygame_connector)

    while True:
        state = pygame_joystick.get_state()
        print("Current state")
        dict_state = state.to_dict()

        for k, v in dict_state.items():
            print(k, v)

        time.sleep(0.1)
