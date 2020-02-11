import tinydb

_db = None


def db(path):
    """
    Get a handle for the data store.

    :param path:
    :return:
    """
    global _db
    if _db is None:
        _db = tinydb.TinyDB(path)
    return _db
