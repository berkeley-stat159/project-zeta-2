""" Tests for vol_std function in diagnostics module

Run with:

    nosetests test_vol_std.py
"""

import numpy as np
from .. import diagnostics
from numpy.testing import assert_almost_equal, assert_array_equal

def test_vol_std():
    # We make a fake 4D image
    shape_3d = (2, 3, 4)
    V = np.prod(shape_3d)
    T = 10  # The number of 3D volumes
    # Make a 2D array that we will reshape to 4D
    arr_2d = np.random.normal(size=(V, T))
    expected_stds = np.std(arr_2d, axis=0)
    # Reshape to 4D
    arr_4d = np.reshape(arr_2d, shape_3d + (T,))
    actual_stds = diagnostics.vol_std(arr_4d)
    assert_almost_equal(expected_stds, actual_stds)
