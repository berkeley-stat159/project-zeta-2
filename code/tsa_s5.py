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
subid = "sub005"

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

brain1 = sub_data["sub005_run001"]
x1 = copy.deepcopy(sub_data)
maskedDict, volDict = msk.generateMaskedBrain(x1)
s5r1Masked = maskedDict["sub005_run001"]
s5r1Vol = volDict["sub005_run001"]

brain2 = sub_data["sub005_run002"]
s5r2Masked = maskedDict["sub005_run002"]
s5r2Vol = volDict["sub005_run002"]

brain3 = sub_data["sub005_run003"]
s5r3Masked = maskedDict["sub005_run003"]
s5r3Vol = volDict["sub005_run003"]

brain4 = sub_data["sub005_run004"]
s5r4Masked = maskedDict["sub005_run004"]
s5r4Vol = volDict["sub005_run004"]

brain5 = sub_data["sub005_run005"]
s5r5Masked = maskedDict["sub005_run005"]
s5r5Vol = volDict["sub005_run005"]

brain6 = sub_data["sub005_run006"]
s5r6Masked = maskedDict["sub005_run006"]
s5r6Vol = volDict["sub005_run006"]

brain7 = sub_data["sub005_run007"]
s5r7Masked = maskedDict["sub005_run007"]
s5r7Vol = volDict["sub005_run007"]

brain8 = sub_data["sub005_run008"]
s5r8Masked = maskedDict["sub005_run008"]
s5r8Vol = volDict["sub005_run008"]

brain9 = sub_data["sub005_run009"]
s5r9Masked = maskedDict["sub005_run009"]
s5r9Vol = volDict["sub005_run009"]

brain10 = sub_data["sub005_run010"]
s5r10Masked = maskedDict["sub005_run010"]
s5r10Vol = volDict["sub005_run010"]

brain11 = sub_data["sub005_run011"]
s5r11Masked = maskedDict["sub005_run011"]
s5r11Vol = volDict["sub005_run011"]


# Focus on z = 31:36, y = 25 to 50, all of x

# brain = brain[:, 25:50, 32, :]
# s1r1Masked = s1r1Masked[:, 25:50, 32]
# brain = brain[s1r1Masked, :]

brains5r1 = brain1[:, 25:50, 31:36, :]
s5r1Masked = s5r1Masked[:, 25:50, 31:36]
brains5r1 = brains5r1[s5r1Masked, :]

brains5r2 = brain2[:, 25:50, 31:36, :]
s5r2Masked = s5r2Masked[:, 25:50, 31:36]
brains5r2 = brains5r2[s5r2Masked, :]

brains5r3 = brain3[:, 25:50, 31:36, :]
s5r3Masked = s5r3Masked[:, 25:50, 31:36]
brains5r3 = brains5r3[s5r3Masked, :]

brains5r4 = brain4[:, 25:50, 31:36, :]
s5r4Masked = s5r4Masked[:, 25:50, 31:36]
brains5r4 = brains5r4[s5r4Masked, :]

brains5r5 = brain5[:, 25:50, 31:36, :]
s5r5Masked = s5r5Masked[:, 25:50, 31:36]
brains5r5 = brains5r5[s5r5Masked, :]

brains5r6 = brain6[:, 25:50, 31:36, :]
s5r6Masked = s5r6Masked[:, 25:50, 31:36]
brains5r6 = brains5r6[s5r6Masked, :]

brains5r7 = brain7[:, 25:50, 31:36, :]
s5r7Masked = s5r7Masked[:, 25:50, 31:36]
brains5r7 = brains5r7[s5r7Masked, :]

brains5r8 = brain8[:, 25:50, 31:36, :]
s5r8Masked = s5r8Masked[:, 25:50, 31:36]
brains5r8 = brains5r8[s5r8Masked, :]

brains5r9 = brain9[:, 25:50, 31:36, :]
s5r9Masked = s5r9Masked[:, 25:50, 31:36]
brains5r9 = brains5r9[s5r9Masked, :]

