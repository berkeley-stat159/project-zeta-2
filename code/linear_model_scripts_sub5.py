# Goal for this scripts:
#
# Perform linear regression and analyze the similarity in terms of the activated brain area when recognizing different
# objects in odd and even runs of subject 1


# Load required function and modules:
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
from utils import smooth as sm
from utils import linear_model as lm
from utils import maskfunc as msk
from utils import affine
import copy


# important path:
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")
# where to store figures
figure_path = os.path.join(base_path, "code", "images", "")
# where to store txt files
file_path = os.path.join(base_path, "code", "txt", "")


# help to make directory to save figures and txt files
# if figure folder doesn't exist -> make it
if not os.path.exists(figure_path):
    os.makedirs(figure_path)
# if txt folder doesn't exist -> make it
if not os.path.exists(file_path):
    os.makedirs(file_path)


# color display:
# list of all objects in this study in alphabetical order
object_list = ["bottle", "cat", "chair", "face", "house", "scissors", "scrambledpix", "shoe"]
# assign color for task time course for each object
color_list_s = ["b", "g", "r", "c", "m", "y", "k", "sienna"]
match_color_s = dict(zip(object_list, color_list_s))
# assign color for convolved result for each object
color_list_c = ["royalblue", "darksage", "tomato", "cadetblue", "orchid", "goldenrod", "dimgrey", "sandybrown"]
match_color_c = dict(zip(object_list, color_list_c))
# color for showing beta values
nice_cmap_values = np.loadtxt(file_path + 'actc.txt')
nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')


# assign object parameter number: each object has a iterable number
match_para = dict(zip(object_list, range(8)))


# check slice number:
# this is the specific slice we use to run 2D correlation
slice_number = 35


# separator for better report display
sec_separator = '#' * 80
separator = "-" * 80


# which subject to work on?
subid = "sub005"


# work on results from this subject:
################################### START #####################################
print (sec_separator)
print ("Project-Zeta: use linear regression to study ds105 dataset")
print (separator)
print ("Focus on %s for the analysis" % subid)
print (sec_separator)
print ("Progress: Clean up data")
print (separator)
# load important data for this subject by using subject_class
sub = sc.subject(subid)

# get image files of this subject:
sub_img = sub.run_img_result

# get run numbers of this subject:
run_num = len(sub.run_keys)

# report keys of all images:
print ("Import %s images" % subid)
print (separator)
print ("These images are imported:")
img_key = sub_img.keys()
img_key = sorted(img_key)
for i in img_key:
    print (i)
# report how many runs in this subject
print ("There are %d runs for %s" % (run_num, subid))
print (separator)


# get data for those figures
print ("Get data from images...")
sub_data = {}
for key, img in sub_img.items():
    sub_data[key] = img.get_data()
print ("Complete!")
print (separator)


# use rms_diff to check outlier for all runs of this subject
print ("Analyze outliers in these runs:")
for key, data in sub_data.items():
    rms_diff = diagnos.vol_rms_diff(data)
    # get outlier indices and the threshold for the outlier
    rms_outlier_indices, rms_thresh = diagnos.iqr_outliers(rms_diff)
    y_value2 = [rms_diff[i] for i in rms_outlier_indices]
    # create figures to show the outlier
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    ax.plot(rms_diff, label='rms')
    ax.plot([0, len(rms_diff)], [rms_thresh[1], rms_thresh[1]], "k--",\
    label='high threshold', color='m')
    ax.plot([0, len(rms_diff)], [rms_thresh[0], rms_thresh[0]], "k--",\
    label='low threshold', color='c')
    ax.plot(rms_outlier_indices, y_value2, 'o', color='g', label='outlier')
    # label the figure
    ax.set_xlabel('Scan time course')
    ax.set_ylabel('Volumne RMS difference')
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    fig.text(0.05, 0.9, 'Volume RMS Difference with Outliers for %s' % key, weight='bold')
    # save figure
    fig.savefig(figure_path + 'Volume_RMS_Difference_Outliers_%s.png' % key)
    # clear figure
    fig.clf()
# close pyplot window
plt.close()
# report
print ("Outlier analysis results are saved as figures!")
print (separator)


# remove outlier from images
sub_clean_img, outlier_index = outlier.remove_data_outlier(sub_img)
print ("Remove outlier:")
print ("outliers are removed from each run!")
print (sec_separator)

