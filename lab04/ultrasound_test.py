from rcwl1601 import HCSR04
from machine import Pin,I2C
import time

sensor = HCSR04(trigger_pin=14, echo_pin=22,echo_timeout_us=1000000)

try:
  while True:
    distance = sensor.distance_cm()
    time.sleep(2)
    print(distance)
except KeyboardInterrupt:
        pass
