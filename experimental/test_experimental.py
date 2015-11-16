""" Tests for all modules within experimental
Run with:
    nosetests test_experimental.py
"""

from nose.tools import assert_equal
import subject_class as sub

testsubject = sub.subject('sub001')

def test_dummy():
	assert_equal(3, 3)

def test_sub_id():
	assert_equal(testsubject.sub_BOLD_path, 
				 "../data/ds105/sub001/BOLD/")