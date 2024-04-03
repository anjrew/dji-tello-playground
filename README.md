# 🛸 DJI Tello Drone Playground

Welcome to the DJI Tello Drone Playground! This project is designed for enthusiasts and learners who want to explore the capabilities of the DJI Tello drone through a series of practical exercises.

# 🚀 Getting Started

1. [Setup your development environment](./docs/setting_up_the_environment.md).
2. [Connect](#setup-drone-connection) to the drone.
3. Try controlling the drone manually with your smartphone. See [this](./docs/manual_control_with_smartphone.md) guide
4. See the [example exercises](./src/examples) in the [`src`](./src/) folder
5. Try some of the other more advanced exercises in the [`src`](./src/) folder
6. Get creative and make your own scripts
7. Have fun!

## 📡 Setup Drone Connection

To interact with the drone, you must first establish a WiFi connection:

1. Power on your DJI Tello drone.
2. Connect your computer to the drone's WiFi network.

    ![Connecting to Tello WiFi](./docs/images/trello_wifi.png)

    The WiFi network typically appears as `TELLO-XXXXXX`. Default password is usually `12345678`.

## 📝 Exercises

Dive into various [example exercises](./src/examples) located in the `src` folder. Each script guides you through different functionalities of the DJI Tello drone.

To run an exercise, navigate to the [`src`](./src/)  folder and execute the corresponding script:

```bash
python src/<script_name>.py
```

Replace <script_name> with the script you wish to run.

## 🔍 Troubleshooting

- See the drone status indicator states [here](./docs/drone_status_indicator_states.md)
- There are some instances where the drones IMU may need to be calibrated. See the [calibration video guide]([./docs/calibrating_the_drone.md](https://youtu.be/ne5bofb7J9Y?si=JrDHTRJOB3Kxdrs4))
- The firmware on the Tello drone may need to be updated. See the [firmware update video guide](https://youtu.be/zHYj1hzlH20?si=KWMkrB6HlDayjDrj)
- To position itself, the drone uses a downward-facing camera. Ensure the surface is well-lit and has distinct features for the drone to detect. Poor lighting or a lack of distinct patterns on the floor may cause the drone to drift or lose position.

## 🐞 Debugging with Visual Studio Code

To enhance your coding and debugging experience, we recommend using the launch configurations with Visual Studio Code (VS Code). 

## 📚 Other Resources

- [Official Docs](https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf)
- [Gamepad Control](https://github.com/cozmobotics/Tello-Swarm-Gamepad)
- [Alternate SDK](https://github.com/ErnGusMik/python-tello/tree/main)
- [Api Repository](https://github.com/honglan3/dji-sdk-DJITelloPy?tab=readme-ov-file)
- [User Manual](https://dl-cdn.ryzerobotics.com/downloads/Tello/20180212/Tello+User+Manual+v1.0_EN_2.12.pdf)
- [Swarm Programming](https://drive.google.com/file/d/1vV73j8Axua5dT8gTwts66TzexJLJBqKR/view)
- [Basic Simulator](https://github.com/Fireline-Science/tello_sim)
- [Advanced Simulator](https://dev.droneblocks.io/simulator.html)
- [YolovV8 Inference Container](https://github.com/anjrew/yolo-v8-inference-container/tree/main?tab=readme-ov-file)
