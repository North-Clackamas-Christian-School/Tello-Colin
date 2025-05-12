import threading, time, os, djitellopy, pygame.freetype, pygame,random
from djitellopy import Tello
pygame.init()
screen = pygame.display.set_mode((960,720))
font = pygame.freetype.Font('arial', 30)
surface = pygame.Surface((960,720))
font.render_to(surface, (100, 100), "Hello, Pygame with Freetype!", (255, 255, 255))

run = True
while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.display.flip()