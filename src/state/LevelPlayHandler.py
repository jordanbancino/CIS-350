import pygame

from src import game_state
from src.graphics import load_asset


class LevelPlayHandler(game_state.StateHandler):
    def __init__(self):
        self.font_size = 20
        self.score = 0
        self.image_background = load_asset('background.png')
        self.image_character = load_asset('stickman.png')
        self.stickman = pygame.Rect(300, 315, 100, 100)
        self.font = pygame.font.SysFont("comicsans", self.font_size)

        self.init = False

    def process(self, context: game_state.StateHandlerContext) -> game_state.GameState:
        window = context.get_window()

        if not self.init:
            width = window.get_width()
            height = window.get_height()

            self.image_background = pygame.transform.scale(self.image_background, (width, height))
            self.image_character = pygame.transform.scale(self.image_character, (100, 100))

            self.init = True

        pause_info = self.font.render("Press SPACEBAR To Pause", True, "black")  # antialias makes text look better
        score_info = self.font.render("SCORE: " + str(self.score), True, "black")

        window.blit(self.image_background, (0, 0))
        # set pause_info text on top right with 5x5 px padding
        window.blit(pause_info, (window.get_width() - pause_info.get_width() - 5, 5))  # blit pause_info post background to be front
        window.blit(score_info, (350, 5))
        window.blit(self.image_character, (self.stickman.x, self.stickman.y))  # displays the character at a position

        return game_state.GameState.LEVEL_PLAY
