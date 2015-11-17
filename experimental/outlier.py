# remove data outliers from the data by using rms_diff and extend indices
def remove_data_outlier (img_dict):
    result = {}
    outlier_index = {}
    for key, imgresult in img_dict.iteritems():
        result[key] = imgresult.get_data()
        rms_diff = vol_rms_diff(result[key])
        rms_outlier_indices, rms_thresh = iqr_outliers(rms_diff)
        rms_extend_indices = extend_diff_outliers(rms_outlier_indices)
        outlier_index[key] = rms_extend_indices
        result[key] = np.delete(result[key], outlier_index[key], axis = 3)
    return result, outlier_index

