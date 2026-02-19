from umqtt.simple import MQTTClient
from math import sin
import network
import sys
from ina219 import INA219
from machine import SoftI2C, Pin
import time


i2c = SoftI2C(scl=Pin(20), sda=Pin(22)) # Need to change scl & sda GPIO Pin number (enter only the number inside the parenthesis)

print("scanning I2C bus ...")
print("I2C:", i2c.scan())

SHUNT_RESISTOR_OHMS = 0.1
ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
ina.configure()

"""
Send measurement results from microphyton board to host computer.
Use in combination with mqtt_plot_host.py.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_host.py
session = 'ethansie/esp32/helloworld'
BROKER = 'broker.hivemq.com'

# check wifi c1onnection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(client_id="esp32_ethansie",server=BROKER,port=1883)
mqtt.connect()
print("Connected!")

# send data
# In this sample, we send "fake" data. Replace this code to send useful data,
# e.g. measurement results.

voltage = ina.voltage()         
current_mA = ina.current()       
power_mW = ina.power()

current_A = current_mA/1000

if current_A != 0:
    load_resistance = voltage / current_A
else:
    load_resistance = float('inf')

powerList = []
currIndex = 0

while load_resistance > 500:
    voltage = ina.voltage()         
    current_mA = ina.current()       
    power_mW = ina.power()
    
    current_A = current_mA/1000

    if current_A != 0:
        load_resistance = voltage / current_A
    else:
        load_resistance = float('inf')
    
    powerList.append(power_mW)
    
    if powerList[-1] > powerList[currIndex] * 1.1 or powerList[-1] < powerList[currIndex] * 0.9:
        topic = "{}/data".format(session)
        data = "{},{}".format(power_mW, load_resistance)
        print("send topic='{}' data='{}'".format(topic, data))
        mqtt.publish(topic, data)
        currIndex = len(powerList) - 1
    
    time.sleep(0.3)

# do the plotting (on host)
print("tell host to do the plotting ...")
mqtt.publish("{}/plot".format(session), "create the plot")

# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()