# run generate predicted bold signals:
print ("Progress: create predicted BOLD signals based on condition files")
# get general all tr times == 121*2.5 = about 300 s
# this is the x-axis to plot hemodynamic prediction
all_tr_times = np.arange(sub.BOLD_shape[-1]) * sub.TR

# the y-axis to plot hemodynamic prediction is the neural value from condition (on-off)
sub_neural = neural.get_object_neural(sub.sub_id, sub.conditions, sub.TR, sub.BOLD_shape[-1])

# report info for all run details
print ("The detailed run info for %s:" % subid)
neural_key = sub_neural.keys()
neural_key = sorted(neural_key)
for i in neural_key:
    print (i)
print (separator)


# get task time course for all runs -> save as images
print ("generate task time course images")
print (separator)
for run in range(1, run_num):
    # make plots to display task time course
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
    for item in object_list:
        check_key = "run0%02d-%s" % (run, item)
        ax.plot(all_tr_times, sub_neural[check_key][0], label="%s" % item, c=match_color_s[item])
    # make labels:
    ax.set_title("Task time course for %s-run0%02d" % (subid, run), weight='bold')
    ax.set_xlabel("Time course (second)")
    ax.set_ylabel("Task (Off = 0, On = 1)")
    ax.set_yticks([0, 1])
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    # save figure
    fig.savefig(figure_path + "Task_time_course_%s_run0%02d" % (subid, run))
    # clear figure
    fig.clf()
# close pyplot window
plt.close()
# report
print ("task time course images are saved!")
print (separator)


# assume true HRF starts at zero, and gets to zero sometime before 35 seconds.
tr_times = np.arange(0, 30, sub.TR)
hrf_at_trs = convol.hrf(tr_times)


# get convolution data for each objects in this run -> show figure for run001
print ("Work on convolution based on condition files:")
print (separator)
sub_convolved = convol.get_all_convolved(sub_neural, hrf_at_trs, file_path)
print ("convolution analysis for all runs is complete")
print (separator)

# save convolved data
for key, data in sub_convolved.items():
    np.savetxt(file_path + "convolved_%s.txt" % key, data)
print ("convolved results are saved as txt files")


# show relationship between task time course and bold signals
print ("Show relationship between task time course and predicted BOLD signals")
# get keys for each neural conditions
sub_neural_key = sub_neural.keys()
# sort key for better display
sub_neural_key = sorted(sub_neural_key)
# create figures
fig = plt.figure()
for run in range(1, run_num):
    ax = plt.subplot(111)
    ax2 = ax.twinx()
    figures = {}
    count = 0
    for item in object_list:
        # focus on one at a time:
        check_key = "run0%02d-%s" % (run, item)
        # perform convolution to generate estimated BOLD signals
        convolved = convol.convolution(sub_neural[check_key][0], hrf_at_trs)
        # plot the task time  course and the estimated BOLD signals in same plot
        # plot the estimated BOLD signals
        # plot the task time course
        figures["fig" + "%s" % str(count)] = ax.plot(all_tr_times, sub_neural[check_key][0], c=match_color_s[item], label="%s-task" % item)
        count += 1
        # plot estimated BOLD signal
        figures["fig" + "%s" % str(count)] = ax2.plot(all_tr_times, convolved, c=match_color_c[item], label="%s-BOLD" % item)
        count += 1
    # label this plot
    plt.subplots_adjust(left=0.1, right=0.6, bottom=0.1, top=0.85)
    plt.text(0.25, 1.05, "Hemodynamic prediction of %s-run0%02d" % (subid, run), weight='bold')
    ax.set_xlabel("Time course (second)")
    ax.set_ylabel("Task (Off = 0, On = 1)")
    ax.set_yticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8,  1.0])
    ax2.set_ylabel("Estimated BOLD signal")
    ax2.set_yticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # label legend
    total_figures = figures["fig0"]
    for i in range(1, len(figures)):
        total_figures += figures["fig" + "%s" % str(i)]
    labs = [fig.get_label() for fig in total_figures]
    ax.legend(total_figures, labs, bbox_to_anchor=(1.2, 1.0), loc=0, borderaxespad=0., fontsize=11)
    # save plot
    plt.savefig(figure_path + "%s_run0%02d_bold_prediction.png" % (subid, run))
    # clear plot
    plt.clf()
# close pyplot window
plt.close()
print (sec_separator)


# remove outlier from convolved results
print("Progress: clean up convolved results")
sub_convolved = convol.remove_outlier(sub.sub_id, sub_convolved, outlier_index)
print ("Outliers are removed from convolved results")
print (sec_separator)


