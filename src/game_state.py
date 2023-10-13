import pygame
import pygame_gui


class GameState:
    GAME_QUIT = 0
    MAIN_MENU = 1
    LEVEL_PLAY = 2


class StateHandlerContext:
    def __init__(self, state: GameState, events: list[pygame.event.Event], window: pygame.Surface, gui: pygame_gui.UIManager):
        self.state = state
        self.events = events
        self.window = window
        self.gui = gui

    def get_state(self):
        return self.state

    def get_events(self):
        return self.events

    def get_window(self):
        return self.window

    def get_gui(self):
        return self.gui

class StateHandler:
    def process(self, context: StateHandlerContext) -> GameState:
        pass
