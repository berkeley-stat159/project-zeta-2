import numpy as np
from .. import smooth as sm
from numpy.testing import assert_equal

def test_smooth():
	x = {}
	y = sm.smooth(x)
	assert_equal(len(x), 0)