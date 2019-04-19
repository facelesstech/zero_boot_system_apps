#! /usr/bin/env python

# Screen stuff
from pygame.locals import *
from subprocess import call

#IR temp stuff
from mlx90614 import MLX90614
thermometer_address = 0x5a
thermometer = MLX90614(thermometer_address)
string_temp = "0C"
string_hold_temp = "0C"

import pygame, math

screen = pygame.display.set_mode((480, 320),pygame.NOFRAME)
pygame.font.init()
smallfont = pygame.font.SysFont('freesansbold.ttf', 30)
midfont = pygame.font.SysFont('freesansbold.ttf', 50)
bigfont = pygame.font.SysFont('freesansbold.ttf', 100)
myFontTopbar = pygame.font.SysFont('freesansbold.ttf', 30)
pygame.mouse.set_visible(False)

white = (255,255,255) # White colour
red = (255,0,0) # Colours for the red dot
green = (0,255,0) # Colours for the red dot
blue = (0,0,255) # Colours for the red dot
bright_green = (0,0,255) # Colours for the red dot
black = (0,0,0) # Colours for the red dot

import time

# Import the ADS1x15 module.
#import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
#GAIN = 1

maxRead = 0
minRead = 0
breathRead = 0
firstTime = 0

counter = 1.5
start = time.time()
reading = 0
hold = 0
showIt = 0 
recal = 0

# A recreation of the mapping function used in arduino
#def translate(value, leftMin, leftMax, rightMin, rightMax):
#    # Figure out how 'wide' each range is
#    leftSpan = leftMax - leftMin
#    rightSpan = rightMax - rightMin
#
#    # Convert the left range into a 0-1 range (float)
#    valueScaled = float(value - leftMin) / float(leftSpan)
#
#    # Convert the 0-1 range into a value in the right range.
#    return rightMin + (valueScaled * rightSpan)

while True:

#    if (firstTime == 0):
#        print "startup"
#        minRead = adc.read_adc(0, gain=GAIN)
#        maxRead = adc.read_adc(0, gain=GAIN) + 15000
#        breathRead = adc.read_adc(0, gain=GAIN) 
#        print minRead
#        print maxRead
#        firstTime = 1

#    input_state = GPIO.input(23)
#    if (input_state == False):
#        showIt = 1
#        print('Button Pressed')
#        reading = 1
#        time.sleep(0.2)
#
#    input_state = GPIO.input(18)
#    if (input_state == False):
#        showIt = 1 
#        print('Button Pressed 2')
#        recal = 1
#        time.sleep(0.2)

    if (reading == 1):
        if time.time() - start > 1:
            start = time.time()
            counter = counter - 1

            ### This will be updated once per second
            print "%s seconds remaining" % counter

#            breathRead = adc.read_adc(0, gain=GAIN) 
            screen.fill(white)
            textsurface = bigfont.render("Current", True, black) # Draw text
            screen.blit(pygame.transform.rotate(textsurface, 270), (380,30))
            textsurface = bigfont.render("Temp", True, black) # Draw text
            screen.blit(pygame.transform.rotate(textsurface, 270), (300,60))

            textsurface = bigfont.render(string_temp, True, black) # Draw text
            screen.blit(pygame.transform.rotate(textsurface, 270), (220,50))

#            screen.blit(textsurface,(150,120)) # Draw text
#            screen.blit(pygame.transform.rotate(screen, 90), (0, 0))
#            screen.blit(textsurface,(150,120), angle=90) # Draw text
#            screen.draw.text("hello world", (100, 100), angle=10)
#            screen.draw.text(textsurface, (100, 100), angle=90)
#            pygame.transform.rotate(textsurface, 90)
#            rotate(textsurface, 90)
            pygame.display.update()

            ### Countdown finished, ending loop
            if counter <= 0:
                counter = 1.5
                reading = 0 
                showIt = 0 

    if (hold == 1):
        if time.time() - start > 1:
            start = time.time()
            counter = counter - 1

            ### This will be updated once per second
            print "%s seconds remaining" % counter

            screen.fill(white)
            textsurface = bigfont.render("Hold", True, black) # Draw text
            screen.blit(pygame.transform.rotate(textsurface, 270), (380,70))
            textsurface = bigfont.render(string_temp, True, black) # Draw text
            screen.blit(pygame.transform.rotate(textsurface, 270), (300,50))

            pygame.display.update()

            ### Countdown finished, ending loop
            if counter <= 0:
                counter = 1.5
                hold = 0 
                showIt = 0 

