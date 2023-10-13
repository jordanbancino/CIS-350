"""
arg module: where the game lives
"""
import pygame
import pygame_gui

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

    gui_manager = pygame_gui.UIManager((width, height))  # keeps track / creates of all gui components

    window = pygame.display.set_mode((width, height))  # create window and set size
    pygame.display.set_caption("ARG")  # set window title

    state = GameState.MAIN_MENU  # Initial state
    handlers = {
        GameState.GAME_QUIT: QuitHandler(),
        GameState.MAIN_MENU: MainMenuHandler(),
        GameState.LEVEL_PLAY: LevelPlayHandler()
    }

    # equation = arithmetic.generate_arithmetic()  # initial equation
    # print(equation[0])  # test first answer
    # speed = 1  # speed of character

    log.msg(log.DEBUG, f"Entering game loop with handlers {handlers}")
    while state != GameState.GAME_QUIT:
        # Tick the clock
        time_delta = clock.tick(fps) / 1000

        # Empty the pygame event queue
        events = pygame.event.get()

        # Clear last frame
        window.fill('black')

        # Invoke state handler to update state
        if state not in handlers:
            log.msg(log.ERROR, f"Game entered invalid state: {state}. This is a programming error.")
            state = GameState.GAME_QUIT

        handler = handlers[state]
        context = StateHandlerContext(state, events, window, gui_manager)

        state = handler.process(context)

        for event in events:
            # Check for quit state
            if event.type == pygame.QUIT:
                state = GameState.GAME_QUIT
            gui_manager.process_events(event)

        gui_manager.draw_ui(window)  # has manager look at the full window

        gui_manager.update(time_delta)  # updates cursor on text box
        gui_manager.draw_ui(window)  # has manager look at the full window

        pygame.display.update()  # updates screen

    pygame.quit()


if __name__ == "__main__":
    main()
