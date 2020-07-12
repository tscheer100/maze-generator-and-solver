import random
import time

import pygame

WIDTH = 850
HEIGHT = 850
FPS = 60
SIZE = 30
GRID_SIZE = 15
THICC = 10

grid = []
visited = []
visited_stack = []

prev_cell = 0

pygame.mixer.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

clock = pygame.time.Clock()

run = True
run_alg = True

win.fill((255,255,255))

dir_choice = ["north", "west", "east", "south"]

def redrawGameWin():
    pygame.display.update()

class cell(object):
    def __init__(self, x, y): 
        self.x = x
        self.y = y
        self.top_edge = False
        self.right_edge = False
        self.left_edge = False
        self.bottom_edge = False

def drawGrid():
    for row in range(1, GRID_SIZE + 1):
        for col in range(1, GRID_SIZE + 1):
            pygame.draw.line(win, (0,0,0), (row * SIZE, col * SIZE), (row * SIZE + SIZE, col * SIZE), THICC)
            pygame.draw.line(win, (0,0,0), (row * SIZE, col * SIZE + SIZE), (row * SIZE, col * SIZE), THICC) 

    # finishing lines that the for loop didn't catch.        
    pygame.draw.line(win, (0,0,0), (SIZE * GRID_SIZE + SIZE, SIZE), (SIZE * GRID_SIZE + SIZE, SIZE * GRID_SIZE + SIZE), THICC)
    pygame.draw.line(win, (0,0,0), (SIZE, SIZE * GRID_SIZE + SIZE), (SIZE * GRID_SIZE + SIZE, SIZE * GRID_SIZE + SIZE), THICC)  
drawGrid()

def makeGrid():
    for r in range(1, GRID_SIZE + 1):
        for c in range(1, GRID_SIZE + 1):
            grid.append(cell(c * SIZE, r * SIZE))          
makeGrid()

def addEdgeCells():

    for k in range(0,len(grid)):

        if k >= 0 and k < 10:
            grid[k].top_edge = True
        elif k % GRID_SIZE == GRID_SIZE-1:
            grid[k].right_edge = True
        elif k % GRID_SIZE == 0:
            grid[k].left_edge = True
        elif k >= ((GRID_SIZE * GRID_SIZE) - (GRID_SIZE) + 1) and k <= (GRID_SIZE * GRID_SIZE):
            grid[k].bottom_edge = True

        # check for zero because, for the left edge, k % 10 is not valid
        if k == 0:
            grid[k].left_edge = True
        # same idea with 9 
        grid[SIZE-1].right_edge = True

addEdgeCells()



def wallKnock(dir, cell):
    if dir == "north":
        pygame.draw.line(win, (255,255,255), (cell.x + (THICC/2+ 1) , cell.y), (cell.x + SIZE - (THICC/2), cell.y), THICC) 
    elif dir == "south":
        pygame.draw.line(win, (255,255,255), (cell.x + (THICC/2 + 1) , cell.y + SIZE), (cell.x - (THICC/2) + SIZE, cell.y + SIZE), THICC)
    elif dir == "west":
        pygame.draw.line(win, (255,255,255), (cell.x, cell.y + (THICC/2 + 1)), (cell.x, cell.y + SIZE - (THICC/2)), THICC)
    elif dir == "east": 
        pygame.draw.line(win, (255,255,255), (cell.x + SIZE, cell.y + (THICC/2 + 1)), (cell.x + SIZE, cell.y + SIZE - (THICC/2)), THICC)


def getNeighbors(current_cell):
    nextdoor = []
    if current_cell - GRID_SIZE >= 0:
        if grid[current_cell].top_edge == False:
            if not grid[current_cell - GRID_SIZE] in visited:
                nextdoor.append(current_cell - GRID_SIZE)

    if current_cell - 1 >= 0:
        if grid[current_cell].left_edge == False:
            if not grid[current_cell - 1] in visited:
                nextdoor.append(current_cell - 1)

    if current_cell + 1 < len(grid):
        if grid[current_cell].right_edge == False:
            if not grid[current_cell + 1] in visited:
                nextdoor.append(current_cell + 1)

    if current_cell + GRID_SIZE < len(grid):
        if grid[current_cell].bottom_edge == False:
            if not grid[current_cell + GRID_SIZE] in visited:
                nextdoor.append(current_cell + GRID_SIZE)
    
    # debug
    # print("nextdoor" + str(nextdoor))

    return [c for c in nextdoor if c not in visited]

def knockNeighbor(current_cell):
    neighbors = getNeighbors(current_cell)
    visited.append(current_cell)

    dir = ""
    
    if not neighbors:
        backtrack_to_cell = visited_stack.pop() if visited_stack else None
        print("no neighbours. pop visited", backtrack_to_cell)
        return backtrack_to_cell

    visited_stack.append(current_cell)
    choice = random.choice(neighbors)

    if choice == current_cell - GRID_SIZE:
        dir = "north"
    elif choice == current_cell - 1:
        dir = "west"
    elif choice == current_cell + 1:
        dir = "east"
    elif choice == current_cell + GRID_SIZE:
        dir = "south"
    else:
        print("error in knockNeighbor() during dir selection")
    wallKnock(dir, grid[current_cell])
    current_cell = choice
    # print("choice " + str(choice))
    # print(visited)
    return current_cell

# debug
# print(current_cell)

# Debug edge cells
# for l in range(0,(len(grid))):
#     print(str(l) + " top edge " + str(grid[l].top_edge) + " right edge " + str(grid[l].right_edge) + " left edge " + str(grid[l].left_edge) + " bottom edge " + str(grid[l].bottom_edge) ) 

# Debug wall knockdown
# chooseWallKnock("north", grid[14])
# chooseWallKnock("south", grid[14])
# chooseWallKnock("west", grid[14])
# chooseWallKnock("east", grid[14])

# Debug grid cords
# for i in range(0, len(grid)):
#     print(grid[i].x, grid[i].y) 



current_cell = 0
backtracked = False

def colorChecking():
    for vis in range(0,len(grid)):
        if vis in visited:   
            pygame.draw.rect(win, (255,255,255), (grid[vis].x + (THICC/2 + 1), grid[vis].y + (THICC/2 + 1), SIZE - (THICC), SIZE - (THICC)), 0)
    
    pygame.draw.rect(win, (255,0,0), (grid[current_cell].x + (THICC/2 + 1), grid[current_cell].y + (THICC/2 + 1), SIZE - (THICC), SIZE - (THICC)), 0)

while run:
    time.sleep(.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # print(visited_stack)
    if run_alg:
        current_cell = knockNeighbor(current_cell)
    if not current_cell:
        run_alg = False



    colorChecking()
    redrawGameWin()

pygame.quit