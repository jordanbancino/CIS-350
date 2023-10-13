import pygame
import pygame_gui

from src import game_state
from src.graphics import load_asset
from src import arithmetic


class LevelPlayHandler(game_state.StateHandler):
    def __init__(self):
        self.font_size = 20
        self.score = 0
        self.image_background = load_asset('background.png')
        self.image_character = load_asset('stickman.png')
        self.stickman = pygame.Rect(300, 315, 100, 100)
        self.font = pygame.font.SysFont("comicsans", self.font_size)

        self.speed = 0
        self.equation = arithmetic.generate_arithmetic()

        self.init = False

    def process(self, context: game_state.StateHandlerContext) -> game_state.GameState:
        window = context.get_window()

        if not self.init:
            width = window.get_width()
            height = window.get_height()

            self.image_background = pygame.transform.scale(self.image_background, (width, height))
            self.image_character = pygame.transform.scale(self.image_character, (100, 100))

            self.user_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 400), (100, 50)),
                                                                  manager=
                                                                  context.get_gui(), object_id="answer_input_box")
            self.user_input.placeholder_text = ""

            self.init = True

        pause_info = self.font.render("Press SPACEBAR To Pause", True, "black")  # antialias makes text look better
        score_info = self.font.render("SCORE: " + str(self.score), True, "black")

        window.blit(self.image_background, (0, 0))
        # set pause_info text on top right with 5x5 px padding
        window.blit(pause_info, (window.get_width() - pause_info.get_width() - 5, 5))  # blit pause_info post background to be front
        window.blit(score_info, (350, 5))
        window.blit(self.image_character, (self.stickman.x, self.stickman.y))  # displays the character at a position

        # check if player presses enter in text box
        for event in context.get_events():
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "answer_input_box":
                answer = int(event.text)
                if arithmetic.solve_arithmetic(self.equation[1:], int(answer)):  # checks if answer is correct
                    self.speed += 1  # increase speed by 1 to character
                else:
                    self.speed = 0  # set speed of character to 0
                self.user_input.set_text("")  # reset textbox

        return game_state.GameState.LEVEL_PLAY
