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
subid = "sub001"

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

brain = sub_data["sub001_run001"]
x = copy.deepcopy(sub_data)
maskedDict, volDict = msk.generateMaskedBrain(x)
s1r1Masked = maskedDict["sub001_run001"]
s1r1Vol = volDict["sub001_run001"]

brain = brain[:, 25:50, 32, :]
s1r1Masked = s1r1Masked[:, 25:50, 32]
brain = brain[s1r1Masked, :]

arr = [0.0] * 121
for i in range(121):
	arr[i] = np.mean(brain[:, i])

fig = plt.figure(figsize = (12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(arr, lags = 20, ax = ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(arr, lags = 20, ax = ax2)
#plt.show()
plt.savefig("sub001_run001_corrFunc.png")
plt.clf()
plt.close()

s1r1_arimaFit = sm.tsa.ARIMA(arr, (2, 0, 0)).fit()

plt.gca().set_color_cycle(['red', 'blue'])
plt.plot(arr)
plt.plot(s1r1_arimaFit.fittedvalues)
plt.legend(['Actual', 'Fitted'], loc='upper left')
plt.title("Actual vs Fitted Time Series")
plt.savefig("sub001_run001_TimeSeries.png")
plt.clf()
plt.close()
#print("Printing ARIMA parameters")
#print(s1r1_arimaFit.params)

# Plot residuals of the fit here
plt.plot(s1r1_arimaFit.resid)
plt.title("Residuals of ARIMA Model on Run 1")
plt.savefig("sub001_run001_residFit.png")
plt.clf()
plt.close()

# print("P-Value for independence of residuals. If greater than 0.05, model is correct")
# print(sm.stats.diagnostic.acorr_ljungbox(s1r1_arimaFit.resid, lags = 20))[1]

fig = plt.figure(figsize = (12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(s1r1_arimaFit.resid, lags = 20, ax = ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(s1r1_arimaFit.resid, lags = 20, ax = ax2)
#plt.show()
plt.savefig("sub001_run001_residcorrFunc.png")
plt.clf()
plt.close()

# Focus on z = 32, y = 25 to 50, all of x

# The sub_data is a dictionary for all 4D runs of this subject
# The key for this dictionary are:
# sub001_run001
# sub001_run002
# sub001_run003
# sub001_run004
# sub001_run005
# sub001_run006
# sub001_run007
# sub001_run008
# sub001_run009
# sub001_run010
# sub001_run011
# sub001_run012
# These are the raw data, so, they all have the same 4D dimension