import numpy as np
from .. import get_object_neural as gon
from numpy.testing import assert_equal

def testFile1():
	sub_ID = 1
	condition_dict = {}
	TR = 1
	n_vox = 1
	x = gon.get_object_neural(sub_ID, condition_dict, TR, n_vox, object_name="face", check=0)
	assert_equal(len(x), 0)


def testFile2():
	sub_ID = 1
	condition_dict = {}
	TR = 1
	n_vox = 1
	x = gon.get_object_neural(sub_ID, condition_dict, TR, n_vox, object_name="all", check=0)
	assert_equal(len(x), 0)

def testFile3():
	sub_ID = 1
	condition_dict = {}
	condition_dict["run002-face"] = np.array([0, 1, 2, 3, 4])
	TR = 1
	n_vox = 1
	x = gon.get_object_neural(sub_ID, condition_dict, TR, n_vox, object_name="face", check=1)
	assert_equal(len(x), 0)

def testFile4():
	sub_ID = 1
	condition_dict = {}
	condition_dict["run001-face"] = np.array([0, 1, 2, 3, 4])
	TR = 1
	n_vox = 1
	x = gon.get_object_neural(sub_ID, condition_dict, TR, n_vox, object_name="face", check=2)
	assert_equal(len(x), 0)