import numpy as np
from .. import maskfunc as msk
from .. import subject_class as sc
import os
from numpy.testing import assert_equal
import copy

basepath = os.path.abspath(os.path.dirname(__file__))

realpath = os.path.join(basepath, "..", "..", "..", "data", "ds105")
realpath = os.path.join(realpath, "sub001", "model", "model001")
realpath = os.path.join(realpath, "task001_run001.feat", "filtered_func_data_mni.nii.gz")
dummypath = os.path.join(basepath, "testsub001run001.nii.gz")

def test_dictionary():
	# which subject to work on?
	subid = "sub001"
	sub = sc.subject(subid)
	sub_img = sub.run_img_result
	sub_data = {}
	for key, img in sub_img.iteritems():
	    sub_data[key] = img.get_data()
	x = copy.deepcopy(sub_data)
	maskedDict, volDict = msk.generateMaskedBrain(x)
	assert_equal(len(maskedDict), len(volDict))


