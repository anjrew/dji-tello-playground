import time
import logging

from pygame_connector import PyGameConnector
from tello_controller import TelloControlState, TelloController

LOGGER = logging.getLogger(__name__)

from enum import Enum


class XboxButton(Enum):
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
    DPAD_LEFT = 11
    DPAD_RIGHT = 12
    DPAD_DOWN = 13
    DPAD_UP = 14


class XboxXsSeriesPyGameJoystick(TelloController):
    """
    The controller works on two main principles
        - That the axes act like a stream of data and are constant
        - The buttons are event based as in only when a button is pressed is the button acknowledged.
            The release of the button is not acknowledged directly but can be inferred
    """

    # The axis id with its name
    AXIS_NAMES = {
        0: "left_stick_horizontal",
        1: "left_stick_vertical",
        2: "left_analog_trigger",
        3: "right_stick_horizontal",
        4: "right_stick_vertical",
        5: "right_analog_trigger",
    }

    # The button id with its name
    BUTTON_NAMES = {
        0: "A",
        1: "B",
        2: "X",
        3: "Y",
        4: "LB",
        5: "RB",
        6: "View",
        7: "Menu",
        8: "N/A",
        9: "Left Stick",
        10: "Right Stick",
        11: "D-Pad Left",
        12: "D-Pad Right",
        13: "D-Pad Down",
        14: "D-Pad Up",
    }

    def __init__(self, pygame_connector: PyGameConnector, joystick_id: int = 0):
        self.pygame_connector = pygame_connector
        pygame_connector.init_joystick()
        self.joystick = pygame_connector.create_joystick(joystick_id)
        self.joystick.init()

        name = self.joystick.get_name()
        LOGGER.info(f"detected joystick device: {name}")
        if "xbox" not in name.lower():
            raise ValueError(
                f"Xbox controller not detected. Controller detected was {name}"
            )

        self.axis_states = [0.0 for i in range(self.joystick.get_numaxes())]
        self.button_states = [
            False
            for i in range(
                self.joystick.get_numbuttons() + self.joystick.get_numhats() * 4
            )
        ]
        self.axis_ids = {}
        self.button_ids = {}
        self.dead_zone = 0.07
        for i in range(self.joystick.get_numaxes()):
            self.axis_ids[i] = i
        for i in range(
            self.joystick.get_numbuttons() + self.joystick.get_numhats() * 4
        ):
            self.button_ids[i] = i

    def get_state(self) -> TelloControlState:
        self.pygame_connector.get_events()

        left_right_velocity = 0
        forward_backward_velocity = 0
        up_down_velocity = 0
        yaw_velocity = 0

        for i in range(self.joystick.get_numaxes()):
            val = self.joystick.get_axis(i)
            if abs(val) < self.dead_zone:
                val = 0.0
            if self.axis_states[i] != val and i in self.axis_ids:
                axis = self.axis_ids[i]
                self.axis_states[i] = val
                logging.debug("axis: %s val: %f" % (axis, val))

                if axis == "left_right":
                    left_right_velocity = int(val * 100)
                elif axis == "forward_backward":
                    forward_backward_velocity = int(val * 100)
                elif axis == "up_down":
                    up_down_velocity = int(val * 100)
                elif axis == "yaw":
                    yaw_velocity = int(val * 100)

        for i in range(self.joystick.get_numbuttons()):
            state = bool(self.joystick.get_button(i))
            if self.button_states[i] != state:
                if i not in self.button_ids:
                    LOGGER.info(f"button: {i}")
                    continue
                button = self.button_ids[i]
                self.button_states[i] = state
                LOGGER.info("button: %s state: %d" % (button, state))

        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            horz, vert = hat
            iBtn = self.joystick.get_numbuttons() + (i * 4)
            states = (horz == -1, horz == 1, vert == -1, vert == 1)
            for state in states:
                state = bool(state)
                if self.button_states[iBtn] != state:
                    if iBtn not in self.button_ids:
                        LOGGER.info(f"button: {iBtn}")
                        continue
                    button = self.button_ids[iBtn]
                    self.button_states[iBtn] = state
                    LOGGER.info("button: %s state: %d" % (button, state))
                iBtn += 1

        pressed_button_ids = [
            index
            for index, is_pressed_state in enumerate(self.button_states)
            if is_pressed_state
        ]
        if LOGGER.level == logging.DEBUG:
            LOGGER.debug(
                f"Axis {list(zip(self.AXIS_NAMES.values() ,self.axis_ids, self.axis_states))}"
            )
            LOGGER.debug(
                f"Buttons {list(zip(self.BUTTON_NAMES.values(), self.button_ids, self.button_states))}"
            )
            LOGGER.debug(
                f"Pressed Buttons { [ v for k,v in self.BUTTON_NAMES.items() if k in pressed_button_ids ]}"
            )
        return TelloControlState(
            left_right_velocity=left_right_velocity,
            forward_backward_velocity=forward_backward_velocity,
            up_down_velocity=up_down_velocity,
            yaw_velocity=yaw_velocity,
            speed=50,
            take_off=False,
        )


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    pygame_joystick = XboxXsSeriesPyGameJoystick(pygame_connector)
    LOGGER.setLevel("DEBUG")
    while True:
        state = pygame_joystick.get_state()
        print("Current state", state)
        time.sleep(0.1)
