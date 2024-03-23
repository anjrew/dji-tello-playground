import time
from typing import List

from models.tello_control_event import TelloControlEvent
from enums.tello_action_type import TelloActionType
from interfaces.controller import Controller
from services.pygame_connector import PyGameConnector


import logging

LOGGER = logging.getLogger(__name__)


# class KeyboardController(Controller):
#     """
#     A class representing a keyboard controller for the Tello drone.

#     Attributes:
#         controller_connector: The connector used to interface with the keyboard (default: pygame).
#         max_intensity: The maximum intensity value for key press counters (default: 10).
#         key_mapping: A dictionary mapping keyboard keys to Tello action types.
#         key_press_counters: A dictionary storing the key press counters for each key.

#     Methods:
#         get_action: Returns the Tello action corresponding to the currently pressed key, if any.
#     """

#     def __init__(self, pygame_connector: PyGameConnector, max_intensity=100):
#         """
#         Initializes a new instance of the KeyboardController class.

#         Args:
#             pygame_connector: The connector used to interface with pygame.
#             max_intensity: The maximum intensity value for key press counters (default: 10).
#         """
#         self._max_intensity = max_intensity
#         self._pygame_connector = pygame_connector

#         # Initialize key press counters
#         self.key_press_counters = {key: 0 for key in self._key_mapping.keys()}
#         LOGGER.info("Key Mappings:")
#         for key, action in self._key_mapping.items():
#             LOGGER.info(f"{pygame_connector.get_key_name(key).upper()}: {action.name}")

#     def get_actions(self) -> List[TelloControlEvent]:
#         """
#         Checks if any of the defined keys are currently being pressed and returns the corresponding Tello action.

#         Returns:
#             A TelloActionEvent object representing the Tello action corresponding to the currently pressed key, if any.
#             Returns None if no action keys are pressed.
#         """
#         LOGGER.debug(f"Getting actions from {self.__class__.__name__}")
#         self._pygame_connector.pump_events()  # Process internal pygame event handlers.
#         keys = self._pygame_connector.get_pressed_keys()

#         actions: List[TelloControlEvent] = []
#         for key in keys:
#             if key in self._key_mapping.keys():
#                 action = self._key_mapping[key]
#                 # Increment key press counter up to the maximum intensity
#                 if self.key_press_counters[key] < self._max_intensity:
#                     self.key_press_counters[key] += 1
#                 else:
#                     # Reset counter if the key is not pressed
#                     self.key_press_counters[key] = 0
#                 count = self.key_press_counters[key]
#                 intensity = min(count, self._max_intensity)
#                 LOGGER.debug(
#                     f"{key} pressed {count} times meaning intensity {intensity}"
#                 )
#                 actions.append(TelloControlEvent(action, intensity))

#         return actions

#     def dispose(self):
#         self._pygame_connector.dispose()


class PyGameJoystick(Controller):

    def __init__(self, pygame_connector: PyGameConnector, joystick_id: int = 0):
        self.pygame_connector = pygame_connector
        pygame_connector.init_joystick()
        self.joystick = pygame_connector.create_joystick(joystick_id)
        self.joystick.init()

        name = self.joystick.get_name()
        LOGGER.info(f"detected joystick device: {name}")

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

    def get_actions(self) -> List[TelloControlEvent]:

        button = None
        button_state = None
        axis = None
        axis_val = None

        self.pygame_connector.get_events()

        for i in range(self.joystick.get_numaxes()):
            val = self.joystick.get_axis(i)
            if abs(val) < self.dead_zone:
                val = 0.0
            if self.axis_states[i] != val and i in self.axis_names:
                axis = self.axis_names[i]
                axis_val = val
                self.axis_states[i] = val
                logging.debug("axis: %s val: %f" % (axis, val))

        for i in range(self.joystick.get_numbuttons()):
            state = self.joystick.get_button(i)
            if self.button_states[i] != state:
                if not i in self.button_names:
                    LOGGER.info(f"button: {i}")
                    continue
                button = self.button_names[i]
                button_state = state
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
                    if not iBtn in self.button_names:
                        logger.info(f"button: {iBtn}")
                        continue
                    button = self.button_names[iBtn]
                    button_state = state
                    self.button_states[iBtn] = state
                    logging.info("button: %s state: %d" % (button, state))
                    # print("button: %s state: %d" % (button, state))

                iBtn += 1

        return button, button_state, axis, axis_val

    def set_deadzone(self, val):
        self.dead_zone = val


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    pygame_joystick = PyGameJoystick(pygame_connector)
    while True:
        pygame_joystick.poll()
        time.sleep(0.1)
