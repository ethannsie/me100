import network
import espnow
import time

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
for i in range(100):
    e.send(peer, "Hi! I've sent this many messages: " + str(i), True)
    time.sleep(1)
    # Arguments for send are Mac address of receiver, message string, and whether or not to wait for a
    # confirmation from the receiver that the message has been received before moving on from this line (good for debugging). 
e.send(peer, b'end')
