# DJI Tello Drone Playground

Welcome to the DJI Tello Drone Playground! This project is designed for enthusiasts and learners who want to explore the capabilities of the DJI Tello drone through a series of practical exercises.

# Getting Started

1. [Setup your development environment](./docs/setting_up_the_environment.md).
2. Connect to the drone.
3. Work through the exercises


## Setup Drone Connection

To interact with the drone, you must first establish a WiFi connection:

1. Power on your DJI Tello drone.
2. Connect your computer to the drone's WiFi network.

    ![Connecting to Tello WiFi](./docs/images/trello_wifi.png)

    The WiFi network typically appears as `TELLO-XXXXXX`. Default password is usually `12345678`.

## Exercises

Dive into various exercises located in the `src` folder. Each script guides you through different functionalities of the DJI Tello drone.

1. **Manual Control with Smartphone**
   
   Learn how to control the drone manually using your smartphone.

   Firstly lets get a feel for the drone by controlling it manually. Download the Tello app on your smartphone and connect to the drone's WiFi network. Open the app and you should see a live feed from the drone's camera. You can now control the drone using the on-screen controls.

   [Download](https://www.dji.com/de/downloads/djiapp/tello)

2. **Simple Takeoff**
   
   [Script](./src/simple_takeoff_land.py) for basic takeoff and landing.

   Here we will write a simple script to takeoff and land the drone. The drone will takeoff, hover for a few seconds, and then land.

3. **Follow with Face Detection**
   
   Implement face detection to make the drone follow a person.

   Here we will implement face detection to make the drone follow a person. The drone will takeoff to a height of 1 meter, and then follow the person around. If the person moves out of the drone's field of view, the drone will follow the person around until they are back in the center of the view.

4. **Navigate Route**
   
   Program the drone to navigate a predefined route. Try to achieve the fastest lap for an added challenge!

   In this challenge, we will program the drone to navigate a predefined route. The drone will takeoff, and then navigate a predefined route. The drone must navigate to gate in order. The drone will should land once the route is complete.

5. **Orchestrate Swarm**
   
   Explore controlling multiple drones simultaneously.

   Now it is time to work together with your fellow drone pilots! In this challenge, we will explore controlling multiple drones simultaneously. The drones will takeoff and then fly in formation. The drones will then land once the formation is complete.

6. **Do Stunts**
   
   Execute and customize various drone stunts.

   Lets get a little crazy! In this challenge, we will explore the various stunts that the drone can perform. The drone will takeoff and then perform a series of stunts. The drone will then land once the stunts are complete.

7. **Make Deliveries**
   
   Simulate delivery tasks using the drone.

   Lets get some work done here. In this challenge, we will simulate delivery tasks using the drone. The drone will takeoff and then navigate to a delivery location. The drone will then drop off the package and return to the starting location. The drone will then land once the delivery is complete.

To run an exercise, navigate to the `src` folder and execute the corresponding script:

```bash
python src/<script_name>.py
```

Replace <script_name> with the script you wish to run.

## Debugging with Visual Studio Code

To enhance your coding and debugging experience, we recommend using Visual Studio Code (VS Code). For guidance on setting up and using the debugger in VS Code with your DJI Tello scripts, refer to this detailed guide:

Using VS Code Debugger with DJI Tello

This guide covers everything from setting up VS Code to step-by-step instructions for using the debugger effectively.

For more detailed instructions, troubleshooting, or to contribute to this project, please refer to our contribution guidelines and the issue tracker.


## Dev Container with VS Code

This project includes a dev container for VS Code. This allows you to develop and debug your code in a containerized environment. This is useful if you don't want to install Python and other dependencies on your local machine.

**Note:** At the moment, the dev container is only working and tested on Ubuntu Linux systems.

To use the dev container, follow these steps:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in VS Code
3. Open the project in VS Code
4. Click the green "Open a Remote Window" button in the bottom left corner of VS Code
5. Select "Remote-Containers: Reopen in Container" from the menu
6. VS Code will now build the dev container and open the project inside the container