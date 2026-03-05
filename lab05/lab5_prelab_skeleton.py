from machine import Pin, PWM, Timer
from time import sleep

### Copy over led pinout setup command here ###
#led = Pin(13, Pin.OUT)
led = Pin(13, Pin.OPEN_DRAIN) 
######

brightness = 0
L1 = PWM(led, freq=500, duty=brightness)

def led_cb(timer):   
    global brightness  # Variable 'brightness' is a percentage
    print(brightness)
    L1.duty(int(brightness * 1023 / 100))
    
    ### Set up loop for LED to go from off to gradually on then back ###
    brightness += 1
    
    if (brightness >= 100):
        brightness = 0
        
    ######

    print(brightness)


t1 = Timer(1)
t1.init(period=50, mode=t1.PERIODIC, callback=led_cb)


# Deinitialize the timer after some time (enough for 3 cycles in this case)...
sleep(15.1)
t1.deinit()
L1.deinit()
print('All timers deinitialized.')