#    if (recal == 1):
#        screen.fill(white)
#        textsurface = bigfont.render("Recalibrating", True, black) # Draw text
#        screen.blit(textsurface,(15,120)) # Draw text
#        pygame.display.update()
#
#        minRead = adc.read_adc(0, gain=GAIN)
#        maxRead = adc.read_adc(0, gain=GAIN) + 10000
#        breathRead = adc.read_adc(0, gain=GAIN) 
#        print minRead
#        print maxRead
#
#        recal = 0 
#        showIt = 0

        
    if (showIt == 0):
        print "showIt"
#        mapped_value = translate(breathRead, minRead, maxRead, 0, 10)
#        string_number_drunk_level = "%d" % mapped_value
#        print string_number_drunk_level
#        print adc.read_adc(0, gain=GAIN)
#        print minRead
#        print maxRead
#        print mapped_value 

#        rounded = int("%d" % mapped_value)
#        print rounded 
#        time.sleep(2)
        showIt = 1
#        backgroundImg = pygame.image.load('/home/pi/zero_boot_system_apps/weather_status/    weather_newyear/newyear1.jpg') # Load up the photo you just took
        backgroundImg = pygame.image.load('/home/pi/ir_temp_test/beehive-hexagon-white.jpg') # Load up the photo you just took
        scalePhoto = pygame.transform.scale(backgroundImg, (480, 320)) # Scale to fit scr        een
        screen.blit(scalePhoto, (0,0))

#        screen.fill(white)
### Top bar code start
        pygame.draw.lines(screen, black, True, [[445, 320],[445, 0]], 2) # Draw a triangle
#        pygame.draw.lines(screen, black, True, [[0, 160],[480, 160]], 2) # Center line for dev 
        textExit = myFontTopbar.render("Exit", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textExit, 270), (450,280))
        textsurface = myFontTopbar.render("IR Temp", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (450,120))
        pygame.draw.ellipse(screen, red, [453, 5, 20, 20], 2) 
        pygame.draw.lines(screen, red, True, [[465, 14],[477, 14]], 2) # Draw a triangle
### Top bar code end

#        pygame.draw.rect(screen, red, pygame.Rect(10, 255, 25, 25))
#        textsurface = smallfont.render("Recalibrate", True, red) # Draw text
#        screen.blit(textsurface,(40,260)) # Draw text

### Buttons and text on buttons start
        pygame.draw.rect(screen, red, pygame.Rect(50, 110, 100, 100)) # Square
        pygame.draw.rect(screen, black, [50, 110, 100, 100], 2)
#        pygame.draw.ellipse(screen, red, [50, 110, 100, 100]) #Circle
        pygame.draw.rect(screen, green, pygame.Rect(160, 110, 100, 100))
        pygame.draw.rect(screen, black, [160, 110, 100, 100], 2)
        textsurface = smallfont.render("Temp", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (90,133))
        textsurface = smallfont.render("Hold", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (200,137))
### Buttons and text on buttons end

#
#        pygame.draw.rect(screen, green, pygame.Rect(10, 285, 25, 25))
#        textsurface = smallfont.render("Take reading", True, green) # Draw text
#        screen.blit(textsurface,(40,290)) # Draw text

#        screen.blit(textsurface,(40,10)) # Draw text

#        textsurface = bigfont.render(string_number_drunk_level, True, black) # Draw text
#        screen.blit(textsurface,(220,70)) # Draw text

#        pygame.display.flip()
#        pygame.display.update()

        textsurface = midfont.render("Temp -", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (380,20))
        textsurface = midfont.render(string_temp, True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (380,140))

        textsurface = midfont.render("Hold -", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (320,30))
        textsurface = midfont.render(string_hold_temp, True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (320,140))
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
            if y > 110 and y < 210 and x > 50 and x < 150:
                showIt = 1
                print thermometer.get_amb_temp()
                print thermometer.get_obj_temp() 
                string_temp = "%.2fC" % thermometer.get_obj_temp()
                reading = 1
                time.sleep(0.2)
            if y > 110 and y < 210 and x > 160 and x < 260:
                print('Hold')
                string_hold_temp = string_temp
                hold = 1
            if y > 270 and y < 320 and x > 450 and x < 480:
                print('exit Button Pressed')
                pygame.quit() # Quits the python script
            if y > 0 and y < 50 and x > 450 and x < 480:
                print("shutdown")
                call(["sudo", "shutdown", "-h", "now" ])
