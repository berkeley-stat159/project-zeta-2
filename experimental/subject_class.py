from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import nibabel as nib


class subject(object):
    """try to organize data based on subject ex sub001"""
    # deal with path problem

    def __init__(self, sub):
        # subject info ex: 'sub001'
        self.sub_id = sub

        # deal with path problem
        root_path = "."
        pattern = re.compile(r'[/\\]')
        cwd = os.getcwd()
        check_path = pattern.split(cwd)
        if "project" not in check_path[-1]:
            root_path = ".."

        # check if the input is valid
        valid_sub = ["sub001", "sub002", "sub003", "sub004", "sub005", "sub006"]
        assert self.sub_id in valid_sub, "%s is not a valid input" % self.sub_id

        # BOLD folder for this subject
        sub_BOLD_path = os.path.join(root_path, "data", "ds105", "%s" % self.sub_id, "BOLD")

        # anatomy folder for this subject
        sub_anatomy_file = os.path.join(root_path, "data", "ds105", "%s" % self.sub_id, "anatomy",
                                        "highres001_brain.nii.gz")

        # runfile_list: ['task001_run001', 'task001_run002'......]
        runfile_list = ['task001_run' + i + '.txt' for i in
                        ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012']]
        runlist = ['run' + i for i in
                   ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012']]
        # deal with sub005 which has only 11 run results
        if self.sub_id == "sub005":
            runfile_list = runfile_list[:-1]
            runlist = runlist[:-1]

        # TR info:
        self.TR = 2.5

        # load high resolution brain structure for this subject
        self.brain_img = nib.load(sub_anatomy_file)

        # load all bold image file for this subject
        self.run_img_result = {}
        for i in runlist:
            img_file_path = os.path.join(sub_BOLD_path, "task001_%s" % i, "bold.nii.gz")
            self.run_img_result[self.sub_id + '_' + i] = nib.load(img_file_path)

        # ordered run keys:
        ordered_run_keys = self.run_img_result.keys()
        ordered_run_keys.sort()
        self.run_keys = ordered_run_keys

        # shape of the BOLD data:
        self.BOLD_shape = self.run_img_result[self.run_keys[1]].shape

        # conditions setting: which condition is for which category
        condition_key_path = os.path.join(root_path, "data", "ds105", "models", "model001", "condition_key.txt")
        condition_key_file = open(condition_key_path)
        condition_list = condition_key_file.readlines()
        condition = re.compile(r'(cond\d+) (\w+)')
        result = {}
        for item in condition_list:
            for match in condition.finditer(item):
                result[match.group(1)] = match.group(2)
        self.condition_key = result

        # condition files for each objects for each run
        sub_condition_path = os.path.join(root_path, "data", "ds105", "%s" % self.sub_id, "model", "model001",
                                          "onsets")
        self.conditions = {}
        for i in runfile_list:
            for j in self.condition_key.keys():
                self.conditions[i[8:14] + '-' + self.condition_key[j]] = os.path.join(sub_condition_path, i[:-4],
                                                                                      j + '.txt')
