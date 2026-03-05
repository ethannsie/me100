from machine import Pin, PWM, Timer, reset
from time import sleep
from bachnotes import bach

# The pin you want to use (usual pin setup)
speaker = Pin(...)
pwm_speaker = PWM(speaker, freq=131, duty=200) # Don't change the duty cycle of the speaker. Instead, modify its frequency to change the note being played. 

note_index = 0


"""This is the loop version (Part C4). For part C5, use the later code and comment this out. """

for note in bach:
    
    # What should the frequency be? (Hint: check the bachnotes.py file)
    pwm_speaker.freq(...)
    
    sleep(.5) #The length of time each note gets played

"""Loop version ends here"""



"""This is the timer version (Part C5). For part C4, use the previous code and comment this out.
Note also, the blinking light code should be inserted above this, but they should be able to run concurrently"""
def tcb_speaker(timer):
    global note_index
    
    #Similar to before
    pwm_speaker.freq(...)
    
    if note_index == len(bach):
        #Restart the song
        note_index = ...
    else:
        #Move on to the next note
        note_index = ...
    

t1 = Timer(1) #Note once you incorporate the blinking LED you will need to change this to a different numbered timer, ie Timer(2)
t1.init(period=100, mode=t1.PERIODIC, callback=tcb_speaker)

sleep(15)
t1.deinit() # Need to deinitialize timer at the end (clean up)
print('All timers deinitialized.')

"""Timer version ends here"""

pwm_speaker.deinit()  # Need to deinitialize pwm at the end (clean up)
print('All PWM deinitialized.')

