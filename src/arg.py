"""
arg module: where the game lives
"""
import pygame
from game_state import GameState, StateHandler
from src.state.LevelPlayHandler import LevelPlayHandler
from src.state.QuitHandler import QuitHandler
from state.MainMenuHandler import MainMenuHandler
import log


def main() -> None:
    """
    The game entry function. All initial setup and final teardown
    happens here; this function is always the first pushed on the
    stack and the last popped off, at which point the program
    exits.
    """
    log.getLogger().set_level(log.DEBUG)

    log.msg(log.DEBUG, "Initializing Pygame...")

    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()  # keep track of time

    width, height = 900, 500
    fps = 60  # frames per second

    window = pygame.display.set_mode((width, height))  # create window and set size
    pygame.display.set_caption("ARG")  # set window title

    state = prev_state = GameState.MAIN_MENU  # Initialize state, prev_state for knowing when to set level for example
    events = pygame.event.get()
    handlers = {
        GameState.GAME_QUIT: QuitHandler(state, events, window),
        GameState.MAIN_MENU: MainMenuHandler(state, events, window),
        GameState.LEVEL_PLAY: LevelPlayHandler(state, events, window)
    }

    log.msg(log.DEBUG, f"Entering game loop with handlers {handlers}")
    while state != GameState.GAME_QUIT:
        window.fill('black')  # Clear last frame
        events = pygame.event.get()
        for event in events:  # Check for quit state
            if event.type == pygame.QUIT:
                state = GameState.GAME_QUIT
                break
        match state:
            case GameState.GAME_QUIT:
                break
            case GameState.MAIN_MENU:
                pass
            case GameState.LEVEL_PLAY:
                handlers[state].game_step(pygame.key.get_pressed())  # transfer pressed keys during last iteration
            case _:
                log.msg(log.ERROR, f"Game entered invalid state: {state}. This is a programming error.")
                state = GameState.GAME_QUIT
        handler = handlers[state]
        state = handler.assign_state()
        pygame.display.update()  # new frame, updates screen
        clock.tick(fps)  # next iteration after fps ms
    pygame.quit()


if __name__ == "__main__":
    main()