brains5r10 = brain10[:, 25:50, 31:36, :]
s5r10Masked = s5r10Masked[:, 25:50, 31:36]
brains5r10 = brains5r10[s5r10Masked, :]

brains5r11 = brain11[:, 25:50, 31:36, :]
s5r11Masked = s5r11Masked[:, 25:50, 31:36]
brains5r11 = brains5r11[s5r11Masked, :]



arr1 = [0.0] * 121
for i in range(121):
	arr1[i] = np.mean(brains5r1[:, i])

r1house = arr1[93:103]
r1scram = arr1[107:117]
r1cat = arr1[21:31]
r1shoe = arr1[35:45]
r1bottle = arr1[78:88]
r1scissor = arr1[64:74]
r1chair = arr1[50:60]
r1face = arr1[6:16]


arr2 = [0.0] * 121
for i in range(121):
	arr2[i] = np.mean(brains5r2[:, i])

r2house = arr2[6:16]
r2scram = arr2[107:117]
r2cat = arr2[93:103]
r2shoe = arr2[78:88]
r2bottle = arr2[35:45]
r2scissor = arr2[21:31]
r2chair = arr2[64:74]
r2face = arr2[50:60]


arr3 = [0.0] * 121
for i in range(121):
	arr3[i] = np.mean(brains5r3[:, i])

r3house = arr3[78:88]
r3scram = arr3[21:31]
r3cat = arr3[6:16]
r3shoe = arr3[64:74]
r3bottle = arr3[50:60]
r3scissor = arr3[107:117]
r3chair = arr3[35:45]
r3face = arr3[93:103]


arr4 = [0.0] * 121
for i in range(121):
	arr4[i] = np.mean(brains5r4[:, i])

r4house = arr4[107:117]
r4scram = arr4[21:31]
r4cat = arr4[78:88]
r4shoe = arr4[50:60]
r4bottle = arr4[64:74]
r4scissor = arr4[35:45]
r4chair = arr4[93:103]
r4face = arr4[6:16]


arr5 = [0.0] * 121
for i in range(121):
	arr5[i] = np.mean(brains5r5[:, i])

r5house = arr5[50:60]
r5scram = arr5[64:74]
r5cat = arr5[35:45]
r5shoe = arr5[78:88]
r5bottle = arr5[93:103]
r5scissor = arr5[107:117]
r5chair = arr5[21:31]
r5face = arr5[6:16]


arr6 = [0.0] * 121
for i in range(121):
	arr6[i] = np.mean(brains5r6[:, i])

r6house = arr6[6:16]
r6scram = arr6[21:31]
r6cat = arr6[78:88]
r6shoe = arr6[50:60]
r6bottle = arr6[93:103]
r6scissor = arr6[107:117]
r6chair = arr6[64:74]
r6face = arr6[35:45]


arr7 = [0.0] * 121
for i in range(121):
	arr7[i] = np.mean(brains5r7[:, i])

r7house = arr7[78:88]
r7scram = arr7[64:74]
r7cat = arr7[93:103]
r7shoe = arr7[50:60]
r7bottle = arr7[107:117]
r7scissor = arr7[35:45]
r7chair = arr7[21:31]
r7face = arr7[6:16]


arr8 = [0.0] * 121
for i in range(121):
	arr8[i] = np.mean(brains5r8[:, i])

r8house = arr8[50:60]
r8scram = arr8[35:45]
r8cat = arr8[21:31]
r8shoe = arr8[93:103]
r8bottle = arr8[107:117]
r8scissor = arr8[64:74]
r8chair = arr8[78:88]
r8face = arr8[6:16]


arr9 = [0.0] * 121
for i in range(121):
	arr9[i] = np.mean(brains5r9[:, i])

r9house = arr9[21:31]
r9scram = arr9[50:60]
r9cat = arr9[93:103]
r9shoe = arr9[78:88]
r9bottle = arr9[6:16]
r9scissor = arr9[107:117]
r9chair = arr9[35:45]
r9face = arr9[64:74]


