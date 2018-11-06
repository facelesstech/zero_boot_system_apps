#! /usr/bin/env python

# Screen stuff
from pygame.locals import *
from subprocess import call

import pygame, math

screen = pygame.display.set_mode((480, 320),pygame.NOFRAME)
pygame.font.init()
smallfont = pygame.font.SysFont('freesansbold.ttf', 30)
midfont = pygame.font.SysFont('freesansbold.ttf', 50)
bigfont = pygame.font.SysFont('freesansbold.ttf', 100)
pygame.mouse.set_visible(False)

white = (255,255,255) # White colour
red = (255,0,0) # Colours for the red dot
green = (0,255,0) # Colours for the red dot
blue = (0,0,255) # Colours for the red dot
bright_green = (0,0,255) # Colours for the red dot
black = (0,0,0) # Colours for the red dot

import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

maxRead = 0
minRead = 0
breathRead = 0
firstTime = 0

counter = 3
start = time.time()
reading = 0
showIt = 0 
recal = 0

# A recreation of the mapping function used in arduino
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

while True:

    if (firstTime == 0):
        print "startup"
        minRead = adc.read_adc(0, gain=GAIN)
        maxRead = adc.read_adc(0, gain=GAIN) + 15000
        breathRead = adc.read_adc(0, gain=GAIN) 
        print minRead
        print maxRead
        firstTime = 1

    input_state = GPIO.input(23)
    if (input_state == False):
        showIt = 1
        print('Button Pressed')
        reading = 1
        time.sleep(0.2)

    input_state = GPIO.input(18)
    if (input_state == False):
        showIt = 1 
        print('Button Pressed 2')
        recal = 1
        time.sleep(0.2)

    if (reading == 1):
        if time.time() - start > 1:
            start = time.time()
            counter = counter - 1

            ### This will be updated once per second
            print "%s seconds remaining" % counter

            breathRead = adc.read_adc(0, gain=GAIN) 
            screen.fill(white)
            textsurface = bigfont.render("blow", True, black) # Draw text
            screen.blit(textsurface,(150,120)) # Draw text
            pygame.display.update()

            ### Countdown finished, ending loop
            if counter <= 0:
                reading = 0 
                showIt = 0 
                counter = 3

    if (recal == 1):
        screen.fill(white)
        textsurface = bigfont.render("Recalibrating", True, black) # Draw text
        screen.blit(textsurface,(15,120)) # Draw text
        pygame.display.update()

        minRead = adc.read_adc(0, gain=GAIN)
        maxRead = adc.read_adc(0, gain=GAIN) + 10000
        breathRead = adc.read_adc(0, gain=GAIN) 
        print minRead
        print maxRead

        recal = 0 
        showIt = 0

        
    if (showIt == 0):
        print "showIt"
        mapped_value = translate(breathRead, minRead, maxRead, 0, 10)
        string_number_drunk_level = "%d" % mapped_value
#        print string_number_drunk_level
#        print adc.read_adc(0, gain=GAIN)
#        print minRead
#        print maxRead
#        print mapped_value 

        rounded = int("%d" % mapped_value)
        print rounded 
        time.sleep(2)
        showIt = 1
        screen.fill(white)

        pygame.draw.rect(screen, red, pygame.Rect(10, 255, 25, 25))
        textsurface = smallfont.render("Recalibrate", True, red) # Draw text
        screen.blit(textsurface,(40,260)) # Draw text

        pygame.draw.rect(screen, green, pygame.Rect(10, 285, 25, 25))
        textsurface = smallfont.render("Take reading", True, green) # Draw text
        screen.blit(textsurface,(40,290)) # Draw text

        textsurface = bigfont.render("Drunk score", True, black) # Draw text
        screen.blit(textsurface,(40,10)) # Draw text

        textsurface = bigfont.render(string_number_drunk_level, True, black) # Draw text
        screen.blit(textsurface,(220,70)) # Draw text

        textsurface = smallfont.render("Exit", True, black) # Draw text
        screen.blit(textsurface,(430,290)) # Draw text

        textsurface = smallfont.render("Shutdown", True, black) # Draw text
        screen.blit(textsurface,(300,290)) # Draw text

        pygame.display.flip()
        pygame.display.update()

        if (rounded == 0):
            print "sober" 
            textsurface = midfont.render("Sober as a judge", True, black) # Draw text #        screen.blit(textsurface,(430,300)) # Draw text
            screen.blit(textsurface,(100,150)) # Draw text
            pygame.display.update()

        if (rounded == 1):
            textsurface = midfont.render("Are you even trying", True, black) # Draw text
            screen.blit(textsurface,(80,150)) # Draw text
            pygame.display.update()
            
        if (rounded == 2):
            textsurface = midfont.render("Can you feel it", True, black) # Draw text
            screen.blit(textsurface,(120,150)) # Draw text
            pygame.display.update()

        if (rounded == 3):
            textsurface = midfont.render("Now your talking", True, black) # Draw text
            screen.blit(textsurface,(110,150)) # Draw text
            pygame.display.update()

        if (rounded == 4):
            textsurface = midfont.render("Now the party is", True, black) # Draw text
            screen.blit(textsurface,(100,150)) # Draw text
            textsurface = midfont.render("getting started", True, black) # Draw text
            screen.blit(textsurface,(110,190)) # Draw text
            pygame.display.update()

        if (rounded == 5):
            textsurface = midfont.render("You might want to", True, black) # Draw text
            screen.blit(textsurface,(95,150)) # Draw text
            textsurface = midfont.render("start on the shots", True, black) # Draw text
            screen.blit(textsurface,(100,190)) # Draw text
            pygame.display.update()

        if (rounded == 6):
            textsurface = midfont.render("Your well on your way", True, black) # Draw text
            screen.blit(textsurface,(60,150)) # Draw text
            pygame.display.update()
            
        if (rounded == 7):
            textsurface = midfont.render("Your on a roll", True, black) # Draw text
            screen.blit(textsurface,(130,150)) # Draw text
            textsurface = midfont.render("get another one", True, black) # Draw text
            screen.blit(textsurface,(110,190)) # Draw text
            pygame.display.update()

        if (rounded == 8):
            textsurface = midfont.render("Pretty impressive", True, black) # Draw text
            screen.blit(textsurface,(100,150)) # Draw text
            textsurface = midfont.render("have you puked yet?", True, black) # Draw text
            screen.blit(textsurface,(80,190)) # Draw text
            pygame.display.update()

        if (rounded == 9):
            textsurface = midfont.render("The room will be", True, black) # Draw text
            screen.blit(textsurface,(100,150)) # Draw text
            textsurface = midfont.render("spinning tonight", True, black) # Draw text
            screen.blit(textsurface,(100,190)) # Draw text
            pygame.display.update()

        if (rounded == 10):
            textsurface = midfont.render("Your steaming", True, black) # Draw text
            screen.blit(textsurface,(110,150)) # Draw text
            pygame.display.update()

    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print pos
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print pos
            #Find which quarter of the screen we're in
            x,y = pos
            if y > 290 and x > 400:
                print("exit")
                pygame.quit() # Quits the python script
            if y > 290 and x < 400 and x > 170:
                print("shutdown")
                call(["sudo", "shutdown", "-h", "now" ])
