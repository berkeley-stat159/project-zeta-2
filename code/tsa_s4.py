from __future__ import print_function, division
import numpy as np
import numpy.linalg as npl
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import gridspec
import os
import re
import json
import nibabel as nib
from utils import subject_class as sc
from utils import outlier
from utils import diagnostics as diagnos
from utils import get_object_neural as neural
from utils import stimuli
from utils import convolution as convol
from utils import linear_model as lm
from utils import maskfunc as msk
import copy
import statsmodels.api as sm
from operator import add

# important path:

base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")
figure_path = os.path.join(base_path, "code", "images", "")
file_path = os.path.join(base_path, "code", "txt", "")

# help to make directory to save figure and txt
if not os.path.exists(figure_path):
    os.makedirs(figure_path)
if not os.path.exists(file_path):
    os.makedirs(file_path)

# separator:
separator = "-" * 80

# which subject to work on?
subid = "sub004"

# work on results from this subject:
########################################

print (separator)
print ("Project-Zeta: use times series to study ds105 dataset")
print (separator)
print ("Focus on %s for the analysis" % subid)
print (separator)


sub = sc.subject(subid)

# get image files of this subject:
sub_img = sub.run_img_result

# get data for those figures
print ("Get data from images...")
sub_data = {}
for key, img in sub_img.iteritems():
    sub_data[key] = img.get_data()
print ("Complete!")
print (separator)

brain1 = sub_data["sub004_run001"]
x1 = copy.deepcopy(sub_data)
maskedDict, volDict = msk.generateMaskedBrain(x1)
s4r1Masked = maskedDict["sub004_run001"]
s4r1Vol = volDict["sub004_run001"]

brain2 = sub_data["sub004_run002"]
s4r2Masked = maskedDict["sub004_run002"]
s4r2Vol = volDict["sub004_run002"]

brain3 = sub_data["sub004_run003"]
s4r3Masked = maskedDict["sub004_run003"]
s4r3Vol = volDict["sub004_run003"]

brain4 = sub_data["sub004_run004"]
s4r4Masked = maskedDict["sub004_run004"]
s4r4Vol = volDict["sub004_run004"]

brain5 = sub_data["sub004_run005"]
s4r5Masked = maskedDict["sub004_run005"]
s4r5Vol = volDict["sub004_run005"]

brain6 = sub_data["sub004_run006"]
s4r6Masked = maskedDict["sub004_run006"]
s4r6Vol = volDict["sub004_run006"]

brain7 = sub_data["sub004_run007"]
s4r7Masked = maskedDict["sub004_run007"]
s4r7Vol = volDict["sub004_run007"]

brain8 = sub_data["sub004_run008"]
s4r8Masked = maskedDict["sub004_run008"]
s4r8Vol = volDict["sub004_run008"]

brain9 = sub_data["sub004_run009"]
s4r9Masked = maskedDict["sub004_run009"]
s4r9Vol = volDict["sub004_run009"]

brain10 = sub_data["sub004_run010"]
s4r10Masked = maskedDict["sub004_run010"]
s4r10Vol = volDict["sub004_run010"]

brain11 = sub_data["sub004_run011"]
s4r11Masked = maskedDict["sub004_run011"]
s4r11Vol = volDict["sub004_run011"]

brain12 = sub_data["sub004_run012"]
s4r12Masked = maskedDict["sub004_run012"]
s4r12Vol = volDict["sub004_run012"]
# Focus on z = 37:42, y = 25 to 50, all of x

# brain = brain[:, 25:50, 32, :]
# s1r1Masked = s1r1Masked[:, 25:50, 32]
# brain = brain[s1r1Masked, :]

brains4r1 = brain1[:, 25:50, 37:42, :]
s4r1Masked = s4r1Masked[:, 25:50, 37:42]
brains4r1 = brains4r1[s4r1Masked, :]

brains4r2 = brain2[:, 25:50, 37:42, :]
s4r2Masked = s4r2Masked[:, 25:50, 37:42]
brains4r2 = brains4r2[s4r2Masked, :]

brains4r3 = brain3[:, 25:50, 37:42, :]
s4r3Masked = s4r3Masked[:, 25:50, 37:42]
brains4r3 = brains4r3[s4r3Masked, :]

brains4r4 = brain4[:, 25:50, 37:42, :]
s4r4Masked = s4r4Masked[:, 25:50, 37:42]
brains4r4 = brains4r4[s4r4Masked, :]

brains4r5 = brain5[:, 25:50, 37:42, :]
s4r5Masked = s4r5Masked[:, 25:50, 37:42]
brains4r5 = brains4r5[s4r5Masked, :]

brains4r6 = brain6[:, 25:50, 37:42, :]
s4r6Masked = s4r6Masked[:, 25:50, 37:42]
brains4r6 = brains4r6[s4r6Masked, :]

brains4r7 = brain7[:, 25:50, 37:42, :]
s4r7Masked = s4r7Masked[:, 25:50, 37:42]
brains4r7 = brains4r7[s4r7Masked, :]

