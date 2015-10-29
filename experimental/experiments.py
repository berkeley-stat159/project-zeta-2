import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as npl
# from stimuli import events2neural



%matplotlib

img = nib.load('../data/bold.nii.gz')
data = img.get_data()
voxel_time_course = data[35, 32, 19]
# plt.plot(voxel_time_course)
convolved = np.loadtxt('../data/fd.txt')
# plt.plot(convolved)

N = len(convolved)
X = np.ones((N, 2))
X[:, 0] = convolved
# plt.imshow(X, interpolation='nearest', cmap='gray', aspect=0.1)
Xp = npl.pinv(X)
Xp.shape
beta_hat = Xp.dot(voxel_time_course)
beta_hat

y_hat = X.dot(beta_hat)
e_vec = voxel_time_course - y_hat
print(np.sum(e_vec ** 2))
plt.plot(voxel_time_course)
plt.plot(y_hat)


# plt.imshow(data[:, :, 30, 64], cmap='gray', interpolation = "nearest")
# plt.imshow(data[:, :, 30, 68], cmap='gray', interpolation = "nearest")

# TR = 2.5
# n_trs = img.shape[-1]  # The original number of TRs
# neural = events2neural('cond001.txt', TR, n_trs)

# dataX = data[:, :, 30, 64]




