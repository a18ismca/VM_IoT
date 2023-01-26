from machine import Pin, I2C
from hcsr04 import HCSR04
from time import sleep
import dht
import network
from umqtt.simple import MQTTClient

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

connect_wifi("Virtual-GBG", "awellhiddensecret")



#Broker
CLIENT_NAME = '080 Tulip/Work Instructions and TAKT/ESP32/Sensor1'
BROKER_ADDR = '172.16.2.7'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

#Topics
BTN_TOPIC_DIST = CLIENT_NAME.encode() + b'/distance'

# Assign the trigger and the echo pin of the sensor
# where these pins are wired to the ESP32 pins

sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

graph = ""
timerCount = 0

while True:
    try:
      timerCount += 0.5;
      
      # The distance is printed out on the shell terminal each 0.5 secs
      sleep(0.5)
      distance = sensor.distance_mm(),
      print('Distance:', distance, 'mm')
      print(timerCount)
      
      mqttc.publish( BTN_TOPIC_DIST, (str(distance).encode()) )
    except OSError as e:
        print("FAILED")
