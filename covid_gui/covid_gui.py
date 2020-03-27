import os
import pygame
from pygame.locals import *
from pygame import gfxdraw
from time import strftime
from subprocess import call
from datetime import datetime, time
import time

import requests

showIt = 0
getWeather = 0
#current.icon = 0

counter = 900
#counter = 10
start = time.time()

white = (255,255,255) # White colour
red = (255,0,0) # Colours for the red dot
orange = (255,128,0) # Colours for the red dot
yellow = (255,215,0) # Colours for the red dot
green = (0,255,0) # Colours for the red dot
blue = (0,0,255) # Colours for the red dot
lightBlue = (0,206,209) # Colours for the red dot
black = (0,0,0) # Colours for the red dot

# Screen res
cam_width = 480 
cam_height = 320 

pygame.init() # Start pygame
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myFontTiny = pygame.font.SysFont('freesansbold.ttf', 20)
myFontSmall = pygame.font.SysFont('freesansbold.ttf', 40)
myFontMid = pygame.font.SysFont('freesansbold.ttf', 50)
myFontBig = pygame.font.SysFont('freesansbold.ttf', 70)
myFontNumber = pygame.font.SysFont('freesansbold.ttf', 80)
myFontTopbar = pygame.font.SysFont('freesansbold.ttf', 30)
bigfont = pygame.font.SysFont('freesansbold.ttf', 100)

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 

while True:
    screen.fill(white)
### Top bar code start
    pygame.draw.aaline(screen, black, [480, 30],[0, 30], True)
#    pygame.draw.aaline(screen, white, [240, 280],[240, 30], True)
    displayTime = strftime("%H:%M:%S")
    textCurrentCount = myFontTopbar.render("%s" % displayTime, True, black) # Draw text
    screen.blit(textCurrentCount,(200, 5)) # Draw text

    textExit = myFontTopbar.render("Exit", True, black) # Draw text
    screen.blit(textExit,(440,5)) # Draw text
    pygame.draw.ellipse(screen, red, [5, 6, 20, 20], 2) 
    pygame.draw.lines(screen, red, True, [[14, 14],[14, 2]], 2) # Draw a triangle
### Top bar code end


    if (getWeather == 0):

        # Get data on only confirmed cases
        api_response = requests.get('https://covid19api.herokuapp.com/confirmed')
        api_response_deaths = requests.get('https://covid19api.herokuapp.com/deaths')
         
        # Print latest data for location ID 100: California, USA
        print(api_response.json()['locations'][223]['latest'])
        print(api_response_deaths.json()['locations'][223]['latest'])

        string_cases = "%d" % api_response.json()['locations'][223]['latest']
        string_deaths = "%d" % api_response_deaths.json()['locations'][223]['latest']
#        string_cases = "1000" # Test
#        string_deaths = "100" # Test

        getWeather = 1 
            
    if (showIt == 0):
        if time.time() - start > 1:
            start = time.time()
            counter = counter - 1

            ### This will be updated once per second
#            print "%s seconds remaining" % counter
                                                                                        ### Countdown finished, ending loop
            if counter <= 0:
                print "done"
#                counter = 900 # 15 mins
                counter = 1800 # 30 mins
#                counter = 10 
                getWeather = 0 

#        tempText = myFontSmall.render("Cases", True, white) # Draw text
        tempText = myFontNumber.render("Cases", True, black) # Draw text
        screen.blit(tempText,(10,60)) # Draw text
        textTemp = myFontNumber.render(string_cases, True, black) # Draw text
        screen.blit(textTemp,(220,60)) # Draw text

        feelsTempText = myFontNumber.render("Deaths", True, black) # Draw text
        screen.blit(feelsTempText,(10,150)) # Draw text
        textFeelTemp = myFontNumber.render(string_deaths, True, black) # Draw text
        screen.blit(textFeelTemp,(220,150)) # Draw text       screen.blit(textTemp,(100,40)) # Draw text

    pygame.display.update() # Update screen

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
            if y > 0 and y < 25 and x > 60 and x < 420: # Top left
                print("util")
                call(["sudo", "python", "/home/pi/zero_boot_system_apps/utility/utility.py"])

