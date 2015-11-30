import numpy as np
import nibabel as nib
import numpy.linalg as npl

# This function takes in an image, a 2D array,
# and a z value. It will return a 3D array with
# mm coordinates for each of the x, y pairs in 
# the 2D array with a z-coordinate of z.

def voxels_to_mm(img, xyarray, z):
	xyshape = xyarray.shape
	xyzshape = (xyshape[0], xyshape[1] + 1)
	xyzarray = np.zeros(xyzshape)
	xyzarray[:, : - 1] = xyarray
	xyzarray[:, -1] = z
	vox_to_mm = convert_to_mm(img)
	return np.apply_along_axis(vox_to_mm, axis = 1, arr = xyzarray)

# Helper method to use np.apply_along_axis

def convert_to_mm(img):
	def inputvoxel(voxel):
		vox_to_mm = img.affine
		return nib.affines.apply_affine(vox_to_mm, voxel)
	return inputvoxel

# This function will be the inverse of voxels_to_mm.

def mm_to_voxels(img, xyzarray):
	mm_to_vox = convert_to_vox(img)
	return np.apply_along_axis(mm_to_vox, axis = 1, arr = xyzarray)

# Helper method to use np.apply_along_axis

def convert_to_vox(img):
	def inputmm(mm):
		mm_to_vox = npl.inv(img.affine)
		return nib.affines.apply_affine(mm_to_vox, mm)
	return inputmm
