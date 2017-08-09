#!/usr/bin/python

import logging
from time import time

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
