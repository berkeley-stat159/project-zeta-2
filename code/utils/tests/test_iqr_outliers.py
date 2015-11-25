""" Tests for iqr_outliers function in diagnostics module

Run with:

    nosetests test_iqr_outliers
"""

import numpy as np
from .. import diagnostics
from nose.tools import assert_equal
from numpy.testing import assert_almost_equal, assert_array_equal


def test_iqr_outliers():
    # Test with simplest possible array
    arr = np.arange(101)  # percentile same as value
    # iqr = 50
    exp_lo = 25 - 75
    exp_hi = 75 + 75
    indices, thresholds = diagnostics.iqr_outliers(arr)
    assert_array_equal(indices, [])
    assert_equal(thresholds, (exp_lo, exp_hi))
    # Reverse, same values
    indices, thresholds = diagnostics.iqr_outliers(arr[::-1])
    assert_array_equal(indices, [])
    assert_equal(thresholds, (exp_lo, exp_hi))
    # Add outliers
    arr[0] = -51
    arr[1] = 151
    arr[100] = 1  # replace lost value to keep centiles same
    indices, thresholds = diagnostics.iqr_outliers(arr)
    assert_array_equal(indices, [0, 1])
    assert_equal(thresholds, (exp_lo, exp_hi))
    # Reversed, then the indices are reversed
    indices, thresholds = diagnostics.iqr_outliers(arr[::-1])
    assert_array_equal(indices, [99, 100])
    assert_equal(thresholds, (exp_lo, exp_hi))


def test_iqr_scaling():
    # Check that the scaling of IQR works
    # Test with simplest possible array
    arr = np.arange(101)  # percentile same as value
    # iqr = 50
    exp_lo = 25 - 100
    exp_hi = 75 + 100
    indices, thresholds = diagnostics.iqr_outliers(arr, 2)
    assert_array_equal(indices, [])
    assert_equal(thresholds, (exp_lo, exp_hi))
    # Add outliers - but these aren't big enough now
    arr[0] = -51
    arr[1] = 151
    indices, thresholds = diagnostics.iqr_outliers(arr, 2)
    assert_array_equal(indices, [])
    # Add outliers - that are big enough
    arr[0] = -76
    arr[1] = 176
    arr[100] = 1  # replace lost value to keep centiles same
    indices, thresholds = diagnostics.iqr_outliers(arr, 2)
    assert_array_equal(indices, [0, 1])
