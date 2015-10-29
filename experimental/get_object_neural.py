
def get_object_neural(sub_ID ,condition_dict, object_name, TR, n_vox, check = 0, ):
    """
    get object neural array for specific object from all runs, odd runs or even runs
    
    parameters
    ----------
    condition_dict: dictionary of all condition files
    object_name: desired object name: 'house','scrambledpix','cat','shoe','bottle','scissors','chair','face'
    TR: TR for fMRI
    n_vox: time course of fMRI
    check: 1= odd runs, 2=even runs, others = all runs
    
    output
    -------
    a dictionary of run name : (neural array, path of the bold image) for that run
    ex:
    
    {
    'run001-bottle-neural': (array([ 0.,  0.,  0.,  0.,  0., ...]), bold path)
    'run002-bottle-neural': (array([ 0.,  0.,  0.,  0.,  0., ...]), bold path)
    }
    
    
    """
    
    condition_dict_key = condition_dict.keys()
    result = {}
    for i in condition_dict_key:
        if check == 1:
            if object_name in i:
                if int(i[3:6])%2 ==1:
                    result[i+'-neural'] = (events2neural(condition_dict[i], TR, n_vox), "../data/ds105/%s/BOLD/task001_"% sub_ID + i[:6]+"/bold.nii.gz")
        elif check == 2:
            if object_name in i: 
                if int(i[3:6])%2 ==0:
                    result[i+'-neural'] = (events2neural(condition_dict[i], TR, n_vox), "../data/ds105/%s/BOLD/task001_"% sub_ID + i[:6]+"/bold.nii.gz")
        else:
            if object_name in i:
                result[i+'-neural'] = (events2neural(condition_dict[i], TR, n_vox), "../data/ds105/%s/BOLD/task001_"%sub_ID + i[:6]+"/bold.nii.gz")
    
    return result


