import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import colors
import copy
# from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})

# maximally responsed area, percentile setting:
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

# subject list
subject_list = ["sub0%02d" % i for i in range(1, 7)]

# generate list for odd and even run values:

# separator:
separator = "-" * 80
sec_separator = '=' * 80

################################### Start #####################################
################################ 2D analysis ##################################
print(sec_separator)
print("Cross subject correlation analysis")
print(separator)
print("Focus on 2D correlation analysis")
print(separator)
print ("Load correlation table of each subjects:")
correlation_values = {}
for i in subject_list:
    correlation_values[i] = np.loadtxt(file_path + "correlation_value_%s.txt" % i)
print ("Complete")
print (separator)


# get total average:
num_count = 0
total_average = np.zeros((8, 8))
total_array = np.zeros((6, 64))
for key, value in correlation_values.items():
    nparray = np.array(value)
    total_array[num_count, :] = nparray
    nparray = np.reshape(nparray, (8, 8))
    total_average += nparray
    num_count += 1
total_average = total_average/num_count

# generate table plot
fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=total_average.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.2, 0.85, "Total correlation between odd runs and even runs", weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "2d_total_correlation_table_%s.png")

# calculate standard deviation across subjects:
total_std = np.std(total_array, axis=0)
total_std = np.reshape(total_std, (8, 8))


################################# 2D non_max ##################################

print ("Load correlation table of each subjects:")
correlation_values_non_max = {}
for i in subject_list:
    correlation_values_non_max[i] = np.loadtxt(file_path + "non_max_correlation_value_%s.txt" % i)
print ("Complete")
print (separator)


# get total average:
num_count = 0
total_average_non_max = np.zeros((8, 8))
total_array_non_max = np.zeros((6, 64))
for key, value in correlation_values_non_max.items():
    nparray = np.array(value)
    total_array_non_max[num_count, :] = nparray
    nparray = np.reshape(nparray, (8, 8))
    total_average_non_max += nparray
    num_count += 1
total_average_non_max = total_average_non_max/num_count

# generate table plot
fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=total_average_non_max.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.2, 0.85, "Non-Max Total correlation between odd runs and even runs", weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "2d_total_correlation_table_non_max.png")

# calculate standard deviation across subjects:
total_std_non_max = np.std(total_array_non_max, axis=0)
total_std_non_max = np.reshape(total_std_non_max, (8, 8))


# generate bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(10, 24))
for plot_num in range(8):
    i = plot_num -1
    ax = plt.subplot(8, 1, plot_num, frameon=False)
    bar_plot1 = ax.bar(ind, total_average[i, :], width, color='teal', yerr=total_std[i, :])
    bar_plot2 = ax.bar(ind+width, total_average_non_max[i, :], width, color='turquoise', yerr=total_std_non_max[i, :])
    # add some label:
    ax.set_ylabel(u"Mean correlation \u00B1 std")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.5, bottom=0.05, top=0.95)
plt.savefig(figure_path + "2d_total_correlation_bar_both.png")

# generate individual bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(12, 5))
for i in range(8):
    ax = plt.subplot(111, frameon=False)
    bar_plot1 = ax.bar(ind, total_average[i, :], width, color='teal', yerr=total_std[i, :])
    bar_plot2 = ax.bar(ind+width, total_average_non_max[i, :], width, color='turquoise', yerr=total_std_non_max[i, :])
    # add some label:
    ax.set_ylabel(u"Mean correlation \u00B1 std")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
    ax.legend((bar_plot1[0], bar_plot2[0]), ('All responding voxels', 'Excluding max responded voxels'), bbox_to_anchor=(0.7, 1.06), loc=2, borderaxespad=0., fontsize=12)
    plt.savefig(figure_path + "2d_total_correlation_bar_both_%s.png" % object_list[i])
    plt.clf()
plt.close()
print ("Correlation tables and bar graphs for 3D analysis are saved")
print (sec_separator)

