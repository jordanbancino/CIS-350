import pygame

from src import game_state


class QuitHandler(game_state.StateHandler):
    def __init__(self, state, events, window):
        super().__init__(state, events, window)

    def assign_state(self) -> game_state.GameState:
        return game_state.GameState.GAME_QUIT
