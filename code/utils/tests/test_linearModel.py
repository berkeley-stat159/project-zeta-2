import numpy as np
from .. import linear_model as lm
from numpy.testing import assert_equal
import copy
import math

def test_scaleDesignMtx():
	x = range(16)
	y = np.reshape(x, (4, 4))
	a = lm.scale_design_mtx(y)
	assert_equal(a[0], 0)

def test_batchScaleMatrix():
	x = range(16)
	y = np.reshape(x, (4, 4))
	iDict = {}
	iDict["001"] = y
	n = lm.batch_scale_matrix(iDict)
	assert_equal(len(n), 1)

def test_batchConvert_2d():
	x = range(16)
	y = np.reshape(x, (4, 4))
	iDict = {}
	iDict["001"] = y
	n = lm.batch_convert_2d(iDict)
	assert_equal(len(n), 1)

def test_batchConvert2dBased():
	x = range(16)
	y = np.reshape(x, (4, 4))
	iDict = {}
	iDict["001"] = y
	cDict = {}
	cDict["001"] = [16]
	n = lm.batch_convert_2d_based(iDict, cDict)
	assert_equal(len(n), 1)

def test_apply_mask():
	x = range(16)
	y = np.reshape(x, (4, 4))
	iDict = {}
	iDict["001"] = y
	cDict = {}
	cDict["001"] = 1
	p = lm.apply_mask(iDict, cDict)
	assert_equal(len(p), 1)

def test_tStat():
	x = range(4)
	X = np.reshape(x, (2, 2))
	y = [1, 2]
	p = np.reshape(x, (2, 2))
	one, two, three, four = lm.t_stat(y, X, p)
	assert_equal(len(one), 2)
	assert_equal(len(two), 2)
	assert_equal(three, 0)
	l = float('nan')
	assert_equal(four, np.array([[l, l], [l, l]]))
