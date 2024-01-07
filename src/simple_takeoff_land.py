from djitellopy import Tello

# Create a Tello instance
tello = Tello()

# Connect to Tello
tello.connect()

# Check battery
print(f"Battery: {tello.get_battery()}%")

# Takeoff
tello.takeoff()

# Perform a simple movement
tello.move_up(30)

# Land
tello.land()

# End the connection
tello.end()
