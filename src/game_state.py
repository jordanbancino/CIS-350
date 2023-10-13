import pygame
import pygame_gui


class GameState:
    GAME_QUIT = 0
    MAIN_MENU = 1
    LEVEL_PLAY = 2
    LEVEL_PAUSE = 3
    LEVEL_END = 4


class StateHandlerContext:
    def __init__(self, state: GameState, events: list[pygame.event.Event] | None, window: pygame.Surface,
                 gui: pygame_gui.UIManager):
        self.state = state
        self.events = events
        self.window = window
        self.gui = gui

    def get_state(self):
        return self.state

    def get_events(self):
        return self.events

    def get_window(self):
        return self.window

    def get_gui(self):
        return self.gui


class StateHandler:
    def __init__(self, context: StateHandlerContext):
        pass

    def on_enter(self, context: StateHandlerContext) -> None:
        pass

    def process(self, context: StateHandlerContext) -> GameState:
        pass

    def on_exit(self, context: StateHandlerContext) -> None:
        # By default, clear the GUI manager on state change so that
        # the next state can draw a new GUI.
        gui_manager = context.get_gui()
        gui_manager.clear_and_reset()
