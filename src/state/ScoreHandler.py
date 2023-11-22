import time

import pygame

import user_data
from state.MainMenuHandler import Button
import game_state
from arg import load_asset


class ScoreHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)

        self._image_border = load_asset('menu_border.png')
        self.button = load_asset('button.png')
        self.button = load_asset('button.png')

        window = context.get_window()
        width = window.get_width()
        height = window.get_height()

        self._image_border = pygame.transform.scale(
            self._image_border, (width, height))

        self._data = user_data.get().snapshot()

    @staticmethod
    def cell(tot_width, n_cols, width, col=1, off=0):
        return ((tot_width / (n_cols * 2)) * col) - (width / 2) + off

    @staticmethod
    def center(w1, w2):
        return ScoreHandler.cell(w1, 1, w2)

    def make_closure(self, frame_wid, type_col, frame_off, row):
        return lambda s: (self.cell(frame_wid, 4, s.get_width(), type_col, frame_off), row)

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()

        # create button instances
        back_button = Button(350, 345, self.button, "BACK")
        buttons = [back_button]

        window.fill((100, 100, 100))  # Gray
        window.blit(self._image_border, (0, 0))

        for button in buttons:
            button.blit(window)

        frame_off = 75
        frame_wid = window.get_width() - (2 * frame_off)

        strings = [
            [55, "SCORES", (lambda s: (
            self.center(window.get_width(), s.get_width()), 65))],
            [50, "Math ∞", (lambda s: (
            self.cell(frame_wid, 2, s.get_width(), 1, frame_off), 110))],
            [50, "Flashcards", (lambda s: (
            self.cell(frame_wid, 2, s.get_width(), 3, frame_off), 110))],
            [30, "Top", (lambda s: (self.cell(frame_wid, 4, s.get_width(), 1, frame_off), 160))],
            [30, "Recent", (lambda s: (
            self.cell(frame_wid, 4, s.get_width(), 3, frame_off), 160))],
            [30, "Top", (lambda s: (
            self.cell(frame_wid, 4, s.get_width(), 5, frame_off), 160))],
            [30, "Recent", (lambda s: (
                self.cell(frame_wid, 4, s.get_width(), 7, frame_off), 160))]
        ]

        lines = [
            [(100, 155), (window.get_width() - 100, 155)]
        ]

        if self._data['scores']:
            lines.append([(window.get_width() / 2, 120), (window.get_width() / 2, 350)])

            type_col = 1
            for mode in ['math', 'card']:
                for type in ['top', 'recent']:

                    row = 200
                    for score in self._data['scores'][mode][type]:
                        string = [30, f"{score['score']} ({time.strftime('%M:%S', time.gmtime(score['time']))})",
                                    self.make_closure(frame_wid, type_col, frame_off, row)]
                        strings.append(string)
                        row = row + 30

                    type_col = type_col + 2
            pass
        else:
            strings.append([50, "No scores yet.", (lambda s: (self.center(window.get_width(), s.get_width()), 220))])
            strings.append([50, "Play the game first!", (lambda s: (self.center(window.get_width(), s.get_width()), 270))])

        for string in strings:
            font = pygame.font.SysFont('consolas', string[0])
            rendered = font.render(string[1], True, 'white')
            window.blit(rendered, string[2](rendered))

        for line in lines:
            pygame.draw.line(window, 'white', line[0], line[1])

        clicked_buttons = []

        # Dispatch all events to all buttons
        for event in context.get_events():
            for button in buttons:
                if button.dispatch_event(event):
                    clicked_buttons.append(button)

        # Handle buttons that were clicked
        for button in clicked_buttons:
            if button == back_button:
                return game_state.GameState.MAIN_MENU

        return game_state.GameState.SCORE
