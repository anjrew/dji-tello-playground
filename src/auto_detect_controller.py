import sys
import os

script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, "..")
sys.path.append(parent_dir)

from typing import Dict, Callable, Optional
from services.tello_command_dispatcher import TelloCommandDispatcher
from services.tello_connector import TelloConnector
from djitellopy import Tello
from joysticks.pygame_connector import PyGameConnector
from services.tello_controller import TelloController
from tello_adapters.xbox_one_tello_adapter import XboxOneTelloControlAdapter
from tello_adapters.xbox_controller_tello_adapter import XboxTelloControlAdapter
from joysticks.xbox_one_controller import XboxOnePyGameController
from joysticks.xbox_controller import XboxPyGameController
from joysticks.game_controller_type import GameControllerType
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


def get_controller_type(platform: str, joystick_name: str) -> GameControllerType:
    mapping = {
        # Linux
        "linux": {},
        # MAC
        "darwin": {"Xbox Series X Controller": GameControllerType.XBOX360},
        # Windows
        "win": {},
    }
    try:
        return mapping[platform][joystick_name]
    except KeyError:
        raise ValueError(
            f"No Controller type mapping found for platform {platform} and joystick name {joystick_name}"
        )


def main(
    log_level: int = logging.DEBUG,
) -> None:
    logging.basicConfig(level=log_level)
    LOGGER = logging.getLogger(__name__)

    controller: Optional[TelloController] = None
    try:

        pygame_connector = PyGameConnector()
        pygame_connector.init_joystick()
        joystick = pygame_connector.create_joystick(0)
        joystick.init()

        name = joystick.get_name()
        platform = sys.platform

        controller_type = get_controller_type(platform, name)
        controller = controller_mapping[controller_type](pygame_connector)
    except (KeyError, ValueError) as e:
        LOGGER.error(f"Error detecting controller: {e}")
        LOGGER.info("Defaulting to Keyboard Controller")
        controller = KeyboardControlAdapter(PyGameConnector())

    tello = Tello()
    tello_service = TelloConnector(tello)
    tello_service.connect()

    dispatcher = TelloCommandDispatcher(tello_service)

    while True:
        try:
            control_state = controller.get_state()
            dispatcher.send_commands(control_state)
        except Exception as e:
            LOGGER.error(e, "Error Issuing command")


if __name__ == "__main__":
    main()
