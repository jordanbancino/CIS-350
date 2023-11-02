import pygame

import game_state


class LevelPauseHandler(game_state.StateHandler):
    def __init__(self, context: game_state.StateHandlerContext):
        super().__init__(context)
        self._font = pygame.font.SysFont("consolas", 50)

    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)

        window = context.get_window()
        window.fill('black')

        # antialias makes text look better
        pause_info = self._font.render(
            "Press SPACEBAR To Resume", True, "white")
        window.blit(pause_info,
                    ((window.get_width() - pause_info.get_width()) / 2,
                     (window.get_height() - pause_info.get_height()) / 2))

        next_state = game_state.GameState.LEVEL_PAUSE

        for event in context.get_events():
            if (event.type == pygame.KEYUP and
                    event.__dict__['key'] == pygame.K_SPACE):  # Space
                next_state = game_state.GameState.LEVEL_PLAY

        return next_state
