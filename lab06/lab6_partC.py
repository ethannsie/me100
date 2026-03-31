from machine import Pin
from time import sleep, ticks_ms
from micropython import schedule
import machine

# Set variables
counter = 0
state = 0
last_time = ticks_ms()
t = 0 # dummy value
delta_t = 0 # dummy value

button = Pin(##, mode=Pin.IN, pull=Pin.PULL_UP)

# for loop to print button state. Use this code for Part A2 instructions
for i in range(1000):
    print(button.value())
    i = i + 1
    sleep(0.1)

# Comment out the above code for Part A3 and uncomment all the code below

# # Report function to print counter value when ISR callback updated
# def report(pin):
#     global counter
#     global state
#     print('Counter = ' + str(counter))
#     
# # ISR handler function when button is pressed
# def bhandler(pin):
#     global counter
#     global state
#     global last_time
#     global t
#     global delta_t
#
#     counter += 1
#     report(button)
# 
#     # Part A4. Insert below your debounce code (from lecture and posted discussion slides!)
# 
# 
# # Initialize pin with ISR
# button.irq(handler=bhandler,trigger=Pin.CHANGE_ME) # Change the trigger to Pin.IRQ_RISING or Pin.IRQ_FALLING