arr10 = [0.0] * 121
for i in range(121):
	arr10[i] = np.mean(brains5r10[:, i])

r10house = arr10[21:31]
r10scram = arr10[78:88]
r10cat = arr10[50:60]
r10shoe = arr10[6:16]
r10bottle = arr10[93:103]
r10scissor = arr10[107:117]
r10chair = arr10[35:45]
r10face = arr10[64:74]


arr11 = [0.0] * 121
for i in range(121):
	arr11[i] = np.mean(brains5r11[:, i])

r11house = arr11[64:74]
r11scram = arr11[78:88]
r11cat = arr11[35:45]
r11shoe = arr11[50:60]
r11bottle = arr11[93:103]
r11scissor = arr11[6:16]
r11chair = arr11[107:117]
r11face = arr11[21:31]


evenHouse = (np.array(r2house) + np.array(r4house) + np.array(r6house) + np.array(r8house) + np.array(r10house)) / 5
oddHouse = (np.array(r1house) + np.array(r3house) + np.array(r5house) + np.array(r7house) + np.array(r9house) + np.array(r11house)) / 6
evenScram = (np.array(r2scram) +  np.array(r4scram) + np.array(r6scram) + np.array(r8scram) + np.array(r10scram)) / 5
oddScram = (np.array(r1scram) + np.array(r3scram) + np.array(r5scram) + np.array(r7scram) + np.array(r9scram) + np.array(r11scram)) / 6
evenCat = (np.array(r2cat) + np.array(r4cat) + np.array(r6cat) + np.array(r8cat) + np.array(r10cat)) / 5
oddCat = (np.array(r1cat) + np.array(r3cat) + np.array(r5cat) + np.array(r7cat) + np.array(r9cat) + np.array(r11cat)) / 6
evenShoe = (np.array(r2shoe) + np.array(r4shoe) + np.array(r6shoe) + np.array(r8shoe) + np.array(r10shoe)) / 5
oddShoe = (np.array(r1shoe) + np.array(r3shoe) + np.array(r5shoe) + np.array(r7shoe) + np.array(r9shoe) + np.array(r11shoe)) / 6
evenBottle = (np.array(r2bottle) + np.array(r4bottle) + np.array(r6bottle) + np.array(r8bottle) + np.array(r10bottle)) / 5
oddBottle = (np.array(r1bottle) + np.array(r3bottle) + np.array(r5bottle) + np.array(r7bottle) + np.array(r9bottle) + np.array(r11bottle)) / 6
evenScissor = (np.array(r2scissor) + np.array(r4scissor) + np.array(r6scissor) + np.array(r8scissor) + np.array(r10scissor)) / 5
oddScissor = (np.array(r1scissor) + np.array(r3scissor) + np.array(r5scissor) + np.array(r7scissor) + np.array(r9scissor) + np.array(r11scissor)) / 6
evenChair = (np.array(r2chair) + np.array(r4chair) + np.array(r6chair) + np.array(r8chair) + np.array(r10chair)) / 5
oddChair = (np.array(r1chair) + np.array(r3chair) + np.array(r5chair) + np.array(r7chair) + np.array(r9chair) + np.array(r11chair)) / 6
evenFace = (np.array(r2face) + np.array(r4face) + np.array(r6face) + np.array(r8face) + np.array(r10face)) / 5
oddFace = (np.array(r1face) + np.array(r3face) + np.array(r5face) + np.array(r7face) + np.array(r9face) + np.array(r11face)) / 6

evenRun = [evenBottle, evenCat, evenChair, evenFace, evenHouse, evenScissor, evenScram, evenShoe]
oddRun = [oddBottle, oddCat, oddChair, oddFace, oddHouse, oddScissor, oddScram, oddShoe]

all_results = [0.0] * 64
all_results = np.reshape(all_results, (8, 8))
for i in range(8):
	for j in range(8):
		all_results[i, j] = np.corrcoef(evenRun[i], oddRun[j])[0, 1]

print(all_results)