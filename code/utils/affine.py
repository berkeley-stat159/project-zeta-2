import numpy
import nibabel as nib
import numpy.linalg as npl
import os

base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..", "..", "data", "ds105")

# This function takes in the path
# to an image, and a list of voxel
# coordinates that you wish to track
# in another picture. The function will
# return the corresponding affine values
# as a list of numpy arrayss.

def voxels_to_mm(subject, run, voxellist):
	subjectpath = os.path.join(base_path, subject, "model", "model001")
	subjectpath = os.path.join(subjectpath, run, "filtered_func_data_mni.nii.gz")
	img = nib.load(subjectpath)
	vox_to_mm = img.affine
	mmlist = []
	for voxel in voxellist:
		mmlist.append(nib.affines.apply_affine(vox_to_mm, voxel))
	return mmlist

# This function will be the inverse of the
# function above. Thus, it will take in a list
# of numpy arrays and will convert them back to a
# a list of voxel coordinates as numpy arrays.

def mm_to_voxels(subject, run, mmlist):
	subjectpath = os.path.join(base_path, subject, "model", "model001")
	subjectpath = os.path.join(subjectpath, run, "filtered_func_data_mni.nii.gz")
	img = nib.load(subjectpath)	
	mm_to_vox = npl.inv(img.affine)
	voxellist = []
	for mm in mmlist:
		voxellist.append(nib.affines.apply_affine(mm_to_vox, mm))
	return voxellist


