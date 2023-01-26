# Streaming sensor data from Ultrasonic Sensor HC-SR04 to the no-code platform Tulip using Thonny IDE, MQTT Explorer and Node-RED
Written by: Ismet Catovic. Credit to Divya Kara who has done a similar project using MQTT, Node-Red and InfluxDB to stream sensor data to Grafana. Click on the following link for more details of Divya's project: https://github.com/divyakara/VM-IoT#project-overview

This project is about connecting the sensors to Tulip.

## Project overview

The purpose of this project is to explain how to set up two HC-SR04 Ultrasonic Sensors using the MicroPython firmware. Moreover, I will explain how to send data from the sensor to NODE-Red and Tulip.

### Materials

The first sensor uses the ESP32 device from AZ-Delivery (Fig. 1) and the other sensor uses the Wemos D1 Mini ESP8266 motherboard (Fig 2). Figure 3 shows how the sensor looks like.

Each sensor is placed on separate breadboards.

### Environment setup

The following were used when setting up the environment for the two sensors:

- Thonny IDE: A beginner-friendly Python editor. Download it by entering the following link: https://thonny.org/
  - NOTE: Two instances of this IDE are required in order for both sensors to work simultaneously. When installing the IDE and running it, enter Tools > Options >    General > unmark Allow only single Thonny Instance.
- Node-RED: A flow diagram that sends data from Thonny to Tulip using the MQTT.
  - Node-RED can be accessed by selecting one of the Edge Devices by their IP address available in your local Tulip instance. When entering the menu of the Edge I/O, click on the Node-RED editor link.
- Edge I/O: A Tulip compatible edge device required for sending data between Tulip and Thonny using Node-RED.
- Tulip Platform: A no-code platform that receives data from the Node-RED diagram created through the Edge IO.
- Python (latest version)

## Instructions

Below are instructions how to setup the two scanners using different motherboards.

Each Thonny IDE instance will have a different intepreter.

### Setting up the sensor with ESP32 (pictures will come later)

1. Setup the motherboard according to the circuit diagram below.

2. Install esptool.py and setuptools by entering the following commands
```
pip install esptool
pip install setuptools
python -m esptool
```

3. Connect the motherboard to your computer using a USB cable. A red light on the motherboard should turn on if properly connected. Find and remember which COM port is used by opening the device manager on Windows (see Ports.) NOTE: If the port is not detected, download the USB serial driver here https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads.

4. Download the latest version of MicroPython from https://micropython.org/download/#esp32. Select ESP32 by Espressif and download the latest .bin release.

5. Open Thonny IDE and select Run > Configure Intepreter

### Setting up the sensor with ESP8266 (pictures will come later)

1. Setup the motherboard according to the circuit diagram below.

2. 


