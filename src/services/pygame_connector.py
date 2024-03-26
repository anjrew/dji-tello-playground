from typing import List
import pygame
from pygame.key import ScancodeWrapper
from pygame.event import Event


class PyGameConnector:

    def __init__(self):
        pygame.init()

    def pump_events(self):
        pygame.event.pump()

    def get_events(self) -> List[Event]:
        return pygame.event.get()

    def get_pressed_keys(self) -> ScancodeWrapper:
        return pygame.key.get_pressed()

    def get_key_name(self, key_code: int) -> str:
        return pygame.key.name(key_code)

    def dispose(self) -> None:
        pygame.quit()

    def init_joystick(self):
        pygame.joystick.init()
        return pygame.joystick.get_count()

    def get_joystick_count(self) -> int:
        return pygame.joystick.get_count()

    def create_joystick(self, which_js: int) -> pygame.joystick.JoystickType:
        return pygame.joystick.Joystick(which_js)
