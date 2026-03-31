from machine import ADC, Pin, PWM, Timer
from neopixel import NeoPixel
from time import sleep

# Set pins respectively
xcontrol = Pin($$, mode=Pin.IN)
ycontrol = Pin($$, mode=Pin.IN)
button = Pin($$, mode=Pin.IN, pull=Pin.PULL_UP)

# Assign DAC and ADC converter objects to each pin
adc_x = ADC(xcontrol)
adc_y = ADC(ycontrol)
# adc.val(0)
# ADC configs
adc_x.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_y.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_val = 0  # set val of ADC to dummy value to start off

pwr = Pin(2, Pin.OUT) # Initialize NeoPixel
pwr.value(1)
np = NeoPixel(Pin(0), 1)

np[0] = (0,0,0) # Start with NeoPixel OFF
np.write()
print('Neopixel OFF')

def position(timer):
    global adc_x
    global adc_y
    global adc_val_x
    global adc_val_y
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()
    sw_val = button()

def NEO_cb(timer):
    red = 0
    green = 0
    blue = 0
    global adc_x
    global adc_y
    
    # When the joystick is at its "neutral" or unmoved position, 
    # there should not be any light

    #See whiteboard for diagram of Joystick and NEO behavior

    if $$$$$ < adc_val_x < $$$$$ and $$$$$ < adc_val_y < $$$$$:
        green = 0
        red = 0
        blue = 0

    # NEO should become more green as joystick is pushed further left
    elif adc_val_x < $$$$$: 
        green = int(($$$$$-adv_val_x) * 255/$$$$$)
                     
    # What about blue? 
    else:     
        ... 

    # And red? 
    if adc_val_y < $$$$$: 
        ...

    # Feel free to change the inequalities to number ranges that make more sense to you. 
    # If done correctly, NEO should also show some intermediary colors when the joystick is swiveled! (ex. a pinkish/purple)

    np[0] = (red, green, blue)
    np.write()

t3 = Timer(3)
t3.init(period=200, mode=t3.PERIODIC, callback=position)
t4 = Timer(4)
t4.init(period=100, mode=t4.PERIODIC, callback=NEO_cb)

sleep(30)
t3.deinit()
t4.deinit()

        
