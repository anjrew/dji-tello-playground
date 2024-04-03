import argparse
import time
from services.tello_command_dispatcher import TelloCommandDispatcher
from services.tello_connector import TelloConnector
from djitellopy import Tello
from joysticks.pygame_connector import PyGameConnector
from services.tello_controller import TelloController
from src.xbox_one_tello_adapter import XboxOneTelloControlAdapter
from xbox_controller_tello_adapter import XboxTelloControlAdapter
from joysticks.xbox_one_controller import XboxOnePyGameController
from joysticks.xbox_controller import XboxPyGameController
from keyboard_controller import KeyboardControlAdapter

import logging

LOGGER = logging.getLogger(__name__)

from enum import Enum


class _ControllerType(Enum):
    XBOX360 = "xbox360"
    KEYBOARD = "keyboard"
    XBOXONE = "xboxone"


def main(controller_type: str, cadence_secs: float, log_level: str) -> None:
    logging.basicConfig(level=log_level)
    LOGGER = logging.getLogger(__name__)

    pygame_connector = PyGameConnector()

    controller: TelloController

    if controller_type == _ControllerType.XBOX360:
        joystick = XboxPyGameController(pygame_connector)
        controller = XboxTelloControlAdapter(joystick)
    if controller_type == _ControllerType.KEYBOARD:
        controller = KeyboardControlAdapter(pygame_connector)
    elif controller_type == _ControllerType.XBOXONE:
        joystick = XboxOnePyGameController(pygame_connector)
        controller = XboxOneTelloControlAdapter(joystick)
    else:
        raise ValueError(f"Unsupported controller type: {controller_type}")

    tello = Tello()
    tello_service = TelloConnector(tello)
    tello_service.connect()

    dispatcher = TelloCommandDispatcher(tello_service)

    while True:
        time.sleep(cadence_secs)
        try:
            control_state = controller.get_state()
            dispatcher.send_commands(control_state)
        except Exception as e:
            LOGGER.error(e, "Error Issuing command")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--controller",
        default=_ControllerType.XBOX360,
        choices=list(_ControllerType),
        help="Specify the controller type (default: xbox360)",
    )
    args.add_argument(
        "--cadence",
        type=float,
        default=0.1,
        help="Specify the cadence in seconds (default: 0.1)",
    )
    args.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Specify the log level (default: INFO)",
    )
    parsed_args = args.parse_args()
    main(parsed_args.controller, parsed_args.cadence, parsed_args.log_level)
