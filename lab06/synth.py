### Skeleton Code for Part E, Synthesizer and Light Show

# These comments are to help you figure out what code to copy and paste, 
# and where you will need some changes/additions.

# You are welcome to ignore these comments and just dump code, 
# but that may be more confusing to debug.

# IMPORTS
# put all your imports here

## INITIALIZATIONS
# Buzzer Pin and PWM (previous code from lab 5)
# Button from part C (dummy variables, button or switch pin, initialization)
# NeoPixel from part D (xcontrol and ycontrol pins, DAC/ADC conversion, initalization)
# Joystick and debouncing dummy variables

## FUNCTIONS
# Speaker/Buzzer function
# ISR handler function for the button (from Part C), and report function if you want to use it to help debug
# Position function in x-and-y code or neo code
# Neopixel function (from part D) 

## TIMERS
# Speaker/Buzzer Timer, use a period of 250
# You should have 3 timers

# sleep for 30-60 seconds

## DEINITIALIZE
# You should have 3 timers, 1 PWM function to deinitialize


# If everything you've written up to this point is correct
# you will only need to reduce redundancies and modify the
# speaker/buzzer interrupt function.

# HINT: When you press the joystick button, your counter should
# increase by 1. When the counter is even, we want to play the 
# bach tune, but when the counter is odd, we want to change the 
# frequency and duty cycle of the Buzzer PWM while the speaker/buzzer 
# plays a note. What mathematical operator can we utilize to 
# capture this functionality? Also note that adc_val_x and adc_val_y 
# are defined as global variables. 

# DO NOT USE TRY/CATCH or STATE MATCHINE code. These are beyond the scope 
# of this class and will only confuse you. We will not help debug 
# such code. 