# smooth the images:
print ("Progress: Smooth images")
# subject clean and smooth img == sub_cs_img
sub_cs_img = sm.smooth(sub_clean_img)
print ("Smooth images: Complete!")
print (sec_separator)

# get shape info of the images
print ("Progress: record shape information")
shape = {}
for key, img in sub_cs_img.items():
    shape[key] = img.shape
    print ("shape of %s = %s" % (key, shape[key]))
with open(file_path+'new_shape.json', 'a') as fp:
    json.dump(shape, fp)
print ("New shape info of images is recorded and saved as file")
print (sec_separator)


############################## Linear regression ##############################
print ("Let's run Linear regression")
print (separator)
# generate design matrix
print ("Progress: generate design matrix")
# generate design matrix for each runs
design_matrix = lm.batch_make_design(sub_cs_img, sub_convolved)
# check parameter numbers
parameters = design_matrix["%s_run001" % subid].shape[-1]
print ("parameter number: %d" % parameters)
print ("Design matrix generated")
print (separator)


# rescale design matrix
print ("Progress: rescale design matrix")
design_matrix = lm.batch_scale_matrix(design_matrix)
print ("Rescale design matrix: complete!")

# save scaled design matrix as figure
# plot scaled design matrix
fig = plt.figure(figsize=(8.0, 8.0))
for key, matrix in design_matrix.items():
    ax = plt.subplot(111)
    ax.imshow(matrix, aspect=0.1, interpolation="nearest", cmap="gray")
    # label this plot
    fig.text(0.15, 0.95, "scaled design matrix for %s" % key, weight='bold', fontsize=18)
    ax.set_xlabel("Parameters", fontsize=16)
    ax.set_xticklabels([])
    ax.set_ylabel("Scan time course", fontsize=16)
    # save plot
    plt.savefig(figure_path + "design_matrix_%s" % key)
    # clean plot
    plt.clf()
# close pyplot window
plt.close()
print ("Design matrices are saved as figures")
print (separator)

# use maskfunc to generate mask
print ("Progress: generate mask for brain images")
mask, mean_data = msk.generateMaskedBrain(sub_clean_img)
print ("Generate mask for brain images: complete!")

# save mask as figure
for key, each in mask.items():
    for i in range(1, 90):
        plt.subplot(9, 10, i)
        plt.imshow(each[:, :, i], interpolation="nearest", cmap="gray", alpha=0.5)
        # label plot
        ax = plt.gca()
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    # save plot
    plt.savefig(figure_path + "all_masks_for_%s.png" % key)
    # clear plot
    plt.clf()
# close pyplot window
plt.close()
print (separator)


# run linear regression to generate betas
# first step: use mask to get data and reshape to 2D
print ("Progress: Use mask to subset brain images")
sub_cs_mask_img = lm.apply_mask(sub_cs_img, mask)
sub_cs_mask_img_2d = lm.batch_convert_2d_based(sub_cs_mask_img, shape)
# sub1_cs_mask_img_2d = lm.batch_convert_2d(sub1_cs_mask_img)
print ("Use mask to subset brain images: complete!")
print (separator)

# second step: run linear regression to get betas:
print ("Progress: Run linear regression to get beta hat")
all_betas = {}
for key, img in sub_cs_mask_img_2d.items():
    #img_2d = np.reshape(img, (-1, img.shape[-1]))
    Y = img.T
    all_betas[key] = npl.pinv(design_matrix[key]).dot(Y)
print ("Getting betas from linear regression: complete!")
print (separator)

