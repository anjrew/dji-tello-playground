"""

"""
import sys
import os

script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, "..")
sys.path.append(parent_dir)

import argparse
import time
from typing import Callable, Dict, Literal
from services.tello_command_dispatcher import TelloCommandDispatcher
from services.tello_connector import TelloConnector
from djitellopy import Tello
from joysticks.pygame_connector import PyGameConnector
from joysticks.game_controller_type import GameControllerType
from joysticks.xbox_one_controller import XboxOnePyGameController
from joysticks.xbox_controller import XboxPyGameController
from services.tello_controller import TelloController
from tello_adapters.xbox_one_tello_adapter import XboxOneTelloControlAdapter
from tello_adapters.xbox_controller_tello_adapter import XboxTelloControlAdapter
from keyboard_controller import KeyboardControlAdapter

import logging

LOGGER = logging.getLogger(__name__)

controller_mapping: Dict[
    GameControllerType, Callable[[PyGameConnector], TelloController]
] = {
    GameControllerType.XBOX360: lambda connector: XboxTelloControlAdapter(
        XboxPyGameController(connector)
    ),
    GameControllerType.KEYBOARD: lambda connector: KeyboardControlAdapter(connector),
    GameControllerType.XBOXONE: lambda connector: XboxOneTelloControlAdapter(
        XboxOnePyGameController(connector)
    ),
}


def main(
    ctrl_type: Literal[
        "xbox360",
        "keyboard",
        "xboxone",
    ],
    cadence_secs: float,
    log_level: str,
) -> None:
    logging.basicConfig(level=log_level)
    LOGGER = logging.getLogger(__name__)

    pygame_connector = PyGameConnector()

    controller: TelloController

    try:
        controller_type = GameControllerType[ctrl_type.upper()]
        controller = controller_mapping[controller_type](pygame_connector)
    except KeyError:
        raise ValueError(f"Unsupported controller type: {ctrl_type}")

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
        default=GameControllerType.XBOX360,
        choices=list([x.name.lower() for x in GameControllerType]),
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
