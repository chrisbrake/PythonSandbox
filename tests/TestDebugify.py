import logging
import sys
import unittest

sys.path.append('../')
from debugify import debugify


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')


@debugify
def method_to_debug(*args, **kwargs):
    if args and not kwargs:
        return args
    elif kwargs and not args:
        return kwargs
    else:
        return args, kwargs


class TestDebugify(unittest.TestCase):
    """Unit tests for the debugify module"""

    def test_return(self):
        """Confirm the return value is not modified by the process"""
        args = ('a', 'b', 'c', 1, 2, 3)
        kwargs = {'a': 1, 'b': 2, 'c':3}
        for log_level in [i*10 for i in range(0, 6)]:
            logger.setLevel(log_level)
            self.assertTupleEqual(args, method_to_debug(*args))
            self.assertDictEqual(kwargs, method_to_debug(**kwargs))

if __name__ == '__main__':
    unittest.main()
