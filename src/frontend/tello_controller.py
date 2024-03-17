from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from pygame_connector import PyGameConnector

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
    K_l,
)


class TelloActionType(Enum):
    SET_FORWARD_VELOCITY = 1
    SET_BACKWARD_VELOCITY = 2
    SET_LEFT_VELOCITY = 3
    SET_RIGHT_VELOCITY = 4
    SET_UP_VELOCITY = 5
    SET_DOWN_VELOCITY = 6
    SET_YAW_CLOCKWISE_VELOCITY = 7
    SET_YAW_COUNTER_CLOCKWISE_VELOCITY = 8
    TAKEOFF = 9
    LAND = 10


class TelloControlEvent:
    def __init__(self, action, intensity):
        self.action = action
        self.intensity = intensity


class Controller(ABC):

    @abstractmethod
    def get_actions(self) -> List[TelloControlEvent]:
        pass


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

    def __init__(self, pygame_connector: PyGameConnector, max_intensity=10):
        """
        Initializes a new instance of the KeyboardController class.

        Args:
            pygame_connector: The connector used to interface with pygame.
            max_intensity: The maximum intensity value for key press counters (default: 10).
        """
        self.max_intensity = max_intensity
        self.pygame_connector = pygame_connector
        self.key_mapping = {
            K_UP: TelloActionType.SET_FORWARD_VELOCITY,
            K_DOWN: TelloActionType.SET_BACKWARD_VELOCITY,
            K_LEFT: TelloActionType.SET_LEFT_VELOCITY,
            K_RIGHT: TelloActionType.SET_RIGHT_VELOCITY,
            K_w: TelloActionType.SET_UP_VELOCITY,
            K_s: TelloActionType.SET_DOWN_VELOCITY,
            K_a: TelloActionType.SET_YAW_COUNTER_CLOCKWISE_VELOCITY,
            K_d: TelloActionType.SET_YAW_CLOCKWISE_VELOCITY,
            K_t: TelloActionType.TAKEOFF,
            K_l: TelloActionType.LAND,
        }
        # Initialize key press counters
        self.key_press_counters = {key: 0 for key in self.key_mapping.keys()}

    def get_actions(self) -> List[TelloControlEvent]:
        """
        Checks if any of the defined keys are currently being pressed and returns the corresponding Tello action.

        Returns:
            A TelloActionEvent object representing the Tello action corresponding to the currently pressed key, if any.
            Returns None if no action keys are pressed.
        """
        self.pygame_connector.pump_events()  # Process internal pygame event handlers.
        keys = (
            self.pygame_connector.get_pressed_keys()
        )  # Get the currently pressed keys.

        actions: List[TelloControlEvent] = []
        for key, action in self.key_mapping.items():
            if keys[key]:  # If the key is pressed
                # Increment key press counter up to the maximum intensity
                if self.key_press_counters[key] < self.max_intensity:
                    self.key_press_counters[key] += 1
                intensity = (
                    self.key_press_counters[key] / self.max_intensity
                )  # Normalize intensity
                actions.append(TelloControlEvent(action, intensity))
            else:
                # Reset counter if the key is not pressed
                self.key_press_counters[key] = 0

        return actions

    def dispose(self):
        self.pygame_connector.dispose()
