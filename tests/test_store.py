from os import remove
from sys import path
from tempfile import mkstemp
from unittest import TestCase

path.append('../')

from store import store


class TestStore(TestCase):
    def setUp(self):
        (_, self.tmp_file) = mkstemp()

    def tearDown(self):
        remove(self.tmp_file)

    def test_get_exclusive_lock_success(self):
        with open(self.tmp_file, 'w') as f:
            store.get_exclusive_lock(f, timeout=1)
            f.write('test data')
