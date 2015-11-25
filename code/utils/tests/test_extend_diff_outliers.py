""" Tests for extend_diff_outliers function in diagnostics module

Run with:

    nosetests test_extend_diff_outliers
"""

import numpy as np
from .. import diagnostics
from nose.tools import assert_equal
from numpy.testing import assert_almost_equal, assert_array_equal


def test_extend_diff_outliers():
    # Test function to extend difference outlier indices
    indices = np.array([3, 7, 12, 20])
    assert_array_equal(diagnostics.extend_diff_outliers(indices),
                       [3, 4, 7, 8, 12, 13, 20, 21])


def test_sequential_input():
    indices = np.array([4, 5, 9, 10])
    assert_array_equal(diagnostics.extend_diff_outliers(indices),
                       [4, 5, 6, 9, 10, 11])
    indices = np.array([1, 2, 4, 5, 9, 10])
    assert_array_equal(diagnostics.extend_diff_outliers(indices),
                       [1, 2, 3, 4, 5, 6, 9, 10, 11])
    indices = np.array([3, 7, 8, 12, 20])
    assert_array_equal(diagnostics.extend_diff_outliers(indices),
                       [3, 4, 7, 8, 9, 12, 13, 20, 21])
