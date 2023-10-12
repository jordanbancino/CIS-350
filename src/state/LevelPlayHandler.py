import pygame

from src import game_state
from src.graphics import load_asset
from src import arithmetic


class LevelPlayHandler(game_state.StateHandler):
    def __init__(self, state: game_state.GameState, events: list[pygame.event.Event], window: pygame.Surface):
        super().__init__(state, events, window)
        self.font_size = 20
        self.score = 0
        self.image_background = load_asset('background.png')
        self.image_character = load_asset('stickman.png')
        self.stickman = pygame.Rect(150, 315, 100, 100)
        self.font = pygame.font.SysFont("comicsans", self.font_size)
        self.width = window.get_width()
        self.height = window.get_height()
        self.image_background = pygame.transform.scale(self.image_background, (self.width, self.height))
        self.image_character = pygame.transform.scale(self.image_character, (100, 100))
        self.pause_info = self.font.render("Press SPACEBAR To Pause", True, "black")  # antialias makes text look better
        self.score_info = self.font.render("SCORE: " + str(self.score), True, "black")
        self.question = arithmetic.generate_arithmetic()
        self.answer = '_'
        self.answered = False

    def assign_state(self) -> game_state.GameState:
        # TODO: check for PAUSE and LEVEL_END states
        return game_state.GameState.LEVEL_PLAY

    def game_step(self, keys):
        """Updated frame of the game."""
        self.window.blit(self.image_background, (0, 0))
        # set pause_info text on top right with 5x5 px padding
        self.window.blit(self.pause_info, (self.width - self.pause_info.get_width() - 5, 5))
        self.window.blit(self.image_character,
                         (self.stickman.x, self.stickman.y))  # displays the character at a position
        self.stickman.x = self.stickman.x + 0.7 if self.stickman.x < self.width else 0 - self.stickman.width

        self.score += 0.02
        self.score_info = self.font.render(f"SCORE: {self.score:.0f}", True, "black")
        self.window.blit(self.score_info, (45, 5))
        prev_key = 0
        for i in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                  pygame.K_8, pygame.K_9]:
            if keys[i] != prev_key:  # FIXME: debouncing issue
                prev_key = keys[i]
                if self.answer == '_':
                    self.answer = str(i - 48)
                else:
                    self.answer += str(i - 48)
        if self.answered:
            self.question = arithmetic.generate_arithmetic()
        qa = self.font.render(f'{self.question[1]} {self.question[2]} {self.question[3]} = {self.answer}', True, "yellow")
        self.window.blit(qa, (650, 150))
