"""Persist a Python dictionary across program executions. This module
provides the UserData class, which allows the program to store data without
regard for how it ends up in persistent storage.

Note that you should use user_data.get() to get the default instance of
UserData instead of instantiating it yourself in most cases, although you
may wish to instantiate a new UserData with a different store location."""
import json
import os
import pathlib
import sys

import log


class UserData:
    """
    UserData is a simple dictionary-like class that persists its keys and
    values to the disk in JSON format. The logic for persisting values is
    entirely abstracted away such that any data inserted into the store is
    automatically persisted without further caller intervention.

    This class currently provides no method for tuning the cache lifetime or
    write frequency; the persistent storage is written immediately when data
    is pushed with __setitem__().

    Data is accessed and persisted exactly as if the object were a
    dictionary, so use the Python dictionary syntax to store data.
    """

    # For consistency, only one UserData class can correspond to a file on
    # the disk. This is how we keep track.
    __open_handles = []

    @staticmethod
    def get_data_dir() -> pathlib.Path:
        """
        Get the application data directory in a platform-agnostic manner.
        This function supports Windows, Linux, and MacOS, although I am
        unfamiliar with MacOS so I don't know if I got the directory correct.
        """
        platform = sys.platform
        home = pathlib.Path.home()

        if platform == 'win32':
            path = os.getenv('APPDATA')
        elif platform.startswith('linux'):
            path = os.getenv('XDG_DATA_HOME') or home / '.local/share'
        elif platform == 'darwin':
            path = home / 'Library/Application Support'
        else:
            raise OSError(f"Unknown platform: {platform}")

        return pathlib.Path(path)

    def __init__(self, store: pathlib.Path):
        """
        Construct a new persistent user data store. The passed parameter
        should be a path from which data will be loaded and into which data
        will be stored transparently. Note that only one UserData class can
        correspond to a single file on the disk at a time, and runtime
        checks are in place to ensure this is the case.
        """
        if store in UserData.__open_handles:
            raise NameError(
                'Handle already open. '
                'Did you forget to call close() on a different UserData?')

        self.store = store
        self.cache = {}

        log.msg(log.DEBUG, f"User data store: {self.store}")
        if not self.store.exists():
            log.msg(log.DEBUG, "Creating new data store...")
            self.store.write_text(json.dumps(self.cache))
        else:
            json_str = self.store.read_text()
            self.cache = json.loads(json_str)
            log.msg(log.DEBUG,
                    f"Loaded {len(self.cache.keys())} key(s) from data store.")

        UserData.__open_handles.append(self.store)
        self.closed = False

    def __getitem__(self, key):
        if self.closed:
            raise AssertionError('Use after close.')

        if key not in self.cache:
            # This message is worded the way it is because if we say
            # "Key not fount in" then PEP8 throws a warning? For a Python-ism
            # inside a string literal?
            log.msg(log.WARNING, f"Key found not in data store: '{key}'")
            return None

        value = self.cache[key]
        log.msg(log.DEBUG, f"'{key}' = '{value}'")
        return value

    def __setitem__(self, key, value):
        if self.closed:
            raise AssertionError('Use after close.')

        self.cache[key] = value
        json_str = json.dumps(self.cache)
        self.store.write_text(json_str)
        log.msg(log.DEBUG, f"'{key}' = '{value}'")

    def get_path(self) -> pathlib.Path:
        """
        Get the name of the file backing this persistent user data store.
        """
        return self.store

    def close(self):
        """
        When a UserData store is no longer in use, this function should be
        called on it to notify the system that the handle can be closed.
        This flushes the cache and allows the user to create new UserData
        stores in the future that are backed by the same file as this one was.

        Note that closed stores can no longer be used; they must be re-created.
        """
        if self.store in UserData.__open_handles:
            UserData.__open_handles.remove(self.store)
            log.msg(log.DEBUG,
                    f"Removed store {self.store} from __open_handles.")
            self.closed = True
        else:
            raise AssertionError(
                'Failed to remove handle. Double-close() on UserData?')


#  Construct a global, default user data store.
data = UserData(UserData.get_data_dir() / 'arg.json')


def get() -> UserData:
    """
    Get the global, default UserData store. This is the one that should be
    used for most purposes; it is unlikely that you will have to manually
    create new UserData stores. Note that this store should be closed before
    the program exits.
    """
    return data
