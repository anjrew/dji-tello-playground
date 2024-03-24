from typing import List

from models.tello_control_event import TelloControlEvent
from interfaces.controller import Controller
from services.pygame_connector import PyGameConnector

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_a,
    K_d,
    K_t,
    K_SPACE,
    K_KP_PLUS,
    K_k,
)

import logging

LOGGER = logging.getLogger(__name__)


class KeyboardController(Controller):
    """
    A class representing a keyboard controller for the Tello drone.

    Attributes:
        controller_connector: The connector used to interface with the keyboard (default: pygame).
        max_intensity: The maximum intensity value for key press counters (default: 10).
        key_mapping: A dictionary mapping keyboard keys to Tello action types.
        key_press_counters: A dictionary storing the key press counters for each key.

    Methods:
        get_action: Returns the Tello action corresponding to the currently pressed key, if any.
    """

    def __init__(self, pygame_connector: PyGameConnector, max_intensity=100):
        """
        Initializes a new instance of the KeyboardController class.

        Args:
            pygame_connector: The connector used to interface with pygame.
            max_intensity: The maximum intensity value for key press counters (default: 10).
        """
        self._max_intensity = max_intensity
        self._pygame_connector = pygame_connector
        self._key_mapping = {
            K_UP: TelloActionType.SET_FORWARD_VELOCITY,
            K_DOWN: TelloActionType.SET_BACKWARD_VELOCITY,
            K_LEFT: TelloActionType.SET_LEFT_VELOCITY,
            K_RIGHT: TelloActionType.SET_RIGHT_VELOCITY,
            K_w: TelloActionType.SET_UP_VELOCITY,
            K_s: TelloActionType.SET_DOWN_VELOCITY,
            K_a: TelloActionType.SET_YAW_COUNTER_CLOCKWISE_VELOCITY,
            K_d: TelloActionType.SET_YAW_CLOCKWISE_VELOCITY,
            K_t: TelloActionType.TAKEOFF,
            K_SPACE: TelloActionType.LAND,
            K_k: TelloActionType.EMERGENCY_LAND,
            K_KP_PLUS: TelloActionType.EMERGENCY_LAND,
        }
        # Initialize key press counters
        self.key_press_counters = {key: 0 for key in self._key_mapping.keys()}
        LOGGER.info("Key Mappings:")
        for key, action in self._key_mapping.items():
            LOGGER.info(f"{pygame_connector.get_key_name(key).upper()}: {action.name}")

    def get_actions(self) -> List[TelloControlEvent]:
        """
        Checks if any of the defined keys are currently being pressed and returns the corresponding Tello action.

        Returns:
            A TelloActionEvent object representing the Tello action corresponding to the currently pressed key, if any.
            Returns None if no action keys are pressed.
        """
        LOGGER.debug(f"Getting actions from {self.__class__.__name__}")
        self._pygame_connector.pump_events()  # Process internal pygame event handlers.
        keys = self._pygame_connector.get_pressed_keys()

        actions: List[TelloControlEvent] = []
        for key in keys:
            if key in self._key_mapping.keys():
                action = self._key_mapping[key]
                # Increment key press counter up to the maximum intensity
                if self.key_press_counters[key] < self._max_intensity:
                    self.key_press_counters[key] += 1
                else:
                    # Reset counter if the key is not pressed
                    self.key_press_counters[key] = 0
                count = self.key_press_counters[key]
                intensity = min(count, self._max_intensity)
                LOGGER.debug(
                    f"{key} pressed {count} times meaning intensity {intensity}"
                )
                actions.append(TelloControlEvent(action, intensity))

        return actions

    def dispose(self):
        self._pygame_connector.dispose()
