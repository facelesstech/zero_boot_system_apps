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

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 

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

while True:

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

    if (showIt == 0):
        print "showIt"
        showIt = 1
        backgroundImg = pygame.image.load('/home/pi/zero_boot_system_apps/ir_temp/beehive-hexagon-white.jpg') # Load up the photo you just took
        scalePhoto = pygame.transform.scale(backgroundImg, (480, 320)) # Scale to fit scr        een
        screen.blit(scalePhoto, (0,0))

### Top bar code start
        pygame.draw.lines(screen, black, True, [[445, 320],[445, 0]], 2) # Draw a triangle
        textExit = myFontTopbar.render("Exit", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textExit, 270), (450,280))
        textsurface = myFontTopbar.render("IR Temp", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (450,120))
        pygame.draw.ellipse(screen, red, [453, 5, 20, 20], 2) 
        pygame.draw.lines(screen, red, True, [[465, 14],[477, 14]], 2) # Draw a triangle
### Top bar code end

### Buttons and text on buttons start
        pygame.draw.rect(screen, red, pygame.Rect(50, 110, 100, 100)) # Square
        pygame.draw.rect(screen, black, [50, 110, 100, 100], 2)
        pygame.draw.rect(screen, green, pygame.Rect(160, 110, 100, 100))
        pygame.draw.rect(screen, black, [160, 110, 100, 100], 2)
        textsurface = smallfont.render("Temp", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (90,133))
        textsurface = smallfont.render("Hold", True, black) # Draw text
        screen.blit(pygame.transform.rotate(textsurface, 270), (200,137))
### Buttons and text on buttons end

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
