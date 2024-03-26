from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from typing import List


class TelloActionType(Enum):
    TAKEOFF = 0
    LAND = 1
    EMERGENCY_LAND = 2
    INCREASE_SPEED_CM_S = 3
    DECREASE_SPEED_CM_S = 4


@dataclass
class TelloControlState:
    """
    This state represents the desired state for the tello.
    A digital twin of the tello that should be sent to the tello so it can try and replicate it
    """

    # The control range [-100, 100]
    MIN_VAL = -100
    MAX_VAL = 100

    # Speed range cm/s
    MIN_SPEED = 10
    MAX_SPEED = 100

    # Direction variables
    right_velocity: int
    forward_velocity: int
    up_velocity: int
    yaw_right_velocity: int

    # A list of events coming from the controller
    events: List[TelloActionType]

    def __post_init__(self):
        self.validate_direction("right_velocity", self.right_velocity)
        self.validate_direction("forward_velocity", self.forward_velocity)
        self.validate_direction("up_velocity", self.up_velocity)
        self.validate_direction("yaw_right_velocity", self.yaw_right_velocity)

    def validate_direction(self, attribute_name: str, value: int):
        if not isinstance(value, int):
            raise ValueError(f"Value needs to be an integer. Got {type(value)}")
        if not (self.MIN_VAL <= value <= self.MAX_VAL):
            raise ValueError(
                f"Value {value} for attribute '{attribute_name}' is not in the range [{self.MIN_VAL}, {self.MAX_VAL}]"
            )

    def to_dict(self):
        return asdict(self)


class TelloController(ABC):
    @abstractmethod
    def get_state(self) -> TelloControlState:
        """Gets the current controller state of the drone"""
