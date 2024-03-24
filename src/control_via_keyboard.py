import argparse
from services.tello_connector import TelloConnector
from djitellopy import Tello
from services.pygame_connector import PyGameConnector
from services.keyboard_controller import KeyboardController
from services.tello_frontend import FrontEnd

import logging

args = argparse.ArgumentParser()

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


def main():

    pygame_connector = PyGameConnector()
    controller = KeyboardController(pygame_connector)
    tello = Tello()
    tello_service = TelloConnector(tello)
    tello_service.connect()
    tello_service.streamon()
    frontend = FrontEnd(controller, tello_service)
    frontend.run()


if __name__ == "__main__":
    main()
