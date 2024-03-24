import time

from pygame_connector import PyGameConnector


import logging

from tello_controller import TelloControlState, TelloController

LOGGER = logging.getLogger(__name__)


class XboxXsSeriesPyGameJoystick(TelloController):

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
            0
            for i in range(
                self.joystick.get_numbuttons() + self.joystick.get_numhats() * 4
            )
        ]
        self.axis_names = {}
        self.button_names = {}
        self.dead_zone = 0.07
        for i in range(self.joystick.get_numaxes()):
            self.axis_names[i] = i
        for i in range(
            self.joystick.get_numbuttons() + self.joystick.get_numhats() * 4
        ):
            self.button_names[i] = i

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
            if self.axis_states[i] != val and i in self.axis_names:
                axis = self.axis_names[i]
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
            state = self.joystick.get_button(i)
            if self.button_states[i] != state:
                if i not in self.button_names:
                    LOGGER.info(f"button: {i}")
                    continue
                button = self.button_names[i]
                self.button_states[i] = state
                LOGGER.info("button: %s state: %d" % (button, state))

        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            horz, vert = hat
            iBtn = self.joystick.get_numbuttons() + (i * 4)
            states = (horz == -1, horz == 1, vert == -1, vert == 1)
            for state in states:
                state = int(state)
                if self.button_states[iBtn] != state:
                    if iBtn not in self.button_names:
                        LOGGER.info(f"button: {iBtn}")
                        continue
                    button = self.button_names[iBtn]
                    self.button_states[iBtn] = state
                    LOGGER.info("button: %s state: %d" % (button, state))
                iBtn += 1
        LOGGER.debug(self.axis_names)
        LOGGER.debug(self.axis_states)
        LOGGER.debug(self.button_names)
        LOGGER.debug(self.button_states)
        return TelloControlState(
            left_right_velocity=left_right_velocity,
            forward_backward_velocity=forward_backward_velocity,
            up_down_velocity=up_down_velocity,
            yaw_velocity=yaw_velocity,
            speed=50,
            take_off=False,
        )

    def set_deadzone(self, val):
        self.dead_zone = val


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    pygame_joystick = XboxXsSeriesPyGameJoystick(pygame_connector)
    LOGGER.setLevel("DEBUG")
    while True:
        state = pygame_joystick.get_state()
        print("Current state", state)
        time.sleep(0.1)
