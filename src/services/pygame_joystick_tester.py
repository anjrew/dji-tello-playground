import logging
import time

from pygame_connector import PyGameConnector

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class JoyStickTester:
    """
    A class for testing the joysticks
    """

    def __init__(self, pygame_connector: PyGameConnector, joystick_id: int = 0):
        self.pygame_connector = pygame_connector
        pygame_connector.init_joystick()
        self.joystick = pygame_connector.create_joystick(joystick_id)
        self.joystick.init()

        name = self.joystick.get_name()
        LOGGER.info(f"Detected joystick device: {name}")

    def get_state(self) -> None:
        self.pygame_connector.get_events()

        LOGGER.info(f"Reading out {self.joystick.get_name()} state {time.time()}")
        for axis in range(self.joystick.get_numaxes()):
            LOGGER.info(f"Axis {axis} value: {self.joystick.get_axis(axis)}")
        for button in range(self.joystick.get_numbuttons()):
            LOGGER.info(f"Button {button} value: {self.joystick.get_button(button)}")
        for hat in range(self.joystick.get_numhats()):
            LOGGER.info(f"Hat {hat} value: {self.joystick.get_hat(hat)}")


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    joystick_tester = JoyStickTester(pygame_connector)
    LOGGER.setLevel("DEBUG")
    while True:
        state = joystick_tester.get_state()
        print("Current state")

        time.sleep(0.1)
