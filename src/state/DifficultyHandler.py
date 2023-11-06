import pygame
from state.MainMenuHandler import Button
import game_state
from arg import load_asset


class DifficultyHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self._image_border = load_asset('menu_border.png')
        self.button = load_asset('button.png')
        self.infinity = load_asset("infinity.png")
        self._font = pygame.font.SysFont("consolas", 50)

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self.infinity_image = pygame.transform.scale(
            self.infinity, (100, 50))
        self._image_border = pygame.transform.scale(
            self._image_border, (width, height))

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()

        # create button instances
        easy_button = Button(125, 300, self.button)
        medium_button = Button(350, 300, self.button)
        hard_button = Button(575, 300, self.button)
        infinite_button = Button(350, 175, self.button)
        buttons = [easy_button, medium_button, hard_button, infinite_button]

        window.fill((100, 100, 100))  # Gray
        window.blit(self._image_border, (0, 0))

        for button in buttons:
            button.blit(window)

        easy = self._font.render("EASY", True, "white")
        medium = self._font.render("MEDIUM", True, "white")
        hard = self._font.render("HARD", True, "white")
        difficulty = self._font.render("DIFFICULTY", True, "white")

        window.blit(easy, (170, 325))
        window.blit(medium, (368, 325))
        window.blit(hard, (620, 325))
        window.blit(self.infinity_image, (400, 200))
        window.blit(difficulty, (((window.get_width() / 2) - (difficulty.get_width() / 2)), 75))

        clicked_buttons = []

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == easy_button:
                return game_state.GameState.LEVEL_PLAY
            elif button == medium_button:
                return game_state.GameState.LEVEL_PLAY
            elif button == hard_button:
                return game_state.GameState.LEVEL_PLAY
            elif button == infinite_button:
                return game_state.GameState.LEVEL_PLAY

        return game_state.GameState.DIFFICULTY
