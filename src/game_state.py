import pygame


class GameState:
    GAME_QUIT = 0
    MAIN_MENU = 1
    LEVEL_PLAY = 2


class StateHandlerContext:
    def __init__(self, state: GameState, events: list[pygame.event.Event], window: pygame.Surface):
        self.state = state
        self.events = events
        self.window = window

    def get_state(self):
        return self.state

    def get_events(self):
        return self.events

    def get_window(self):
        return self.window


class StateHandler:
    def process(self, context: StateHandlerContext) -> GameState:
        pass
