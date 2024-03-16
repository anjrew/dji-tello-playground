import pygame
from pygame.key import ScancodeWrapper


class PyGameConnector:

    def pump_events(self):
        pygame.event.pump()

    def get_pressed_keys(self) -> ScancodeWrapper:
        return pygame.key.get_pressed()

    def dispose(self):
        pygame.quit()
