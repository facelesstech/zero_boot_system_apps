import os
import pygame
from pygame.locals import *
from pygame import gfxdraw
from time import strftime
from subprocess import call
from datetime import datetime, time
import time

# Weather stuff
iconSizex = 150 
iconSizey = 150
iconPosX = 0
iconPosY = 140
iconFlag = True

showIt = 0
getWeather = 0
newCurrent = 0

# Read API key from file
target = open("/home/pi/zero_boot_system_apps/weather_status/just_the_weather/api_key.txt")
read_api = target.read()

import forecastio
api_key = read_api 
lat = 53.2052792
lng = -2.9350749

counter = 900
#counter = 10
start = time.time()

def icon_mapping(icon, size):

    if icon == 'clear-day':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/clear.png'.format(size)
    elif icon == 'clear-night':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/nt_clear.png'.format(size)
    elif icon == 'rain':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/rain.png'.format(size)
    elif icon == 'snow':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/snow.png'.format(size)
    elif icon == 'sleet':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/sleet.png'.format(size)
    elif icon == 'wind':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/alt_icons/{}/wind.png'.format(size)
    elif icon == 'fog':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/fog.png'.format(size)
    elif icon == 'cloudy':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/cloudy.png'.format(size)
    elif icon == 'partly-cloudy-day':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/partlycloudy.png'.format(size)
    elif icon == 'partly-cloudy-night':
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/nt_partlycloudy.png'.format(size)
    else:
        icon_path = '/home/pi/zero_boot_system_apps/weather_status/icons/{}/unknown.png'.format(size)

    return icon_path

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
myFontSmall = pygame.font.SysFont('freesansbold.ttf', 40)
myFontMid = pygame.font.SysFont('freesansbold.ttf', 50)
myFontBig = pygame.font.SysFont('freesansbold.ttf', 70)
myFontNumber = pygame.font.SysFont('freesansbold.ttf', 80)
myFontTopbar = pygame.font.SysFont('freesansbold.ttf', 30)
bigfont = pygame.font.SysFont('freesansbold.ttf', 100)

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 

while True:
    screen.fill(black)
### Top bar code start
    pygame.draw.aaline(screen, white, [480, 30],[0, 30], True)
    pygame.draw.aaline(screen, white, [240, 280],[240, 30], True)
    displayTime = strftime("%H:%M:%S")
    textCurrentCount = myFontTopbar.render("%s" % displayTime, True, white) # Draw text
    screen.blit(textCurrentCount,(200, 5)) # Draw text

    textExit = myFontTopbar.render("Exit", True, white) # Draw text
    screen.blit(textExit,(440,5)) # Draw text
    pygame.draw.ellipse(screen, red, [5, 6, 20, 20], 2) 
    pygame.draw.lines(screen, red, True, [[14, 14],[14, 2]], 2) # Draw a triangle
### Top bar code end


    if (getWeather == 0):
        forecast = forecastio.load_forecast(api_key, lat, lng)
        byHour = forecast.hourly()
        current = forecast.currently()
#        print byHour.summary
#        print byHour.icon
#        print byHour.temperature
        print current.summary
        print current.icon
#        print round(current.temperature)
        roundedUp =  round(current.temperature)
#        string_temp_test = "%d" % current.temperature
#        print string_temp_test
#        print string_temp_test
        takeTemp = current.temperature
        string_temp = "%.1fC" % current.temperature
        string_feeltemp = "%.1fC" % current.apparentTemperature

#        string_summary = "%" % current.summary
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
                counter = 900 
#                counter = 10 
                getWeather = 0 

        tempText = myFontSmall.render("Temp", True, white) # Draw text
        screen.blit(tempText,(10,40)) # Draw text
        textTemp = myFontMid.render(string_temp, True, white) # Draw text
        screen.blit(textTemp,(100,40)) # Draw text

        if current.summary == "Breezy and Mostly Cloudy":
            newCurrentFirst = "Breezy and"
            newCurrentSecond = "Mostly Cloudy"
            textSummaryFirst = myFontSmall.render(newCurrentFirst, True, white) # Draw text
            screen.blit(textSummaryFirst,(10,80)) # Draw text

            textSummarySecond = myFontSmall.render(newCurrentSecond, True, white) # Draw text
            screen.blit(textSummarySecond,(10,110)) # Draw text
            current.icon = "cloudy"

        elif current.summary == "Breezy and Partly Cloudy":
            newCurrentFirst = "Breezy and"
            newCurrentSecond = "Partly Cloudy"
            textSummaryFirst = myFontSmall.render(newCurrentFirst, True, white) # Draw text
            screen.blit(textSummaryFirst,(10,80)) # Draw text

            textSummarySecond = myFontSmall.render(newCurrentSecond, True, white) # Draw text
            screen.blit(textSummarySecond,(10,110)) # Draw text


        elif current.summary == "Windy and Partly Cloudy":
            newCurrentFirst = "Windy and"
            newCurrentSecond = "Partly Cloudy"
            textSummaryFirst = myFontSmall.render(newCurrentFirst, True, white) # Draw text
            screen.blit(textSummaryFirst,(10,80)) # Draw text

            textSummarySecond = myFontSmall.render(newCurrentSecond, True, white) # Draw text
            screen.blit(textSummarySecond,(10,110)) # Draw text

        elif current.summary == "Windy and Mostly Cloudy":
            newCurrentFirst = "Windy and"
            newCurrentSecond = "Mostly Cloudy"
            textSummaryFirst = myFontSmall.render(newCurrentFirst, True, white) # Draw text
            screen.blit(textSummaryFirst,(10,80)) # Draw text

            textSummarySecond = myFontSmall.render(newCurrentSecond, True, white) # Draw text
            screen.blit(textSummarySecond,(10,110)) # Draw text

        elif current.summary == "Dangerously Windy and Partly Cloudy":
            newCurrentFirst = "Dangerously Windy and"
            newCurrentSecond = "Partly Cloudy"
            textSummaryFirst = myFontSmall.render(newCurrentFirst, True, white) # Draw text
            screen.blit(textSummaryFirst,(10,80)) # Draw text

            textSummarySecond = myFontSmall.render(newCurrentSecond, True, white) # Draw text
            screen.blit(textSummarySecond,(10,110)) # Draw text

        elif current.summary == "Light Rain and Windy":
