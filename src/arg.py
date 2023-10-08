"""
arg module: where the game lives
"""
import pygame

import arithmetic
from game_state import GameState, StateHandler, StateHandlerContext
import log
from src.state.LevelPlayHandler import LevelPlayHandler
from src.state.QuitHandler import QuitHandler
from state.MainMenuHandler import MainMenuHandler


def main() -> None:
    """
    The game entry function. All initial setup and final teardown
    happens here; this function is always the first pushed on the
    stack and that last popped off, at which point the program
    exits.
    """
    log.getLogger().set_level(log.DEBUG)

    log.msg(log.DEBUG, "Initializing Pygame...")

    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()  # keep track of time

    width, height = 900, 500
    fps = 120  # frames per second

    window = pygame.display.set_mode((width, height))  # create window and set size
    pygame.display.set_caption("ARG")  # set window title

    state = GameState.MAIN_MENU
    handlers = {
        GameState.GAME_QUIT: QuitHandler(),
        GameState.MAIN_MENU: MainMenuHandler(),
        GameState.LEVEL_PLAY: LevelPlayHandler()
    }

    log.msg(log.DEBUG, f"Entering game loop with handlers {handlers}")
    while state != GameState.GAME_QUIT:
        events = pygame.event.get()
        # Check for quit state
        for event in events:
            if event.type == pygame.QUIT:
                state = GameState.GAME_QUIT

        # Clear last frame
        window.fill('black')

        # Invoke state handler to update state
        if state not in handlers:
            log.msg(log.ERROR, f"Game entered invalid state: {state}. This is a programming error.")
            state = GameState.GAME_QUIT

        handler = handlers[state]
        context = StateHandlerContext(state, events, window)

        state = handler.process(context)

        # Push to display and tick the clock
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
