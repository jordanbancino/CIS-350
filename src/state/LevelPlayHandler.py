"""
This handler handles the `LEVEL_PLAY` state, which is the actual core of the
game logic. In this handler, the user actually plays the game by answering
questions and causing the character to jump. This handler keeps track of score
and updates the scene by scrolling it to the left.
"""
import random

import pygame
import pygame_gui
import os

from pygame import mixer
from src import arithmetic
from src import game_state
from arg import load_asset


class LevelPlayHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self._equation = None
        self._font_size = 20
        self._score = 0
        self._image_background_night = load_asset('night.jpg')
        self._image_background_day = load_asset("day.jpg")
        self._image_character = load_asset('stickman.png')
        self._obstacle_image = load_asset("calculator1.png")
        self._obstacle_width = 50
        self._obstacle_height = 125
        self._clock = pygame.time.Clock()
        self._time = 0  # start stopwatch at 0
        self._countdown_time = 60  # 1 minute
        self._font = pygame.font.SysFont("consolas", self._font_size)

        self._speed = 2
        self._temp_speed = self._speed
        self._jump_speed = 3
        self._jumping = False
        self._scored = True

        self._window = context.get_window()
        self._width = self._window.get_width()
        self._height = self._window.get_height()
        self._image_background_night = (
            pygame.transform.scale(self._image_background_night,
                                   (self._width, self._height)))

        # pos of initial night background
        self._image_background_night_pos1 = pygame.Rect(self._width * 2, 0,
                                                        self._width,
                                                        self._height)
        # pos of init night img
        self._image_background_night_pos2 = pygame.Rect(self._width * 3, 0,
                                                        self._width,
                                                        self._height)

        self._image_background_day = pygame.transform.scale(
            self._image_background_day, (self._width, self._height))
        # pos init day image
        self._image_background_day_pos1 = pygame.Rect(0, 0,
                                                      self._width,
                                                      self._height)
        # pos init day image
        self._image_background_day_pos2 = pygame.Rect(self._width, 0,
                                                      self._width,
                                                      self._height)
        # position of end of level for easy, medium, and hard difficulties
        self._end = 9000

        # Scale character, then crop it so that the bounding box doesn't extend
        # out into space, thus creating ghost hits.
        self._image_character = pygame.transform.scale(self._image_character,
                                                       (100, 100))
        self._image_character = self._image_character.subsurface((20, 5,
                                                                  60, 80))

        self._distance_covered = 0
        self._user_input = None

        self._ground = 330
        self._jump = 0
        self._next_jump = -490
        self._gravity = 970
        self._stickman = pygame.Rect(0, self._ground,
                                     self._image_character.get_width(),
                                     self._image_character.get_height())

        self._obstacle_y = self._ground
        self._obstacle_image = pygame.transform.scale(
            self._obstacle_image,
            (self._obstacle_width, self._obstacle_height))
        self._obstacle_hitbox = pygame.Rect(950, self._obstacle_y,
                                            self._obstacle_width,
                                            self._obstacle_height)
        #print("t, s =", self._stickman.right - self._stickman.left, self._stickman.top - self._stickman.bottom)
    def on_enter(self, context: game_state.StateHandlerContext) -> None:
        super().on_enter(context)
        window = context.get_window()

        input_width = 100
        input_height = 50
        input_left = (window.get_width() - input_width) / 2
        # 10px padding from bottom
        input_top = window.get_height() - input_height - 10
        input_rect = pygame.Rect((input_left, input_top),
                                 (input_width, input_height))

        self._user_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=input_rect, manager=context.get_gui(),
            object_id="answer_input_box")
        self._user_input.placeholder_text = ""
        self._user_input.focus()

        if context.get_storage()['difficulty'] == "easy":
            self._equation = arithmetic.generate_arithmetic("easy")
        elif context.get_storage()['difficulty'] == "medium":
            self._equation = arithmetic.generate_arithmetic("medium")
        elif context.get_storage()['difficulty'] == "hard":
            self._equation = arithmetic.generate_arithmetic("hard")
        elif context.get_storage()['difficulty'] == "infinite":
            self._scored = False
            if self._score >= 10:
                self._equation = arithmetic.generate_arithmetic("hard")
            elif self._score >= 5:
                self._equation = arithmetic.generate_arithmetic("medium")
            else:
                self._equation = arithmetic.generate_arithmetic("easy")

        if self._time > 0:
            self._time = context.get_storage()['last_play_time']
        self._clock.tick(60) / 1000  # resets the tick

    def draw_scene(self, context):
        dt = context.get_delta()

        d1 = self._image_background_day_pos1.x
        d2 = self._image_background_day_pos2.x
        n1 = self._image_background_night_pos1.x
        n2 = self._image_background_night_pos2.x

        d1 -= self._speed
        d2 -= self._speed
        n1 -= self._speed
        n2 -= self._speed

        if context.get_storage()['difficulty'] == "easy" or \
                context.get_storage()['difficulty'] == "medium" or \
                context.get_storage()['difficulty'] == "hard":
            self._end -= self._speed

        if n2 <= 0:
            d1 = n2 + self._width
            d2 = d1 + self._width
        if n2 <= -self._width:
            n1 = d2 + self._width
            n2 = n1 + self._width

        self._image_background_day_pos1.update(d1, 0,
                                               self._width, self._height)
        self._window.blit(self._image_background_day,
                          (d1, self._image_background_day.get_rect().y))
        self._image_background_day_pos2.update(d2, 0,
                                               self._width, self._height)
        self._window.blit(self._image_background_day,
                          (d2, self._image_background_day.get_rect().y))
        self._image_background_night_pos1.update(n1, 0,
                                                 self._width, self._height)
        self._window.blit(self._image_background_night,
                          (n1, self._image_background_night.get_rect().y))
        self._image_background_night_pos2.update(n2, 0,
                                                 self._width, self._height)
        self._window.blit(self._image_background_night,
                          (n2, self._image_background_night.get_rect().y))

        obstacle = self._obstacle_hitbox.x
        obstacle -= self._speed
        self._obstacle_hitbox.update(obstacle, self._obstacle_y,
                                     self._obstacle_width,
                                     self._obstacle_height)
        self._window.blit(self._obstacle_image, (obstacle, self._obstacle_y))

        if obstacle < -51:
            # makes the obstacle have a random position off-screen that the
            # player has to overcome
            self._obstacle_hitbox.update(random.randint(905, 1800),
                                         self._obstacle_y,
                                         self._obstacle_width,
                                         self._obstacle_height)

        if self._countdown_time == 120 and self._time == 0:
            self._clock.tick(60) / 1000  # resets the tick
        # stopwatch
        if context.get_storage()['difficulty'] == "infinite":
            self._time += self._clock.tick(60) / 1000
        else:
            # countdown
            self._countdown_time -= self._clock.tick(60) / 1000

    def draw_ui(self, context):
        window = context.get_window()
        # antialias makes text look better
        pause_info = self._font.render(
            "Press SPACEBAR To Pause", True, "white")
        score_info = self._font.render(
            "SCORE: " + str(self._score), True, "white")
        # stopwatch
        time_info = self._font.render(f"Time in game: {self._time:.2f}s", True, "white")
        # countdown
        countdown_info = self._font.render(f"Time remaining: {self._countdown_time:.2f}s", True, "white")

        # set pause_info text on top right with 5x5 px padding
        window.blit(pause_info,
                    (window.get_width() - pause_info.get_width() - 5, 5))
        if context.get_storage()['difficulty'] == "infinite":
            window.blit(score_info, (350, 5))
            # stopwatch
            window.blit(time_info, (5, 5))
        else:
            # countdown
            window.blit(countdown_info, (5, 5))

        equation = self._font.render(self._equation[0] + ' = ', True, "white")
        window.blit(equation,
                    ((window.get_width() - equation.get_width()) / 3, 450))

    def draw_character(self, context):
        window = context.get_window()
        dt = context.get_delta()

        # Character is always centered on the screen
        self._stickman.x = (window.get_width() -
                            self._image_character.get_width()) / 2

        self._stickman.y += self._jump * dt
        self._jump += self._gravity * dt

        if self._stickman.y > self._ground:
            self._stickman.y = self._ground
            self._jump = 0

        # displays the character at a position
        window.blit(self._image_character,
                    (self._stickman.x, self._stickman.y))

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        self.draw_scene(context)
        self.draw_character(context)
        self.draw_ui(context)

        next_state = game_state.GameState.LEVEL_PLAY
        window = context.get_window()

        # game ends when countdown hits 0
        if self._countdown_time <= 0:
            next_state = game_state.GameState.LEVEL_END

        self._distance_covered += self._speed

        if (self._jumping and self._stickman.right >= self._obstacle_hitbox.left - 50
                and not self._stickman.left > self._obstacle_hitbox.right):
            self._temp_speed = self._speed
            self._speed = self._jump_speed
            self._jump = self._next_jump
            self._jumping = False
            self._scored = False
            path = os.path.join("music", "jump.mp3")
            jump_sound = pygame.mixer.Sound(path)
            jump_sound.play()

        if not self._scored and self._stickman.right >= self._obstacle_hitbox.right + 50:
            self._score += 1
            self._speed = self._temp_speed + 1
            if self._score >= 10 or context.get_storage()['difficulty'] == "hard":
                self._equation = arithmetic.generate_arithmetic("hard")
            elif self._score >= 5 or context.get_storage()['difficulty'] == "medium":
                self._equation = arithmetic.generate_arithmetic("medium")
            else:
                self._equation = arithmetic.generate_arithmetic("easy")
            self._scored = True

        # check if player presses enter in text box
        for event in context.get_events():
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == "answer_input_box"):
                try:
                    # checks if answer is correct
                    if float(event.text) == self._equation[1] and not self._jumping:
                        self._jumping = True

                except ValueError:
                    # If the user inputs an invalid number, just clear the box.
                    pass

                self._user_input.set_text("")  # reset textbox
            elif ((event.type == pygame.KEYUP and
                  event.__dict__['key'] == pygame.K_SPACE) or
                  event.type == pygame.WINDOWLEAVE):
                # If user pressed the space key or left the game window,
                # go to the pause state.
                next_state = game_state.GameState.LEVEL_PAUSE

        if (self._stickman.right > self._obstacle_hitbox.left and
                self._stickman.left < self._obstacle_hitbox.right):
            if self._obstacle_hitbox.top <= self._stickman.bottom:
                path = os.path.join("music", "game_over.mp3")
                game_over_sound = pygame.mixer.Sound(path)
                game_over_sound.play()

                next_state = game_state.GameState.LEVEL_END
                if context.get_storage()['difficulty'] == "infinite":
                    context.get_storage()['end_game'] = "Nice Run!"
                else:
                    context.get_storage()['end_game'] = "You Lose."

        if self._end <= self._stickman.right:
            next_state = game_state.GameState.LEVEL_END
            context.get_storage()['end_game'] = "You Win!"

        return next_state

    def on_exit(self, context):
        super().on_exit(context)

        self._jump = -150

        if context.get_storage()['difficulty'] == "infinite":
            context.get_storage()['last_play_time'] = self._time
            context.get_storage()['last_score'] = self._score
        else:
            context.get_storage()['last_play_time'] = self._countdown_time

        if context.get_state() == game_state.GameState.LEVEL_END:
            # The game has ended; reset all state so that when we are
            # re-started, we start from the beginning and not where we left
            # off.
            #
            # TODO: We should probably see if Pygame requires us to clean up
            # any resources (such as closing images) before we lose references
            # to resources and thus leak them. For now, this probably isn't a
            # problem because it's unlikely that the game will be played more
            # than just a few times during each execution of the program, but
            # this feels like a hack so it would be nice to know if there are
            # any unintended side effects of this.
            self.__init__(context)
            pass
        else:
            # The game was just paused, don't reset the state.
            context.get_storage()['last_play_time'] = self._time
            pass
