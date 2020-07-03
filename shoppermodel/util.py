"""
Utility functions
"""
import numpy as np


def random_datetimes(minimum, maximum, size):
    """
    Returns a numpy array of random values.
    :param minimum: minimum allowed value.
    :param maximum: maximum allowed value.
    :param size: size of the output array.
    :return: a numpy array of random values.
    """
    result = np.random.rand(size) * (maximum - minimum) + minimum
    return result
