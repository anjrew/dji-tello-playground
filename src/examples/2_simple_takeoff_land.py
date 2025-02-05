from djitellopy import Tello

import time

# Create a Tello instance
tello = Tello()

print("Attempting to connect to drone ...")

# Connect to Tello
tello.connect()

print("Starting flying in ...")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

# Takeoff
print("Take off")
tello.takeoff()

print("Hovering for...")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

print("Landing")
# Land
tello.land()

# End the connection
tello.end()
