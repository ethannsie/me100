from machine import DAC, ADC, Pin, PWM, Timer
from time import sleep

# Set pins A0 and A2 for DAC and ADC respectively
xcontrol = Pin(34, mode=Pin.IN)
ycontrol = Pin(39, mode=Pin.IN)
swcontrol = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)

# Assign DAC and ADC converter objects to each pin
adc_x = ADC(xcontrol)
adc_y = ADC(ycontrol)
# adc.val(0)
# ADC configs
adc_x.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_y.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_val = 0  # set val of ADC to dummy value to start off


# Print DAC and ADC values with a 100 ms delay
def position(timer):
    global adc_x
    global adc_y
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()
    sw_val = swcontrol()
    print("Joystic (ADC): X =", adc_val_x, "Y =", adc_val_y, "SW =", sw_val)

# Swivel the joystick and see what numbers you get! What's the range, why? How 
# could you use this code to help you code certain colors to match certain
# joystick positions? 

t_position = Timer(4)
t_position.init(period=100, mode=t_position.PERIODIC, callback=position)


sleep(20)
t_position.deinit()
