import random
import time

import pygame

WIDTH = 850
HEIGHT = 850
FPS = 60
SIZE = 25
GRID_SIZE = 25
THICC = 10
DELAY = 0.01 # in seconds

current_cell = 0

grid = []
solve = []
visited_stack = []
visited = set()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

run_gen = True
run_alg = True
run_solve = True
solved = False

win.fill((255, 255, 255))

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top_edge = False
        self.right_edge = False
        self.left_edge = False
        self.bottom_edge = False

def redraw_game_win():
    pygame.display.update()

def draw_grid():
    for row in range(1, GRID_SIZE + 1):
        for col in range(1, GRID_SIZE + 1):
            pygame.draw.line(win, (0, 0, 0,), (row * SIZE, col * SIZE), (row * SIZE + SIZE, col * SIZE), THICC)
            pygame.draw.line(win, (0, 0, 0,), (row * SIZE, col * SIZE + SIZE), (row * SIZE, col * SIZE), THICC)

    # finishing lines that the for loop didn't catch.
    pygame.draw.line(win, (0, 0, 0,), (SIZE * GRID_SIZE + SIZE, SIZE), (SIZE * GRID_SIZE + SIZE, SIZE * GRID_SIZE + SIZE), THICC)
    pygame.draw.line(win, (0, 0, 0,), (SIZE, SIZE * GRID_SIZE + SIZE), (SIZE * GRID_SIZE + SIZE, SIZE * GRID_SIZE + SIZE), THICC)

    # Make opening
    pygame.draw.line(win, (255, 255, 255), (SIZE, SIZE), (SIZE, SIZE+ SIZE - (THICC//2)), THICC)
    # Make exit
    pygame.draw.line(win, (255, 255, 255), ((GRID_SIZE * SIZE) + SIZE, (GRID_SIZE * SIZE)), ((GRID_SIZE * SIZE) + SIZE, (GRID_SIZE * SIZE) + GRID_SIZE + THICC), THICC)
draw_grid()

def make_grid():
    for r in range(1, GRID_SIZE + 1):
        for c in range(1, GRID_SIZE + 1):
            grid.append(Cell(c * SIZE, r * SIZE))
make_grid()

def add_edge_Cells():
    for k, _ in enumerate(grid):
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
add_edge_Cells()

def wall_knock(directionection, cell):
    if directionection == "north":
        pygame.draw.line(win, (255, 255, 255), (cell.x + (THICC//2+ 1), cell.y), (cell.x + SIZE - (THICC//2), cell.y), THICC)
    elif directionection == "south":
        pygame.draw.line(win, (255, 255, 255), (cell.x + (THICC//2 + 1), cell.y + SIZE), (cell.x - (THICC//2) + SIZE, cell.y + SIZE), THICC)
    elif directionection == "west":
        pygame.draw.line(win, (255, 255, 255), (cell.x, cell.y + (THICC//2 + 1)), (cell.x, cell.y + SIZE - (THICC//2)), THICC)
    elif directionection == "east":
        pygame.draw.line(win, (255, 255, 255), (cell.x + SIZE, cell.y + (THICC//2 + 1)), (cell.x + SIZE, cell.y + SIZE - (THICC//2)), THICC)

def get_neeighbors(current_cell):
    nextdoor = []
    if current_cell - GRID_SIZE >= 0:
        if not grid[current_cell].top_edge:
            if not grid[current_cell - GRID_SIZE] in visited:
                nextdoor.append(current_cell - GRID_SIZE)

    if current_cell - 1 >= 0:
        if not grid[current_cell].left_edge:
            if not grid[current_cell - 1] in visited:
                nextdoor.append(current_cell - 1)

    if current_cell + 1 < len(grid):
        if not grid[current_cell].right_edge:
            if not grid[current_cell + 1] in visited:
                nextdoor.append(current_cell + 1)

    if current_cell + GRID_SIZE < len(grid):
        if not grid[current_cell].bottom_edge:
            if not grid[current_cell + GRID_SIZE] in visited:
                nextdoor.append(current_cell + GRID_SIZE)

    return [c for c in nextdoor if c not in visited]

def knock_neighbor(current_cell):
    neighbors = get_neeighbors(current_cell)
    visited.add(current_cell)

    if not neighbors:
        backtrack_to_cell = visited_stack.pop() if visited_stack else None
        return backtrack_to_cell

    visited_stack.append(current_cell)
    choice = random.choice(neighbors)

    if choice == current_cell - GRID_SIZE:
        direction = "north"
    elif choice == current_cell - 1:
        direction = "west"
    elif choice == current_cell + 1:
        direction = "east"
    elif choice == current_cell + GRID_SIZE:
        direction = "south"
    else:
        print("error in knock_neighbor() during direction selection")
    wall_knock(direction, grid[current_cell])
    current_cell = choice
    return current_cell

def color_checking():
    for vis, _ in enumerate(grid):
        if vis in visited:
            pygame.draw.rect(win, (255, 255, 255), (grid[vis].x + (THICC//2 + 1), grid[vis].y + (THICC//2 + 1), SIZE - (THICC), SIZE - (THICC)), 0)

    pygame.draw.rect(win, (255, 0, 0), (grid[current_cell].x + (THICC//2 + 1), grid[current_cell].y + (THICC//2 + 1), SIZE - (THICC), SIZE - (THICC)), 0)

while run_gen:
    current_cell = knock_neighbor(current_cell)

    if not current_cell:
        break

    if not solved:
        if current_cell == GRID_SIZE * GRID_SIZE - 1:
            solve = visited_stack.copy()
            solved = True

    color_checking()
    redraw_game_win()
    time.sleep(DELAY/2)

while run_solve:
    for sol, _ in enumerate(solve):
        pygame.draw.rect(win, (0, 255, 0), (grid[solve[sol]].x + (THICC//2 + 1), grid[solve[sol]].y + (THICC//2 + 1), SIZE - (THICC), SIZE - (THICC)), 0)
        pygame.display.update()
        time.sleep(DELAY)

    # fill last square
    pygame.draw.rect(win, (0, 255, 0), (grid[len(grid)-1].x + (THICC//2 + 1), grid[len(grid)-1].y + (THICC//2 + 1), SIZE - (THICC), SIZE - (THICC)), 0)