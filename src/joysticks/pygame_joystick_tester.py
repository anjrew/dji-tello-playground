import logging
import time

try:
    from joysticks.pygame_connector import PyGameConnector
except ModuleNotFoundError:
    from pygame_connector import PyGameConnector

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

    def get_state(self) -> str:
        self.pygame_connector.get_events()
        state = f"Reading out {self.joystick.get_name()} state {time.time()}\n"
        for axis in range(self.joystick.get_numaxes()):
            state += f"Axis {axis} value: {self.joystick.get_axis(axis)}\n"
        for button in range(self.joystick.get_numbuttons()):
            state += f"Button {button} value: {self.joystick.get_button(button)}\n"
        for hat in range(self.joystick.get_numhats()):
            state += f"Hat {hat} value: {self.joystick.get_hat(hat)}\n"
        return state


if __name__ == "__main__":
    import os

    logging.basicConfig(level=logging.INFO)
    LOGGER.setLevel("DEBUG")

    pygame_connector = PyGameConnector()
    joystick_tester = JoyStickTester(pygame_connector)

    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear the console
        print("\033[1;1H")  # Move the cursor to the top-left corner
        state = joystick_tester.get_state()
        print("Current state:")
        print(state)
        time.sleep(0.1)
