"""
log module: A simple logging facility intended to be used to log messages to
the console or a log file. It may be extended in the future, but for now
is intended to define a stable interface with which messages can be
logged such that, if the log format needs to change in the future, it
can easily be changed in only one spot and all log messages will be
updated accordingly.
"""
import inspect

DEBUG = 10
"""Debug messages are intended only for developers and should be disabled in 
production."""

INFO = 20
"""Info messages are informative to users and developers."""

WARNING = 30
"""Notify the user that something is wrong. Note that this is a non-fatal
condition, and that the user can't be reasonably expected to actually check
this since users might not even be running the program in a terminal. If the
warning must be presented to the user, it must be drawn in the GUI."""

ERROR = 40
"""Notify the user that something is *very* wrong. Same statements apply as
noted in `WARNING`."""

CRITICAL = 50
"""Only use this if you are about to abort the program immediately after
writing the message."""


class Log:
    """
    The `Log` class provides all the logging functionality. Note
    that there is a global log instance accessible via the global
    `get_logger()` function, so this class will not normally be
    instantiated by outside code.
    """

    def __init__(self, level: int):
        """
        Initialize the logging class with an initial log level.
        Messages with a lower log level will not be displayed. The
        log level can be changed with setLevel() after the class is
        constructed.
        """
        self._level = level

    def set_level(self, level: int) -> None:
        """
        Set the log level, above which to log messages as they show
        up. Messages with a lower log level will not be displayed.
        """
        self._level = level

    def get_level(self) -> int:
        """
        Get the current log level.
        """
        return self._level

    def msg(self, level: int, text: str) -> bool:
        """
        Log a message to the output. The message is prefaced with a
        string representation of the log level, the function and module
        from which the log call was made, and the message itself, in
        that order.
        """
        if level < self._level:
            return False

        stack = inspect.stack()
        frame = stack[2][0]

        if 'self' in frame.f_locals:
            clazz = frame.f_locals['self'].__class__.__name__
        else:
            clazz = None

        if level == DEBUG:
            level_str = 'DEBUG'
        elif level == INFO:
            level_str = 'INFO'
        elif level == WARNING:
            level_str = 'WARNING'
        elif level == ERROR:
            level_str = 'ERROR'
        elif level == CRITICAL:
            level_str = 'CRITICAL'
        else:
            level_str = 'UNKNOWN LEVEL'

        method = frame.f_code.co_name

        msg_id = f"{clazz}.{method}()"

        print(f"[{level_str}]: {msg_id}: {text}")

        return True


_log = Log(INFO)


def get_logger() -> Log:
    """
    Get the default logger. All code should use this logger; that is,
    there should only ever be one instance of the Log class.
    """
    return _log


def msg(level: int, text: str) -> bool:
    """
    A shorthand for `log.get_logger().msg()` that allows the syntax
    `log.msg()` to be used.
    """
    return get_logger().msg(level, text)
