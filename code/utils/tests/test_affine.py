import numpy as np
from .. import affine
from numpy.testing import assert_array_equal

def test_voxels_to_mm():
	subject = "sub001"
	run = "task001_run001.feat"
	voxellist = [[100, 150, 200],
				 [130, 145, 176],
				 [95, 99, 23]]
	x = affine.voxels_to_mm(subject, run, voxellist)
	expected = [np.array([-110, 174, 328]),
				np.array([-170, 164, 280]),
				np.array([-100, 72, -26])]
	assert_array_equal(expected, x)

def test_mm_to_voxels():
	subject = "sub004"
	run = "task001_run008.feat"
	mmlist = [np.array([-110, 174, 328]),
				np.array([-170, 164, 280]),
				np.array([-100, 72, -26])]
	x = affine.mm_to_voxels(subject, run, mmlist)
	expected = [np.array([100, 150, 200]),
				np.array([130, 145, 176]),
				np.array([95, 99, 23])]
	assert_array_equal(expected, x)
