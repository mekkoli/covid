#https://devdocs.io/pygame/
#http://inventwithpython.com/chapter17.html

import pygame, sys, time
from pygame.locals import *
import time

# set up pygame
pygame.init()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

# set up direction variables
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

MOVESPEED = 10

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# set up the block data structure
b = {
  'line':pygame.Rect(30, 30, 370, 30), 
  'color':BLUE, 
  'dir':UPRIGHT
}

# run the game loop
windowSurface.fill(BLACK)
while True:
  # check for the QUIT event
  for event in pygame.event.get():
    if event.type == QUIT:
      b['line'] = pygame.Rect(0, 0, 0, 0)
      pygame.display.update()
      pygame.quit()
      sys.exit()

  # draw the black background onto the surface
  pygame.draw.line(windowSurface, WHITE, (0, 0), (400, 400), 1)
  pygame.draw.line(windowSurface, RED, (0, 400), (400, 0), 1)
    
  b['line'].x = 0
  b['line'].y = 30
  pygame.draw.line(windowSurface, b['color'], (b['line'].x, b['line'].y), (b['line'].x+b['line'].width, b['line'].y+b['line'].height),1)
  pygame.display.update()
  time.sleep(1)

  b['line'].x = 30
  b['line'].y = 60
  pygame.draw.line(windowSurface, b['color'], (b['line'].x, b['line'].y), (b['line'].x+b['line'].height, b['line'].y+b['line'].width),1)
  pygame.display.update()
  time.sleep(0.1)

