import numpy as np
from .. import maskfunc as msk
from .. import subject_class as sc
from numpy.testing import assert_equal
import copy

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


