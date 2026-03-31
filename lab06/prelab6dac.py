from machine import DAC, ADC, Pin
from time import sleep

# Set pins A0 and A2 for DAC and ADC respectively
dac_pin = Pin(25,mode=Pin.OUT)
adc_pin = Pin(32,mode=Pin.IN)

# Assign DAC and ADC converter objects to each pin
dac = DAC(dac_pin)
adc = ADC(adc_pin)
#adc.val(0)
# ADC configs
adc.atten(ADC.ATTN_11DB) #change range of converter to be V_ref = 3.2
adc_val = 0 # set val of ADC to dummy value to start off

# Print DAC and ADC values with a 100 ms delay
for i in range(255):
    print("DAC:",i)
    dac.write(i)
    adc_val = adc.read_u16()
    print("ADC:",adc_val)
    sleep(0.1)
    


