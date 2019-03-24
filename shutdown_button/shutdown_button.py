# Shtdown button connected to pin 27
# Restart button connected to pin 22 
# LED connected to pin 23

import RPi.GPIO as GPIO
from subprocess import call
import time

GPIO.setmode(GPIO.BCM)  

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set up pin 27 as an output
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set up pin 22 as an output
GPIO.setup(23, GPIO.OUT) # Set up pin 23 as an output

def buttonStateChanged(pin):

    if not (GPIO.input(pin)):
        print"Shutdown button press"
        GPIO.output(23, True) # Turn on pin 23 (LED)
        call(['shutdown', '-h', 'now'], shell=False)

def buttonStateChanged1(pin):

    if not (GPIO.input(pin)):
        print"Restart button press"
        GPIO.output(23, True) # Turn on pin 23 (LED)
        call(['reboot'], shell=False)

GPIO.add_event_detect(27, GPIO.BOTH, callback=buttonStateChanged)
GPIO.add_event_detect(22, GPIO.BOTH, callback=buttonStateChanged1)

while True:
    # sleep to reduce unnecessary CPU usage
    time.sleep(5)
