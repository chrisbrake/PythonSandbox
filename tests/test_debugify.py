import logging
import unittest

from hypothesis import given, settings
from hypothesis.strategies import dictionaries, text, tuples
from debugify import debugify


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')


@debugify
def method_to_debug(*args, **kwargs):
    return args, kwargs


class TestDebugify(unittest.TestCase):
    """Unit tests for the debugify module"""

    @given(args=tuples(text()),
           kwargs=dictionaries(keys=text(), values=text()))
    @settings(max_examples=100)
    def test_return(self, args, kwargs):
        """Confirm the return value is not modified by the process"""
        for log_level in range(0, 51, 10):
            logger.setLevel(log_level)
            self.assertTupleEqual((args, kwargs),
                                  method_to_debug(*args, **kwargs))


if __name__ == '__main__':
    unittest.main()
