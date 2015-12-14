import numpy as np
from .. import diagnostics as di
from numpy.testing import assert_almost_equal, assert_array_equal

def test_evd():
    # We make a fake 4D image
    y = [3, 7, 8, 12, 20]
    x = di.extend_diff_outliers(y)
    assert_array_equal(x, [3, 4, 7, 8, 9, 12, 13, 20, 21])
