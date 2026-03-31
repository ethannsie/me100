from machine import Pin
from time import sleep

# Define pins
ENC_1 = Pin(XX, Pin.IN)
ENC_2 = Pin(XX, Pin.IN)

while True:
    e1 = ENC_1.value()
    e2 = ENC_2.value()

    print("E1 = {}, E2 = {}".format(e1, e2))

    sleep(0.1) 
    
    