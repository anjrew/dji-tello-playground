from tello_service import TelloService
from djitellopy import Tello
from pygame_connector import PyGameConnector
from tello_controller import KeyboardController
from tello_frontend import FrontEnd


def main():

    pygame_connector = PyGameConnector()
    controller = KeyboardController(pygame_connector)
    tello = Tello()
    tello_service = TelloService(tello)
    frontend = FrontEnd(controller, tello_service)
    frontend.run()


if __name__ == "__main__":
    main()