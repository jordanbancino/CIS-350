"""
The game state machine requires a number of components to be useful:

- `GameState`: An enumeration of all the possible game states. This enumeration
is used by the main event loop to keep track of which state handler to invoke,
as well as by the state handlers themselves to signal state transitions.
- `StateHandlerContext`: A simple data object that stores the game context,
which is passed to each state handler function when it is being invoked.
- `StateHandler`: A simple interface that implements a state handler. State
handlers are expected to adhere to this interface, and may implement any or no
functions. Note that they should always call their parent functions listed
in the interface, because these parent functions perform useful logic.
"""
import pygame
import pygame_gui


class GameState:
    """
    The game itself may be in any of the following states:
    """

    GAME_QUIT = 0
    """The program is ending and should exit as quickly as possible."""

    MAIN_MENU = 1
    """The game is displaying the main menu and waiting for the user to make
    a choice."""

    LEVEL_PLAY = 2
    """The game is currently being played. The user is making moves."""

    LEVEL_PAUSE = 3
    """The game is paused. It is waiting for user input before resuming."""

    LEVEL_END = 4
    """The current game has ended, either because the user hit an obstacle,
    or because a question was incorrectly answered."""

    DIFFICULTY = 5
    """The game is displaying the Difficulty meters for the MATH mode and
    waiting for the user to make a choice"""

    SCORE = 6
    """The game is displaying the recent scores"""

    GAME_MODE = 7
    """The game is displaying the mode select screen, which allows users to
    select between math and flashcard mode."""


class StateHandlerContext:
    """
    The state handler context is populated by the main state machine event
    loop, and is provided to state handlers so that they have easy access to
    everything necessary to draw to the screen, process user input, and update
    the game state.

    The state machine is run iteratively at a fixed frame rate. A
    `StateHandlerContext` gets generated for each and every frame that is
    rendered. During each iteration, all events are collected and passed into
    the context so that handlers can handle any events that may have passed
    since the handler function was last executed.
    """

    def __init__(self,
                 state: GameState, events: list[pygame.event.Event] | None,
                 window: pygame.Surface,
                 gui: pygame_gui.UIManager,
                 delta: float, storage: dict):
        self._state = state
        self._events = events
        self._window = window
        self._gui = gui
        self._delta = delta
        self._storage = storage

    def get_state(self) -> GameState:
        """
        Get the current game state. Note that this is not always the state
        that the currently running state handler was registered to handle. See
        `StateHandler` for more details.
        """
        return self._state

    def get_events(self) -> list[pygame.event.Event] | None:
        """
        Get a list of Pygame events that have taken place since the last
        iteration. Each fired event only shows up in this list exactly once,
        so it is recommended to iterate over it during each function call and
        process the events that need to be dealt with as soon as they are
        fired.
        """
        return self._events

    def get_window(self) -> pygame.Surface:
        """
        Get the Pygame drawing surface onto which all game components are
        blitted. This surface represents the entire screen area, so each state
        handler can draw anywhere on the screen and update the entire screen
        as necessary. Note that individual handlers don't have to update the
        display by calling out to pygame explicitly; this is all handled by the
        state machine event loop. State handlers must only blit everything onto
        this surface.

        Note that the window is not preserved across frames; each state handler
        will have to re-draw the entire frame on every iteration of the state
        machine. By default, each frame is filled in solid black, so if there
        are black parts on the window that a state handler did not draw, it is
        simply because the state handler did not blit anything over the empty
        frame in that location.
        """
        return self._window

    def get_gui(self) -> pygame_gui.UIManager:
        """
        This game utilizes Pygame GUI for some user inputs. If a state handler
        must register components, it should do so with this `UIManager`, which
        is automatically managed and updated by the state machine loop.

        If a state handler is going to register GUI components, it should do so
        only once when the state is entered&mdash;not iteratively. Note that
        by default, the `UIManager` is cleared automatically on every state
        change.
        """
        return self._gui

    def get_delta(self) -> float:
        """
        Get the amount of time that has passed (in *seconds*) since the last
        invocation of a state handler. This is effectively the time since the
        last frame was rendered, and should be used to compute object motion in
        a frame rate-independent manner, because the frame rate may not always
        be steady on all platforms.
        """
        return self._delta

    def get_storage(self) -> dict:
        """
        Get a dictionary that is accessible to all state handlers. This storage
        dictionary can be in any format agreed upon by the state handlers, and
        is used to pass data between them. State handlers can process the
        storage in their `on_enter()` and `on_exit()` functions.

        State handlers should make an effort to refrain from storing internal
        data in the context storage. This storage should be reserved only for
        exporting data to other state handlers.
        """
        return self._storage


class StateHandler:
    """
    A `StateHandler` defines functions that are invoked at certain periods
    during the lifetime of the state machine. State handlers are registered
    with the main state machine loop so that they are executed when the game
    enters a given state.

    Each function takes a `StateHandlerContext` so that there are no
    limitations as to what a state handler can do at any point during its
    lifetime.
    """

    def __init__(self, context: StateHandlerContext):
        """
        Construct a new `StateHandler`.
        """
        pass

    def on_enter(self, context: StateHandlerContext) -> None:
        """
        This function is invoked at the rising edge of a state transition. A
        state transition occurs either when the main loop begins, or after a
        previous state yielded its control of the state machine. It is invoked
        *before* `process()` exactly once per state transition.

        For our application, this function is primarily used to draw Pygame
        GUI components onto the screen for the current state, since they only
        need to be registered with the `UIManager` once.
        """
        pass

    def process(self, context: StateHandlerContext) -> GameState:
        """
        This function is invoked iteratively at a fixed frame
        rate&mdash;though this rate should be assumed to be
        unknown&mdash;for the entire duration that the state machine remains
        in the current state. It is always invoked after `on_enter()` and
        before `on_exit()`, although it may be executed many times between each
        of those invocations.

        For our application, this function is primarily used to draw the game
        scene and process user input.

        This function should return the next state that the state machine
        should enter. If the state machine should remain in the same state, it
        should return `context.get_state()`.
        """
        pass

    def on_exit(self, context: StateHandlerContext) -> None:
        """
        This function is invoked at the falling edge of a state transition. It
        operates just like `on_enter()`, except it is executed when the current
        state indicates that it would like to transition to another state. This
        allows the state handler to clean up anything as necessary.

        For our application, this function is primarily used to reset
        Pygame GUI for each screen, as well as any state that should not carry
        over the next time this state is entered.

        By default, `on_exit()` will clear the Pygame GUI, so individual state
        handlers need only register their components on enter; they don't have
        to worry about de-registering them on exit. Note, of course, that this
        function may be overridden and thus not execute if the child function
        does not make a call to `super().on_exit()`.
        """
        gui_manager = context.get_gui()
        gui_manager.clear_and_reset()
