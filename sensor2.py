from machine import Pin, I2C
import ssd1306
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
CLIENT_NAME = '080 Tulip/Work Instructions and TAKT/ESP8266/Sensor2'
BROKER_ADDR = '172.16.2.7'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

BTN_TOPIC_DIST = CLIENT_NAME.encode() + b'/distance'

# ESP8266
sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)

oled_width = 128
oled_height = 64


graph = ""
timerCount = 0

while True:
    try:
      timerCount += 0.5;
      sleep(0.5)
      distance = sensor.distance_mm()
      print('Distance:', distance, 'mm')
      #print(timerCount)
      
      mqttc.publish( BTN_TOPIC_DIST, (str(distance).encode()) )
    except OSError as e:
        print("FAILED")
