from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass


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
    left_right_velocity: int
    forward_backward_velocity: int
    up_down_velocity: int
    yaw_velocity: int

    # Other action variables
    speed: int
    take_off: bool
    """If false then the device should be trying to land"""

    def __post_init__(self):
        self.validate_direction("left_right_velocity", self.left_right_velocity)
        self.validate_direction(
            "forward_backward_velocity", self.forward_backward_velocity
        )
        self.validate_direction("up_down_velocity", self.up_down_velocity)
        self.validate_direction("yaw_velocity", self.yaw_velocity)
        if not (self.MIN_SPEED <= self.speed <= self.MAX_SPEED):
            raise ValueError(
                f"Speed {self.speed} is not within the range of {self.MIN_SPEED} and {self.MAX_SPEED}"
            )
        if not isinstance(self.take_off, bool):
            raise ValueError("Take off should be a boolean")

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