################################ 3D analysis ##################################
print ("Focus on 3D correlation analysis")
print (separator)
print ("Load correlation table of each subjects:")
correlation_values_for3d = {}
for i in subject_list:
    correlation_values_for3d[i] = np.loadtxt(file_path + "3d_correlation_value_%s.txt" % i)
print ("Complete")
print (separator)


# get total average:
num_count = 0
total_average_for3d = np.zeros((8, 8))
total_array_for3d = np.zeros((6, 64))
for key, value in correlation_values_for3d.items():
    nparray = np.array(value)
    total_array_for3d[num_count, :] = nparray
    nparray = np.reshape(nparray, (8, 8))
    total_average_for3d += nparray
    num_count += 1
total_average_for3d = total_average_for3d/num_count

# generate table plot
fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=total_average_for3d.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.2, 0.85, "3D Total correlation between odd runs and even runs", weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "3d_total_correlation_table.png")

# calculate standard deviation across subjects:
total_std_for3d = np.std(total_array_for3d, axis=0)
total_std_for3d = np.reshape(total_std_for3d, (8, 8))


################################### 3D non_max ##################################

print ("Load correlation table of each subjects:")
correlation_values_non_max_for3d = {}
for i in subject_list:
    correlation_values_non_max_for3d[i] = np.loadtxt(file_path + "3d_non_max_correlation_value_%s.txt" % i)
print ("Complete")
print (separator)


# get total average:
num_count = 0
total_average_non_max_for3d = np.zeros((8, 8))
total_array_non_max_for3d = np.zeros((6, 64))
for key, value in correlation_values_non_max_for3d.items():
    nparray = np.array(value)
    total_array_non_max_for3d[num_count, :] = nparray
    nparray = np.reshape(nparray, (8, 8))
    total_average_non_max_for3d += nparray
    num_count += 1
total_average_non_max_for3d = total_average_non_max_for3d/num_count

# generate table plot
fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=total_average_non_max_for3d.round(4), colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.2, 0.85, "3D Non-Max Total correlation between odd runs and even runs", weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "3d_total_correlation_table_non_max.png")

# calculate standard deviation across subjects:
total_std_non_max_for3d = np.std(total_array_non_max_for3d, axis=0)
total_std_non_max_for3d = np.reshape(total_std_non_max_for3d, (8, 8))

# generate bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(10, 24))
for plot_num in range(8):
    i = plot_num -1
    ax = plt.subplot(8, 1, plot_num, frameon=False)
    bar_plot1 = ax.bar(ind, total_average_for3d[i, :], width, color='mediumslateblue', yerr=total_std[i, :])
    bar_plot2 = ax.bar(ind+width, total_average_non_max_for3d[i, :], width, color='plum', yerr=total_std_non_max[i, :])
    # add some label:
    ax.set_ylabel(u"Mean correlation \u00B1 std")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.5, bottom=0.05, top=0.95)
plt.savefig(figure_path + "3d_total_correlation_bar_both.png")

# generate individual bar plot
ind = np.arange(8)
width = 0.35
fig = plt.figure(figsize=(12, 5))
for i in range(8):
    ax = plt.subplot(111, frameon=False)
    bar_plot1 = ax.bar(ind, total_average_for3d[i, :], width, color='mediumslateblue', yerr=total_std[i, :])
    bar_plot2 = ax.bar(ind+width, total_average_non_max_for3d[i, :], width, color='plum', yerr=total_std_non_max[i, :])
    # add some label:
    ax.set_ylabel(u"Mean correlation \u00B1 std")
    ax.set_title("%s" % object_list[i])
    ax.set_xticks(ind+width)
    ax.set_xticklabels(object_list)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
    ax.legend((bar_plot1[0], bar_plot2[0]), ('All responding voxels', 'Excluding max responded voxels'), bbox_to_anchor=(0.7, 1.06), loc=2, borderaxespad=0., fontsize=12)
    plt.savefig(figure_path + "3d_total_correlation_bar_both_%s.png" % object_list[i])
    plt.clf()
plt.close()


# report
print ("Correlation tables and bar graphs for 3D analysis are saved")
print (separator)
print ("Analysis Complete!!")
print (sec_separator)