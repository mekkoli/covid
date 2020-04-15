import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clk = pygame.time.Clock()

# carica l'immagine del panda
surf_panda = pygame.image.load("panda.png")
rect_panda = surf_panda.get_rect()

# velocita' del panda
vel_panda = [2,5]

# ciclo principale
done = False
while not done:
    # sottociclo degli eventi
    for ev in pygame.event.get():
        if ev.type == QUIT:
            done = True

    # movimento
    if rect_panda.left < 0 or rect_panda.right > screen.get_width():
        vel_panda[0] *= -1
    if rect_panda.top < 0 or rect_panda.bottom > screen.get_height():
        vel_panda[1] *= -1

    rect_panda.x += vel_panda[0]
    rect_panda.y += vel_panda[1]

    # aggiornamento dello schermo
    #screen.fill((0, 0, 0))
    screen.blit(surf_panda, rect_panda)
    pygame.display.flip()

    clk.tick(100)

pygame.quit()