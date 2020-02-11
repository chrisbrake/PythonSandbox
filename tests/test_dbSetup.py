from dbSetup.tinyDbSetup import db
import tinydb

PATH = 'tinydb.json'

TEST_DATA = [
    {'name': 'John', 'age': 22},
    {'name': 'Ringo', 'age': 23},
    {'name': 'Paul', 'age': 24},
    {'name': 'Peter', 'age': 25}
]


def test_basic():
    """ simplest possible test to verify the import works """
    db(PATH).purge_tables()
    db(PATH).insert({'thing1': 'thing2'})
    assert db(PATH).all() == [{'thing1': 'thing2'}]


def test_selects():
    """ confirm I can narrow from 'all' """
    db(PATH).purge_tables()
    for d in TEST_DATA:
        db(PATH).insert(d)

    assert db(PATH).all() == TEST_DATA
    paul = db(PATH).search(tinydb.where('name') == 'Paul')
    assert paul == [{'name': 'Paul', 'age': 24}]


def test_insert_list():
    """ Confirm there is syntax for inserting many """
    db(PATH).purge_tables()
    db(PATH).insert_multiple(TEST_DATA)
    assert db(PATH).all() == TEST_DATA

