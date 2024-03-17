import logging
import numpy as np
import pytest
from unittest.mock import MagicMock
from pygame_connector import PyGameConnector
from tello_service import TelloService
from tello_controller import (
    Controller,
    TelloActionType,
    TelloControlEvent,
)
from tello_frontend import FrontEnd


@pytest.fixture
def mock_tello_service() -> MagicMock:
    mock_service = MagicMock(spec=TelloService)
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


def test_frontend_run(mock_tello_service, mock_controller):

    # Set up the mock controller to return specific actions
    mock_controller.get_action.side_effect = [
        TelloControlEvent(TelloActionType.TAKEOFF, 0),
        TelloControlEvent(TelloActionType.SET_FORWARD_VELOCITY, 0.5),
        TelloControlEvent(TelloActionType.SET_YAW_CLOCKWISE_VELOCITY, 0.3),
        TelloControlEvent(TelloActionType.LAND, 0),
    ]

    frontend = FrontEnd(controller=mock_controller, tello_service=mock_tello_service)
    frontend.run(max_iterations=4)  # Run for a specific number of iterations

    # Verify that the expected methods were called on the mock TelloService
    mock_tello_service.takeoff.assert_called_once()
    mock_tello_service.send_rc_control.assert_called_with(0, 5, 0, 3)
    mock_tello_service.land.assert_called_once()
    mock_tello_service.end.assert_called_once()


def test_frontend_takeoff(mock_tello_service: MagicMock):
    frontend = FrontEnd(controller=MagicMock(), tello_service=mock_tello_service)
    frontend.take_off()
    logging.info(f"takeoff call count: {mock_tello_service.takeoff.call_count}")

    mock_tello_service.takeoff.assert_called_once()
    assert frontend.state.send_rc_control is True


def test_frontend_land(mock_tello_service):
    frontend = FrontEnd(controller=MagicMock(), tello_service=mock_tello_service)
    frontend.land()
    mock_tello_service.land.assert_called_once()
    assert frontend.state.send_rc_control is False


def test_no_action_does_not_throw(mock_tello_service, mock_controller):

    # Set up the mock controller to return specific actions
    mock_controller.get_action.side_effect = [None, None, None, None]

    frontend = FrontEnd(controller=mock_controller, tello_service=mock_tello_service)
    frontend.run(max_iterations=4)  # Run for a specific number of iterations


def test_landing_action_lands(mock_tello_service, mock_controller):

    # Set up the mock controller to return specific actions
    mock_controller.get_action.side_effect = [
        TelloControlEvent(TelloActionType.TAKEOFF, 0),
        TelloControlEvent(TelloActionType.LAND, 0),
    ]

    frontend = FrontEnd(controller=mock_controller, tello_service=mock_tello_service)
    frontend.run(max_iterations=1)  # Run for a specific number of iterations

    mock_tello_service.land.assert_called_once()