brains4r8 = brain8[:, 25:50, 37:42, :]
s4r8Masked = s4r8Masked[:, 25:50, 37:42]
brains4r8 = brains4r8[s4r8Masked, :]

brains4r9 = brain9[:, 25:50, 37:42, :]
s4r9Masked = s4r9Masked[:, 25:50, 37:42]
brains4r9 = brains4r9[s4r9Masked, :]

brains4r10 = brain10[:, 25:50, 37:42, :]
s4r10Masked = s4r10Masked[:, 25:50, 37:42]
brains4r10 = brains4r10[s4r10Masked, :]

brains4r11 = brain11[:, 25:50, 37:42, :]
s4r11Masked = s4r11Masked[:, 25:50, 37:42]
brains4r11 = brains4r11[s4r11Masked, :]

brains4r12 = brain12[:, 25:50, 37:42, :]
s4r12Masked = s4r12Masked[:, 25:50, 37:42]
brains4r12 = brains4r12[s4r12Masked, :]

arr1 = [0.0] * 121
for i in range(121):
	arr1[i] = np.mean(brains4r1[:, i])

r1house = arr1[78:88]
r1scram = arr1[64:74]
r1cat = arr1[93:103]
r1shoe = arr1[50:60]
r1bottle = arr1[107:117]
r1scissor = arr1[35:45]
r1chair = arr1[21:31]
r1face = arr1[6:16]


arr2 = [0.0] * 121
for i in range(121):
	arr2[i] = np.mean(brains4r2[:, i])

r2house = arr2[107:117]
r2scram = arr2[21:31]
r2cat = arr2[6:16]
r2shoe = arr2[78:88]
r2bottle = arr2[64:74]
r2scissor = arr2[35:45]
r2chair = arr2[50:60]
r2face = arr2[93:103]


arr3 = [0.0] * 121
for i in range(121):
	arr3[i] = np.mean(brains4r3[:, i])

r3house = arr3[107:117]
r3scram = arr3[21:31]
r3cat = arr3[78:88]
r3shoe = arr3[50:60]
r3bottle = arr3[64:74]
r3scissor = arr3[35:45]
r3chair = arr3[93:103]
r3face = arr3[6:16]


arr4 = [0.0] * 121
for i in range(121):
	arr4[i] = np.mean(brains4r4[:, i])

r4house = arr4[50:60]
r4scram = arr4[35:45]
r4cat = arr4[21:31]
r4shoe = arr4[93:103]
r4bottle = arr4[107:117]
r4scissor = arr4[64:74]
r4chair = arr4[78:88]
r4face = arr4[6:16]


arr5 = [0.0] * 121
for i in range(121):
	arr5[i] = np.mean(brains4r5[:, i])

r5house = arr5[78:88]
r5scram = arr5[21:31]
r5cat = arr5[6:16]
r5shoe = arr5[64:74]
r5bottle = arr5[50:60]
r5scissor = arr5[107:117]
r5chair = arr5[35:45]
r5face = arr5[93:103]


arr6 = [0.0] * 121
for i in range(121):
	arr6[i] = np.mean(brains4r6[:, i])

r6house = arr6[93:103]
r6scram = arr6[107:117]
r6cat = arr6[21:31]
r6shoe = arr6[35:45]
r6bottle = arr6[78:88]
r6scissor = arr6[64:74]
r6chair = arr6[50:60]
r6face = arr6[6:16]


arr7 = [0.0] * 121
for i in range(121):
	arr7[i] = np.mean(brains4r7[:, i])

r7house = arr7[6:16]
r7scram = arr7[21:31]
r7cat = arr7[78:88]
r7shoe = arr7[50:60]
r7bottle = arr7[93:103]
r7scissor = arr7[107:117]
r7chair = arr7[64:74]
r7face = arr7[35:45]


arr8 = [0.0] * 121
for i in range(121):
	arr8[i] = np.mean(brains4r8[:, i])

r8house = arr8[21:31]
r8scram = arr8[78:88]
r8cat = arr8[50:60]
r8shoe = arr8[6:16]
r8bottle = arr8[93:103]
r8scissor = arr8[107:117]
r8chair = arr8[35:45]
r8face = arr8[64:74]


arr9 = [0.0] * 121
for i in range(121):
	arr9[i] = np.mean(brains4r9[:, i])

r9house = arr9[64:74]
r9scram = arr9[78:88]
r9cat = arr9[35:45]
r9shoe = arr9[50:60]
r9bottle = arr9[93:103]
r9scissor = arr9[6:16]
r9chair = arr9[107:117]
r9face = arr9[21:31]


arr10 = [0.0] * 121
for i in range(121):
	arr10[i] = np.mean(brains4r10[:, i])

