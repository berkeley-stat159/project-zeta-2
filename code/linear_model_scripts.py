

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
figure_path = os.path.join(base_path, "code", "images", "")
file_path = os.path.join(base_path, "code", "txt", "")

# help to make directory to save figure and txt
if not os.path.exists(figure_path):
    os.makedirs(figure_path)
if not os.path.exists(file_path):
    os.makedirs(file_path)

# color display:
object_list = ["bottle", "cat", "chair", "face", "house", "scissors", "scrambledpix", "shoe"]
# color for stimulation
color_list_s = ["b", "g", "r", "c", "m", "y", "k", "sienna"]
match_color_s = dict(zip(object_list, color_list_s))
# color for convolved result
color_list_c = ["royalblue", "darksage", "tomato", "cadetblue", "orchid", "goldenrod", "dimgrey", "sandybrown"]
match_color_c = dict(zip(object_list, color_list_c))
# color for showing betas
nice_cmap_values = np.loadtxt(file_path + 'actc.txt')
nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')

# object parameter number:

match_para = dict(zip(object_list, xrange(8)))

# check slice:
slice_number = 32

# separator:
separator = "-" * 80

# which subject to work on?
subid = "sub001"

# work on results from this subject:
########################################

print (separator)
print ("Project-Zeta: use linear regression to study ds105 dataset")
print (separator)
print ("Focus on %s for the analysis" % subid)
print (separator)


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
img_key.sort()
for i in img_key:
    print (i)
print ("There are %d runs for %s" % (run_num, subid))
print (separator)

# get data for those figures
print ("Get data from images...")
sub_data = {}
for key, img in sub_img.iteritems():
    sub_data[key] = img.get_data()
print ("Complete!")
print (separator)

# use rms_diff to check outlier for all runs of this subject
print ("Analyze outliers in these runs:")
for key, data in sub_data.iteritems():
    rms_diff = diagnos.vol_rms_diff(data)
    rms_outlier_indices, rms_thresh = diagnos.iqr_outliers(rms_diff)
    y_value2 = [rms_diff[i] for i in rms_outlier_indices]

    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])

    ax.plot(rms_diff, label='rms')
    ax.plot([0, len(rms_diff)], [rms_thresh[1], rms_thresh[1]], "k--",\
    label='high threshold', color='m')
    ax.plot([0, len(rms_diff)], [rms_thresh[0], rms_thresh[0]], "k--",\
    label='low threshold', color='c')
    ax.plot(rms_outlier_indices, y_value2, 'o', color = 'g', label='outlier')
    ax.set_xlabel('Scan time course')
    ax.set_ylabel('Volumne RMS difference')
    ax.set_title('Volume RMS Difference with Outliers for %s' % key)
    ax.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0., numpoints=1)

    fig.savefig(figure_path + 'Volume_RMS_Difference_Outliers_%s.png' % key)
    fig.clf()
plt.close()

print ("Outlier analysis results are saved as figures!")
print (separator)

###################


# remove outlier from images
sub_clean_img, outlier_index = outlier.remove_data_outlier(sub_img)
print ("Remove outlier:")
print ("outliers are removed from each run!")
print (separator)

# get general all tr times == 121*2.5 = about 300 s
# this is the x-axis to plot hemodynamic prediction
all_tr_times = np.arange(sub.BOLD_shape[-1]) * sub.TR

# the y-axis to plot hemodynamic prediction is the neural value from condition (on-off)
sub_neural = neural.get_object_neural(sub.sub_id, sub.conditions, sub.TR, sub.BOLD_shape[-1])

# report info for all run details
print ("The detailed run info for %s:" % subid)
neural_key = sub_neural.keys()
neural_key.sort()
for i in neural_key:
    print (i)
print (separator)


