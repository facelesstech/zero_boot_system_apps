#! /usr/bin/env python

# Screen stuff
from pygame.locals import *
import pygame, os
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

while True:

    screen.fill(white)
    
    ### Top bar code start
#    pygame.draw.aaline(screen, black, [480, 30],[0, 30], True)
#
#    textExit = myFontTopbar.render("Exit", True, black) # Draw text
#    screen.blit(textExit,(440,5)) # Draw text
#
#    textTitle = myFontTopbar.render("NameTag", True, black) # Draw text
#    screen.blit(textTitle,(210,5)) # Draw text
#    pygame.draw.ellipse(screen, red, [5, 6, 20, 20], 2) 
#    pygame.draw.lines(screen, red, True, [[14, 14],[14, 2]], 2) # Draw a triangle
    ### Top bar code end

    backgroundImg = pygame.image.load('/home/pi/zero_boot_system_apps/nametag/flt_logo_page.jpg') # Load up the photo you just took
    scalePhoto = pygame.transform.scale(backgroundImg, (480, 320)) # Scale to fit scr        een
    screen.blit(scalePhoto, (0,0))


#    textsurface = mediumfont.render("Facelesstech" , True, black) # Draw text
##    textsurface = mediumfont.render("IP Address %s" % stringIP, True, black) # Draw text
#    screen.blit(textsurface,(10,45)) # Draw text




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
### Top bar touch start            
            if y > 0 and y < 25 and x > 430 and x < 480: # Top right 
                print("exit")
                pygame.quit() # Quits the python script
#            if y > 0 and y < 25 and x > 0 and x < 30: # Top left
#                print("shutdown")
#                call(["sudo", "shutdown", "-h", "now" ])
#### Top bar touch end            
#            if y > 50 and y < 160 and x > 0 and x < 240: # Top left
#                print("IR Temp")
##                call(["sudo", "python", "/home/pi/zero_boot_system_apps/ir_temp/ir_temp.py"])
#            if y > 50 and y < 160 and x >240 and x < 480: # Top right
#                print("Breath")
##                call(["sudo", "python", "/home/pi/zero_boot_system_apps/pialyzer/pialyzer.py"])
#
#            if y > 260 and y < 320 and x >0 and x < 240: # Bottom left
#                print("Bottom left")
##                call(["git", "pull"])
#                proc = Popen(["git pull"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
#                out, err = proc.communicate()  # Read data from stdout and stderr
##                print out
#                updaterStrip =  out.rstrip('\n')
##                print updaterStrip
#                if updaterStrip == "Already up-to-date.":
##                    print "not updated"
#                    updateFlag = 0
#                else:
#                    updateFlag = 1 
##                    print "updated"
#
#            if y > 260 and y < 320 and x >240 and x < 480: # Bottom right 
#                print("Bottom right")
#                call(["sudo", "reboot"])
