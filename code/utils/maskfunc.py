import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd

# Takes in a dictionary with (K, V) pair (subxxx_runyyy, modified 4D Array)
# Returns the masked with time collapsed and vol_mean
def generateMaskedBrain(allFiguresDict):
	maskedDict = {}
	volumeDict = {}
	for key, value in allFiguresDict.iteritems():
		data = value
		vol_mean = np.mean(data, axis = -1)
		percentile = np.percentile(np.ravel(vol_mean), q = 80)
		data[vol_mean > percent, :] = True
		data[vol_mean < perecent, :] = False
		maskedDict[key] = data
		volumeDict[key] = vol_mean
    return maskedDict, volumeDict	

#def generateMaskedBrain(paths):
	#for path in paths:
		#img = nib.load(path + '/filtered_func_data_mni.nii.gz')
		#print(img.shape)
		#data = img.get_data()

		#vol_shape = data.shape[:-1]
		#n_trs = data.shape[-1]
		#print(vol_shape, n_trs)
		#mean_vol = np.mean(data, axis = -1)
		#percent = np.percentile(np.ravel(mean_vol), q = 80)
		#print(percent)
		#plt.hist(np.ravel(mean_vol), bins = 100)
		#plt.show()

		# in_brain_mask = mean_vol > percent

		#data[mean_vol > percent, :] = True
		#data[mean_vol < percent, :] = False
		#print data[:,25,25,25]
		#return data
		# brainSave = save_obj(in_brain_tcs, 'test1')
		# print(in_brain_tcs.shape)

		# plt.imshow(mean_vol[:, :, 50])
		# plt.show()
		# plt.imshow(in_brain_mask[:, :, 50])
		# plt.show()

def save_obj(obj, name):
	with open('/Users/mike/Downloads/ds105/sub001/model/model001/task001_run001.feat/' + name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	with open('/Users/mike/Downloads/ds105/sub001/model/model001/task001_run001.feat/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)

# generateMaskedBrain(['/Users/edithho/Downloads/ds105/sub001/model/model001/task001_run002.feat'])
# test = load_obj('test1')
# print(test.shape)