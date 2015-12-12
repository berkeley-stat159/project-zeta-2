import numpy as np
from .. import subject_class as sc
from numpy.testing import assert_equal
import copy

def test_subject():
	subid = "sub001"
	sub = sc.subject(subid)
	sub_img = sub.run_img_result
	assert_equal(len(sub_img), 12)
