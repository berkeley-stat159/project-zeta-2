import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib

def pull3D(vector):
	img = nib.load('bold.nii')
	data = img.get_data()
	Three_D_Data = []
	for i in range(0, len(vector)):
		if vector[i] == 1:
			Three_D_Data.append(data[:, :, :, i])
	return Three_D_Data

def ShowCortex(ListOf3dImages):
	for image in ListOf3dImages:
		zDimension = np.shape(image)[2]
		for i in range(0, zDimension):
			plt.imshow(image[:, :, i], cmap = "gray")
			plt.show()

# You'll have to guess the Z value from the images show in the previous function
def generateEvenlySpacedZpoints(zValue):
	return np.linspace(start = 0, stop = zValue, num = zValue)
