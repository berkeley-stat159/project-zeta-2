import numpy as np
import os
from utils import convolution as convol
from utils import get_object_neural as neural
from utils import subject_class as sc
import statsmodels.api as sm
import matplotlib.pyplot as plt

base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")
figure_path = os.path.join(base_path, "code", "images", "")
file_path = os.path.join(base_path, "code", "txt", "")


sub1 = sc.subject("sub001")
sub1_neural = neural.get_object_neural(sub1.sub_id ,sub1.conditions, sub1.TR, sub1.BOLD_shape[-1])
tr_times = np.arange(0, 30, sub1.TR)
hrf_at_trs = convol.hrf(tr_times)
object_list = ["bottle", "cat", "chair", "face", "house", "scissors", "scrambledpix", "shoe"]
sub1_convolved = convol.get_all_convolved(sub1_neural, hrf_at_trs, file_path)

s1run1 = np.array([0.0] * 121)
for key, data in sub1_convolved.iteritems():
    x = file_path + "convolved_%s.txt" % key, data
    y = x[1]
    s1run1 += y

fig = plt.figure(figsize = (12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(s1run1, lags = 20, ax = ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(s1run1, lags = 20, ax = ax2)
#plt.show()
plt.savefig("sub001_run001_corrFunc.png")
plt.clf()
plt.close()

s1r1_arimaFit = sm.tsa.ARIMA(s1run1, (2, 0, 2)).fit()

plt.gca().set_color_cycle(['red', 'blue'])
plt.plot(s1run1)
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
# Based on the autocorrelation and partial autocorrelation of the residuals,
# they do not have significant lags. Thus an ARIMA (2, 0, 2) model is good
# at representing the time series.

