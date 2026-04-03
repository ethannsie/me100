from machine import Pin
from time import ticks_ms, ticks_diff, sleep

count = 0
last_press = 0

button = Pin(14, Pin.IN, Pin.PULL_UP)

def button_handler(pin):
    global count, last_press
    now = ticks_ms()
    if ticks_diff(now, last_press) > 200:
        count += 1
        last_press = now
        print("Button presses:", count)

button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

sleep(30)
