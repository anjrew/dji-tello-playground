# Not verified working on normal Tello!

from djitellopy import Tello

import time


# Create a Tello instance
tello = Tello()

# Connect to Tello
tello.connect()

print("Starting motors ...")
tello.turn_motor_on()

print("Running for...")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

print("Stopping motors ...")
# Land
tello.turn_motor_off()

# End the connection
tello.end()
