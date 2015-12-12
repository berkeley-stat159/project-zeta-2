import nibabel as nib
import numpy as np

# Takes in a dictionary with (K, V) pair (subxxx_runyyy, modified 4D Array)
# Returns the masked with time collapsed and vol_mean
def generateMaskedBrain(allFiguresDict):
	maskedDict = {}
	volumeDict = {}
	for key, value in allFiguresDict.items():
		data = value
		vol_mean = np.mean(data, axis = -1)
		percentile = np.percentile(np.ravel(vol_mean), q = 80)
		data[vol_mean > percentile, :] = True
		data[vol_mean < percentile, :] = False
		maskedDict[key] = vol_mean > percentile
		volumeDict[key] = vol_mean
	return maskedDict, volumeDict

def generateMask(allFiguresDict, percent):
	maskedDict = {}
	volumeDict = {}
	for key, value in allFiguresDict.items():
		data = value
		vol_mean = np.mean(data, axis = -1)
		percentile = np.percentile(np.ravel(vol_mean), q = percent)
		data[vol_mean > percentile, :] = True
		data[vol_mean < percentile, :] = False
		maskedDict[key] = vol_mean > percentile
		volumeDict[key] = vol_mean
	return maskedDict, volumeDict

# generateMaskedBrain(['/Users/edithho/Downloads/ds105/sub001/model/model001/task001_run002.feat'])
# test = load_obj('test1')
# print(test.shape)