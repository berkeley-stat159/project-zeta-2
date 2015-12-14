import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import colors
import copy

# maximally responded area, percentile setting:
percent = 80

# object_list
object_list = ["bottle", "cat", "chair", "face", "house", "scissors", "scrambledpix", "shoe"]

# important path:
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")
figure_path = os.path.join(base_path, "code", "images", "")
file_path = os.path.join(base_path, "code", "txt", "")

# color display
nice_cmap_values = np.loadtxt(file_path + 'actc.txt')
nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')

# generalized analysis, choose which subject to focus on:
subid = "sub004"

# generate list for odd and even run values:
odd_runs = ["%s_odd_%s" % (subid, i) for i in object_list]
even_runs = ["%s_even_%s" % (subid, i) for i in object_list]

# separator:
separator = "-" * 80


############################ Start 2D analysis #############################
print ("Advanced correlation analysis:")
print (separator)
print ("")

# load even and odd run results
all_runs = {}
for i in odd_runs:
    all_runs[i] = np.loadtxt(file_path + i + ".txt")
for i in even_runs:
    all_runs[i] = np.loadtxt(file_path + i + ".txt")

# reshape to 3d images
all_3d = {}
for key, txt in all_runs.items():
    all_3d[key] = np.reshape(txt, (-1, 25, 1))


# make a copy of the images for making figures:
all_3d_fig = copy.deepcopy(all_3d)

