import network
import espnow
import time
from rcwl1601 import HCSR04
import struct
from machine import Pin,I2C

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\x0C\x8B\x95\xB7\xC4\xD8'   # MAC address of peer's wifi interface
# me = f4 65 0b 30 a8 30

e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")

sensor = HCSR04(trigger_pin=14, echo_pin=22,echo_timeout_us=1000000)

try:
  while True:
    distance = sensor.distance_cm()
    time.sleep(0.25)
    format_string = '>fH'

    # Pack the data into a bytes object
    packed_data = struct.pack(format_string, distance)

    # Convert to a mutable bytearray if desired
    data_bytearray = bytearray(packed_data)
    
    e.send(peer, data_bytearray)
except KeyboardInterrupt:
        pass


e.send(peer, b'end')

