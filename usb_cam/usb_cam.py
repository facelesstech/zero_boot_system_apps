import pygame
import pygame.camera
from pygame.locals import *

DEVICE = '/dev/video0'
SIZE = (640, 480)
scaleSize = (480, 320)
FILENAME = 'capture.png'

def camstream():
    pygame.init()
    display = pygame.display.set_mode(scaleSize, pygame.NOFRAME)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True
    pygame.mouse.set_visible(False) # Turned off the mouse pointer   pygame.camera.init()
    while capture:
        screen = camera.get_image(screen)
        display.blit(screen, (0,0))
        pygame.display.flip()
        for event in pygame.event.get(): # Events for the mouse and hit target code
            if(event.type is MOUSEBUTTONDOWN): # If the mouse is clicked
                pos = pygame.mouse.get_pos() # Get mouse pointer position

            elif(event.type is MOUSEBUTTONUP):# If the mouse click is let go
                pos = pygame.mouse.get_pos() # Get mouse pointer position

                x,y = pos
                print pos

                if y > 270 and y < 320 and x > 430 and x < 480: # bottom right 

    #                call(["sudo", "shutdown", "-h", "now" ])
                    print "shutdown"

                if y > 290 and x > 0 and x < 50: # Bottom left
                    pygame.quit() # Quits the python script
#        for event in pygame.event.get():
#            if event.type == QUIT:
#                capture = False
#            elif event.type == KEYDOWN and event.key == K_s:
#                pygame.image.save(screen, FILENAME)
    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
