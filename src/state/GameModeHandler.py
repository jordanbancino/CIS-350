import pygame
from state.MainMenuHandler import Button
import game_state
from arg import load_asset


class GameModeHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self._image_border = load_asset('menu_border.png')
        self.button = load_asset('button.png')
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
        math_button = Button(225, 300, self.button)
        flashcard_button = Button(475, 300, self.button)
        buttons = [math_button, flashcard_button]

        window.fill((100, 100, 100))  # Gray
        window.blit(self._image_border, (0, 0))

        for button in buttons:
            button.blit(window)

        math = self._font.render("MATH", True, "white")
        flashcard = self._font.render("CARD", True, "white")
        gamemode = self._font.render("GAME MODE", True, "white")

        window.blit(math, (270, 325))
        window.blit(flashcard, (520, 325))
        window.blit(gamemode, (((window.get_width() / 2) - (gamemode.get_width() / 2)), 75))

        clicked_buttons = []

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == math_button:
                return game_state.GameState.DIFFICULTY
            elif button == flashcard_button:
                "TO DO: Make flashcard mode"
                pass

        return game_state.GameState.GAME_MODE
