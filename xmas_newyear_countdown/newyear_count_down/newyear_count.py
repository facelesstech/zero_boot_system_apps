import os
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
import time
from time import strftime
import datetime
import picamera
import picamera.array
import datetime as dt

from subprocess import call

import datetime
from time import strftime

from datetime import datetime, time

red = (255,0,0) # Colours for the red dot

timeReached = 0

def dateDiffInSeconds(date1, date2):
    timedelta = date2 - date1
    return timedelta.days * 24 * 3600 + timedelta.seconds

def daysHoursMinutesSecondsFromSeconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
#    return (days, hours, minutes, seconds)
    return (hours, minutes, seconds)

#gpio_pin1=18 # The GPIO pin the button is attached to K1
#gpio_pin2=23 # The GPIO pin the button is attached to K2
#gpio_pin3=24 # The GPIO pin the button is attached to K3
#
#GPIO.setmode(GPIO.BCM) # Set GPIO mode
#
#GPIO.setup(gpio_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K1 on the screen
#GPIO.setup(gpio_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K2 on the screen
#GPIO.setup(gpio_pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K3 on the screen

white = (255,255,255) # White colour
red = (255,0,0) # Colours for the red dot
green = (0,255,0) # Colours for the red dot
bright_green = (0,0,255) # Colours for the red dot
black = (0,0,0) # Colours for the red dot

# Screen res
cam_width = 480 
cam_height = 320 

pygame.init() # Start pygame
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('freesansbold.ttf', 30)
myfontNumber = pygame.font.SysFont('freesansbold.ttf', 80)
myFontTopbar = pygame.font.SysFont('freesansbold.ttf', 30)
myFontBig = pygame.font.SysFont('freesansbold.ttf', 70)

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 

#def buttonStateChanged1(gpio_pin1):
#
#    if(GPIO.input(gpio_pin1) == True):  
#        print("Button pressed three")
#        pygame.quit() # Quits the python script
#
#
#GPIO.add_event_detect(gpio_pin1, GPIO.RISING, callback=buttonStateChanged1,bouncetime=400)
#
#
#def buttonStateChanged2(gpio_pin2):
#    if(GPIO.input(gpio_pin2) == True):  
#        pass
#
#GPIO.add_event_detect(gpio_pin2, GPIO.RISING, callback=buttonStateChanged2,bouncetime=400)
#
#def buttonStateChanged3(gpio_pin3):
#    if(GPIO.input(gpio_pin3) == True):  
#        pass
#
#GPIO.add_event_detect(gpio_pin3, GPIO.RISING, callback=buttonStateChanged3,bouncetime=400)
#
while True:
    lastImg = pygame.image.load('/home/pi/xmas_newyear_countdown/newyear_count_down/new_year.jpeg') # Load up the photo you just t    ook
#    scalePhoto = pygame.transform.scale(lastImg, (320, 240)) # Scale to fit scr    een
    scalePhoto = pygame.transform.scale(lastImg, (480, 320)) # Scale to fit scr    een
    screen.blit(scalePhoto, (0,0))


    leaving_date = datetime.strptime('2020-12-31 00:00:00', '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    stringTime = "%02d:%02d:%02d" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, leaving_date))

    ### Top bar code start
    pygame.draw.aaline(screen, white, [480, 30],[0, 30], True)
#    pygame.draw.aaline(screen, white, [240, 280],[240, 30], True)
    displayTime = strftime("%H:%M:%S")
    textCurrentCount = myFontTopbar.render("%s" % displayTime, True, white)     # Draw text
    screen.blit(textCurrentCount,(200, 5)) # Draw text

    textExit = myFontTopbar.render("Exit", True, white) # Draw text
    screen.blit(textExit,(440,5)) # Draw text
    pygame.draw.ellipse(screen, red, [5, 6, 20, 20], 2) 
    pygame.draw.lines(screen, red, True, [[14, 14],[14, 2]], 2) # Draw a tri    angle
    ### Top bar code end

#    pygame.gfxdraw.aacircle(screen, 295, 215, 15, red) # Draw an anti alias circle
#    pygame.gfxdraw.aacircle(screen, 295, 215, 14, red) # Draw an anti alias circle
#    pygame.gfxdraw.aacircle(screen, 295, 215, 13, red) # Draw an anti alias circle
#    pygame.gfxdraw.aacircle(screen, 295, 215, 12, red) # Draw an anti alias circle
#    pygame.draw.lines(screen, red, True, [[295, 215],[295, 192]], 3) # Draw a triangle

    textNewyear1 = myFontBig.render("New year", True, white) # Draw text
    textNewyear2 = myFontBig.render("Count down", True, white) # Draw text
    textCount = myfontNumber.render("%s" % stringTime, True, white) # Draw text
    textHappyNewyear1 = myfontNumber.render("Happy", True, white) # Draw text
    textHappyNewyear2 = myfontNumber.render("New", True, white) # Draw text
    textHappyNewyear3 = myfontNumber.render("Year", True, white) # Draw text

    screen.blit(textNewyear1,(20,35)) # Draw text
    screen.blit(textNewyear2,(20,80)) # Draw text
    screen.blit(textCount,(30,250)) # Draw text

    pygame.display.update() # Update screen

#    if (stringTime == "13:04:30"):
#    if (stringTime == "00:00:00"):
#        timeReached = 1
#
#    if (timeReached == 1):
##    if (stringTime == "09:31:20"):
#        screen.blit(textHappyNewyear1,(20,20)) # Draw text
#        screen.blit(textHappyNewyear2,(20,50)) # Draw text
#        screen.blit(textHappyNewyear3,(20,80)) # Draw text
#        pygame.display.update() # Update screen
#    else:
#        screen.blit(textNewyear1,(20,35)) # Draw text
#        screen.blit(textNewyear2,(20,80)) # Draw text
#        screen.blit(textCount,(30,250)) # Draw text
#        pygame.display.update() # Update screen



#    for event in pygame.event.get(): # Events for the mouse and hit target code
#
#        if(event.type is MOUSEBUTTONDOWN): # If the mouse is clicked
#            mouse = pygame.mouse.get_pos() # Get mouse pointer position
#
#        elif(event.type is MOUSEBUTTONUP):# If the mouse click is let go
#            mouse = pygame.mouse.get_pos() # Get mouse pointer position
#
#            if 270+50 > mouse[0] > 270 and 200+50 > mouse[1] > 200: # Draw a hit target
#                call(["sudo", "shutdown", "-h", "now" ])
#
#            if 0+50 > mouse[0] > 0 and 200+50 > mouse[1] > 200: # Draw a hit target
#                pygame.quit() # Quits the python script


# Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print pos
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print pos
            x,y = pos
#            if y > 290 and x > 0 and x < 50: # Bottom left
#             if y > 270 and y < 320 and x > 430 and x < 480: # bottom right  
            if y > 0 and y < 50 and x > 430 and x < 480: # Top right 
                print("exit")
                pygame.quit() # Quits the python script
            if y > 0 and y < 50 and x > 0 and x < 50: # Top left
                print("shutdown")
                call(["sudo", "shutdown", "-h", "now" ])
