"""
arg module: where the game lives
"""
import pygame
import pygame_gui

import arithmetic
from game_state import GameState, StateHandlerContext
import log
from src.state.LevelPlayHandler import LevelPlayHandler
from src.state.LevelPauseHandler import LevelPauseHandler
from src.state.QuitHandler import QuitHandler
from state.MainMenuHandler import MainMenuHandler
from state.LevelEndHandler import LevelEndHandler


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
    fps = 60  # frames per second

    gui_manager = pygame_gui.UIManager((width, height))  # keeps track / creates of all gui components

    window = pygame.display.set_mode((width, height))  # create window and set size
    pygame.display.set_caption("Arithman")  # set window title

    prev_state = None
    state = GameState.MAIN_MENU  # Initial state

    init_context = StateHandlerContext(state, None, window, gui_manager, -1)
    handlers = {
        GameState.GAME_QUIT: QuitHandler(init_context),
        GameState.MAIN_MENU: MainMenuHandler(init_context),
        GameState.LEVEL_PLAY: LevelPlayHandler(init_context),
        GameState.LEVEL_PAUSE: LevelPauseHandler(init_context),
        GameState.LEVEL_END: LevelEndHandler(init_context)
    }

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
        context = StateHandlerContext(state, events, window, gui_manager, time_delta)

        if state != prev_state:
            log.msg(log.DEBUG, f"Entering state {state}.")
            handler.on_enter(context)

        prev_state = state
        state = handler.process(context)

        for event in events:
            # log.msg(log.DEBUG, f"Received event: {event}")

            # Process global events
            if event.type == pygame.QUIT:
                state = GameState.GAME_QUIT
            if event.type == pygame.WINDOWLEAVE and state == GameState.LEVEL_PLAY:
                state = GameState.LEVEL_PAUSE

            # Dispatch events to Pygame GUI
            gui_manager.process_events(event)

        if state != prev_state:
            log.msg(log.DEBUG, f"Leaving state {prev_state}.")
            handler.on_exit(context)

        gui_manager.update(time_delta)
        gui_manager.draw_ui(window)

        pygame.display.update()  # updates screen

    pygame.quit()


if __name__ == "__main__":
    main()