# get task time course for all runs -> save as images
print ("generate task time course images")
print (separator)
for run in xrange(1, run_num):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])

    for item in object_list:
        check_key = "run0%02d-%s" % (run, item)
        ax.plot(all_tr_times, sub_neural[check_key][0], label="%s" % object, c=match_color_s[item])
    ax.set_title("Task time course for %s-run0%02d" % (subid, run))
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    fig.savefig(figure_path + "Task_time_course_%s_run0%02d" % (subid, run))
    fig.clf()
plt.close()

print ("task time course images are saved!")
print (separator)

# assume true HRF starts at zero, and gets to zero sometime before 35 seconds.
tr_times = np.arange(0, 30, sub.TR)
hrf_at_trs = convol.hrf(tr_times)


# get convolution data for each objects in this run -> show figure for run001
print ("Work on convolution based on condition files")
print (separator)
sub_convolved = convol.get_all_convolved(sub_neural, hrf_at_trs, file_path)
print ("convolution analysis for all runs is complete")
print (separator)

# save convolved data
for key, data in sub_convolved.iteritems():
    np.savetxt(file_path + "convolved_%s.txt" % key, data)
print ("convolved results are saved as txt files")


# show relationship between stimulation time and bold signals
sub_neural_key = sub_neural.keys()
sub_neural_key.sort()
for run in xrange(1, run_num):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.4, 0.75])

    for item in object_list:
        # plot the convolution/bold signal
        check_key = "run0%02d-%s" % (run, item)
        convolved = convol.convolution(sub_neural[check_key][0], hrf_at_trs)
        ax.plot(all_tr_times, convolved, c=match_color_c[item], label="%s-BOLD" % item)
        # plot the stimulation:
        ax.plot(all_tr_times, sub_neural[check_key][0], c=match_color_s[item], label="%s-task" % item)
    ax.set_title("hemodynamic prediction of %s-run0%02d" % (subid, run))
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    fig.savefig(figure_path + "%s_run0%02d_bold_prediction.png" % (subid, run))
    fig.clf()
plt.close()


# remove outlier from convolved results
sub_convolved = convol.remove_outlier(sub.sub_id, sub_convolved, outlier_index)
print ("Outliers are removed from convolved results")

# subject clean and smooth img == sub_cs_img
sub_cs_img = sm.smooth(sub_clean_img)
print ("Smooth images: Complete!")

# get shape info of the images
shape = {}
for key, img in sub_cs_img.iteritems():
    shape[key] = img.shape
    print ("shape of %s = %s" % (key, shape[key]))
with open(file_path+'new_shape.json', 'w') as fp:
    json.dump(shape, fp)
print ("New shape info of images is recorded and saved as file")

####### Run linear regression #######
# generate design matrix
design_matrix = lm.batch_make_design(sub_cs_img, sub_convolved)
parameters = design_matrix["sub001_run001"].shape[-1]
print ("parameter number: %d" % parameters )
print ("Design matrix generated")

# rescale design matrix
design_matrix = lm.batch_scale_matrix(design_matrix)
print ("Design matrix rescaled")

# save scaled design matrix as figure
for key, matrix in design_matrix.iteritems():
    # plt.figure()
    plt.imshow(matrix, aspect=0.1, interpolation="nearest", cmap="gray")
    plt.title("scaled design matrix for %s" % key)
    plt.savefig(figure_path + "design_matrix_%s" % key)
    plt.clf()
plt.close()
print ("Design matrices are saved as figures")

# use maskfunc to generate mask
mask, mean_data = msk.generateMaskedBrain(sub_clean_img)

# save mask as figure
for key, each in mask.iteritems():
    for i in xrange(1, 90):
        plt.subplot(9, 10, i)
        plt.imshow(each[:, :, i], interpolation="nearest", cmap="gray", alpha=0.5)
        ax = plt.gca()
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    plt.savefig(figure_path + "all_masks_for_%s.png" % key)
    plt.clf()

# run linear regression to generate betas
# first step: use mask to get data and reshape to 2D
sub_cs_mask_img = lm.apply_mask(sub_cs_img, mask)
sub_cs_mask_img_2d = lm.batch_convert_2d_based(sub_cs_mask_img, shape)
# sub1_cs_mask_img_2d = lm.batch_convert_2d(sub1_cs_mask_img)

