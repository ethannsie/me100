from machine import ADC, Pin, Timer
from neopixel import NeoPixel
from time import sleep

xcontrol = Pin(34, mode=Pin.IN)
ycontrol = Pin(39, mode=Pin.IN)
button = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)

adc_x = ADC(xcontrol)
adc_y = ADC(ycontrol)

adc_x.atten(ADC.ATTN_11DB)
adc_y.atten(ADC.ATTN_11DB)

adc_val_x = 0
adc_val_y = 0

pwr = Pin(2, Pin.OUT)
pwr.value(1)
np = NeoPixel(Pin(0), 1)

np[0] = (0, 0, 0)
np.write()

def position(timer):
    global adc_val_x, adc_val_y
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()
    print("X =", adc_val_x, "Y =", adc_val_y)

def NEO_cb(timer):
    global adc_val_x, adc_val_y

    red = 0
    green = 0
    blue = 0

    # adjust these based on your measured center values
    x_center_low = 28000
    x_center_high = 38000
    y_center_low = 28000
    y_center_high = 38000

    # center = off
    if x_center_low < adc_val_x < x_center_high and y_center_low < adc_val_y < y_center_high:
        red = 0
        green = 0
        blue = 0

    # left = green
    elif adc_val_x < x_center_low:
        green = int((x_center_low - adc_val_x) * 255 / x_center_low)

    # right = blue
    elif adc_val_x > x_center_high:
        blue = int((adc_val_x - x_center_high) * 255 / (65535 - x_center_high))

    # up/down controls red
    if adc_val_y < y_center_low:
        red = int((y_center_low - adc_val_y) * 255 / y_center_low)
    elif adc_val_y > y_center_high:
        red = int((adc_val_y - y_center_high) * 255 / (65535 - y_center_high))

    red = max(0, min(255, red))
    green = max(0, min(255, green))
    blue = max(0, min(255, blue))

    np[0] = (red, green, blue)
    np.write()

t3 = Timer(3)
t3.init(period=200, mode=Timer.PERIODIC, callback=position)

t4 = Timer(4)
t4.init(period=100, mode=Timer.PERIODIC, callback=NEO_cb)

sleep(30)

t3.deinit()
t4.deinit()