r10house = arr10[6:16]
r10scram = arr10[107:117]
r10cat = arr10[93:103]
r10shoe = arr10[78:88]
r10bottle = arr10[35:45]
r10scissor = arr10[21:31]
r10chair = arr10[64:74]
r10face = arr10[50:60]


arr11 = [0.0] * 121
for i in range(121):
	arr11[i] = np.mean(brains4r11[:, i])

r11house = arr11[21:31]
r11scram = arr11[50:60]
r11cat = arr11[93:103]
r11shoe = arr11[78:88]
r11bottle = arr11[6:16]
r11scissor = arr11[107:117]
r11chair = arr11[35:45]
r11face = arr11[64:74]


arr12 = [0.0] * 121
for i in range(121):
	arr12[i] = np.mean(brains4r12[:, i])

r12house = arr12[50:60]
r12scram = arr12[64:74]
r12cat = arr12[35:45]
r12shoe = arr12[78:88]
r12bottle = arr12[93:103]
r12scissor = arr12[107:117]
r12chair = arr12[21:31]
r12face = arr12[6:16]

evenHouse = (np.array(r2house) + np.array(r4house) + 
			 np.array(r6house) + np.array(r8house) + 
			 np.array(r10house) + np.array(r12house)) / 6
oddHouse = (np.array(r1house) + np.array(r3house) + 
			np.array(r5house) + np.array(r7house) + 
			np.array(r9house) + np.array(r11house)) / 6
evenScram = (np.array(r2scram) +  np.array(r4scram) + 
			 np.array(r6scram) + np.array(r8scram) + 
			 np.array(r10scram) +  np.array(r12scram)) / 6
oddScram = (np.array(r1scram) + np.array(r3scram) + 
			np.array(r5scram) + np.array(r7scram) + 
			np.array(r9scram) + np.array(r11scram)) / 6
evenCat = (np.array(r2cat) + np.array(r4cat) + 
		   np.array(r6cat) + np.array(r8cat) + 
		   np.array(r10cat) + np.array(r12cat)) / 6
oddCat = (np.array(r1cat) + np.array(r3cat) + 
		  np.array(r5cat) + np.array(r7cat) + 
		  np.array(r9cat) + np.array(r11cat)) / 6
evenShoe = (np.array(r2shoe) + np.array(r4shoe) +
		    np.array(r6shoe) + np.array(r8shoe) + 
		    np.array(r10shoe) + np.array(r12shoe)) / 6
oddShoe = (np.array(r1shoe) + np.array(r3shoe) + 
		   np.array(r5shoe) + np.array(r7shoe) + 
		   np.array(r9shoe) + np.array(r11shoe)) / 6
evenBottle = (np.array(r2bottle) + np.array(r4bottle) + 
			  np.array(r6bottle) + np.array(r8bottle) + 
			  np.array(r10bottle) + np.array(r12bottle)) / 6
oddBottle = (np.array(r1bottle) + np.array(r3bottle) + 
			 np.array(r5bottle) + np.array(r7bottle) + 
			 np.array(r9bottle) + np.array(r11bottle)) / 6
evenScissor = (np.array(r2scissor) + np.array(r4scissor) + 
			   np.array(r6scissor) + np.array(r8scissor) + 
			   np.array(r10scissor) + np.array(r12scissor)) / 6
oddScissor = (np.array(r1scissor) + np.array(r3scissor) + 
			  np.array(r5scissor) + np.array(r7scissor) + 
			  np.array(r9scissor) + np.array(r11scissor)) / 6
evenChair = (np.array(r2chair) + np.array(r4chair) + 
			 np.array(r6chair) + np.array(r8chair) + 
			 np.array(r10chair) + np.array(r12chair)) / 6
oddChair = (np.array(r1chair) + np.array(r3chair) + 
			np.array(r5chair) + np.array(r7chair) + 
			np.array(r9chair) + np.array(r11chair)) / 6
evenFace = (np.array(r2face) + np.array(r4face) + 
			np.array(r6face) + np.array(r8face) + 
			np.array(r10face) + np.array(r12face)) / 6
oddFace = (np.array(r1face) + np.array(r3face) + 
		   np.array(r5face) + np.array(r7face) + 
		   np.array(r9face) + np.array(r11face)) / 6

evenRun = [evenBottle, evenCat, evenChair, evenFace,
		   evenHouse, evenScissor, evenScram, evenShoe]
oddRun = [oddBottle, oddCat, oddChair, oddFace, 
		  oddHouse, oddScissor, oddScram, oddShoe]

all_results = [0.0] * 64
all_results = np.reshape(all_results, (8, 8))
for i in range(8):
	for j in range(8):
		all_results[i, j] = np.corrcoef(evenRun[i], oddRun[j])[0, 1]

object_list = ["bottle", "cat", "chair", "face",
			   "house", "scissor", "scram", "shoe"]

fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=all_results.round(4), colLabels=object_list,
				  rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.3, 0.85, "Correlation of TSA brain images of %s" % subid,
		 weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "subtracted_correlation_table_%s.png" % subid)
plt.close()