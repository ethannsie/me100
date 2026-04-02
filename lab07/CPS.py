from machine import Pin, PWM, Timer
from time import sleep

""" You may need to change pinouts from your board depending on what you use """

encoder_count = 0


def counter(__):
    global encoder_count
    encoder_count = encoder_count + 1


def calculate_speed(timer):
    global encoder_count
    global number_of_degrees_per_encoder_tick
    delta_t = 1  # delta_t = 1 sec, as we're calling back this function every 1000ms
    speed = encoder_count * number_of_degrees_per_encoder_tick / delta_t
    print('CPS is', encoder_count)
    print('Speed is', speed, 'deg/s')
    # Reset the counter for the next speed
    encoder_count = 0


# def duty_u16(value):
#     return int(value / 100 * (2 ** 16 - 1))

def pwm_percent(percent):
    return int(percent * 1023 / 100)

def forward(speed):
    AIN1.duty(pwm_percent(100))
    AIN2.duty(pwm_percent(speed))

def reverse(speed):
    AIN1.duty(pwm_percent(speed))
    AIN2.duty(pwm_percent(100))

def stop():
    AIN1.duty(pwm_percent(100))
    AIN2.duty(pwm_percent(100))

# """AIN1 and AIN2"""
# motor_vpin = Pin(XX, mode=Pin.OUT)
# motor_gnd = Pin(XX, mode=Pin.OUT)
# 
# """ percent Full power motor (sometimes does not run below 33%"""
# speed_as_percent = 30
# L1 = PWM(motor_vpin, freq=1000, duty_u16=duty_u16(speed_as_percent))
# motor_gnd.value(0)

"""AIN1 and AIN2"""
AIN1 = PWM(Pin(XX), freq=10000, duty=1023)
AIN2 = PWM(Pin(XX), freq=10000, duty=1023)

"""See how many times the encoder is getting triggered"""
encoder_0 = Pin(XX, mode=Pin.IN)
encoder_0.irq(handler=counter, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

"""Find the average speed"""
number_of_degrees_per_encoder_tick = 0.28
t1 = Timer(1)
t1.init(period=1000, mode=t1.PERIODIC, callback=calculate_speed)

forward(0)
sleep(2)

forward(50)
sleep(2)

stop()
sleep(2)

reverse(50)
sleep(2)

reverse(0)
sleep(2)

t1.deinit()
AIN1.deinit()
AIN2.deinit()

