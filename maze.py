import random
import time

import pygame

WIDTH = 500
HEIGHT = 500
FPS = 60
SIZE = 40
GRID_SIZE = 10

pygame.init()
pygame.mixer.init()


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")


clock = pygame.time.Clock()

run = True


win.fill((255,255,255))

dir_choice = ["north", "west", "east", "south"]

def redrawGameWin():
    pygame.display.update()


class cell(object):
    def __init__(self, x, y): 
        self.visited = False
        self.x = x
        self.y = y


def drawGrid():
    for row in range(1, GRID_SIZE + 1):
        for col in range(1, GRID_SIZE + 1):
            pygame.draw.line(win, (0,0,0), (row * SIZE, col * SIZE), (row * SIZE + SIZE, col * SIZE))
            pygame.draw.line(win, (0,0,0), (row * SIZE, col * SIZE + SIZE), (row * SIZE, col * SIZE)) 

    # finishing lines that the for loop didn't catch.        
    pygame.draw.line(win, (0,0,0), (SIZE * GRID_SIZE + SIZE, SIZE), (SIZE * GRID_SIZE + SIZE, SIZE * GRID_SIZE + SIZE))
    pygame.draw.line(win, (0,0,0), (SIZE, SIZE * GRID_SIZE + SIZE), (SIZE * GRID_SIZE + SIZE, SIZE * GRID_SIZE + SIZE))  
drawGrid()

grid = []

def makeGrid():
    for r in range(1, GRID_SIZE + 1):
        for c in range(1, GRID_SIZE + 1):
            grid.append(cell(r * SIZE, c * SIZE))
            
            
makeGrid()
for i in range(0, len(grid)):
    print(grid[i].x, grid[i].y)            

while run:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    redrawGameWin()

pygame.quit
