#http://inventwithpython.com/chapter17.html
#sudo pip3 install pygame
#/usr/local/lib/python3.6/dist-packages/pygame/__init__.py line 380 commented to avoid hello msg
import pygame, sys
from time import sleep
from pygame.locals import *
# set up pygame
pygame.init()
# set up the window
graphWin = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('covid infection simulation')
# set up the colors
VOID = (0, 0, 0)          # black desert cell
SUSCEPT = (255, 255, 255) # white susceptible cell
INFECT = (255, 0, 0)      # red infected cell
RECOVER = (0, 255, 0)     # green recovered cell
BLUE = (0, 0, 255)        #
graphWin.fill(VOID)
x = 400
y = 300
dx = 20
dy = 20
dt = .5
pygame.draw.rect(graphWin, SUSCEPT, (x, y, dx, dy))
pygame.display.update()
sleep(dt)

pygame.draw.rect(graphWin, VOID, (x, y, dx, dy))
x += 10
y += 10
pygame.draw.rect(graphWin, INFECT, (x, y, dx, dy))
pygame.display.update()
sleep(dt)

pygame.draw.rect(graphWin, VOID, (x, y, dx, dy))
x += 10
y += 10
pygame.draw.rect(graphWin, RECOVER, (x, y, dx, dy))
pygame.display.update()
sleep(dt)

pygame.draw.rect(graphWin, VOID, (x, y, dx, dy))
x += 10
y += 10
pygame.draw.rect(graphWin, BLUE, (x, y, dx, dy))
pygame.display.update()

sleep(dt)
sleep(2)