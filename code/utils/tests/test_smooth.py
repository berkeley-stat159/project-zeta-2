import numpy as np
from .. import smooth as sm
from numpy.testing import assert_equal
import copy
import math

def test_smooth():
	x = {}
	y = sm.smooth(x)
	assert_equal(len(x), 0)