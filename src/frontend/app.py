import argparse
import asyncio
from tello_service import TelloService
from djitellopy import Tello
from pygame_connector import PyGameConnector
from tello_controller import KeyboardController
from tello_frontend import FrontEnd

import logging

args = argparse.ArgumentParser()

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


async def main():
    pygame_connector = PyGameConnector()
    controller = KeyboardController(pygame_connector)
    tello = Tello()
    tello_service = TelloService(tello)
    tello_service.connect()

    frontend = FrontEnd(controller, tello_service)

    # Run the pygame event loop, frontend, and controller tasks concurrently
    await asyncio.gather(pygame_connector.run(), frontend.run(), controller.run())


if __name__ == "__main__":
    asyncio.run(main())
