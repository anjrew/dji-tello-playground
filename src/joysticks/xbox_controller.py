"""
This module contains the implementation of a General "Xbox Wireless" controller that works with linux systems.
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

from joysticks.xbox_controller_mac import MacXboxPyGameJoystick
from joysticks.xbox_controller_linux import LinuxXboxPyGameJoystick

try:
    from joysticks.pygame_connector import PyGameConnector
    from joysticks.game_controller import (
        Controller,
        ControllerState,
        ControllerButtonPressedState,
    )
except ModuleNotFoundError:
    from pygame_connector import PyGameConnector
    from game_controller import (
        Controller,
        ControllerState,
        ControllerButtonPressedState,
    )


LOGGER = logging.getLogger(__name__)


class ButtonKeys(Enum):
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


class DPadKeys(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class AxisKeys(Enum):
    LEFT_STICK_HORIZONTAL = 0
    LEFT_STICK_VERTICAL = 1
    LEFT_ANALOG_TRIGGER = 2
    RIGHT_STICK_HORIZONTAL = 3
    RIGHT_STICK_VERTICAL = 4
    RIGHT_ANALOG_TRIGGER = 5


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
    NA: bool
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

    platform_controller: Controller

    def __init__(self, pygame_connector: PyGameConnector, joystick_id: int = 0):
        if sys.platform == "darwin":
            self.platform_controller = MacXboxPyGameJoystick(
                pygame_connector, joystick_id
            )
        elif sys.platform.startswith("linux"):
            self.platform_controller = LinuxXboxPyGameJoystick(
                pygame_connector, joystick_id
            )
        else:
            raise ValueError(
                f"Unknown platform {sys.platform}. Cannot create XboxPyGameJoystick"
            )

    def get_state(self) -> ControllerState:
        return self.platform_controller.get_state()


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
