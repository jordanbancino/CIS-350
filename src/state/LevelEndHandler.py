"""
This handler handles the `LEVEL_END` state, which is entered when the user dies
either by hitting an obstacle because the equation was solved too slowly, or
the user answered the equation incorrectly.

This handler is responsible for displaying the end game menu, which prompts the
player with a few buttons similar to the main menu.

TODO: This screen should display the time and the score.
"""
import pygame

from pygame import mixer
import game_state
import user_data
from arg import load_asset
from game_state import StateHandlerContext
from state.MainMenuHandler import Button


class LevelEndHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)
        self.title_font = pygame.font.SysFont("consolas", 80)
        self._font = pygame.font.SysFont("consolas", 50)
        self._border_image = load_asset('menu_border.png')
        self.button = load_asset('button.png')

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self._border_image = pygame.transform.scale(self._border_image,
                                                    (width, height))

    def process(self,
                context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()

        window.fill((100, 100, 100))

        window.blit(self._border_image, (0, 0))

        reset_button = Button(125, 300, self.button, "RESET")
        back_button = Button(350, 300, self.button, "BACK")
        quit_button = Button(575, 300, self.button, "QUIT")

        buttons = [reset_button, back_button, quit_button]

        gameover = self.title_font.render("GAME OVER", True,"white")

        end_message = self._font.render(str(context.get_storage()['end_game']), True, "white")
        if context.get_storage()['difficulty'] == "infinite":
            time = self._font.render("Time: " + str(round(context.get_storage()['last_play_time'], 2)) +
                                     "s", True, "white")
            score = self._font.render("Score: " + str(context.get_storage()['last_score']), True, "white")
        else:
            time = self._font.render("Time remaining: " + str(round(context.get_storage()['last_play_time'], 2)) +
                                     "s", True, "white")

        for button in buttons:
            button.blit(window)

        clicked_buttons = []

        window.blit(gameover, (((window.get_width() / 2) -
                                (gameover.get_width() / 2)), 75))

        window.blit(end_message, ((window.get_width() - end_message.get_width()) / 2, 150))
        if context.get_storage()['difficulty'] == "infinite":
            window.blit(score, ((window.get_width() - score.get_width()) / 2, 200))
        window.blit(time, ((window.get_width() - time.get_width()) / 2, 250))

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == quit_button:
                mixer.music.stop()
                return game_state.GameState.GAME_QUIT
            elif button == back_button:
                return game_state.GameState.MAIN_MENU
            elif button == reset_button:
                return game_state.GameState.LEVEL_PLAY

        next_state = game_state.GameState.LEVEL_END

        return next_state
