"""
This handler handles the `MAIN_MENU` state. It displays the main menu and waits
for the user to make a selection.
"""
import pygame
from pygame import mixer
import game_state
from arg import load_asset


class Button:
    """
    A simple class that represents a Pygame button. Note that this class does
    *not* use the Pygame GUI module; rather, it simply blits an image to the
    window and monitors incoming events to know if that area was clicked. In
    the future, this class may be a proper button class that takes button text
    and color instead of an image.
    """
    def __init__(self, x, y, image):
        self._image = pygame.transform.scale(image, (200, 100))
        self._rect = self._image.get_rect()
        self._rect.topleft = (x, y)
        self._clicked = False

    def blit(self, window):
        """
        Draw the button image on the screen.
        """
        window.blit(self._image, (self._rect.x, self._rect.y))

    def dispatch_event(self, event) -> bool:
        """
        Receive an event from the processor context and use it to determine
        whether this button was clicked, returning `False` if this event does
        not indicate a click of this button and `True` if it does.
        """

        # Only respond to mouse up events
        if event.type == pygame.MOUSEBUTTONUP:
            # Get mouse position when the event was fired.
            # We don't want to use the current mouse position because it
            # may have changed since the event was dispatched to us.
            pos = event.__dict__['pos']

            # If the click was inside our bounding box, this button was
            # pressed.
            return self._rect.collidepoint(pos)
        # Not even a mouse up event, so this can't be a click
        return False


class MainMenuHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self._image_border = load_asset('menu_border.png')
        self._image_button_start = load_asset('start_button.png')
        self._image_button_score = load_asset('score_button.png')
        self._image_button_quit = load_asset('quit_button.png')
        self._font = pygame.font.SysFont("consolas", 80)

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self._image_border = pygame.transform.scale(
            self._image_border, (width, height))

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()

        mixer.music.init()
        mixer.music.load("song.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()

        # create button instances
        start_button = Button(350, 75, self._image_button_start)
        score_button = Button(350, 200, self._image_button_score)
        quit_button = Button(350, 325, self._image_button_quit)
        buttons = [start_button, score_button, quit_button]

        window.fill((47, 79, 79))  # Gray
        window.blit(self._image_border, (0, 0))
       # welcome = self._font.render("ARG", True, "white")
        #window.blit(welcome, (((window.get_width() - welcome.get_width()) / 2), 0))

        for button in buttons:
            button.blit(window)

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
