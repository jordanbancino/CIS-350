import pygame

import game_state
from graphics import load_asset


class Button:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (200, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, window):
        """
        Draws a button on the display and monitors clicking.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))

    def dispatch_event(self, event) -> bool:
        """
        Receive an event from the processor context and use it to determine
        whether this button was clicked.
        """

        # Only respond to mouse up events
        if event.type == pygame.MOUSEBUTTONUP:
            # Get mouse position when the event was fired.
            # We don't want to use the current mouse position because it
            # may have changed since the event was dispatched to us.
            pos = event.__dict__['pos']

            # If the click was inside our bounding box, this button was
            # pressed.
            return self.rect.collidepoint(pos)
        # Not even a mouse up event, so this can't be a click
        return False


class MainMenuHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self.image_border = load_asset('menu_border.png')
        self.image_button_start = load_asset('start_button.png')
        self.image_button_score = load_asset('score_button.png')
        self.image_button_quit = load_asset('quit_button.png')

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self.image_border = pygame.transform.scale(
            self.image_border, (width, height))

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()

        # create button instances
        start_button = Button(350, 75, self.image_button_start)
        score_button = Button(350, 200, self.image_button_score)
        quit_button = Button(350, 325, self.image_button_quit)
        buttons = [start_button, score_button, quit_button]

        window.fill((47, 79, 79))  # Gray
        window.blit(self.image_border, (0, 0))

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
            elif button == start_button:
                return game_state.GameState.LEVEL_PLAY
            elif button == score_button:
                # TODO: Handle score button click
                pass

        return game_state.GameState.MAIN_MENU
