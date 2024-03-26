import time
from pygame_connector import PyGameConnector
from xbox_tello_control_adapter import XboxTelloControlAdapter
from services.xbox_360_controller import Xbox360PyGameJoystick


if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    xbox_controller = Xbox360PyGameJoystick(pygame_connector)

    # Create an instance of XboxTelloControlAdapter with the Xbox controller
    tello_control_adapter = XboxTelloControlAdapter(xbox_controller)

    while True:
        # Test the get_state method
        tello_control_state = tello_control_adapter.get_state()

        # Print the TelloControlState object
        print("TelloControlState:")
        print(f"Forward Velocity: {tello_control_state.forward_velocity}")
        print(f"Right Velocity: {tello_control_state.right_velocity}")
        print(f"Up Velocity: {tello_control_state.up_velocity}")
        print(f"Yaw Right Velocity: {tello_control_state.yaw_right_velocity}")
        print(f"Events: {tello_control_state.events}")

        time.sleep(0.1)
