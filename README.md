# Streaming sensor data from Ultrasonic Sensor HC-SR04 to the no-code platform Tulip using Thonny IDE, MQTT Explorer and Node-RED.

Written by: Ismet Catovic. Credits to Divya Kara who has done a similar project using MQTT, Node-Red and InfluxDB to stream sensor data to Grafana. Click on the following link for more details of Divya's project: https://github.com/divyakara/VM-IoT#project-overview

This project is about connecting the sensors to Tulip.

## Project overview

The purpose of this project is to explain how to set up two HC-SR04 Ultrasonic Sensors using the MicroPython firmware. Moreover, I will explain how to send data from the sensor to NODE-Red and Tulip.

### Materials

The first sensor uses the ESP32 device from AZ-Delivery (Fig. 1) and the other sensor uses the Wemos D1 Mini ESP8266 motherboard (Fig 2). Figure 3 shows how the sensor looks like.

Each sensor is placed on separate breadboards.

### Environment setup

The following were used when setting up the environment for the two sensors:

- Thonny IDE: A beginner-friendly Python editor. Download it by entering the following link: https://thonny.org/
  - NOTE! Two instances of this IDE are required in order for both sensors to work simultaneously. When installing the IDE and running it, enter Tools > Options >    General > unmark Allow only single Thonny Instance.
- Node-RED: A flow diagram that sends data from Thonny to Tulip using the MQTT.
  - Node-RED can be accessed by selecting one of the Edge Devices by their IP address available in your local Tulip instance. When entering the menu of the Edge I/O, click on the Node-RED editor link.
- Edge I/O: A Tulip compatible edge device required for sending data between Tulip and Thonny using Node-RED.
- Tulip Platform: A no-code platform that receives data from the Node-RED diagram created through the Edge IO.
- Python (latest version)

## Instructions

Below are instructions how to setup the two scanners using different motherboards.

Each Thonny IDE instance will have a different intepreter.

### Setting up the sensor with ESP32 (pictures will come later)

1. Setup the motherboard on the breadboard according to the circuit diagram below.

2. Install esptool.py and setuptools by entering the following commands
```
pip install esptool
pip install setuptools
python -m esptool
```

3. Connect the motherboard to your computer using a USB cable. A red light on the motherboard should turn on if properly connected. Find and remember which COM port is used by opening the device manager on Windows (see Ports.) 

  NOTE! If the port is not detected and is unknown, download the USB serial driver here https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads. Unzip the downloaded file, enter the device manager and find the COM port that is unknown. Update the driver by browsing your computer for drivers and select the CP2012 folder that you have unzipped. The name of the Silicon Valley driver should appear.

4. Download the latest version of MicroPython from https://micropython.org/download/#esp32. Select ESP32 by Espressif and download the latest .bin release.
5. Open Thonny IDE options and enter the Interpreter section. Select MicroPython (ESP32) as the interpreter and select Silicon Labs CP210x USB to UART Bridge (COMx) as the port.
6. Before pressing OK in the Thonny Options window, click on "Install or update MicroPython" and select the same port you have chosen on the previous step. The firmware is the .bin file downloaded on step 4. Then, select From image file (Keep) as the flash mode and check "Erase flash before installing." Press Install, this process may take a minute. When the installation is done, leave the window and press OK. You are now configuring the motherboard om COMx.
7. Copy the following HC-SR04 MicroPython Library into a file in Thonny and save the script with the name hcsr04.py to the MicroPython device. The library can be found in https://github.com/rsc1975/micropython-hcsr04 and is not part of the standard MicroPython library by default.

```

import machine, time
from machine import Pin

__version__ = '0.2.0'
__author__ = 'Roberto Sánchez'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin. 
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms

```

8. 


### Setting up the sensor with ESP8266 (pictures will come later)

1. Setup the motherboard according to the circuit diagram below.

2. 

Links helpful for this project:
https://randomnerdtutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/


