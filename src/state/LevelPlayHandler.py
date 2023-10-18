import pygame
import pygame_gui

from src import game_state
from src.game_state import StateHandlerContext
from src.graphics import load_asset
from src import arithmetic


class LevelPlayHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self.font_size = 20
        self.score = 0
        self.image_background_night = load_asset('night.jpg')
        self.image_background_day = load_asset("day.jpg")
        self.image_character = load_asset('stickman.png')
        self.stickman = pygame.Rect(300, 315, 100, 100)
        self.font = pygame.font.SysFont("comicsans", self.font_size)

        self.speed = 1
        self.equation = arithmetic.generate_arithmetic()

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()
        self.image_background_night = pygame.transform.scale(self.image_background_night, (width, height))
        self.image_background_night_pos = pygame.Rect(0, 0, 900, 500)  # position of initial night background
        self.image_background_day = pygame.transform.scale(self.image_background_day, (width, height))
        self.image_background_day_pos = pygame.Rect(900, 0, 900, 500)  # position of initial day background
        self.image_character = pygame.transform.scale(self.image_character, (100, 100))
        self.distance_covered = 0
        self.user_input = None

        self.ground = 315
        self.gravity = 2000
        self.jump = 0

    def on_enter(self, context: StateHandlerContext) -> None:
        super().on_enter(context)
        window = context.get_window()

        input_width = 100
        input_height = 50
        input_left = (window.get_width() - input_width) / 2
        input_top = window.get_height() - input_height - 10  # 10px padding from bottom
        input_rect = pygame.Rect((input_left, input_top), (input_width, input_height))

        self.user_input = pygame_gui.elements.UITextEntryLine(relative_rect=input_rect,
                                                              manager=context.get_gui(),
                                                              object_id="answer_input_box")
        self.user_input.placeholder_text = ""

    def draw_scene(self, context):
        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self.image_background_night_pos.update(self.image_background_night_pos.x - self.speed, 0, width, height)
        window.blit(self.image_background_night, (self.image_background_night_pos.x,
                                                  self.image_background_night.get_rect().y))
        self.image_background_day_pos.update(self.image_background_day_pos.x - self.speed, 0, width, height)
        window.blit(self.image_background_day, (self.image_background_day_pos.x,
                                                self.image_background_day.get_rect().y))
        self.distance_covered += self.speed

        pause_info = self.font.render("Press SPACEBAR To Pause", True, "white")  # antialias makes text look better
        score_info = self.font.render("SCORE: " + str(self.score), True, "white")

        # set pause_info text on top right with 5x5 px padding
        window.blit(pause_info, (window.get_width() - pause_info.get_width() - 5, 5))
        window.blit(score_info, (350, 5))

        equation = self.font.render(self.equation[0] + ' = ', True, "white")
        window.blit(equation, ((window.get_width() - equation.get_width()) / 3, 450))


    def update_character_position(self, context):
        window = context.get_window()
        dt = context.get_delta()

        # Character is always centered on the screen
        self.stickman.x = (window.get_width() - self.image_character.get_width()) / 2

        self.stickman.y += self.jump * dt
        self.jump += self.gravity * dt

        if self.stickman.y > self.ground:
            self.stickman.y = self.ground
            self.jump = 0

        window.blit(self.image_character, (self.stickman.x, self.stickman.y))  # displays the character at a position

    def process(self, context: game_state.StateHandlerContext) -> game_state.GameState:
        super().process(context)

        self.draw_scene(context)
        self.update_character_position(context)
        self.update_character_position(context)

        next_state = game_state.GameState.LEVEL_PLAY

        window = context.get_window()

        # check if player presses enter in text box
        for event in context.get_events():
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "answer_input_box":
                if event.text == self.equation[1]:  # checks if answer is correct
                    self.jump = -600
                    self.equation = arithmetic.generate_arithmetic()
                    self.speed += 1
                    self.score += 1
                else:
                    next_state = game_state.GameState.LEVEL_END

                self.user_input.set_text("")  # reset textbox
            elif event.type == pygame.KEYUP and event.__dict__['key'] == pygame.K_SPACE:
                # If user pressed the space key, go to the pause state.
                next_state = game_state.GameState.LEVEL_PAUSE
            if self.distance_covered >= (window.get_width() * (3/2)):
                next_state = game_state.GameState.LEVEL_END

        return next_state
