import pygame
from state.MainMenuHandler import Button
import game_state
from arg import load_asset


class GameModeHandler(game_state.StateHandler):
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
        math_button = Button(225, 300, self.button, "MATH")
        card_button = Button(475, 300, self.button, "CARD")
        buttons = [math_button, card_button]

        window.fill((100, 100, 100))  # Gray
        window.blit(self._image_border, (0, 0))

        for button in buttons:
            button.blit(window)

        game_mode = self.title_font.render("GAME MODE", True, "white")

        window.blit(game_mode, (((window.get_width() / 2) - (game_mode.get_width() / 2)), 75))
        clicked_buttons = []

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == math_button:
                context.get_storage()['live_mode'] = "math"
                return game_state.GameState.DIFFICULTY
            if button == card_button:
                context.get_storage()['live_mode'] = "card"
                return game_state.GameState.LEVEL_PLAY

        return game_state.GameState.GAME_MODE
