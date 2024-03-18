from abc import ABC, abstractmethod
from typing import List

from models.tello_control_event import TelloControlEvent


class Controller(ABC):

    @abstractmethod
    def get_actions(self) -> List[TelloControlEvent]:
        pass
