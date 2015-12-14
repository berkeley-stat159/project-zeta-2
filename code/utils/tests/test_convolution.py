import numpy as np
from .. import convolution as co
from numpy.testing import assert_equal

def test_hrf():
	x = co.hrf(1)
	assert_equal(x, 0.59999999999999998)

def test_convolution():
	l1 = np.array([1, 2, 3]) 
	l2 = np.array([0, 1, 0.5])
	x = co.convolution(l1, l2)
	assert_equal(x, [0.0, 1.0, 2.5])

def test_getallConvolved():
	iDict = {}
	hrf = 1
	y = co.get_all_convolved(iDict, hrf, ".")
	assert_equal(len(y), 0)

def test_removeOutlier():
	iDict = {}
	a = co.remove_outlier("1" ,iDict, "HAHA", axis=0)
	assert_equal(len(iDict), 0)