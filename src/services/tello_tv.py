from services.tello_connector import TelloConnector


class TelloTV:

    def __init__(self, connector: TelloConnector):
        self.connector = connector