# save each 3d image as figure
for key, fig in all_3d_fig.items():
    fig[fig == 0] = np.nan
    plt.imshow(fig[:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.title("%s" % key)
    plt.savefig(figure_path + "%s.png" % key)
    plt.clf()
plt.close()

# save all 3d images as one compiled figure
fig = plt.figure(figsize=[8.0, 5])
i = 1
# plot odd run results
for item in object_list:
    plt.subplot(2, 8, i, xticks=[], yticks=[])
    plt.imshow(all_3d_fig["%s_odd_%s" % (subid, item)][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.title("%s" % item, fontsize=8, weight='bold')
    i += 1
# plot even run results
for item in object_list:
    plt.subplot(2, 8, i, xticks=[], yticks=[])
    plt.imshow(all_3d_fig["%s_even_%s" % (subid, item)][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    i += 1
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.1, bottom=0.05, top=0.835)
# label the figure:
fig.text(0.03, 0.625, 'Odd runs', ha='left', weight='bold')
fig.text(0.03, 0.225, 'Even runs', ha='left', weight='bold')
fig.text(0.05, 0.93, 'Average brain images for odd runs / even runs of %s' % subid, fontsize=16, weight='bold')
# save figure
plt.savefig(figure_path + "odd_even_compile_%s.png" % subid)
# close pyplot window
plt.close()

# report
print ("Average odd run and even run results are saved as images")
print (separator)


# Run correlation:
all_results = []
print ("correlation analysis:")
for i in odd_runs:
    result = []
    for j in even_runs:
        corr = np.corrcoef(all_runs[i], all_runs[j])
        result.append(corr[0, 1])
        print ("%s vs %s: %.4f" % (i, j, corr[0, 1]))
    all_results.append(result)
table_result = np.array(all_results)
np.savetxt(file_path + "correlation_value_%s.txt" % subid, np.ravel(table_result))


# make table to display the correlation:
fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=table_result.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.2, 0.85, "Correlation between odd runs and even runs for %s" % subid, weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "correlation_table_%s.png" % subid)


###############################################################################
# remove the maximally responded area and perform the correlation once again:

# create a copy of data to work on this analysis:
new_all_runs = copy.deepcopy(all_runs)

# remove data that is >= 80 percentile of all data
for key, result in new_all_runs.items():
    thresh = np.percentile(result, q=80)
    nparray = np.array(result)
    nparray[nparray >= thresh] = 0
    new_all_runs[key] = nparray

# reshape the new_all_runs:
new_all_3d = {}
for key, txt in new_all_runs.items():
    new_all_3d[key] = np.reshape(txt, (-1, 25, 1))

# make a copy of the images for making figures:
new_all_3d_fig = copy.deepcopy(new_all_3d)

# clear the background
for key, fig in new_all_3d_fig.items():
    fig[fig == 0] = np.nan

# save all 3d images as one compiled figure
fig = plt.figure(figsize=[8.0, 5])
i = 1
for item in object_list:
    plt.subplot(2, 8, i, xticks=[], yticks=[])
    plt.imshow(new_all_3d_fig["%s_odd_%s" % (subid, item)][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.title("%s" % item, fontsize=8, weight='bold')
    i += 1
for item in object_list:
    plt.subplot(2, 8, i, xticks=[], yticks=[])
    plt.imshow(new_all_3d_fig["%s_even_%s" % (subid, item)][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    i += 1
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.1, bottom=0.05, top=0.835)
# label the figure:
fig.text(0.03, 0.625, 'Odd runs', ha='left', weight='bold')
fig.text(0.03, 0.225, 'Even runs', ha='left', weight='bold')
fig.text(0.08, 0.93, "Average brain images after removing 80%% max for %s" % subid, fontsize=14, weight='bold')
plt.savefig(figure_path + "non_max_odd_even_compile_%s.png" % subid)
plt.close()


# Run correlation:
non_max_all_results = []
print ("correlation analysis of non-maximal results:")
for i in odd_runs:
    result = []
    for j in even_runs:
        corr = np.corrcoef(new_all_runs[i], new_all_runs[j])
        result.append(corr[0, 1])
        print ("%s vs %s: %.4f" % (i, j, corr[0, 1]))
    non_max_all_results.append(result)

non_max_table_result = np.array(non_max_all_results)
np.savetxt(file_path + "non_max_correlation_value_%s.txt" % subid, np.ravel(non_max_table_result))
# make table to display the correlation:

fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=non_max_table_result.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(1.0, 0.85, "Correlation of non_maximal responded brain of %s" % subid, weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "non_max_correlation_table_%s.png" % subid)
plt.close()


# generate bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(10, 24))
for plot_num in range(8):
    i = plot_num -1
    ax = plt.subplot(8, 1, plot_num, frameon=False)
    bar_plot1 = ax.bar(ind, table_result[i, :], width, color='royalblue')
    bar_plot2 = ax.bar(ind+width, non_max_table_result[i, :], width, color='deepskyblue')
    # add some label:
    ax.set_ylabel("Correlation")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.5, bottom=0.05, top=0.95)
plt.savefig(figure_path + "%s_2d_total_correlation_bar_both.png" % subid)


# generate individual bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(12, 5))
for i in range(8):
    ax = plt.subplot(111, frameon=False)
    bar_plot1 = ax.bar(ind, table_result[i, :], width, color='royalblue')
    bar_plot2 = ax.bar(ind+width, non_max_table_result[i, :], width, color='deepskyblue')
    # add some label:
    ax.set_ylabel("Correlation")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
    plt.savefig(figure_path + "%s_2d_%s_total_correlation_bar_both.png" % (subid, object_list[i]))
    plt.clf()
plt.close()

##################################################################

# subtract the mean and try the correlation:

# create a copy of data to work on this analysis:
subtrmean_all_runs = copy.deepcopy(all_runs)

# performing subtraction:
# even result - odd_scramblepix
# odd result - even_scramblepix

total_mean = np.zeros_like(subtrmean_all_runs["%s_odd_face" % subid])
total_num = 0
for key, result in subtrmean_all_runs.items():
    nparray = np.array(result)
    total_mean += nparray
    total_num += 1
total_mean = total_mean/total_num

subtract_mean_result = {}
for key, result in subtrmean_all_runs.items():
    nparray = np.array(result)
    subtract_mean_result[key] = nparray - total_mean

# reshape the subtract_mean_result:
subtract_mean_all_3d = {}
for key, txt in subtract_mean_result.items():
    subtract_mean_all_3d[key] = np.reshape(txt, (-1, 25, 1))

# make a copy of the images for making figures:
subtract_mean_all_3d_fig = copy.deepcopy(subtract_mean_all_3d)

# clear the background
for key, fig in subtract_mean_all_3d_fig.items():
    fig[fig == 0] = np.nan

# save all 3d images as one compiled figure
fig = plt.figure(figsize=[8.0, 5])
i = 1
for item in object_list:
    plt.subplot(2, 8, i, xticks=[], yticks=[])
    plt.imshow(subtract_mean_all_3d_fig["%s_odd_%s" % (subid, item)][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.title("%s" % item, fontsize=8, weight='bold')
    i += 1
for item in object_list:
    plt.subplot(2, 8, i, xticks=[], yticks=[])
    plt.imshow(subtract_mean_all_3d_fig["%s_even_%s" % (subid, item)][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    i += 1
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.2, bottom=0.05, top=0.9)
# label the figure:
fig.text(0.03, 0.625, 'Odd runs', ha='left', weight='bold')
fig.text(0.03, 0.225, 'Even runs', ha='left', weight='bold')
fig.text(0.16, 0.93, 'Brain images after subtracting mean for %s' % subid, fontsize=16, weight='bold')
plt.savefig(figure_path + "subtract_mean_odd_even_compile_%s.png" % subid)
plt.close()


# Run correlation:
subtract_mean_all_results = []
print ("correlation analysis of subtracted results:")
for i in odd_runs:
    result = []
    for j in even_runs:
        corr = np.corrcoef(subtract_mean_result[i], subtract_mean_result[j])
        result.append(corr[0, 1])
        print ("%s vs %s: %.4f" % (i, j, corr[0, 1]))
    subtract_mean_all_results.append(result)

subtract_mean_table_result = np.array(subtract_mean_all_results)

# make table to display the correlation:

fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=subtract_mean_table_result.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.3, 0.85, "Correlation of mean subtracted brain images of %s" % subid, weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "subtract_mean_correlation_table_%s.png" % subid)
plt.close()

print (separator)
################################## Start 3D analysis ######################################
print ("Advanced correlation analysis with 3D results:")
print (separator)
print ("")
# load even and odd run results
all_runs_3d = {}
for i in odd_runs:
    all_runs_3d[i] = np.loadtxt(file_path + i + "_3d.txt")
for i in even_runs:
    all_runs_3d[i] = np.loadtxt(file_path + i + "_3d.txt")

# reshape to 3d images
all_3d_for3d = {}
for key, txt in all_runs_3d.items():
    all_3d_for3d[key] = np.reshape(txt, (-1, 25, 5))

# make a copy of the images for making figures:
all_3d_for3d_fig = copy.deepcopy(all_3d_for3d)

# clear background
for key, fig in all_3d_for3d_fig.items():
    fig[fig == 0] = np.nan

# save all 3d images as one compiled figure for each z
fig = plt.figure(figsize=[8.0, 20])
i = 1

for item in object_list:
    for index in range(5):
        plt.subplot(16, 5, i, xticks=[], yticks=[])
        plt.imshow(all_3d_for3d_fig["%s_odd_%s" % (subid, item)][:, :, index], interpolation="nearest", cmap=nice_cmap)
        if index == 2:
            plt.title("Odd Run %s" % item, fontsize=8, weight='bold')
        i += 1
    for index in range(5):
        plt.subplot(16, 5, i, xticks=[], yticks=[])
        plt.imshow(all_3d_for3d_fig["%s_even_%s" % (subid, item)][:, :, index], interpolation="nearest", cmap=nice_cmap)
        if index == 2:
            plt.title("Even Run %s" % item, fontsize=8, weight='bold')
        i += 1
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.5, bottom=0.05, top=0.835)
# label the figure:
fig.text(0.25, 0.85, 'Average brain 3D images for odd runs / even runs of %s' % subid, fontsize=16, weight='bold')
plt.savefig(figure_path + "3d_odd_even_compile_%s.png" % subid)
plt.close()

# Run correlation:
all_results_3d = []
print ("3D correlation analysis:")
for i in odd_runs:
    result = []
    for j in even_runs:
        corr = np.corrcoef(np.ravel(all_runs_3d[i]), np.ravel(all_runs_3d[j]))
        result.append(corr[0, 1])
        print ("%s vs %s: %.4f" % (i, j, corr[0, 1]))
    all_results_3d.append(result)

table_result_3d = np.array(all_results_3d)
np.savetxt(file_path + "3d_correlation_value_%s.txt" % subid, np.ravel(table_result_3d))

# make table to display the correlation:

fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=table_result_3d.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.2, 0.85, "Correlation between 3D odd runs and even runs for %s" % subid, weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "3d_correlation_table_%s.png" % subid)


#########################################################################################

# remove the maximally responded 3D area and perform the correlation once again:

# create a copy of data to work on this analysis:
new_all_runs_for3d = copy.deepcopy(all_runs_3d)

# remove data that is >= 80 percentile of all data
for key, result in new_all_runs_for3d.items():
    thresh = np.percentile(result, q=90)
    nparray = np.array(result)
    nparray[nparray >= thresh] = 0
    new_all_runs_for3d[key] = nparray

# reshape the new_all_runs:
new_all_3d_for3d = {}
for key, txt in new_all_runs_for3d.items():
    new_all_3d_for3d[key] = np.reshape(txt, (-1, 25, 5))

# make a copy of the images for making figures:
new_all_3d_fig_for3d = copy.deepcopy(new_all_3d_for3d)

# clear the background
for key, fig in new_all_3d_fig_for3d.items():
    fig[fig == 0] = np.nan

# save all 3d images as one compiled figure
fig = plt.figure(figsize=[8.0, 12.0])
i = 1
for item in object_list:
    for index in range(5):
        plt.subplot(16, 5, i, xticks=[], yticks=[])
        plt.imshow(new_all_3d_fig_for3d["%s_odd_%s" % (subid, item)][:, :, index], interpolation="nearest", cmap=nice_cmap)
        if index == 2:
            plt.title("%s" % item, fontsize=8, weight='bold')
        i += 1
for item in object_list:
    for index in range(5):
        plt.subplot(16, 5, i, xticks=[], yticks=[])
        plt.imshow(new_all_3d_fig_for3d["%s_even_%s" % (subid, item)][:, :, index], interpolation="nearest", cmap=nice_cmap)
        if index == 2:
            plt.title("%s" % item, fontsize=8, weight='bold')
        i += 1
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.1, bottom=0.05, top=0.835)
# label the figure:
fig.text(0.2, 0.85, "Average 3D brain images after removing 80%% max for %s" % subid, weight='bold')
plt.savefig(figure_path + "3d_non_max_odd_even_compile_%s.png" % subid)
plt.close()


# Run correlation:
non_max_all_results_for3d = []
print ("correlation analysis of 3D non-maximal results:")
for i in odd_runs:
    result = []
    for j in even_runs:
        corr = np.corrcoef(new_all_runs_for3d[i], new_all_runs_for3d[j])
        result.append(corr[0, 1])
        print ("%s vs %s: %.4f" % (i, j, corr[0, 1]))
    non_max_all_results_for3d.append(result)

non_max_table_result_for3d = np.array(non_max_all_results_for3d)
np.savetxt(file_path + "3d_non_max_correlation_value_%s.txt" % subid, np.ravel(non_max_table_result_for3d))

# make table to display the correlation:

fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=non_max_table_result_for3d.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.16, 0.85, "3D Correlation of non_maximal responded brain of %s" % subid, weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "3d_non_max_correlation_table_%s.png" % subid)
plt.close()

# generate bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(10, 24))
for plot_num in range(8):
    i = plot_num -1
    ax = plt.subplot(8, 1, plot_num, frameon=False)
    bar_plot1 = ax.bar(ind, table_result_3d[i, :], width, color='darkgoldenrod')
    bar_plot2 = ax.bar(ind+width, non_max_table_result_for3d[i, :], width, color='tan')
    # add some label:
    ax.set_ylabel("Correlation")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.5, bottom=0.05, top=0.95)
plt.savefig(figure_path + "%s_3d_total_correlation_bar_both.png" % subid)

# generate individual bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(12, 5))
for i in range(8):
    ax = plt.subplot(111, frameon=False)
    bar_plot1 = ax.bar(ind, table_result_3d[i, :], width, color='darkgoldenrod')
    bar_plot2 = ax.bar(ind+width, non_max_table_result_for3d[i, :], width, color='tan')
    # add some label:
    ax.set_ylabel("Correlation")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
    plt.savefig(figure_path + "%s_3d_%s_total_correlation_bar_both.png" % (subid, object_list[i]))
    plt.clf()
plt.close()


############################# subtract mean and do the correlation for 3D ##################################
# subtract the mean and try the correlation:

# create a copy of data to work on this analysis:
subtrmean_all_runs_3d = copy.deepcopy(all_runs_3d)

# performing subtraction:
# even result - odd_scramblepix
# odd result - even_scramblepix

total_mean_3d = np.zeros_like(subtrmean_all_runs_3d["%s_odd_face" % subid])
total_num_3d = 0
for key, result in subtrmean_all_runs_3d.items():
    nparray = np.array(result)
    total_mean_3d += nparray
    total_num_3d += 1
total_mean_3d = total_mean_3d/total_num_3d

subtract_mean_result_for3d = {}
for key, result in subtrmean_all_runs_3d.items():
    nparray = np.array(result)
    subtract_mean_result_for3d[key] = nparray - total_mean_3d

# reshape the subtract_mean_result:
subtract_mean_all_3d_for3d = {}
for key, txt in subtract_mean_result_for3d.items():
    subtract_mean_all_3d_for3d[key] = np.reshape(txt, (-1, 25, 5))

# make a copy of the images for making figures:
subtract_mean_all_3d_fig_for3d = copy.deepcopy(subtract_mean_all_3d_for3d)

# clear the background
for key, fig in subtract_mean_all_3d_fig_for3d.items():
    fig[fig == 0] = np.nan


# save all 3d images as one compiled figure
fig = plt.figure(figsize=[8.0, 12.0])
i = 1
for item in object_list:
    for index in range(5):
        plt.subplot(16, 5, i, xticks=[], yticks=[])
        plt.imshow(subtract_mean_all_3d_fig_for3d["%s_odd_%s" % (subid, item)][:, :, index], interpolation="nearest", cmap=nice_cmap)
        if index == 2:
            plt.title("%s" % item, fontsize=8, weight='bold')
        i += 1
for item in object_list:
    for index in range (5):
        plt.subplot(16, 5, i, xticks=[], yticks=[])
        plt.imshow(subtract_mean_all_3d_fig_for3d["%s_even_%s" % (subid, item)][:, :, index], interpolation="nearest", cmap=nice_cmap)
        if index == 2:
            plt.title("%s" % item, fontsize=8, weight='bold')
        i += 1
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.1, bottom=0.05, top=0.835)
# label the figure:
# fig.text(0.03, 0.625, 'Odd runs', ha='left', weight='bold')
# fig.text(0.03, 0.225, 'Even runs', ha='left', weight='bold')
fig.text(0.16, 0.93, '3D Brain images after subtracting mean for %s' % subid, fontsize=16, weight='bold')
plt.savefig(figure_path + "3d_subtract_mean_odd_even_compile_%s.png" % subid)
plt.close()


# Run correlation:
subtract_mean_all_results_for3d = []
print ("correlation analysis of subtracted results:")
for i in odd_runs:
    result = []
    for j in even_runs:
        corr = np.corrcoef(subtract_mean_result_for3d[i], subtract_mean_result_for3d[j])
        result.append(corr[0, 1])
        print ("%s vs %s: %.4f" % (i, j, corr[0, 1]))
    subtract_mean_all_results_for3d.append(result)

subtract_mean_table_result_for3d = np.array(subtract_mean_all_results_for3d)

# make table to display the correlation:

fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=subtract_mean_table_result_for3d.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.3, 0.85, "3D Correlation of mean subtracted brain images of %s" % subid, weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "3d_subtract_mean_correlation_table_%s.png" % subid)
plt.close()

print (separator)

print ("Complete!!!")