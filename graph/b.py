import pygame, sys
from pygame.locals import *

pygame.init()
screen=pygame.display.set_mode((800, 600))
pygame.display.set_caption('Oggetto Rect')

BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

r=pygame.Rect(20,20,30,30)
s=pygame.Surface((30,30))
s.fill(RED)
pygame.draw.line(screen, GREEN, (0,0), (800,600),1)
pygame.draw.line(screen, BLUE, (0,600), (800,0),1)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                r.move_ip(0, -5)
            elif event.key == pygame.K_DOWN:
                r.move_ip(0, 5)
            elif event.key == pygame.K_LEFT:
                r.move_ip(-5, 0)
            elif event.key == pygame.K_RIGHT:
                r.move_ip(5, 0)
                
    #screen.fill(BLACK)         
    screen.blit(s,r)
    pygame.display.update()
