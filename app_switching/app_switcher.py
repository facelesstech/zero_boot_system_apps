#! /usr/bin/env python

# Screen stuff
from pygame.locals import *

import pygame, os
from subprocess import call

screen = pygame.display.set_mode((480, 320),pygame.NOFRAME)
pygame.font.init()
smallfont = pygame.font.SysFont('freesansbold.ttf', 30)
mediumfont = pygame.font.SysFont('freesansbold.ttf', 50)
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

showIt = 0

while True:
    
    if (showIt == 0):
        print "showIt"
#        time.sleep(2)
        showIt = 1
        screen.fill(white)


    ### Top bar code start
        pygame.draw.aaline(screen, black, [480, 30],[0, 30], True)
#        pygame.draw.aaline(screen, black, [240, 320],[240, 30], True)
#        pygame.draw.line(screen, black, [480, 175],[0, 175], True) # Draw line

        textExit = myFontTopbar.render("Exit", True, black) # Draw text
        screen.blit(textExit,(440,5)) # Draw text

        textTitle = myFontTopbar.render("App switcher", True, black) # Draw text
        screen.blit(textTitle,(170,5)) # Draw text
        pygame.draw.ellipse(screen, red, [5, 6, 20, 20], 2) 
        pygame.draw.lines(screen, red, True, [[14, 14],[14, 2]], 2) # Draw a triangle
    ### Top bar code end

        textsurface = mediumfont.render("IR Temp", True, black) # Draw text
        screen.blit(textsurface,(50,85)) # Draw text
        pygame.draw.rect(screen, black, [10, 40, 220, 125], 2)

        textsurface = mediumfont.render("breathalyzer", True, black) # Draw text
        screen.blit(textsurface,(260,85)) # Draw text
        pygame.draw.rect(screen, black, [250, 40, 220, 125], 2)

        textsurface = mediumfont.render("", True, black) # Draw text
        screen.blit(textsurface,(50,230)) # Draw text
        pygame.draw.rect(screen, black, [10, 185, 220, 125], 2)

        textsurface = mediumfont.render("", True, black) # Draw text
        screen.blit(textsurface,(260,230)) # Draw text
        pygame.draw.rect(screen, black, [250, 185, 220, 125], 2)

        pygame.display.update()

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
            if y > 0 and y < 25 and x > 430 and x < 480: # Top right 
                print("exit")
                pygame.quit() # Quits the python script
            if y > 0 and y < 25 and x > 0 and x < 30: # Top left
                print("shutdown")
                call(["sudo", "shutdown", "-h", "now" ])
            if y > 50 and y < 160 and x > 0 and x < 240: # Top left
                print("IR Temp")
                call(["sudo", "python", "/home/pi/zero_boot_system_apps/ir_temp/ir_temp.py"])
            if y > 50 and y < 160 and x >240 and x < 480: # Top right
                print("Breath")
                call(["sudo", "python", "/home/pi/zero_boot_system_apps/pialyzer/pialyzer.py"])

            if y > 160 and y < 320 and x >0 and x < 240: # Bottom left
                print("Bottom left")
#                call(["sudo", "python", "/home/pi/zero_boot_system_apps/pialyzer/pialyzer.py"])

            if y > 160 and y < 320 and x >240 and x < 480: # Bottom right 
                print("Bottom right")
#                call(["sudo", "python", "/home/pi/zero_boot_system_apps/pialyzer/pialyzer.py"])
