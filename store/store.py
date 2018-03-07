import errno
import fcntl
import shelve
import threading
import time

thread_lock = threading.Lock()


def get_exclusive_lock(file_handle, timeout=None):
    """
    Get an exclusive lock so other processes will not mess with your file handle.
    :param file_handle: The open file you want to have an exclusive lock on.
    :param timeout: The max time to wait before giving up.
    :return: None
    :exception IOError, if we cannot get a lock on the file.
    """
    if timeout is None:
        timeout = 3

    start_time = time.time()
    while timeout > time.time() - start_time:
        try:
            fcntl.flock(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except IOError as e:
            if e.errno != errno.EAGAIN:
                raise  # Exceptions for reasons other than file lock will be raised
            time.sleep(0.1)
    raise IOError(errno.EAGAIN, 'Could not get file lock')


def release_exclusive_lock(file_handle):
    """
    Release exclusive lock
    :param file_handle: The open file you want to release the exclusive lock on.
    :return: None
    """
    fcntl.flock(file_handle, fcntl.LOCK_UN)


def put(name, item, file_store):
    """
    Adds, or updates an item
    :param name: The name of the item to store.
    :param item: The item to store
    :param file_store: The location of the filestore we are editing
    :return: None
    :raise: IOError if we cannot write to the file
    """
    with open(file_store, 'r') as f:
        get_exclusive_lock(f, timeout=1)
        with thread_lock:
            s = shelve.open(file_store)
            s[name] = item
            s.close()
        release_exclusive_lock(f)


def get(name, file_store):
    """
    Reads back the content of an item in the store.
    :param name: The name of the item we want.
    :param file_store: The location of the store to read from.
    :return: Object, the item requested.
    """
    try:
        f = shelve.open(file_store, 'r')
        return f[name]
    finally:
        f.close()
