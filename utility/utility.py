#! /usr/bin/env python

# Screen stuff
from pygame.locals import *
from subprocess import Popen, PIPE
import pygame, os
from subprocess import call
import socket
os.chdir("/home/pi/zero_boot_system_apps")
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

ipStore = 0
updaterStrip = 0
updateFlag = 2

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

while True:

    screen.fill(white)
    
    ### Top bar code start
    pygame.draw.aaline(screen, black, [480, 30],[0, 30], True)
#    pygame.draw.aaline(screen, black, [240, 320],[240, 30], True)
#        pygame.draw.line(screen, black, [480, 175],[0, 175], True) # Draw line

    textExit = myFontTopbar.render("Exit", True, black) # Draw text
    screen.blit(textExit,(440,5)) # Draw text

    textTitle = myFontTopbar.render("Utility", True, black) # Draw text
    screen.blit(textTitle,(210,5)) # Draw text
    pygame.draw.ellipse(screen, red, [5, 6, 20, 20], 2) 
    pygame.draw.lines(screen, red, True, [[14, 14],[14, 2]], 2) # Draw a triangle
    ### Top bar code end
    try:
        ipStore = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    except:
        pass

    CPU_temp = getCPUtemperature()
    CPU_usage = getCPUuse()
#    print "CPU Temp %sC" % CPU_temp
#    print "CPU %s%%" % CPU_usage
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)
#    print "Total RAM %sMb" % RAM_total
#    print "RAM free %sMb" % RAM_free
#    print "RAM used %sMb" % RAM_used

### IP Stuff
    textsurface = mediumfont.render("IP Address %s" % ipStore, True, black) # Draw text
    screen.blit(textsurface,(10,45)) # Draw text

### CPU Stuff
    textsurface = mediumfont.render("CPU Temp %sC" % CPU_temp, True, black) # Draw text
    screen.blit(textsurface,(10,80)) # Draw text
    textsurface = mediumfont.render("CPU %s%%" % CPU_usage, True, black) # Draw text
    screen.blit(textsurface,(10,115)) # Draw text

### RAM Stuff
    textsurface = mediumfont.render("Total RAM %sMb" % RAM_total, True, black) # Draw text
    screen.blit(textsurface,(10,150)) # Draw text
    textsurface = mediumfont.render("RAM free %sMb" % RAM_free, True, black) # Draw text
    screen.blit(textsurface,(10,185)) # Draw text
    textsurface = mediumfont.render("RAM used %sMb" % RAM_used, True, black) # Draw text
    screen.blit(textsurface,(10,220)) # Draw text

    if updateFlag == 0:
#        print "not updated"
        pygame.draw.rect(screen, red, pygame.Rect(10, 260, 220, 50))

    elif updateFlag == 1:
        pygame.draw.rect(screen, green, pygame.Rect(10, 260, 220, 50))
#        print "updated"

    textsurface = mediumfont.render("Update", True, black) # Draw text
    screen.blit(textsurface,(65,265)) # Draw text
    pygame.draw.rect(screen, black, [10, 260, 220, 50], 2)

    textsurface = mediumfont.render("Reboot", True, black) # Draw text
    screen.blit(textsurface,(300,265)) # Draw text
    pygame.draw.rect(screen, black, [250, 260, 220, 50], 2)
    

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
            if y > 0 and y < 25 and x > 0 and x < 30: # Top left
                print("shutdown")
                call(["sudo", "shutdown", "-h", "now" ])
### Top bar touch end            
            if y > 50 and y < 160 and x > 0 and x < 240: # Top left
                print("IR Temp")
#                call(["sudo", "python", "/home/pi/zero_boot_system_apps/ir_temp/ir_temp.py"])
            if y > 50 and y < 160 and x >240 and x < 480: # Top right
                print("Breath")
#                call(["sudo", "python", "/home/pi/zero_boot_system_apps/pialyzer/pialyzer.py"])

            if y > 260 and y < 320 and x >0 and x < 240: # Bottom left
                print("Bottom left")
#                call(["git", "pull"])
                proc = Popen(["git pull"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                out, err = proc.communicate()  # Read data from stdout and stderr
#                print out
                updaterStrip =  out.rstrip('\n')
#                print updaterStrip
                if updaterStrip == "Already up-to-date.":
#                    print "not updated"
                    updateFlag = 0
                else:
                    updateFlag = 1 
#                    print "updated"

            if y > 260 and y < 320 and x >240 and x < 480: # Bottom right 
                print("Bottom right")
                call(["sudo", "reboot"])
