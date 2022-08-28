import pygame as pg

pg.init()

# Setting the grid size and difficulty from user input
# while True:
#     try:
#         grid_size = int(input("Enter grid size (5 to 20): "))
#         difficulty = int(input("Enter snake speed (1 to 20): "))
#     except (ValueError, TypeError) as error:
#         print("You must enter an integer.")
#         continue
#     else:
#         break

grid_size = 10
difficulty = 10

# Setting up screen
SCREEN_WIDTH = SCREEN_HEIGHT = 800
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setting up clock
clock = pg.time.Clock()
fps = 60

# Setting up global game variables
TILE_SIZE = SCREEN_WIDTH // grid_size
empty_tiles = [(x, y) for x in range(0, SCREEN_WIDTH, TILE_SIZE) for y in range(0, SCREEN_HEIGHT, TILE_SIZE)]

# Border is not fully functional to work with drawing yet, but can be changed
# to certain values for a different game feel (i.e 2, 4, 6 up to 10)
border = 0