# third step: put betas back into it's original place:
print ("Save beta figures:")
beta_vols = {}
raw_beta_vols = {}
for key, betas in all_betas.items():
    # create 3D zeros to hold betas
    beta_vols[key] = np.zeros(shape[key][:-1] + (parameters,))
    # get the mask info
    check_mask = (mask[key] == 1)
    # fit betas back to 3D
    beta_vols[key][check_mask] = betas.T
    print ("betas of %s is fitted back to 3D!" % key)
    # save 3D betas in dictionary
    raw_beta_vols[key] = beta_vols[key]
    # get min and max of figure
    vmin = beta_vols[key][:, :, 21:70].min()
    vmax = beta_vols[key][:, :, 21:70].max()
    # clear the background
    beta_vols[key][~check_mask] = np.nan
    mean_data[key][~check_mask] = np.nan
    # plot betas
    fig = plt.figure(figsize=(8.0, 8.0))
    for item in object_list:
        # plot 50 pictures
        fig, axes = plt.subplots(nrows=5, ncols=10)
        lookat = 20
        for ax in axes.flat:
            # show plot from z= 21~70
            ax.imshow(mean_data[key][:, :, lookat], interpolation="nearest", cmap="gray", alpha=0.5)
            im = ax.imshow(beta_vols[key][:, :, lookat, match_para[item]], cmap=nice_cmap, alpha=0.5)
            # label the plot
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            lookat += 1
        # label the plot
        fig.subplots_adjust(bottom=0.2, hspace=0)
        fig.text(0.28, 0.9, "Brain area responding to %s in %s" % (item, subid), weight='bold')
        # color bar
        cbar_ax = fig.add_axes([0.15, 0.08, 0.7, 0.04])
        fig.colorbar(im, cax=cbar_ax, ticks=[], orientation='horizontal')
        fig.text(0.35, 0.15, "Relative responding intensity")
        fig.text(0.095, 0.09, "Low")
        fig.text(0.87, 0.09, "High")
        # save plot
        plt.savefig(figure_path + "betas_for_%s_%s.png" % (key, item))
        # clear plot
        plt.clf()
# close pyplot window
plt.close()
# report
print ("beta figures are generated!!")
print (sec_separator)


# analyze based on odd runs even runs using affine
print ("Progress: Use affine matrix to check brain position")
print ("print affine matrix for each images:")
affine_matrix = {}
for key, img in sub_img.items():
    affine_matrix[key] = img.affine
    print("%s :\n %s" % (key, img.affine))
# check if they all have same affine matrix
same_affine = True
check_matrix = affine_matrix["%s_run001" % subid]
for key, aff in affine_matrix.items():
    if aff.all() != check_matrix.all():
        same_affine = False
if same_affine:
    print ("They have the same affine matrix!")
else:
    print ("They don't have same affine matrix -> be careful about the brain position")
print (sec_separator)


############################## 2D correlation #################################

