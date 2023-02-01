# Streaming sensor data from Ultrasonic sensor HC-SR04 to the no-code platform Tulip using Thonny IDE, MQTT Explorer and Node-RED

As of 26.01.2022, I am still working on this README file.

Written by Ismet Catovic. Credits to Divya Kara who has done a similar project using MQTT, Node-Red and InfluxDB to stream sensor data to Grafana. Click on the following link for more details of Divya's project: https://github.com/divyakara/VM-IoT

This project is about connecting the sensors to Tulip.

## Project overview

The purpose of this project is to explain how to set up two HC-SR04 Ultrasonic Sensors using the MicroPython firmware. Moreover, I will explain how to send data from the sensor to NODE-Red and Tulip.

### Materials

The first sensor uses the ESP32 device from AZ-Delivery (Fig. 1) and the other sensor uses the Wemos D1 Mini ESP8266 motherboard (Fig 2). Figure 3 shows how the sensor looks like.

![ESP32-WROOM-32 Motherboard](https://user-images.githubusercontent.com/62876523/215799986-183ab8ab-fea5-4151-a419-ea437d50762f.png)

Figure 1. The ESP32-WROOM-32 motherboard manufactured by AZ-Delivery.

![Lolin Wemos D1](https://user-images.githubusercontent.com/62876523/215805672-2d8db976-6757-4d0f-ac14-a6785e92d703.jpeg)

Figure 2. The Wemos D1 ESP8266 motherboard manufactured by Lolin.

![202860728-c3ccac67-ddfc-421f-8d99-2e3cc3d8aa6a](https://user-images.githubusercontent.com/62876523/215801924-347cf8d5-c40e-4202-9e24-90afd702e666.png)

Figure 3. The HC-SR04 Ultrasonic sensor.

Each sensor and motherboard is using separate breadboards.

### Environment setup

The following were used when setting up the environment for the two sensors:

- Thonny IDE: A beginner-friendly Python editor. Download it by entering the following link: https://thonny.org/
  - NOTE! Two instances of this IDE are required in order for both sensors to work simultaneously. When installing the IDE and running it, enter Tools > Options >          General, then unmark Allow only single Thonny Instance.
- Node-RED: A flow diagram that sends data from Thonny to Tulip using the MQTT.
  - Node-RED can be accessed by selecting one of the Edge Devices by their IP address available in your local Tulip instance. When entering the menu of the Edge I/O,       click on the Node-RED editor link.
- Edge I/O: A Tulip compatible edge device required for sending data between Tulip and Thonny using Node-RED.
- Tulip Platform: A no-code platform that receives data from the Node-RED diagram created through the Edge IO.
- Python (latest version)

## Instructions

Below are instructions how to setup the two scanners using different motherboards.

Each Thonny IDE instance will have a different intepreter.

### Setting up the sensor with ESP32 (pictures will come later)

1. Setup the motherboard on the breadboard according to the circuit diagram below.

![Circuit Diagram AZ-Delivery ESP32-WROOM-32 jpg](https://user-images.githubusercontent.com/62876523/215798947-b83b623d-9e07-45c1-a751-db97a09bbacb.jpg)

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
7. Copy the following HC-SR04 MicroPython Library into a file in Thonny and save the script with the name hcsr04.py to the MicroPython device. The library can be found in https://github.com/rsc1975/micropython-hcsr04 and is not part of the standard MicroPython library by default. It is recommended to save the library under a separate folder, in case the COM port of any motherboards changes when reconnecting the motherboards to different USB ports.

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

8. Create a new script with the name sensor1.py. Import the following libraries:
```
from machine import Pin, I2C
from hcsr04 import HCSR04
from time import sleep
import dht
import network
from umqtt.simple import MQTTClient
```
9. Add the following connect_wifi function to the script in order to enable connection to the router.

```
def connect_wifi(ssid, password):   

#connect to wifi
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
  print('Network config:', wlan.ifconfig())
  print('Connected to ', ssid)
```
Remember to use the def by entering its parameters. The ssid is the name of the WLAN.

10. Connect to the broker by assigning CLIENT_NAME to the broker where the data should be sent. The BROKER_ADDR is assigned to the IP address of the Tulip edge device. When done, define the topics. Use the code below for help.

```
CLIENT_NAME = '080 Tulip/Work Instructions and TAKT/ESP32/Sensor1'
BROKER_ADDR = '172.16.2.7'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

#Topics
BTN_TOPIC_DIST = CLIENT_NAME.encode() + b'/distance'
```

11. Define the sensor by using the HCSR04 class available in hcsr04.py. Set the trigger_pin and the echo_pin according to the circuit diagram.

```
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

graph = ""
timerCount = 0
```

12. Copy the code below which runs the sensor and measure its distance.

```
while True:
    try:
      timerCount += 0.5;
      
      # The distance is printed out on the shell terminal each 0.5 seconds
      sleep(0.5)
      distance = sensor.distance_mm(),
      print('Distance:', distance, 'mm')
      print(timerCount)
      
      # Publish the distances on MQTT. The outputs are represented using the MQTT Explorer.
      mqttc.publish( BTN_TOPIC_DIST, (str(distance).encode()) )
    except OSError as e:
        print("FAILED")
```

13. Save the file as a sensor1.py script and run it. If the sensor works properly, the distance will vary for each half second.

#### MQTT Explorer (Keep the sensor1.py script running in Thonny while configuring MQTT Explorer)

14. Download the MQTT Explorer file on the following link: http://mqtt-explorer.com/. Install it.

15. When opening the MQTT Explorer, add a connection and name it as you want. Use the mqtt:// as a protocol and the 172.16.2.7. Use any port you want, I have used port 1883. Save the connection and then press connect. You will receive data from the script running (I will add a picture here.)

#### Tulip

16. Enter the Machines section in Tulip. If desired, create a new machine type where the machines that you will create are related to the sensors you have setted up.

17. Go the machine type where the machines will be created and add a machine attribute that is related to the distance from the sensor. The data type should be a number.

18. Return to the Machines section and create a machine that belongs to the machine type where the sensors will be stored. When the machine is created, map the machine attribute you have created for the sensor to the Tulip API data source. (Select a machine > Configuration > Attributes Unmapped).

19. A JSON object that has a machine ID and an attribute ID should appear when the attribute has been mapped to the Tulip API. Copy and save the JSON object in case you forget how the object looked like.

#### Node-RED

20. Access the edge device by its local IP address.

21. Create a Node-RED flow diagram according to the one below (picture is missing)

### Setting up the sensor with ESP8266 (pictures will come later)

1. Setup the motherboard according to the circuit diagram below.

![Circuit Diagram Wemos D1 Mini ESP8266 jpg](https://user-images.githubusercontent.com/62876523/215798813-8faaef98-5c49-42ef-a10f-ff2121305566.jpg)

2. Enter Device Manager and see if the motherboard has been properly connected. USB-SERIAL CH340 should be shown under the Ports section.

3. Download the latest version of MicroPython from https://micropython.org/download/esp8266-1m/. Download the latest .bin release.

Links helpful for this project:
https://randomnerdtutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/


