import os
import pygame
from pygame.locals import *
from pygame import gfxdraw
from time import strftime
from subprocess import call
from datetime import datetime, time
import time


def dateDiffInSeconds(date1, date2):
    timedelta = date2 - date1
    return timedelta.days * 24 * 3600 + timedelta.seconds

def daysHoursMinutesSecondsFromSeconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (hours, minutes, seconds)

def justDays(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days)

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
myFontSmall = pygame.font.SysFont('freesansbold.ttf', 40)
myFontMid = pygame.font.SysFont('freesansbold.ttf', 50)
myFontBig = pygame.font.SysFont('freesansbold.ttf', 70)
myFontNumber = pygame.font.SysFont('freesansbold.ttf', 80)
myFontTopbar = pygame.font.SysFont('freesansbold.ttf', 30)
bigfont = pygame.font.SysFont('freesansbold.ttf', 100)
smallfont = pygame.font.SysFont('freesansbold.ttf', 30)
mediumfont = pygame.font.SysFont('freesansbold.ttf', 50)

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 

while True:
    screen.fill(black)
    lastImg = pygame.image.load('/home/pi/zero_boot_system_apps/weather_status/weather_templates/newyear1.jpg') # Load up the photo you just took

    scalePhoto = pygame.transform.scale(lastImg, (240, 250)) # Scale to fit scr    een
    screen.blit(scalePhoto, (240,30))

    leaving_date = datetime.strptime('2018-12-25 00:00:00', '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
#    stringTime = "%02d - %02d:%02d:%02d" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, leaving_date))
    stringDays = "%02d" % justDays(dateDiffInSeconds(now, leaving_date))
    stringTime = "%02d:%02d:%02d" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, leaving_date))

    textXmas1 = myFontSmall.render("Christmas", True, white) # Draw text
    textXmas2 = myFontSmall.render("Count down", True, white) # Draw text
    textDays = myFontMid.render("Days", True, white) # Draw text
#    textCount = myfontNumber.render("%s" % stringTime, True, white) # Draw text
    textCount = myFontNumber.render("%s" % stringTime, True, white) # Draw text
    textCountDays = myFontNumber.render("%s" % stringDays, True, white) # Draw text
    screen.blit(textXmas1,(300,40)) # Draw text
    screen.blit(textXmas2,(285,80)) # Draw text
    screen.blit(textDays,(317,120)) # Draw text
    screen.blit(textCountDays,(330,160)) # Draw text
    screen.blit(textCount,(250,220)) # Draw text

    pygame.draw.aaline(screen, white, [480, 30],[0, 30], True)
    pygame.draw.aaline(screen, white, [240, 280],[240, 30], True)
    pygame.draw.aaline(screen, white, [360, 320],[360, 30], True) # test line
    time = strftime("%H:%M:%S")
    textCurrentCount = myFontTopbar.render("%s" % time, True, white) # Draw text
    screen.blit(textCurrentCount,(200, 5)) # Draw text

    textExit = myFontTopbar.render("Exit", True, white) # Draw text
    screen.blit(textExit,(440,5)) # Draw text
    pygame.draw.ellipse(screen, red, [5, 6, 20, 20], 2) 
    pygame.draw.lines(screen, red, True, [[14, 14],[14, 2]], 2) # Draw a triangle
    pygame.draw.aaline(screen, white, [480, 280],[0, 280], True)
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
#             if y > 270 and y < 320 and x > 430 and x < 480: # Bottom right  
            if y > 0 and y < 50 and x > 430 and x < 480: # Top right 
                print("exit")
                pygame.quit() # Quits the python script
            if y > 0 and y < 50 and x > 0 and x < 50: # Top left
                print("shutdown")
                call(["sudo", "shutdown", "-h", "now" ])
