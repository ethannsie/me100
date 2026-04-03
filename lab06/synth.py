from machine import Pin, PWM, ADC, Timer
from neopixel import NeoPixel
from time import sleep, ticks_ms, ticks_diff

# ==================================================
# NOTES
# ==================================================
C3 = 131
CS3 = 139
D3 = 147
DS3 = 156
E3 = 165
F3 = 175
FS3 = 185
G3 = 196
GS3 = 208
A3 = 220
AS3 = 233
B3 = 247
C4 = 262
CS4 = 277
D4 = 294
DS4 = 311
E4 = 330
F4 = 349
FS4 = 370
G4 = 392
GS4 = 415
A4 = 440
AS4 = 466
B4 = 494
C5 = 523
CS5 = 554
D5 = 587
DS5 = 622
E5 = 659
F5 = 698
FS5 = 740
G5 = 784
GS5 = 831
A5 = 880
AS5 = 932
B5 = 988
C6 = 1047
CS6 = 1109
D6 = 1175
DS6 = 1245
E6 = 1319
F6 = 1397
FS6 = 1480
G6 = 1568
GS6 = 1661
A6 = 1760
AS6 = 1865
B6 = 1976
C7 = 2093
CS7 = 2217
D7 = 2349
DS7 = 2489
E7 = 2637
F7 = 2794
FS7 = 2960
G7 = 3136
GS7 = 3322
A7 = 3520
AS7 = 3729
B7 = 3951
C8 = 4186
CS8 = 4435
D8 = 4699
DS8 = 4978

bach = [
    C4, E4, G4, C5, E5, G4, C5, E5, C4, E4, G4, C5, E5, G4, C5, E5,
    C4, D4, G4, D5, F5, G4, D5, F5, C4, D4, G4, D5, F5, G4, D5, F5,
    B3, D4, G4, D5, F5, G4, D5, F5, B3, D4, G4, D5, F5, G4, D5, F5,
    C4, E4, G4, C5, E5, G4, C5, E5, C4, E4, G4, C5, E5, G4, C5, E5,
    C4, E4, A4, E5, A5, A4, E5, A4, C4, E4, A4, E5, A5, A4, E5, A4,
    C4, D4, FS4, A4, D5, FS4, A4, D5, C4, D4, FS4, A4, D5, FS4, A4, D5,
    B3, D4, G4, D5, G5, G4, D5, G5, B3, D4, G4, D5, G5, G4, D5, G5,
    B3, C4, E4, G4, C5, E4, G4, C5, B3, C4, E4, G4, C5, E4, G4, C5,
    B3, C4, E4, G4, C5, E4, G4, C5, B3, C4, E4, G4, C5, E4, G4, C5,
    A3, C4, E4, G4, C5, E4, G4, C5, A3, C4, E4, G4, C5, E4, G4, C5,
    D3, A3, D4, FS4, C5, D4, FS4, C5, D3, A3, D4, FS4, C5, D4, FS4, C5,
    G3, B3, D4, G4, B4, D4, G4, B4, G3, B3, D4, G4, B4, D4, G4, B4
]

# ==================================================
# INITIALIZATION
# ==================================================

# Buzzer
buzzer = PWM(Pin(27))
buzzer.freq(bach[0])
buzzer.duty(512)

# LED from previous lab
led = PWM(Pin(13))
led.freq(5000)
led.duty(512)

# Joystick pins
xcontrol = Pin(34, Pin.IN)
ycontrol = Pin(39, Pin.IN)
button = Pin(14, Pin.IN, Pin.PULL_UP)

adc_x = ADC(xcontrol)
adc_y = ADC(ycontrol)
adc_x.atten(ADC.ATTN_11DB)
adc_y.atten(ADC.ATTN_11DB)

# NeoPixel
pwr = Pin(2, Pin.OUT)
pwr.value(1)
np = NeoPixel(Pin(0), 1)
np[0] = (0, 0, 0)
np.write()

# ==================================================
# GLOBAL VARIABLES
# ==================================================
i = 0
count = 0
last_press = 0

adc_val_x = 0
adc_val_y = 0

# Change these if your center values are different
x_center_low = 30000
x_center_high = 35000
y_center_low = 30000
y_center_high = 35000

# ==================================================
# FUNCTIONS
# ==================================================

def button_handler(pin):
    global count, last_press
    now = ticks_ms()
    if ticks_diff(now, last_press) > 200:
        count += 1
        last_press = now
        print("Button presses:", count, " Mode:", count % 2)

def position(timer):
    global adc_val_x, adc_val_y
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()

def neopixel_cb(timer):
    global adc_val_x, adc_val_y, count

    red = 0
    green = 0
    blue = 0

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

    # up/down = red
    # If red appears in the wrong direction, swap these two conditions
    if adc_val_y < y_center_low:
        red = int((y_center_low - adc_val_y) * 255 / y_center_low)
    elif adc_val_y > y_center_high:
        red = int((adc_val_y - y_center_high) * 255 / (65535 - y_center_high))

    red = max(0, min(255, red))
    green = max(0, min(255, green))
    blue = max(0, min(255, blue))

    # only show colors in synth mode
    if count % 2 == 1:
        np[0] = (red, green, blue)
    else:
        np[0] = (0, 0, 0)

    np.write()

def buzzer_cb(timer):
    global i, count, adc_val_x, adc_val_y

    # Mode 0: play Bach tune
    if count % 2 == 0:
        buzzer.freq(bach[i])
        buzzer.duty(512)
        led.duty((i * 40) % 1023)
        i += 1
        if i >= len(bach):
            i = 0

    # Mode 1: synthesizer mode
    else:
        # Y controls frequency
        freq = 200 + int(adc_val_y * 800 / 65535)

        # X controls duty cycle
        duty = int(adc_val_x * 1023 / 65535)

        buzzer.freq(freq)
        buzzer.duty(duty)

        # keep LED alive too
        led.duty(duty)

# ==================================================
# INTERRUPT
# ==================================================
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# ==================================================
# TIMERS
# ==================================================
t1 = Timer(1)
t1.init(period=100, mode=Timer.PERIODIC, callback=position)

t2 = Timer(2)
t2.init(period=100, mode=Timer.PERIODIC, callback=neopixel_cb)

t3 = Timer(3)
t3.init(period=250, mode=Timer.PERIODIC, callback=buzzer_cb)

# ==================================================
# RUN
# ==================================================
sleep(60)

# ==================================================
# CLEANUP
# ==================================================
t1.deinit()
t2.deinit()
t3.deinit()

buzzer.deinit()
led.deinit()

np[0] = (0, 0, 0)
np.write()
