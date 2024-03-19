from typing import Callable
from djitellopy import Tello

import time

SPEED_SETTING_CM_S = 30

# Create a Tello instance
tello = Tello()

# Connect to Tello
tello.connect()

print("Starting flying in ...")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

# Takeoff
print("Take off")
tello.takeoff()

print("Setting speed to", SPEED_SETTING_CM_S)
tello.set_speed(SPEED_SETTING_CM_S)


def do_action_for_time(action: Callable, time_in_seconds: int):
    action()
    time.sleep(time_in_seconds)


left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = 0
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

# Move forward
left_right_velocity = 0
forward_backward_velocity = 1
up_down_velocity = 0
yaw_velocity = 0
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

# Move Backwards
left_right_velocity = 0
forward_backward_velocity = -1
up_down_velocity = 0
yaw_velocity = 0
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)


# Move Left
left_right_velocity = 1
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = 0
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

# Move Right
left_right_velocity = -1
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = 0
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

# Move Up
left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = 1
yaw_velocity = 0
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

# Move down
left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = -1
yaw_velocity = 0
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

# Turn Left
left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = 1
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

# Turn Right
left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = -1
do_action_for_time(
    lambda: tello.send_rc_control(
        left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    ),
    1,
)

print("Landing")
# Land
tello.land()

# End the connection
tello.end()
