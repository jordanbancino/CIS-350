"""
This handler is a stub handler that handles the `GAME_QUIT` state by doing
nothing but keeping the state machine in `GAME_QUIT`, because the main state
machine loop is responsible for terminating itself when `GAME_QUIT` is entered,
however a handler must still be executed.
"""
import game_state


class QuitHandler(game_state.StateHandler):
    def process(self, context: game_state.StateHandlerContext) \
            -> game_state.GameState:
        super().process(context)
        return game_state.GameState.GAME_QUIT
