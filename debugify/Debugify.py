#!/usr/bin/python

import logging
from time import sleep, time

logger = logging.getLogger(__name__)


def debugify(method):
    """
    A decorator method to allow debug information to be easily obtained from
    a method without directly modifying it's code, or behavior.

    :param method: The method that was decorated.
    :return: The wrapped method
    """
    def debugger(*args, **kwargs):
        if not logger.isEnabledFor(logging.DEBUG):
            return method(*args, **kwargs)
        else:
            start = time()
            return_value = method(*args, **kwargs)
            end = time()
            elapsed = (end - start) * 1000
            logger.debug('%s(%s%s) -> %s Took %.2f msec.' % (
                method.__name__, args, kwargs, return_value, elapsed))
            return return_value

    return debugger

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s')

    @debugify
    def test_debugger(*args, **kwargs):
        sleep(1)
        return 'A', 42


    logger.setLevel(logging.INFO)
    logger.info('Log level set to info.')
    test_debugger("one", 2, three=3)

    logger.setLevel(logging.DEBUG)
    logger.info('Log level set to debug.')
    test_debugger("one", 2,  three=3)
