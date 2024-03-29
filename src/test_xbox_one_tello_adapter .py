import time

try:
    from joysticks.pygame_connector import PyGameConnector
    from xbox_one_tello_adapter import XboxTelloControlAdapter
    from joysticks.xbox_one_controller import XboxOnePyGameController
except:
    from .joysticks.pygame_connector import PyGameConnector
    from .xbox_one_tello_adapter import XboxTelloControlAdapter
    from .joysticks.xbox_one_controller import XboxOnePyGameController

if __name__ == "__main__":
    import os

    def print_state(state_dict: dict, indent=""):
        for k, v in state_dict.items():
            if isinstance(v, dict):
                print(f"{indent}{k}:")
                print_state(v, indent + "  ")
            else:
                print(f"{indent}{k}: {v}")

    pygame_connector = PyGameConnector()
    xbox_controller = XboxOnePyGameController(pygame_connector)
    tello_control_adapter = XboxTelloControlAdapter(xbox_controller)

    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear the console
        print("\033[1;1H")  # Move the cursor to the top-left corner

        # Test the get_state method
        tello_control_state = tello_control_adapter.get_state()

        # Print the TelloControlState object
        print("TelloControlState:")
        state_dict = tello_control_state.__dict__
        print_state(state_dict)

        time.sleep(0.1)
