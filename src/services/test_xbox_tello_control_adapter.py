import time
from pygame_connector import PyGameConnector
from xbox_tello_control_adapter import XboxTelloControlAdapter
from xbox_xs_series_controller import XboxXsSeriesPyGameJoystick


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    xbox_controller = XboxXsSeriesPyGameJoystick(pygame_connector)

    # Create an instance of XboxTelloControlAdapter with the Xbox controller
    tello_control_adapter = XboxTelloControlAdapter(xbox_controller)

    while True:
        # Test the get_state method
        tello_control_state = tello_control_adapter.get_state()

        # Print the TelloControlState object
        print("TelloControlState:")
        print(
            f"Forward/Backward Velocity: {tello_control_state.forward_backward_velocity}"
        )
        print(f"Left/Right Velocity: {tello_control_state.left_right_velocity}")
        print(f"Up/Down Velocity: {tello_control_state.up_down_velocity}")
        print(f"Yaw Velocity: {tello_control_state.yaw_velocity}")
        print(f"Events: {tello_control_state.events}")

        time.sleep(0.1)
