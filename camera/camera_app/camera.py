#!/usr/bin/python

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
from subprocess import Popen, PIPE

recordButton = 0
photoTaken = 0
mouse = 0

white = (255,255,255) # White colour
red = (255,0,0) # Colours for the red dot
green = (0,255,0) # Colours for the red dot
blue = (0,0,255) # Colours for the red dot
bright_green = (0,0,255) # Colours for the red dot
black = (0,0,0) # Colours for the red dot

# Screen res
cam_width = 480 
cam_height = 320 

# 2X Screen res
#cam_width = 960 
#cam_height = 640 

# 3X Screen res
#cam_width = 1440 
#cam_height = 960 

# QVGA
#cam_width = 800 
#cam_height = 600 

# HD 1080
#cam_width = 1920 
#cam_height = 1080 

# 4X normal res
#cam_width = 1919 
#cam_height = 1280 

camera = picamera.PiCamera()
camera.resolution = (cam_width, cam_height)
camera.hflip = False # Flip the video from the camera
camera.framerate = 24 # Frame rate

photo_dir = '/home/pi/zero_boot_system_apps/camera/camera_photos' # Dir for photos
video_dir = '/home/pi/zero_boot_system_apps/camera/camera_videos' # Dir for videos

pygame.display.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('freesansbold.ttf', 30)

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 
video = picamera.array.PiRGBArray(camera)

state = 0 # State for the button

def rec():

    pygame.gfxdraw.filled_circle(screen, 20, 20, 10, red) # Draw circle
    pygame.gfxdraw.aacircle(screen, 20, 20, 10, red) # Draw an anti alias circle
    textsurface = myfont.render('REC', True, red) # Draw text
    screen.blit(textsurface,(35,10)) # Draw text

def photo(fileName):

#    screen.fill(white) # Flash screen white
    lastImg = pygame.image.load('%s' % fileName) # Load up the photo you just took
    scalePhoto = pygame.transform.scale(lastImg, (480, 320)) # Scale to fit screen
    screen.blit(scalePhoto, (0,0)) 
    pygame.display.update() # Update screen