#            iconFlag = False 
            newCurrentFirst = "Light Rain"
            newCurrentSecond = "and Windy"
            textSummaryFirst = myFontSmall.render(newCurrentFirst, True, white) # Draw text
            screen.blit(textSummaryFirst,(10,80)) # Draw text

            textSummarySecond = myFontSmall.render(newCurrentSecond, True, white) # Draw text
            screen.blit(textSummarySecond,(10,110)) # Draw text

        else:
#            iconFlag = True
#            iconFlag = False
#            newCurrent = current.summary
#            textSummary = myFontSmall.render(newCurrent, True, white) # Draw text
            textSummary = myFontSmall.render(current.summary, True, white) # Draw text
            screen.blit(textSummary,(10,80)) # Draw text

        iconLoad = pygame.image.load(icon_mapping(current.icon, 256))# Load up the photo you just took
        scaleIcon = pygame.transform.scale(iconLoad, (iconSizex, iconSizey)) # Scale to fit screen
        screen.blit(scaleIcon, (iconPosX, iconPosY)) 

#        if iconFlag == True:
#
#            iconLoad = pygame.image.load(icon_mapping(current.icon, 256))# Load up the photo you just took
#            scaleIcon = pygame.transform.scale(iconLoad, (iconSizex, iconSizey)) # Scale to fit screen
#            screen.blit(scaleIcon, (iconPosX, iconPosY)) 
#            
#        else:

#        iconLoad = pygame.image.load(icon_mapping(current.icon, 256))# Load up the photo you just took
#        scaleIcon = pygame.transform.scale(iconLoad, (iconSizex, iconSizey)) # Scale to fit screen
#        screen.blit(scaleIcon, (iconPosX, iconPosY)) 

### Temp section
    convertTemp = 0
    tempColour = red
    takeTemp = 0
    pygame.draw.aaline(screen, white, [480, 280],[0, 280], True)

    if ( roundedUp <= 0):
        tempColour = blue
        takeTemp = abs(roundedUp)
#        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])

    if ( 0.1 <= roundedUp <= 10.9):
        tempColour = lightBlue
        takeTemp = roundedUp
#        takeTemp = string_temp_test

    elif ( 11 <= roundedUp <= 19.9):
        tempColour = yellow 
        takeTemp = roundedUp-10

    elif ( 20 <= roundedUp <= 29.9):
        tempColour = orange 
        takeTemp = roundedUp-20

    elif ( 30 <= roundedUp <= 39.9):
        tempColour = red 
        takeTemp = roundedUp-30

#    if 1 <= takeTemp <= 1.9:
    if 0 <= takeTemp <= 1.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])

    elif 2 <= takeTemp <= 2.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])

    elif 3 <= takeTemp <= 3.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])

    elif 4 <= takeTemp <= 4.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [148, 285, 40, 40])

    elif 5 <= takeTemp <= 5.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [148, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [195, 285, 40, 40])

    elif 6 <= takeTemp <= 6.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [148, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [195, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [242, 285, 40, 40])

    elif 7 <= takeTemp <= 7.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [148, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [195, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [242, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [289, 285, 40, 40])

    elif 8 <= takeTemp <= 8.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [148, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [195, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [242, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [289, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [336, 285, 40, 40])

    elif 9 <= takeTemp <= 9.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [148, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [195, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [242, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [289, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [336, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [383, 285, 40, 40])

    elif 10 <= takeTemp <= 10.9:
        pygame.draw.rect(screen, tempColour, [7, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [54, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [101, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [148, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [195, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [242, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [289, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [336, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [383, 285, 40, 40])
        pygame.draw.rect(screen, tempColour, [430, 285, 40, 40])

    pygame.draw.rect(screen, white, [7, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [54, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [101, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [148, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [195, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [242, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [289, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [336, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [383, 285, 40, 34], 2)
    pygame.draw.rect(screen, white, [430, 285, 40, 34], 2)



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
