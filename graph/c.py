import pygame, sys, time
from pygame.locals import *
import time

pygame.init()
screen = pygame.display.set_mode((400, 400), 0, 32)
pygame.display.set_caption('animation wo refill')

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Draw anything to the display surface named screen, then do:
# By display surface I mean the surface returned by pygame.display.set_mode()
screen.fill(BLACK)
pygame.draw.line(screen, WHITE, (0, 0), (400, 400), 1)
pygame.draw.line(screen, RED, (0, 400), (400, 0), 1)

orig = screen.copy()
pygame.draw.rect(screen,BLUE,(10,10,100,100))
# Sometimes it will not be filled with a image from screen that you have drawn before, so you draw
# all to orig surface
# Then you make a surface that will be shown on the screen and do:
s = pygame.surface.Surface((100,100))
s.blit(orig, (0, 0))
# Then you draw the rectangle or whatever on s, and then:
pygame.display.flip()
# and you keep orig as a starting point for every move