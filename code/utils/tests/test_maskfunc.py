import numpy as np
from .. import maskfunc as msk
from numpy.testing import assert_equal
import copy

def test_dictionary1():
	x = range(16)
	y = np.reshape(x, (2, 2, 2, 2))
	newDict = {}
	newDict["BugsBunny"] = y
	maskedDict, volDict = msk.generateMaskedBrain(newDict)
	assert_equal(len(maskedDict), len(volDict))

def test_dictionary2():
	x = range(16)
	y = np.reshape(x, (2, 2, 2, 2))
	newDict = {}
	newDict["BugsBunny"] = y
	maskedDict, volDict = msk.generateMask(newDict, 80)
	assert_equal(len(maskedDict), len(volDict))


