import random

import pygame
import pygame_gui

import arithmetic
import game_state
from game_state import StateHandlerContext
from graphics import load_asset


class LevelPlayHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self.equation = None
        self.font_size = 20
        self.score = 0
        self.image_background_night = load_asset('night.jpg')
        self.image_background_day = load_asset("day.jpg")
        self.image_character = load_asset('stickman.png')
        self.obstacle_image = load_asset("calculator1.jpg")
        self.obstacle_width = 50
        self.obstacle_height = 125
        self.font = pygame.font.SysFont("comicsans", self.font_size)

        self.speed = 1

        self.window = context.get_window()
        self.width = self.window.get_width()
        self.height = self.window.get_height()
        self.image_background_night = (
            pygame.transform.scale(self.image_background_night,
                                   (self.width, self.height)))

        # pos of initial night background
        self.image_background_night_pos1 = pygame.Rect(0, 0,
                                                       self.width, self.height)
        # pos of init night img
        self.image_background_night_pos2 = pygame.Rect(self.width, 0,
                                                       self.width, self.height)

        self.image_background_day = pygame.transform.scale(
            self.image_background_day, (self.width, self.height))
        # pos init day image
        self.image_background_day_pos1 = pygame.Rect(self.width * 2, 0,
                                                     self.width, self.height)
        # pos init day image
        self.image_background_day_pos2 = pygame.Rect(self.width * 3, 0,
                                                     self.width, self.height)
        self.image_character = pygame.transform.scale(self.image_character,
                                                      (100, 100))
        self.distance_covered = 0
        self.user_input = None

        self.ground = 330
        self.gravity = 2500
        self.jump = -100
        self.stickman = pygame.Rect(0, self.ground, 100, 100)

        self.obstacle_y = self.ground
        self.obstacle_image = pygame.transform.scale(
            self.obstacle_image,
            (self.obstacle_width, self.obstacle_height))
        self.obstacle_hitbox = pygame.Rect(800, self.obstacle_y,
                                           self.obstacle_width,
                                           self.obstacle_height)

    def on_enter(self, context: StateHandlerContext) -> None:
        super().on_enter(context)
        window = context.get_window()

        input_width = 100
        input_height = 50
        input_left = (window.get_width() - input_width) / 2
        # 10px padding from bottom
        input_top = window.get_height() - input_height - 10
        input_rect = pygame.Rect((input_left, input_top),
                                 (input_width, input_height))

        self.user_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=input_rect, manager=context.get_gui(),
            object_id="answer_input_box")
        self.user_input.placeholder_text = ""
        self.user_input.focus()

        self.equation = arithmetic.generate_arithmetic()

    def draw_scene(self, context):
        dt = context.get_delta()

        n1 = self.image_background_night_pos1.x
        n2 = self.image_background_night_pos2.x
        d1 = self.image_background_day_pos1.x
        d2 = self.image_background_day_pos2.x

        n1 -= self.speed
        n2 -= self.speed
        d1 -= self.speed
        d2 -= self.speed

        if d2 <= 0:
            n1 = d2 + self.width
            n2 = n1 + self.width
        if d2 <= -self.width:
            d1 = n2 + self.width
            d2 = d1 + self.width

        self.image_background_night_pos1.update(n1, 0, self.width, self.height)
        self.window.blit(self.image_background_night,
                         (n1, self.image_background_night.get_rect().y))
        self.image_background_night_pos2.update(n2, 0, self.width, self.height)
        self.window.blit(self.image_background_night,
                         (n2, self.image_background_night.get_rect().y))
        self.image_background_day_pos1.update(d1, 0, self.width, self.height)
        self.window.blit(self.image_background_day,
                         (d1, self.image_background_day.get_rect().y))
        self.image_background_day_pos2.update(d2, 0, self.width, self.height)
        self.window.blit(self.image_background_day,
                         (d2, self.image_background_day.get_rect().y))

        obstacle = self.obstacle_hitbox.x
        obstacle -= self.speed
        self.obstacle_hitbox.update(obstacle, self.obstacle_y,
                                    self.obstacle_width, self.obstacle_height)
        self.window.blit(self.obstacle_image, (obstacle, self.obstacle_y))
        if obstacle < -51:
            # makes the obstacle have a random position off-screen that the
            # player has to overcome
            self.obstacle_hitbox.update(random.randint(905, 1800),
                                        self.obstacle_y, self.obstacle_width,
                                        self.obstacle_height)

    def draw_ui(self, context):
        window = context.get_window()
        # antialias makes text look better
        pause_info = self.font.render(
            "Press SPACEBAR To Pause", True, "white")
        score_info = self.font.render(
            "SCORE: " + str(self.score), True, "white")

        # set pause_info text on top right with 5x5 px padding
        window.blit(pause_info,
                    (window.get_width() - pause_info.get_width() - 5, 5))
        window.blit(score_info, (350, 5))

        equation = self.font.render(self.equation[0] + ' = ', True, "white")
        window.blit(equation,
                    ((window.get_width() - equation.get_width()) / 3, 450))

    def draw_character(self, context):
        window = context.get_window()
        dt = context.get_delta()

        # Character is always centered on the screen
        self.stickman.x = (window.get_width() -
                           self.image_character.get_width()) / 2

        self.stickman.y += self.jump * dt
        self.jump += self.gravity * dt

        if self.stickman.y > self.ground:
            self.stickman.y = self.ground
            self.jump = 0

        # displays the character at a position
        window.blit(self.image_character, (self.stickman.x, self.stickman.y))

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        self.draw_scene(context)
        self.draw_character(context)
        self.draw_ui(context)

        next_state = game_state.GameState.LEVEL_PLAY
        window = context.get_window()

        self.distance_covered += self.speed

        # check if player presses enter in text box
        for event in context.get_events():
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == "answer_input_box"):
                try:
                    # checks if answer is correct
                    if float(event.text) == float(self.equation[1]):
                        self.jump = -1100
                        self.equation = arithmetic.generate_arithmetic()
                        self.speed += 1
                        self.score += 1
                    else:
                        next_state = game_state.GameState.LEVEL_END
                except ValueError:
                    # If the user inputs an invalid number, just clear the box.
                    pass

                self.user_input.set_text("")  # reset textbox
            elif (event.type == pygame.KEYUP and
                  event.__dict__['key'] == pygame.K_SPACE):
                # If user pressed the space key, go to the pause state.
                next_state = game_state.GameState.LEVEL_PAUSE
        if (self.stickman.right > self.obstacle_hitbox.left and
                self.stickman.left < self.obstacle_hitbox.right):
            if self.obstacle_hitbox.top <= self.stickman.bottom:
                next_state = game_state.GameState.LEVEL_END

        return next_state

    def on_exit(self, context):
        super().on_exit(context)

        self.jump = -150

        if context.get_state() == game_state.GameState.LEVEL_END:
            # The game has ended; reset all state so that when we are
            # re-started, we start from the beginning and not where we left
            # off.
            self.speed = 1
            self.score = 0
            self.distance_covered = 0
            pass
        else:
            # The game was just paused, don't reset the state.
            pass
