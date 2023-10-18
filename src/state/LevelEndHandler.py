import pygame
from src import game_state
from src.graphics import load_asset
from src.state.MainMenuHandler import Button



class LevelEndHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)
        self.font = pygame.font.SysFont("comicsans", 80)
        self.border_image = load_asset('menu_border.png')
        self.reset_image = load_asset('reset_button.png')
        self.image_button_main_menu = load_asset('main_menu_button.png')
        self.image_button_quit = load_asset('quit_button.png')

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self.border_image = pygame.transform.scale(self.border_image, (width, height))

    def process(self, context: game_state.StateHandlerContext) -> game_state.GameState:
        super().process(context)

        window = context.get_window()
        window.fill((47, 79, 79))

        window.blit(self.border_image, (0, 0))

        reset_button = Button(350, 75, self.reset_image)
        main_menu_button = Button(350, 200, self.image_button_main_menu)
        quit_button = Button(350, 325, self.image_button_quit)

        buttons = [reset_button, main_menu_button, quit_button]

        for button in buttons:
            button.draw(window)

        clicked_buttons = []

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == quit_button:
                return game_state.GameState.GAME_QUIT
            elif button == main_menu_button:
                return game_state.GameState.MAIN_MENU
            elif button == reset_button:
                return game_state.GameState.LEVEL_PLAY

        end_info_game = self.font.render("GAME", True, "white")  # antialias makes text look better
        end_info_over = self.font.render("OVER", True, "white")
        window.blit(end_info_game, (100, (window.get_height() - end_info_game.get_height()) / 2))
        window.blit(end_info_over, (575, (window.get_height() - end_info_over.get_height()) / 2))

        next_state = game_state.GameState.LEVEL_END

        return next_state