import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from stimuli import events2neural



%matplotlib

img = nib.load('bold.nii')
data = img.get_data()
plt.imshow(data[:, :, 30, 64], cmap='gray', interpolation = "nearest")
plt.imshow(data[:, :, 30, 68], cmap='gray', interpolation = "nearest")

TR = 2.5
n_trs = img.shape[-1]  # The original number of TRs
neural = events2neural('cond001.txt', TR, n_trs)

dataX = data[:, :, 30, 64]

