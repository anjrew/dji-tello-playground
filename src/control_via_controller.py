import argparse
import time
from typing import Union
from services.tello_command_dispatcher import TelloCommandDispatcher
from services.tello_connector import TelloConnector
from djitellopy import Tello
from joysticks.pygame_connector import PyGameConnector
from services.xbox_tello_control_adapter import XboxTelloControlAdapter

# from services.xbox_one_tello_control_adapter import XboxOneTelloControlAdapter
from joysticks.xbox_controller_linux import XboxPyGameJoystick
from joysticks.xbox_one_controller import XboxOnePyGameJoystick

import logging

args = argparse.ArgumentParser()
args.add_argument(
    "--controller",
    default="xbox360",
    choices=["xbox360", "xboxone"],
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


def main(controller_type: str, cadence_secs: float, log_level: str) -> None:
    logging.basicConfig(level=log_level)
    LOGGER = logging.getLogger(__name__)

    pygame_connector = PyGameConnector()

    joystick: Union[XboxPyGameJoystick, XboxOnePyGameJoystick]
    controller: XboxTelloControlAdapter
    # controller: Union[XboxTelloControlAdapter, XboxOneTelloControlAdapter]

    if controller_type == "xbox360":
        joystick = XboxPyGameJoystick(pygame_connector)
        controller = XboxTelloControlAdapter(joystick)
    # elif controller_type == "xboxone":
    #     joystick = XboxOnePyGameJoystick(pygame_connector)
    #     controller = XboxOneTelloControlAdapter(joystick)
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
    parsed_args = args.parse_args()
    main(parsed_args.controller, parsed_args.cadence, parsed_args.log_level)
