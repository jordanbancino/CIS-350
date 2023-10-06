"""
arg module: where the game lives
"""
import pygame
from menu import *
from graphics import *
import arithmetic

fps = 120  # frames per second

def main() -> None:
    """
	The game entry function. All initial setup and final teardown
	happens here; this function is always the first pushed on the
	stack and that last popped off, at which point the program
	exits.
	"""
    clock = pygame.time.Clock()  # keep track of time
    set_main_menu(window)
    # start_game()
    running = True
    while running:
        clock.tick(fps) # run while-loop at a max rate of fps
        if start_button.draw(window):
            update_ui(window)
        if quit_button.draw(window):
            running = False
        for event in pygame.event.get():  # iterate over all occurred events since last while-loop iteration
            if event.type == pygame.QUIT:  # if user pressed window's "X"
                running = False
                pygame.quit()

    


if __name__ == "__main__":
    main()
