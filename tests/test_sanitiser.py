from hypothesis import given
from hypothesis.strategies import dictionaries, text, integers
from unittest import TestCase

from sanitiser import sanitiser


class TestSanitiser(TestCase):
    """ Testing Sanitiser Functions """

    @given(test_dict=dictionaries(keys=text(), values=text(), min_size=1))
    def test_keys_are_strings_true(self, test_dict):
        """
        Assuming a dict of at least one entry that contains text we should
        get a True back
        """
        self.assertTrue(sanitiser.keys_and_values_are_strings(test_dict))

    @given(test_dict=dictionaries(keys=integers(), values=integers()))
    def test_keys_are_strings_false(self, test_dict):
        """
        Given an empty dict, or one that contains something other than
        text we should fail.
        """
        self.assertFalse(sanitiser.keys_and_values_are_strings(test_dict))
