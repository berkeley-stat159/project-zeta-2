from __future__ import print_function, division
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

class subject(object):
    """try to organize data based on subject ex 'sub001'"""
    def __init__(self,sub):
        # subject info ex: 'sub001'
        self.sub_id = sub 

        # BOLD folder for this subject
        sub_BOLD_path = "../data/ds105/%s/BOLD/" %self.sub_id

        # anatomy folder for this subject
        sub_anatomy_file = "../data/ds105/%s/anatomy/highres001_brain.nii.gz" %self.sub_id
        
        # runfile_list: ['task001_run001', 'task001_run002'......]
        runfile_list = ['task001_run'+ i+ '.txt' for i in ['001','002','003','004','005','006','007','008','009','010','011','012']]
        runlist = ['run'+ i for i in ['001','002','003','004','005','006','007','008','009','010','011','012']]
        
        # TR info:
        self.TR = 2.5
        
        # load high resolution brain structure for this subject
        self.brain_img = nib.load(sub_anatomy_file)
        
        # load all bold image file for this subject
        self.runresult = {}
        for i in runlist:
            self.runresult[self.sub_id + '_' + i] = nib.load(sub_BOLD_path+'task001_'+i+'/bold.nii.gz')
        
        # all run keys:
        self.run_keys = self.runresult.keys()

        # shape of the BOLD data:
        self.BOLD_shape = self.runresult[self.run_keys[1]].shape
        
        # conditions setting: trying to get a list for all condition files.
        # still in progress!!!!
        self.conditions = open("../data/ds105/models/model001/condition_key.txt")
                
        
