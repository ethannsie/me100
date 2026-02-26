import network
import espnow
from machine import Pin
import struct

led = Pin(13, mode=Pin.OUT)

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

print("Receiver ready. Waiting for messages...")

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        if msg == b'end':
            break
    dist_cm = struct.unpack('>f', msg)[0] 
    if dist_cm < 5:
        led.value(1)
        print(f"WARNING: {dist_cm:.2f} cm < 5 cm (LED ON)")
    else:
        led.value(0)
        print(f"{dist_cm:.2f} cm (LED OFF)")
    
