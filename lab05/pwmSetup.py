from machine import Pin, PWM

# PWM 1 → 5 kHz, 20% duty
pwm1 = PWM(Pin(25))
pwm1.freq(5000)
pwm1.duty(205)

# PWM 2 → 8 kHz, 60% duty
pwm2 = PWM(Pin(26))
pwm2.freq(8000)
pwm2.duty(614)