# Focus on 2D slice to run the analysis:
print ("Progress: Try 2D correlation")
print ("Focus on one slice: k = %d" % slice_number)
print (separator)
print ("Run correlation between run1_house, run2_house and run2_face")
# get 2D slice for run1 house
run1_house = raw_beta_vols["%s_run001" % subid][:, 25:50, slice_number, 5]
# save as plot
plt.imshow(run1_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run1_House" % subid)
plt.savefig(figure_path + "%s_run1_house.png" % subid)
plt.clf()
# get 2D slice of run2 house
run2_house = raw_beta_vols["%s_run002" % subid][:, 25:50, slice_number, 5]
# save as plot
plt.imshow(run2_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run2_House" % subid)
plt.savefig(figure_path + "%s_run2_house.png" % subid)
plt.clf()
# get 2D slice for run2 face
run2_face = raw_beta_vols["%s_run002" % subid][:, 25:50, slice_number, 4]
# save as plot
plt.imshow(run2_face, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run2_Face" % subid)
plt.savefig(figure_path + "%s_run2_face.png" % subid)
plt.close()


# put those 2D plots together
fig = plt.figure()
plt.subplot(1, 3, 1, xticks=[], yticks=[], xticklabels=[], yticklabels=[])
plt.imshow(run1_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("Sub%s_Run1_House" % subid[-1], weight='bold', fontsize=10)

plt.subplot(1, 3, 2, xticks=[], yticks=[])
plt.imshow(run2_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("Sub%s_Run2_House" % subid[-1], weight='bold', fontsize=10)

plt.subplot(1, 3, 3, xticks=[], yticks=[])
plt.imshow(run2_face, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("Sub%s_Run2_Face" % subid[-1], weight='bold', fontsize=10)

# label plot
fig.subplots_adjust(bottom=0.2, hspace=0)
cbar_ax = fig.add_axes([0.15, 0.08, 0.7, 0.04])
plt.colorbar(cax=cbar_ax, ticks=[], orientation='horizontal')
fig.text(0.35, 0.15, "Relative responding intensity")
fig.text(0.095, 0.09, "Low")
fig.text(0.87, 0.09, "High")

# save plot
plt.savefig(figure_path + "%s_run_figure_compile.png" % subid)
# close pyplot window
plt.close()
print ("plots for analysis are saved as figures")

print ("Progress: Run correlation coefficient")
# create a deepcopy of raw_beta_vols for correlation analysis:
raw_beta_vols_corr = copy.deepcopy(raw_beta_vols)

# flatten the 2D matrix
house1 = np.ravel(raw_beta_vols_corr["%s_run001" % subid][:, 25:50, slice_number, match_para["house"]])
house2 = np.ravel(raw_beta_vols_corr["%s_run001" % subid][:, 25:50, slice_number, match_para["house"]])
face2 = np.ravel(raw_beta_vols_corr["%s_run001" % subid][:, 25:50, slice_number, match_para["face"]])

# save flatten results for further analysis
np.savetxt(file_path + "%s_house1.txt" % subid, house1)
np.savetxt(file_path + "%s_house2.txt" % subid, house2)
np.savetxt(file_path + "%s_face2.txt" % subid, face2)

# change nan to 0 in the array
house1[np.isnan(house1)] = 0
house2[np.isnan(house2)] = 0
face2[np.isnan(face2)] = 0

# correlation coefficient study:
house1_house2 = np.corrcoef(house1, house2)
house1_face2 = np.corrcoef(house1, face2)
print ("%s run1 house vs run2 house: %s" % (subid, house1_house2))
print ("%s run1 house vs run2 face : %s" % (subid, house1_face2))
print (sec_separator)

# save individual 2D slice as txt for further analysis
print ("save 2D result for each object and each run individually as txt file")
for i in range(1, run_num+1):
    for item in object_list:
        temp = raw_beta_vols_corr["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
        np.savetxt(file_path + "%s_run0%02d_%s.txt" % (subid, i, item), np.ravel(temp))
print ("Complete!!")
print (sec_separator)


# analyze based on odd runs even runs
print ("Progress: prepare data to run correlation based on odd runs and even runs:")
print ("Take average of odd run / even run results to deal with impacts of variations between runs")

even_run = {}
odd_run = {}
even_count = 0
odd_count = 0
# add up even run results / odd run results and take mean for each groups
for item in object_list:
    even_run[item] = np.zeros_like(raw_beta_vols_corr["%s_run001" % subid][:, 25:50, slice_number, 5])
    odd_run[item] = np.zeros_like(raw_beta_vols_corr["%s_run001" % subid][:, 25:50, slice_number, 5])
    print ("make average of odd run results:")
    # add up odd run results
    for i in range(1, run_num+1, 2):
        temp = raw_beta_vols_corr["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
        temp[np.isnan(temp)] = 0
        odd_run[item] += temp
        odd_count += 1
        print("odd runs: %d-%s" % (i, item))
    print ("make average od even run results:")
    # take mean
    odd_run[item] = odd_run[item]/odd_count

    # add up even run results
    for i in range(2, run_num+1, 2):
        temp = raw_beta_vols_corr["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
        temp[np.isnan(temp)] = 0
        even_run[item] += temp
        even_count += 1
        print("even: %d, %s" % (i, item))
    # take mean
    even_run[item] = even_run[item]/even_count
print (separator)

# save odd run and even run results as txt file
print ("Progress: save flatten mean odd / even run results as txt files")
for key, fig in even_run.items():
    np.savetxt(file_path + "%s_even_%s.txt" % (subid, key), np.ravel(fig))
for key, fig in odd_run.items():
    np.savetxt(file_path + "%s_odd_%s.txt" % (subid, key), np.ravel(fig))
print ("odd run and even run results are saved as txt files!!!!!")
print (separator)


############################ 3D correlation ###################################
# check 3D:

print ("Focus on one 3D analysis, shape = [:, 25:50, 31:36]")

# put 3D slice of run1 house, run2 face, run2 house together
fig = plt.figure()
i = 1
run1_house = raw_beta_vols["%s_run001" % subid][:, 25:50, 33:38, match_para["house"]]
for z in range(5):
    plt.subplot(3, 5, i, xticks=[], yticks=[])
    plt.imshow(run1_house[:, :, z], interpolation="nearest", cmap=nice_cmap, alpha=0.5)
    i += 1
    if z == 2:
        plt.title("%s_run1_house" % subid)
run2_house = raw_beta_vols["%s_run002" % subid][:, 25:50, 33:38, match_para["house"]]
for z in range(5):
    plt.subplot(3, 5, i, xticks=[], yticks=[])
    plt.imshow(run2_house[:, :, z], interpolation="nearest", cmap=nice_cmap, alpha=0.5)
    i += 1
    if z == 2:
        plt.title("%s_run2_house" % subid)
run2_face = raw_beta_vols["%s_run002" % subid][:, 25:50, 33:38, match_para["face"]]
for z in range(5):
    plt.subplot(3, 5, i, xticks=[], yticks=[])
    plt.imshow(run2_face[:, :, z], interpolation="nearest", cmap=nice_cmap, alpha=0.5)
    i += 1
    if z == 2:
        plt.title("%s_run2_face" % subid)
# label plot
fig.subplots_adjust(bottom=0.2, hspace=0.5)
cbar_ax = fig.add_axes([0.15, 0.06, 0.7, 0.02])
plt.colorbar(cax=cbar_ax, ticks=[], orientation='horizontal')
fig.text(0.35, 0.1, "Relative responding intensity")
fig.text(0.095, 0.07, "Low")
fig.text(0.87, 0.07, "High")
plt.savefig(figure_path + "Try_3D_correlation_%s.png" % subid)
plt.close()

# try to run 3D correlation study:
print ("Progress: Run correlation coefficient with 3D data")

# make a deepcopy of the raw_beta_vols for correlation study:
raw_beta_vols_3d_corr = copy.deepcopy(raw_beta_vols)
# get flatten 3D slice:
house1_3d = np.ravel(raw_beta_vols_3d_corr["%s_run001" % subid][:, 25:50, 33:38, match_para["house"]])
house2_3d = np.ravel(raw_beta_vols_3d_corr["%s_run002" % subid][:, 25:50, 33:38, match_para["house"]])
face2_3d = np.ravel(raw_beta_vols_3d_corr["%s_run002" % subid][:, 25:50, 33:38, match_para["face"]])

# change nan to 0 in the array
house1_3d[np.isnan(house1_3d)] = 0
house2_3d[np.isnan(house2_3d)] = 0
face2_3d[np.isnan(face2_3d)] = 0

# correlation coefficient study:
threeD_house1_house2 = np.corrcoef(house1_3d, house2_3d)
threeD_house1_face2 = np.corrcoef(house1_3d, face2_3d)
print ("%s run1 house vs run2 house in 3D: %s" % (subid, threeD_house1_house2))
print ("%s run1 house vs run2 face in 3D: %s" % (subid, threeD_house1_face2))
print (separator)

# prepare data to analyze 3D brain based on odd runs even runs
print ("Prepare data to analyze \"3D\" brain based on odd runs and even runs:")
print ("Take average of \"3D\" odd runs / even runs to deal with impacts of variations between runs")

even_run_3d = {}
odd_run_3d = {}
# add up even run results / odd run results and take mean for each groups
for item in object_list:
    even_run_3d[item] = np.zeros_like(raw_beta_vols_3d_corr["%s_run001" % subid][:, 25:50, 33:38, match_para[item]])
    odd_run_3d[item] = np.zeros_like(raw_beta_vols_3d_corr["%s_run001" % subid][:, 25:50, 33:38, match_para[item]])
    print ("make average of \"3D\" odd run results:")
    # add up odd runs results
    for i in range(1, run_num+1, 2):
        temp = raw_beta_vols_3d_corr["%s_run0%02d" % (subid, i)][:, 25:50, 33:38, match_para[item]]
        temp[np.isnan(temp)] = 0
        odd_run_3d[item] += temp
        print("odd runs 3D: %d-%s" % (i, item))
    # take mean
    odd_run_3d[item] = odd_run_3d[item]/odd_count
    print ("make average of \"3D\" even run results:")
    # add up even runs results
    for i in range(2, run_num+1, 2):
        temp = raw_beta_vols_3d_corr["%s_run0%02d" % (subid, i)][:, 25:50, 33:38, match_para[item]]
        temp[np.isnan(temp)] = 0
        even_run_3d[item] += temp
        print("even runs 3D: %d-%s" % (i, item))
    # take mean
    even_run_3d[item] = even_run_3d[item]/even_count

# save odd run and even run results as txt file
for key, fig in even_run_3d.items():
    np.savetxt(file_path + "%s_even_%s_3d.txt" % (subid, key), np.ravel(fig))
for key, fig in odd_run_3d.items():
    np.savetxt(file_path + "%s_odd_%s_3d.txt" % (subid, key), np.ravel(fig))

print ("\"3D\" odd run and even run results are saved as txt files!!!!!")
print (separator)

print ("Analysis and Data Pre-processing for %s : Complete!!!" % subid)