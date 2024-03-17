import asyncio
from typing import List
import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event
import logging

LOGGER = logging.getLogger(__name__)


class PyGameConnector:
    def __init__(self):
        pygame.init()
        self.event_queue = asyncio.Queue()

    async def run(self):
        while True:
            event = await asyncio.to_thread(pygame.event.wait)
            LOGGER.debug(f"Get event from pygame {vars(event)}")
            await self.event_queue.put(event)

    async def pump_events(self):
        while not self.event_queue.empty():
            event = await self.event_queue.get()
            pygame.event.post(event)

    async def get_events(self) -> List[Event]:
        events = []
        while not self.event_queue.empty():
            event = await self.event_queue.get()
            if event.type == pygame.KEYDOWN:
                events.append(event)
        return events

    async def get_pressed_keys(self) -> ScancodeWrapper:
        return pygame.key.get_pressed()

    def get_key_name(self, key_code: int) -> str:
        return pygame.key.name(key_code)

    def dispose(self):
        pygame.quit()
