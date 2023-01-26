# Streaming sensor data from Ultrasonic Sensor HC-SR04 to the no-code platform Tulip using Thonny IDE, MQTT Explorer and Node-Red
Written by: Ismet Catovic. Credit to Divya Kara who has done a similar project using MQTT, Node-Red and InfluxDB to stream sensor data to Grafana. Click on the following link for more details of Divya's project: https://github.com/divyakara/VM-IoT#project-overview

This project is about connecting the sensors to Tulip.

## Project overview

The purpose of this project is to explain how to set up two HC-SR04 Ultrasonic Sensors using the MicroPython firmware. Moreover, I will explain how to send data from the sensor to NODE-Red and Tulip.

## Materials

The first sensor uses the ESP32 device from AZ-Delivery (Fig. 1) and the other sensor uses the Wemos D1 Mini ESP8266 motherboard (Fig 2). Figure 3 shows how the sensor looks like.

## Environment setup

The following were used when setting up the environment for the two sensors:

- Thonny IDE: A beginner-friendly Python editor. Download it by entering the following link: https://thonny.org/
  - NOTE: Two instances of this IDE are required in order for both sensors to work simultaneously. When installing the IDE and running it, enter Tools > Options >    General > unmark Allow only single Thonny Instance.
- Node-RED: A flow diagram that sends data from Thonny to Tulip using the MQTT.
  - Node-RED can be accessed by selecting one of the Edge Devices by their IP address available in your local Tulip instance. When entering the menu of the Edge I/O, click on the Node-RED editor link.
- Edge I/O: A Tulip compatible edge device required for sending data between Tulip and Thonny using Node-RED.
- Tulip Platform: A no-code platform that receives data from the Node-RED diagram created through the Edge IO.
- MQTT Explorer: A MQTT application that...


