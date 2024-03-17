import asyncio
from abc import ABC, abstractmethod
from typing import List

from models.tello_control_event import TelloControlEvent
from enums.tello_action_type import TelloActionType
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
    K_SPACE,
)
import logging

LOGGER = logging.getLogger(__name__)


class Controller(ABC):
    @abstractmethod
    async def get_actions(self) -> List[TelloControlEvent]:
        pass


class KeyboardController(Controller):
    def __init__(self, pygame_connector: PyGameConnector, max_intensity=10):
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
        }

        self.action_queue = asyncio.Queue()

        LOGGER.debug("Key Mappings:")
        for key, action in self._key_mapping.items():
            print(f"{pygame_connector.get_key_name(key).upper()}: {action.name}")

    async def _process_events(self):
        while True:
            events = await asyncio.to_thread(self._pygame_connector.get_events)
            for event in events:
                key = event.key
                if key in self._key_mapping:
                    action = self._key_mapping[key]
                    intensity = 1.0  # Set intensity to 1.0 for key press events
                    await self.action_queue.put(TelloControlEvent(action, intensity))

    async def get_actions(self) -> List[TelloControlEvent]:
        LOGGER.debug(f"Getting actions from {self.__class__.__name__}")
        actions = []
        await asyncio.sleep(0.1)
        while not self.action_queue.empty():
            action = await self.action_queue.get()
            actions.append(action)
        return actions

    async def run(self):
        await asyncio.gather(self._process_events())

    def dispose(self):
        self._pygame_connector.dispose()
