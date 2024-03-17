import argparse
from tello_service import TelloService
from djitellopy import Tello
from pygame_connector import PyGameConnector
from tello_controller import KeyboardController
from tello_frontend import FrontEnd

import logging

args = argparse.ArgumentParser()

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


def main():

    pygame_connector = PyGameConnector()
    controller = KeyboardController(pygame_connector)
    tello = Tello()
    tello_service = TelloService(tello)
    tello_service.connect()
    tello_service.streamon()
    frontend = FrontEnd(controller, tello_service)
    frontend.run()


if __name__ == "__main__":
    main()