# second step: run linear regression to get betas:
all_betas = {}
for key, img in sub_cs_mask_img_2d.iteritems():
    #img_2d = np.reshape(img, (-1, img.shape[-1]))
    Y = img.T
    all_betas[key] = npl.pinv(design_matrix[key]).dot(Y)
print ("Getting betas from linear regression: complete!")
print (separator)

# third step: put betas back into it's original place:
print ("Show beta figures:")
beta_vols = {}
raw_beta_vols = {}

for key, betas in all_betas.iteritems():
    beta_vols[key] = np.zeros(shape[key][:-1] + (parameters,))
    check_mask = (mask[key] == 1)
    #check_mask_shape = check_mask.shape
    #beta_shape = betas.shape
    #beta_vols_shape = beta_vols.shape
    # print ("mask shape for %s : %s" % (key, check_mask_shape))
    # print ("beta shape for %s : %s" % (key, beta_shape))
    # print ("beta_vols shape for %s : %s" % (key, beta_vols_shape))

    beta_vols[key][check_mask] = betas.T
    print ("betas of %s is fitted back to 3D!" % key)
    raw_beta_vols[key] = beta_vols[key]

    beta_vols[key][~check_mask] = np.nan
    mean_data[key][~check_mask] = np.nan

    for item in object_list:
        for i in xrange(1, 51):
            plt.subplot(5, 10, i)
            lookat = i + 20
            plt.imshow(mean_data[key][:, :, lookat], interpolation="nearest", cmap="gray", alpha=0.5)
            plt.imshow(beta_vols[key][:, :, lookat, match_para[item]], cmap=nice_cmap, alpha=0.5)
            ax = plt.gca()
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_xlabel("z = %d" % lookat)

        plt.savefig(figure_path + "betas for %s-%s.png" % (key, item))
        plt.clf()
plt.close()

print ("beta figures are generated!!")
print (separator)


# check if the result is artificial or not?
# fig = plt.figure(figsize=(8, 8))


# analyze based on odd runs even runs using affine

print ("print affine vectors for each run:")
for key, img in sub_img.iteritems():
    print("%s :\n %s" % (key, img.affine))
print ("They have the same affine matrix!")
print (separator)