for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):

    frame = np.rot90(frameBuf.array)        
    video.truncate(0)
    frame = pygame.surfarray.make_surface(frame)
    scaleVideo = pygame.transform.scale(frame, (480, 320)) # Scales the video to fit the screen
    flipVideo = pygame.transform.flip(scaleVideo, True, False) # Flip the scaled video horizonatly
    screen.fill([0,0,0]) # Fill the screen
    screen.blit(flipVideo, (0,0)) # Post to the screen

    if recordButton == 1:
        rec() # Puts the red dot on screen when recording

    for event in pygame.event.get(): # Events for the mouse and hit target code

        if(event.type is MOUSEBUTTONDOWN): # If the mouse is clicked
            pos = pygame.mouse.get_pos() # Get mouse pointer position

        elif(event.type is MOUSEBUTTONUP):# If the mouse click is let go
            pos = pygame.mouse.get_pos() # Get mouse pointer position

            x,y = pos
            print pos

            if y > 270 and y < 320 and x > 430 and x < 480: # bottom right 

                call(["sudo", "shutdown", "-h", "now" ])
                print "shutdown"

            if y > 290 and x > 0 and x < 50: # Bottom left

                pygame.quit() # Quits the python script

            if y > 0 and y < 50 and x > 430 and x < 480: # Top right 

                print "un mount"
                proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                out, err = proc.communicate()  # Read data from stdout and stderr
                call(["umount", "/media/pi/%s" % out.rstrip('\n')]) # Attemps to make a dir 

            if y > 50 and y < 270 and x > 0 and x < 240: # Top right 

                print "pressed left"

                if (state == 1):
                    state = 0

                elif (state == 0):
                    state = 1

                if (state == 1):
            #        print ("start rec")

                    try: # Checks to see if USB drive is there if not saves to SD card

                        proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                        video_out, err = proc.communicate()  # Read data from stdout and stderr
                        video_dir_usb = '/media/pi/%s/camera_videos' % video_out.rstrip('\n') # Dir for videos on USB

                        proc = Popen(["ls /media/pi/%s" % video_out], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                        video_out_dir, err = proc.communicate()  # Read data from stdout and stderr

                        if (video_out == ''):
                            raise ValueError('empty string')

                        else:
                            print video_dir
            #            if (video_dir == ''):
                            try:
                #                print video_dir
                                call(["mkdir", "/media/pi/%s/camera_videos" % video_out.rstrip('\n')]) # Attemps to make a dir 
                                videoFilenameUsb = os.path.join(video_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264')) # Brings all the elements together to have time and date
                                camera.start_recording(videoFilenameUsb) # Start recording with time and date as file name
            #            else:
                            except: # If it cant make dir then it just uses the one on the flash drive

                                videoFilenameUsb = os.path.join(video_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264')) # Brings all the elements together to have time and date
                                camera.start_recording(videoFilenameUsb) # Start recording with time and date as file name

                    except ValueError as e: # If error happens it falls back to this state and saves to sd card
                        videoFilename = os.path.join(video_dir, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.h264')) # Brings all the elements together to have time and date
            #            print("video taken sd")
                        camera.start_recording(videoFilename) # Start recording with time and date as file name

                    recordButton = 1 # Turns on the record red dot

                elif (state == 0):
            #        print ("stop rec")
                    camera.stop_recording() # Stop the recording
                    recordButton = 0 # Turns off the record red dot

            if y > 50 and y < 270 and x > 240 and x < 480: # Top right 
                print "pressed right"

                try: # Checks to see if USB drive is there if not saves to SD card 
        #            print("USB")
                    proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                    out, err = proc.communicate()  # Read data from stdout and stderr
                    print out
                    photo_dir_usb = '/media/pi/%s/camera_photos' % out.rstrip('\n') # Dir for videos on USB

                    if (out == ''):
                        raise ValueError('empty string')

                    else:
                        try:
                            call(["mkdir", "/media/pi/%s/camera_photos" % out.rstrip('\n')])
                            photoFilenameUsb = os.path.join(photo_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                            camera.capture(photoFilenameUsb)
            #                print("Photo taken usb")
                            photo(photoFilenameUsb)

                        except:
                            photoFilenameUsb = os.path.join(photo_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                            camera.capture(photoFilenameUsb)
            #                print("Photo taken usb")
                            photo(photoFilenameUsb)
                except ValueError as e:
                    photoFilename = os.path.join(photo_dir, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                    print("SD CARD")
        #            print(e)
                    camera.capture(photoFilename)
        #            print("Photo taken")
                    photo(photoFilename)

                photoTaken = 1
                time.sleep(2)
                photoTaken = 0

    proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
    out, err = proc.communicate()  # Read data from stdout and stderr
#    print out

    if (out == ''):
        pygame.draw.lines(screen, green, True, [[445, 20], [475, 20], [460, 5], [445, 20]], 3) # Draw a triangle
        pygame.draw.rect(screen, green, [445, 25, 30, 7], 3) # Draw a rectangle

    else:
        pygame.draw.lines(screen, red, True, [[445, 20], [475, 20], [460, 5], [445, 20]], 3) # Draw a triangle
        pygame.draw.rect(screen, red, [445, 25, 30, 7], 3) # Draw a rectangle

    # Power shutdown on screen button
    pygame.gfxdraw.aacircle(screen, 455, 295, 15, red) # Draw an anti alias circle
    pygame.gfxdraw.aacircle(screen, 455, 295, 14, red) # Draw an anti alias circle
    pygame.gfxdraw.aacircle(screen, 455, 295, 13, red) # Draw an anti alias circle
    pygame.gfxdraw.aacircle(screen, 455, 295, 12, red) # Draw an anti alias circle
    pygame.draw.lines(screen, red, True, [[455, 295],[455, 272]], 3) # Draw a triangle
    textsurface = myfont.render('EXIT', True, blue) # Draw text
    screen.blit(textsurface,(5, 295)) # Draw text

    pygame.display.update() # Update screen

