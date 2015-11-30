"""trying to develop a function to get the convulsion of the time course"""
# noinspection PyUnresolvedReferences

from __future__ import print_function, division
import scipy.stats
from scipy.stats import gamma
import numpy as np

# hrf function from lecture
def hrf(tr_times):
    """ Return values for HRF at given times """
    # Gamma pdf for the peak
    peak_values = gamma.pdf(tr_times, 6)
    # Gamma pdf for the undershoot
    undershoot_values = gamma.pdf(tr_times, 12)
    # Combine them
    values = peak_values - 0.35 * undershoot_values
    # Scale max to 0.6
    return values / np.max(values) * 0.6


# convolution and deal with overflow
def convolution(neural, hrf_at_trs):
    convolved = np.convolve(neural, hrf_at_trs)
    convolved = convolved[:-(len(hrf_at_trs)-1)]
    return convolved

# get all convolved result and save in a dictionary
def get_all_convolved (dictionary_of_all_neural, hrf_at_trs, path ="."):
    result = {}
    dict_key = dictionary_of_all_neural.keys()
    dict_key.sort()
    for i in dict_key:
        convolved = convolution(dictionary_of_all_neural[i][0], hrf_at_trs)
        result[i] = convolved
        np.savetxt(path + "convolved_%s.txt" % i, convolved)
        print ("convolution for %s: complete" % i)
    return result

# remove outlier in convolved results
def remove_outlier (subid ,convolsion_data_dict, outlier_directory, axis=0):
    """
    Parameters
    ----------
    subid = subject ID
    convolsion_data_dict: the convolsion dictionary
    outlier_directory: outlier dictionary
    axis: in this case, axis=0

    Returns
    -------
    dictionary of convolsion result without outlier
    """
    result = {}
    for i in convolsion_data_dict.keys():
        result[i] = np.delete(convolsion_data_dict[i], outlier_directory[subid + '_' + i[:6]], axis)
    return result