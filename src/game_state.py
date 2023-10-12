import pygame


class GameState:
    GAME_QUIT = 0
    MAIN_MENU = 1
    LEVEL_PLAY = 2
    PAUSE = 3
    LEVEL_END = 4


class StateHandler:
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

    def assign_state(self) -> GameState:
        pass
