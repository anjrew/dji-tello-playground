import pygame
from pygame.key import ScancodeWrapper


class PyGameConnector:

    def __init__(self):
        pygame.init()

    def pump_events(self):
        pygame.event.pump()

    def get_pressed_keys(self) -> ScancodeWrapper:
        return pygame.key.get_pressed()

    def get_key_name(self, key_code: int) -> str:
        return pygame.key.name(key_code)

    def dispose(self):
        pygame.quit()
