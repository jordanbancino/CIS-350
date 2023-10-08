import pygame

from src import game_state


class QuitHandler(game_state.StateHandler):
    def process(self, context: game_state.StateHandlerContext) -> game_state.GameState:
        return game_state.GameState.GAME_QUIT
