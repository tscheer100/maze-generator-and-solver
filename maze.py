import random
import time

import pygame

WIDTH = 500
HEIGHT = 500
FPS = 60

pygame.init()
pygame.mixer.init()


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test")

clock = pygame.time.Clock()

run = True


win.fill((255,255,255))

def redrawGameWin():
    pygame.display.update()


class cell(object):
    def __init__(self, x, y): 
        self.visited = False
        self.x = x
        self.y = y

        # n, w, e, s represents north, west, east, south repsectively  
        self.n_wall = pygame.draw.line(win, (0, 0, 0), (self.x - 10, self.y - 10), (self.x + 10, self.y - 10), 5)
        self.w_wall = pygame.draw.line(win, (0, 0, 0), (self.x - 10, self.y - 10), (self.x - 10, self.y + 10), 5)
        self.e_wall = pygame.draw.line(win, (0, 0, 0), (self.x + 10, self.y - 10), (self.x + 10, self.y + 10), 5)
        self.s_wall = pygame.draw.line(win, (0, 0, 0), (self.x - 10, self.y + 10), (self.x + 10, self.y + 10), 5)

while run:

    test_cell = cell(30,30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    redrawGameWin()

pygame.quit
