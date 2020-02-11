import tinydb

_db = None


def db(path):
    """
    Get a handle for the data store.

    :param path: the location of the file to open
    :return: the database
    """
    global _db
    if _db is None:
        _db = tinydb.TinyDB(path)
    return _db