# try to use mask on beta_vols
#
# beta_mean_data, beta_mask = msk.generateMaskedBrain(raw_beta_vols)
# for key, meanvol in beta_mean_data.iteritems():
#     plt.hist(np.ravel(meanvol), bins = 100)
#     plt.savefig(figure_path + "histo for %s.png" % key)
#     plt.clf()
# plt.close()
# print ("histogram: Complete!!!!!!!!!!!!!!!")
#
# for key, mask in beta_mask.iteritems():
#     for i in xrange(1, 51):
#         plt.subplot(5, 10, i)
#         lookat = i +20
#         plt.imshow(beta_mask[key][:, :, lookat], interpolation="nearest", cmap = "gray", alpha=0.5)
#     plt.savefig(figure_path + "mask for %s.png" % key)
#     plt.clf()
# plt.close()
#
# run1_house = raw_beta_vols["sub001_run001"][:, 25:50, slice_number, 5]
# plt.imshow(run1_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
# plt.savefig(figure_path + "run1_house.png")
# plt.clf()
# run2_house = raw_beta_vols["sub001_run002"][:, 25:50, slice_number, 5]
# plt.imshow(run2_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
# plt.savefig(figure_path + "run2_house.png")
# plt.clf()
# run2_face = raw_beta_vols["sub001_run002"][:, 25:50, slice_number, 4]
# plt.imshow(run2_face, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
# plt.savefig(figure_path + "run2_face.png")
# plt.close()
#
# print ("run correlation coefficient")
# house1 = np.ravel(run1_house)
# house2 = np.ravel(run2_house)
# face2 = np.ravel(run2_face)
#
# # save for pretest analysis
# np.savetxt(file_path + "house1.txt", house1)
# np.savetxt(file_path + "house2.txt", house2)
# np.savetxt(file_path + "face2.txt", face2)
#
# # change nan to 0 in the array
# house1[np.isnan(house1)] = 0
# house2[np.isnan(house2)] = 0
# face2[np.isnan(face2)] = 0
#
# # correlation coefficient study:
#
# house1_house2 = np.corrcoef(house1, house2)
# house1_face2 = np.corrcoef(house1, face2)
# print ("run1 house vs run2 house: %s" % house1_house2)
# print ("run1 house vs run2 face : %s" % house1_face2)
#
#
# # print ("check z = 32")
# # slice_z = {}
# # for key, betas in beta_vols.iteritems():
# #     for item in object_list:
# #         slice_z["%s-%s" % (key, item)] = beta_vols[key][:, 25:30, slice_number, match_para[item]]
# print ("Taking slice of %d: complete! " % slice_number)
#
#
# # try to use mask
# betas_mask, beta_vol_mean = msk.generateMaskedBrain(slice_z)
# for key, betas in beta_vol_mean.iteritems():
#     check_mask = (betas_mask[key] == 1)
# # run linear regression to generate betas
# # first step: use mask to get data and reshape to 2D
# sub1_cs_mask_img = lm.apply_mask(sub1_cs_img, mask)
# sub1_cs_mask_img_2d = lm.batch_convert_2d_based(sub1_cs_mask_img, shape)
# # sub1_cs_mask_img_2d = lm.batch_convert_2d(sub1_cs_mask_img)

# # second step: run linear regression to get betas:
# all_betas = {}
# for key, img in sub1_cs_mask_img_2d.iteritems():
#     #img_2d = np.reshape(img, (-1, img.shape[-1]))
#     Y = img.T
#     all_betas[key] = npl.pinv(design_matrix[key]).dot(Y)
# print ("Getting betas from linear regression: complete!")

# # third step: put betas back into it's original place:
# beta_vols = {}
# raw_beta_vols = {}

# for key, betas in all_betas.iteritems():
#     beta_vols[key] = np.zeros(shape[key][:-1] + (parameters,))
#     check_mask = (mask[key] == 1)
#     #check_mask_shape = check_mask.shape
#     #beta_shape = betas.shape
#     #beta_vols_shape = beta_vols.shape
#     # print ("mask shape for %s : %s" % (key, check_mask_shape))
#     # print ("beta shape for %s : %s" % (key, beta_shape))
#     # print ("beta_vols shape for %s : %s" % (key, beta_vols_shape))

#     beta_vols[key][check_mask] = betas.T
#     print ("betas fitted in!")
#     raw_beta_vols[key] = beta_vols[key]

#     beta_vols[key][~check_mask] = np.nan
#     mean_data[key][~check_mask] = np.nan


#     for item in object_list:
#         for i in xrange(1, 51):
#             plt.subplot(5, 10, i)
#             lookat = i + 20
#             plt.imshow(mean_data[key][:, :, lookat], interpolation="nearest", cmap = "gray", alpha=0.5)
#             plt.imshow(beta_vols[key][:, :, lookat, match_para[item]], cmap=nice_cmap, alpha=0.5)
#             ax = plt.gca()
#             ax.set_xticklabels([])
#             ax.set_yticklabels([])
#             ax.set_xlabel("z = %d" % lookat)

#         plt.savefig(figure_path + "betas for %s-%s.png" % (key, item))
#         plt.clf()
#     plt.close()

# # print ("beta figures are generated!!")
#
# # #try to use mask on beta_vols
#
# # beta_mean_data, beta_mask = msk.generateMaskedBrain(raw_beta_vols)
# # for key, meanvol in beta_mean_data.iteritems():
# #     plt.hist(np.ravel(meanvol), bins = 100)
# #     plt.savefig(figure_path + "histo for %s.png" % key)
# #     plt.clf()
# # plt.close()
# # print ("histogram: Complete!!!!!!!!!!!!!!!")

