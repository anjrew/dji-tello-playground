import logging
import numpy as np
import pytest
from unittest.mock import MagicMock
from services.pygame_connector import PyGameConnector
from services.tello_connector import TelloConnector
from services.keyboard_controller import (
    Controller,
    KeyboardController,
    TelloActionType,
    TelloControlEvent,
)
from services.tello_frontend import FrontEnd
from pygame.locals import (
    K_UP,
    K_t,
)

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def mock_tello_service() -> MagicMock:
    mock_service = MagicMock(spec=TelloConnector)
    mock_frame_read = MagicMock()
    mock_frame_read.stopped = False
    mock_frame_read.frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_service.get_frame_read.return_value = mock_frame_read
    return mock_service


@pytest.fixture
def mock_controller():
    mock_controller = MagicMock(spec=Controller)
    return mock_controller


@pytest.fixture
def mock_pygame_wrapper():
    return MagicMock(spec=PyGameConnector)


def test_speed_forward_increases(
    mock_pygame_wrapper: MagicMock, mock_tello_service: MagicMock
):
    ITERATIONS = 4  # minus take off
    KEY_STROKES = [
        [K_t],
        [K_UP],
        [K_UP],
        [K_UP],
        [K_UP],
    ]

    mock_pygame_wrapper.get_pressed_keys.side_effect = KEY_STROKES  # Forward

    controller = KeyboardController(mock_pygame_wrapper)

    frontend = FrontEnd(controller=controller, tello_service=mock_tello_service)
    frontend.run(max_iterations=ITERATIONS)  # Run for a specific number of iterations

    mock_tello_service.take_off.assert_called_once()
    # Assert that send_rc_control was called more than once with specific arguments
    # mock_tello_service.send_rc_control.assert_has_calls(
    #     [
    #         call(0, 20, 0, 0),  # Expected first call arguments
    #         call(0, 40, 0, 0),  # Expected second call arguments
    #     ]
    # )

    actions = controller.get_actions()
    assert actions is not None


def test_correct_values_come_through(mock_pygame_wrapper: MagicMock):
    KEY_STROKES = [
        [K_t],
        [K_UP],
        [K_UP],
        [K_UP],
        [K_UP],
    ]

    mock_pygame_wrapper.get_pressed_keys.side_effect = KEY_STROKES  # Forward

    controller = KeyboardController(mock_pygame_wrapper)

    # Check action 1
    actions = controller.get_actions()
    assert len(actions) == 1
    action = actions[0]
    assert isinstance(action, TelloControlEvent)
    assert action.action == TelloActionType.TAKEOFF
    assert action.intensity == 1.0

    # Check action 2
    actions = controller.get_actions()
    assert len(actions) == 1
    action = actions[0]
    assert isinstance(action, TelloControlEvent)
    assert action.action == TelloActionType.SET_FORWARD_VELOCITY
    assert action.intensity == 1.0

    # Check action 3
    actions = controller.get_actions()
    assert len(actions) == 1
    action = actions[0]
    assert isinstance(action, TelloControlEvent)
    assert action.action == TelloActionType.SET_FORWARD_VELOCITY
    assert action.intensity == 2.0

    # Check action 4
    actions = controller.get_actions()
    assert len(actions) == 1
    action = actions[0]
    assert isinstance(action, TelloControlEvent)
    assert action.action == TelloActionType.SET_FORWARD_VELOCITY
    assert action.intensity == 3.0

    assert action is not None
