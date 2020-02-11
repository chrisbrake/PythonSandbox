import os
from dbSetup.tinyDbSetup import db

PATH = 'tinydb.json'


def test_basic():
    """ simplest possible test to verify the import works """
    if os.path.exists(PATH):
        os.remove(PATH)

    db(PATH).insert({'name': 'John', 'age': 22})
    assert db(PATH).all() == [{'name': 'John', 'age': 22}]
