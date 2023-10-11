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

    gui_manager = pygame_gui.UIManager((width, height)) # keeps track / creates of all gui components
    user_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 400), (100, 50)), manager=
                                                     gui_manager, object_id="answer_input_box")
    user_input.placeholder_text = ""

    window = pygame.display.set_mode((width, height))  # create window and set size
    pygame.display.set_caption("ARG")  # set window title

    state = GameState.MAIN_MENU  # Initial state
    handlers = {
        GameState.GAME_QUIT: QuitHandler(),
        GameState.MAIN_MENU: MainMenuHandler(),
        GameState.LEVEL_PLAY: LevelPlayHandler()
    }

    equation = arithmetic.generate_arithmetic()  # initial equation
    print(equation[0])  # test first answer
    speed = 1  # speed of character

    log.msg(log.DEBUG, f"Entering game loop with handlers {handlers}")
    while state != GameState.GAME_QUIT:
        events = pygame.event.get()
       # ui_refresh_rate = clock.tick(60)/10000  # makes game have a strobe effect but makes text box pop-up
        for event in events:
            # Check for quit state
            if event.type == pygame.QUIT:
                state = GameState.GAME_QUIT
            # check if player presses enter in text box
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "answer_input_box":
                answer = int(event.text)
                if arithmetic.solve_arithmetic(equation[1:], int(answer)):  # checks if answer is correct
                    speed += 1  # increase speed by 1 to character
                else:
                    speed = 0  # set speed of character to 0
                user_input.set_text("")  # reset textbox

            gui_manager.process_events(event)

        gui_manager.update(fps)  # updates cursor on text box

        # Clear last frame
        window.fill('black')

        gui_manager.draw_ui(window)  # has manager look at the full window
        pygame.display.update()  # updates screen

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
