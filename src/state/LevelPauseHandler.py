import pygame

import game_state
from arg import load_asset
from game_state import StateHandlerContext
from state.MainMenuHandler import Button



class LevelPauseHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)
        self.title_font = pygame.font.SysFont("consolas", 80)
        self.button_font = pygame.font.SysFont("consolas", 50)
        self._border_image = load_asset('menu_border.png')
        self.button = load_asset('button.png')

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self._border_image = pygame.transform.scale(self._border_image,
                                                    (width, height))

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()

        resume_button = Button(125, 300, self.button)
        back_button = Button(350, 300, self.button)
        quit_button = Button(575, 300, self.button)
        buttons = [resume_button, back_button, quit_button]

        window.fill((100, 100, 100))
        window.blit(self._border_image, (0, 0))

        resume = self.button_font.render("RESUME", True, "white")
        back = self.button_font.render("BACK", True, "white")
        quit = self.button_font.render("QUIT", True, "white")

        # antialias makes text look better
        pause_info = self.title_font.render(
            "PAUSED", True, "white")

        for button in buttons:
            button.blit(window)

        clicked_buttons = []

        window.blit(resume, (143, 325))
        window.blit(back, (395, 325))
        window.blit(quit, (620, 325))
        window.blit(pause_info, ((window.get_width() - pause_info.get_width()) / 2, 75))

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == quit_button:
                return game_state.GameState.GAME_QUIT
            elif button == resume_button:
                return game_state.GameState.LEVEL_PLAY
            elif button == back_button:
                return game_state.GameState.MAIN_MENU

        return game_state.GameState.LEVEL_PAUSE
