import argparse
import time
import logging
from services.tello_command_dispatcher import TelloCommandDispatcher
from services.tello_connector import TelloConnector
from xbox_controller_tello_adapter import XboxTelloControlAdapter
from joysticks.pygame_connector import PyGameConnector
from joysticks.xbox_controller_linux import XboxPyGameJoystick
from djitellopy import Tello

args = argparse.ArgumentParser()

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)

CADENCE_SECS = 0.1


def main():

    pygame_connector = PyGameConnector()
    joystick = XboxPyGameJoystick(pygame_connector)
    controller = XboxTelloControlAdapter(joystick)
    tello = Tello()
    tello_service = TelloConnector(tello)
    tello_service.connect()
    dispatcher = TelloCommandDispatcher(tello_service)

    while True:
        time.sleep(CADENCE_SECS)
        try:

            control_state = controller.get_state()
            dispatcher.send_commands(control_state)
        except Exception as e:
            LOGGER.error(e, "Error Issuing command")


if __name__ == "__main__":
    main()
