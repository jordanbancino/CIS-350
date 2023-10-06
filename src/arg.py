"""
arg module: where the game lives
"""
import pygame
from menu import *
from graphics import *
import arithmetic

fps = 120  # frames per second

def not_exit():
    """
    Returns True if user clicked "QUIT" or window's "X" buttons.
    """
    if quit_button.draw(window):
        pygame.quit()  # close window, end program
        return False
    for event in pygame.event.get():  # iterate over all occurred events since last while-loop iteration
        if event.type == pygame.QUIT:  # if user pressed window's "X"
            pygame.quit()  # close window, end program
            return False
    return True

def main() -> None:
    """
	The game entry function. All initial setup and final teardown
	happens here; this function is always the first pushed on the
	stack and that last popped off, at which point the program
	exits.
	"""
    clock = pygame.time.Clock()  # keep track of time
    set_main_menu(window,)
    while not_exit():
        if start_button.draw(window):
            break
    # start_game()
    while not_exit():
        clock.tick(fps)  # run while-loop at a max rate of fps
        update_ui(window)
        stickman.x += 1  # character moves 1 pixel per frame


if __name__ == "__main__":
    main()
