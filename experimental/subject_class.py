from __future__ import print_function, division
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

class subject(object):
    """try to organize data based on subject ex sub001"""
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
        self.run_img_result = {}
        for i in runlist:
            self.run_img_result[self.sub_id + '_' + i] = nib.load(sub_BOLD_path+'task001_'+i+'/bold.nii.gz')
        
        # all run keys:
        self.run_keys = self.run_img_result.keys()

        # shape of the BOLD data:
        self.BOLD_shape = self.run_img_result[self.run_keys[1]].shape
        
        # conditions setting: which condition is for which category
        self.condition_key_file = open("../data/ds105/models/model001/condition_key.txt")
        condition_list = self.condition_key_file.readlines()
        condition = re.compile(r'(cond\d+) (\w+)')
        result = {}
        for item in condition_list:
            for match in condition.finditer(item):
                result[match.group(1)] = match.group(2)
        self.condition_key = result
        
        # condition files for each objects for each run
        sub_condition_path = "../data/ds105/%s/model/model001/onsets/" %self.sub_id
        self.conditions = {}
        for i in runfile_list:
            for j in self.condition_key.keys():
                self.conditions[i[8:14]+'-'+self.condition_key[j]] = sub_condition_path + i[:-4]+'/'+j+'.txt'
                   
                

