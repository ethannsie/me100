from machine import ADC, Pin, PWM, Timer
#from board import get_pin
from time import sleep, ticks_ms
from micropython import schedule
import machine


# Function to simplify input of duty cycle for pwm
def pwm_percent(percent):
    out = int(percent * 1023 / 100)
    return out


# Define pins to use with DRV8833
AIN1 = Pin(32, mode=Pin.OUT)
AIN2 = Pin(15, mode=Pin.OUT)

#need to initalize BIN1 and BIN2 if using second motor
#BIN1 = Pin(XX, mode=Pin.OUT)
#BIN2 = Pin(XX, mode=Pin.OUT)

# Forward at 100% speed
pwm_MotorA1 = PWM(AIN1, freq=10, duty=pwm_percent(100))
pwm_MotorA2 = PWM(AIN2, freq=10, duty=pwm_percent(100))
#pwm_MotorB1 = PWM(BIN1, freq=10, duty=pwm_percent())
#pwm_MotorB2 = PWM(BIN2, freq=10, duty=pwm_percent())
sleep(2)


# Forward at 50% speed
pwm_MotorA1.duty(pwm_percent(50))
pwm_MotorA2.duty(pwm_percent(0))
sleep(2)

# Stop
pwm_MotorA1.duty(pwm_percent(0))
pwm_MotorA2.duty(pwm_percent(0))
sleep(2)

# Reverse at 50% speed
pwm_MotorA1.duty(pwm_percent(0))
pwm_MotorA2.duty(pwm_percent(50))
sleep(2)

# Reverse at 100% speed
pwm_MotorA1.duty(pwm_percent(0))
pwm_MotorA2.duty(pwm_percent(100))
sleep(2)


# De-initialize Timers
#sleep(15)
pwm_MotorA1.deinit()
pwm_MotorA2.deinit()
# pwm_MotorB1.deinit()
# pwm_MotorB2.deinit()