# # for key, mask in beta_mask.iteritems():
# #     for i in xrange(1, 51):
# #         plt.subplot(5, 10, i)
# #         lookat = i +20
# #         plt.imshow(beta_mask[key][:, :, lookat], interpolation="nearest", cmap = "gray", alpha=0.5)
# #     plt.savefig(figure_path + "mask for %s.png" % key)
# #     plt.clf()
# # plt.close()



# check just z = 32

print ("Focus on one slice: k = %d" % slice_number)

run1_house = raw_beta_vols["%s_run001" % subid][:, 25:50, slice_number, 5]
plt.imshow(run1_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run1_House" % subid)
plt.savefig(figure_path + "%s_run1_house.png" % subid)
plt.clf()
run2_house = raw_beta_vols["%s_run002" % subid][:, 25:50, slice_number, 5]
plt.imshow(run2_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run2_House" % subid)
plt.savefig(figure_path + "%s_run2_house.png" % subid)
plt.clf()
run2_face = raw_beta_vols["%s_run002" % subid][:, 25:50, slice_number, 4]
plt.imshow(run2_face, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run2_Face" % subid)
plt.savefig(figure_path + "%s_run2_face.png" % subid)
plt.close()

# put together
plt.subplot(1, 3, 1)
run1_house = raw_beta_vols["%s_run001" % subid][:, 25:50, slice_number, 5]
plt.imshow(run1_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run1_House" % subid)
#plt.savefig(figure_path + "run1_house.png")
#plt.clf()
plt.subplot(1, 3, 2)
run2_house = raw_beta_vols["%s_run002" % subid][:, 25:50, slice_number, 5]
plt.imshow(run2_house, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run2_House" % subid)
#plt.savefig(figure_path + "run2_house.png")
#plt.clf()
plt.subplot(1, 3, 3)
run2_face = raw_beta_vols["%s_run002" % subid][:, 25:50, slice_number, 4]
plt.imshow(run2_face, interpolation="nearest", cmap=nice_cmap, alpha=0.5)
plt.title("%s_Run2_Face" % subid)
#plt.savefig(figure_path + "run2_face.png")
plt.savefig(figure_path + "%s_run_figure_compile.png" % subid)
plt.close()


print ("run correlation coefficient")
house1 = np.ravel(run1_house)
house2 = np.ravel(run2_house)
face2 = np.ravel(run2_face)

# save for pretest analysis
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
print (separator)

# analyze based on odd runs even runs
print ("Analyze based on odd runs and even runs:")
print ("Take average for odd runs / even runs to deal with impacts of variations between runs")
# even_run = {}
# odd_run = {}
# for item in object_list:
#     even_run[item] = np.zeros_like(raw_beta_vols["%s_run001" % subid][:, 25:50, slice_number, 5])
#     odd_run[item] = np.zeros_like(raw_beta_vols["%s_run001" % subid][:, 25:50, slice_number, 5])
#     print ("make average of odd run results:")
#     for i in range(1, 13, 2):
#         temp = raw_beta_vols["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
#         temp[np.isnan(temp)] = 0
#         odd_run[item] += temp
#         print("odd runs: %d-%s" % (i, item))
#     print ("make average od even run results:")
#     odd_run[item] = odd_run[item]/6
#
#     for i in range(2, 14, 2):
#         temp = raw_beta_vols["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
#         temp[np.isnan(temp)] = 0
#         even_run[item] += temp
#         print("even: %d, %s" % (i, item))
#     even_run[item] = odd_run[item]/6


even_run = {}
odd_run = {}
for item in object_list:
    even_run[item] = np.zeros_like(raw_beta_vols["%s_run001" % subid][:, 25:50, slice_number, 5])
    odd_run[item] = np.zeros_like(raw_beta_vols["%s_run001" % subid][:, 25:50, slice_number, 5])
    print ("make average of odd run results:")
    for i in range(1, run_num+1, 2):
        temp = raw_beta_vols["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
        temp[np.isnan(temp)] = 0
        odd_run[item] += temp
        print("odd runs: %d-%s" % (i, item))
    print ("make average od even run results:")
    odd_run[item] = odd_run[item]/6

    for i in range(2, run_num+2, 2):
        temp = raw_beta_vols["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
        temp[np.isnan(temp)] = 0
        even_run[item] += temp
        print("even: %d, %s" % (i, item))
    even_run[item] = odd_run[item]/6


# save odd run and even run results as txt file
for key, fig in even_run.iteritems():
    np.savetxt(file_path + "even_%s.txt" % key, np.ravel(fig))
for key, fig in odd_run.iteritems():
    np.savetxt(file_path + "odd_%s.txt" % key, np.ravel(fig))

print ("odd run and even run results are saved as txt files!!!!!")
print (separator)


print ("save result for each object and each run individually")
# check just z = 32
for i in range(1, 13):
    for item in object_list:
        temp = raw_beta_vols["%s_run0%02d" % (subid, i)][:, 25:50, slice_number, match_para[item]]
        np.savetxt(file_path + "%s_run0%02d_%s.txt" % (subid, i, item), np.ravel(temp))
print ("Complete!!")
print (separator)
# # print ("check z = 32")
# # slice_z = {}
# # for key, betas in beta_vols.iteritems():
# #     for item in object_list:
# #         slice_z["%s-%s" % (key, item)] = beta_vols[key][:, 25:30, slice_number, match_para[item]]
# # print ("Taking slice of %d: complete! " % slice_number)
# #
# #
# # # try to use mask
# # betas_mask, beta_vol_mean = msk.generateMaskedBrain(slice_z)
# # for key, betas in beta_vol_mean.iteritems():
# #     check_mask = (betas_mask[key] == 1)
# #     #check_mask_shape = check_mask.shape
# #     #beta_shape = betas.shape
# #     #beta_vols_shape = beta_vols.shape
# #     # print ("mask shape for %s : %s" % (key, check_mask_shape))
# #     # print ("beta shape for %s : %s" % (key, beta_shape))
# #     # print ("beta_vols shape for %s : %s" % (key, beta_vols_shape))
# #
# #     slice_z[key][~check_mask] = np.nan
# #     beta_vol_mean[key][~check_mask] = np.nan
# #
# #     beta_vol_mean_shape = beta_vol_mean[key].shape
# #     slice_z
# #     print ("shape for beta_vol_mean = %s" % beta_vol_mean_shape )
# #
# #
# #     #plt.imshow(beta_vol_mean[key][:, :, slice_number], interpolation="nearest", cmap="gray", alpha=0.5)
# #     plt.imshow(slice_z[key], cmap=nice_cmap, alpha=0.5)
# #
# #     plt.savefig(figure_path + "MASK_betas for %s.png" % key)
# #     plt.clf()
# # plt.close()

#     #mean_data[key] = np.mean(sub1_cs_img[key], axis=-1)
#     #mean_data[key][~check_mask] = np.nan

#     # for item in object_list:
#     #     for i in xrange(1, 51):
#     #         plt.subplot(5, 10, i)
#     #         lookat = i + 20
#     #         #plt.imshow(mean_data[key][:, :, lookat], interpolation="nearest", cmap = "gray", alpha=0.5)
#     #         plt.imshow(beta_vols[key][:, :, lookat, match_para[item]], cmap="Reds", alpha=0.5)
#     #         ax = plt.gca()
#     #         ax.set_xticklabels([])
#     #         ax.set_yticklabels([])
#     #         ax.set_xlabel("z = %d" % lookat)
#     #
#     #     plt.savefig(figure_path + "MASK_betas for %s-%s.png" % (key, item))
#     #     plt.clf()
#     # plt.close()

print ("Analysis Complete!!!")