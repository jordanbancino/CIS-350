import pygame
from state.MainMenuHandler import Button
import game_state
from arg import load_asset


class ScoreHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self._image_border = load_asset('menu_border.png')
        self.button = load_asset('button.png')
        self.title_font = pygame.font.SysFont("consolas", 80)
        self._font = pygame.font.SysFont("consolas", 50)

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self._image_border = pygame.transform.scale(
            self._image_border, (width, height))

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()

        # create button instances
        back_button = Button(350, 300, self.button, "BACK")
        buttons = [back_button]

        window.fill((100, 100, 100))  # Gray
        window.blit(self._image_border, (0, 0))

        for button in buttons:
            button.blit(window)

        score_info = self.title_font.render("RECENT SCORES", True, "white")
        score1 = self._font.render("1: ", True, "white")
        score2 = self._font.render("2: ", True, "white")
        score3 = self._font.render("3: ", True, "white")
        score4 = self._font.render("4: ", True, "white")
        score5 = self._font.render("5: ", True, "white")

        window.blit(score_info, (((window.get_width() / 2) - (score_info.get_width() / 2)), 75))
        window.blit(score1, (300, 150))
        window.blit(score2, (550, 150))
        window.blit(score3, (300, 200))
        window.blit(score4, (550, 200))
        window.blit(score5, (375, 250))

        clicked_buttons = []

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == back_button:
                return game_state.GameState.MAIN_MENU

        return game_state.GameState.SCORE
