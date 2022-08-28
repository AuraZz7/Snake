from core.game import *


"""
This file contains the main game loop which
calls the update, draw and handle_events()
function for the game class every frame.
"""


def main():
    running = True
    while running:
        pg.display.set_caption("Snake by Omar")

        clock.tick(fps)

        if pg.event.get(pg.QUIT):
            running = False

        game.handle_events()
        game.update()
        game.draw()

        pg.display.update()
