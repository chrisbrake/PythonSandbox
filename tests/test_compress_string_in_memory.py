import unittest
from hypothesis import given, settings
from hypothesis.strategies import text
from sys import getsizeof, path

path.append('../')
from compressStr import compress_string, decompress_string


class TestMyGzip(unittest.TestCase):
    """
    Unit tests for the my_gzip module.
    """

    @given(string=text())
    @settings(max_examples=100)
    def test_combined(self, string):
        """
        Test to confirm UTF-8 text is not be modified by this process.

        :param string: UTF-8 Characters
        """
        self.assertEqual(string, decompress_string(compress_string(string)))

    @given(string=text(min_size=25))
    @settings(max_examples=10)
    def test_compression(self, string):
        """
        Test to confirm the compressed string is smaller than the original.

        Using min_size because an empty string, is smaller than an empty
        compressed object.  This min size setting ensures that we do not get
        false positive failures.

        :param string: UTF-8 Characters
        """
        self.assertLess(getsizeof(compress_string(string)), getsizeof(string))


if __name__ == '__main__':
    unittest.main()
