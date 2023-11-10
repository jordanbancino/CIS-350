"""
This module contains the game entry point. It is responsible for setting up
Pygame, Pygame GUI, the game state machine, and any other necessary components
before invoking the initial game state handler.

ARG is a finite state machine; each "screen" that gets drawn to the pygame
window is represented by its own state, which is responsible for drawing the
game UI and moving components accordingly.
"""
import pygame
import pygame_gui
import os
import sys


def load_asset(asset: str) -> pygame.Surface | pygame.SurfaceType:
    """
    Load an asset by name from the default assets directory and return a
    Pygame surface which can be blitted to the main window as necessary.
    This function should be used instead of `pygame.image.load()` because all
    assets live in the same place, and if that place changes, then only this
    function has to be modified, not every single place an asset is used.
    """
    path = os.path.join('assets', asset)
    return pygame.image.load(path)


def main() -> None:
    """
    The game entry function. All initial setup and final teardown
    happens here.
    """

    # Imports happen in main() to avoid circular imports, because some of the
    # other functions in here (load_asset()) are used by some of the imports
    # listed here.
    #
    # Not sure if this is the most Python-ic thing ever, but Python lets us, so
    # it must not be too bad, right?
    import log
    from game_state import GameState, StateHandlerContext
    from state.LevelEndHandler import LevelEndHandler
    from state.LevelPauseHandler import LevelPauseHandler
    from state.LevelPlayHandler import LevelPlayHandler
    from state.MainMenuHandler import MainMenuHandler
    from state.QuitHandler import QuitHandler
    from state.DifficultyHandler import DifficultyHandler
    from state.ScoreHandler import ScoreHandler

    log.get_logger().set_level(log.DEBUG)

    log.msg(log.DEBUG, "Initializing Pygame...")

    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()  # keep track of time

    width, height = 900, 500
    fps = 60  # frames per second

    # keeps track / creates of all gui components
    gui_manager = pygame_gui.UIManager((width, height))

    # create window and set size
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("ARG")  # set window title

    prev_state = None
    state = GameState.MAIN_MENU  # Initial state

    # Initial context
    context = StateHandlerContext(state, None, window, gui_manager, -1, {})

    handlers = {
        GameState.GAME_QUIT: QuitHandler(context),
        GameState.MAIN_MENU: MainMenuHandler(context),
        GameState.LEVEL_PLAY: LevelPlayHandler(context),
        GameState.LEVEL_PAUSE: LevelPauseHandler(context),
        GameState.LEVEL_END: LevelEndHandler(context),
        GameState.DIFFICULTY: DifficultyHandler(context),
        GameState.SCORE: ScoreHandler(context)
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
            log.msg(log.ERROR,
                    f"Game entered invalid state: {state}."
                    f"This is a programming error.")
            state = GameState.GAME_QUIT

        handler = handlers[state]

        # Generate a new context with the current state, events, timing, and
        # GUI components. We also copy over the previous context's storage so
        # that state handlers can share data amongst themselves.
        context = StateHandlerContext(state,
                                      events,
                                      window,
                                      gui_manager,
                                      time_delta,
                                      context.get_storage())

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

            # Dispatch events to Pygame GUI
            gui_manager.process_events(event)

        if state != prev_state:
            log.msg(log.DEBUG, f"Leaving state {prev_state}.")
            # State handler on_exit() should know what the next state is,
            # so it may modify its behavior based on this.
            #
            # Yes, I know _state is private and we shouldn't be poking
            # private variables! But the alternative is to create a new state
            # context entirely, so this is just a shorthand that updates only
            # the values necessary.
            context._state = state
            handler.on_exit(context)

        gui_manager.update(time_delta)
        gui_manager.draw_ui(window)

        pygame.display.update()  # updates screen

    pygame.quit()


if __name__ == "__main__":
    # Add our current directory to the module path so that nested modules can
    # reference parent modules cleanly. This happens here instead of main()
    # because it should always happen before any game logic occurs.
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()
