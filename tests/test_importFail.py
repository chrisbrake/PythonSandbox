from sys import path
from unittest import main, TestCase

path.append('../')


class TestImportFail(TestCase):
    """
    Testing ImportFail Functions
    """

    def test_not_special(self):
        from importFail.importFail import not_special
        self.assertIsInstance(not_special(), str)

    def test_special(self):
        from importFail.importFail import special
        self.assertIsInstance(special(), str)

    def test_impossible(self):
        from importFail.importFail import impossible
        with self.assertRaises(NotImplementedError):
            impossible()

if __name__ == '__main__':
    main()
