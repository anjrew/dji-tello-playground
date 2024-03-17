from enums.tello_action_type import TelloActionType


class TelloControlEvent:
    def __init__(self, action: TelloActionType, intensity: float):
        self.action = action
        self.intensity = intensity
