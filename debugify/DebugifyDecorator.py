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
        if logger.isEnabledFor(logging.DEBUG):
            start = time()
            return_value = method(*args, **kwargs)
            end = time()
            elapsed = (end - start) * 1000
            logger.debug('%s(%s%s) -> %.2f msec -> %s' % (
                method.__name__, args, kwargs, elapsed, return_value))
            return return_value
        else:
            return method(*args, **kwargs)

    return debugger
