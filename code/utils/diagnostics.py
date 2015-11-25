""" Diagnostics.py

A collection of utility functions for diagnostics on FMRI data

See test_* functions in this directory for nose tests
"""
# import important library

from __future__ import division, print_function, absolute_import
import numpy as np

def vol_std(data):
    """ Return standard deviation across voxels for 4D array `data`

    Parameters
    ----------
    data : 4D array
        4D array from FMRI run with last axis indexing volumes.  Call the shape
        of this array (M, N, P, T) where T is the number of volumes.

    Returns
    -------
    std_values : array shape (T,)
        One dimensonal array where ``std_values[i]`` gives the standard
        deviation of all voxels contained in ``data[..., i]``.
    """

    result = [0] * data.shape[-1]
    for i in range(len(result)):
        result[i] = np.std(data[:,:,:,i])
    return result


def iqr_outliers(arr_1d, iqr_scale=1.5):
    """ Return indices of outliers identified by interquartile range

    Parameters
    ----------
    arr_1d : 1D array
        One-dimensional numpy array, from which we will identify outlier
        values.
    iqr_scale : float, optional
        Scaling for IQR to set low and high thresholds.  Low threshold is given
        by 25th centile value minus ``iqr_scale * IQR``, and high threshold id
        given by 75 centile value plus ``iqr_scale * IQR``.

    Returns
    -------
    outlier_indices : array
        Array containing indices in `arr_1d` that contain outlier values.
    lo_hi_thresh : tuple
        Tuple containing 2 values (low threshold, high thresold) as described
        above.
    """
    # Hint : np.lookfor('centile')
    # Hint : np.lookfor('nonzero')
    
    # get parameters
    IQR = np.percentile(arr_1d, 75) - np.percentile(arr_1d, 25)
    lo_thresh = np.percentile(arr_1d, 25) - IQR * iqr_scale
    hi_thresh = np.percentile(arr_1d, 75) + IQR * iqr_scale
    
    # find outlier_indeces
    outlier_indices = []
    for index in range(len(arr_1d)):
        if arr_1d[index] < lo_thresh or arr_1d[index] > hi_thresh:
            outlier_indices.append(index)
    return (outlier_indices, (lo_thresh, hi_thresh))
    

def vol_rms_diff(arr_4d):
    """ Return root mean square of differences between sequential volumes

    Parameters
    ----------
    data : 4D array
        4D array from FMRI run with last axis indexing volumes.  Call the shape
        of this array (M, N, P, T) where T is the number of volumes.

    Returns
    -------
    rms_values : array shape (T-1,)
        One dimensonal array where ``rms_values[i]`` gives the square root of
        the mean (across voxels) of the squared difference between volume i and
        volume i + 1.
    """
    
    time_length = arr_4d.shape[-1]
    diff_vol = []
    for item in range(time_length -1):
        diff_vol.append(arr_4d[...,item+1] - arr_4d[...,item])
    rms_values = []
    for i in diff_vol:
        rms_values.append(np.sqrt(np.mean(i**2)))
   
    return rms_values


def extend_diff_outliers(diff_indices):
    """ Extend difference-based outlier indices `diff_indices` by pairing

    Parameters
    ----------
    diff_indices : array
        Array of indices of differences that have been detected as outliers.  A
        difference index of ``i`` refers to the difference between volume ``i``
        and volume ``i + 1``.

    Returns
    -------
    extended_indices : array
        Array where each index ``j`` in `diff_indices has been replaced by two
        indices, ``j`` and ``j+1``, unless ``j+1`` is present in
        ``diff_indices``.  For example, if the input was ``[3, 7, 8, 12, 20]``,
        ``[3, 4, 7, 8, 9, 12, 13, 20, 21]``.
    """

    extended_indices = []
    for item in diff_indices:
        if item not in extended_indices:
            extended_indices.append(item)
        if (item+1) not in extended_indices:
            extended_indices.append(item+1)
    
    return extended_indices


