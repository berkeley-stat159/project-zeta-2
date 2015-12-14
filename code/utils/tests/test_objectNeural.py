import numpy as np
from .. import get_object_neural as gon
from numpy.testing import assert_equal
import copy
import math

def testFile():
	sub_ID = 1
	condition_dict = {}
	TR = 1
	n_vox = 1

	x = gon.get_object_neural(sub_ID, condition_dict, TR, n_vox, object_name="face", check=0)
	assert_equal(len(x), 0)