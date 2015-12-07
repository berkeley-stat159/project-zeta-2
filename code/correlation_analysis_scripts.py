import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
# from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})

#object_list
object_list = ["bottle", "cat", "chair", "face", "house", "scissors", "scrambledpix", "shoe"]

# important path:
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")
figure_path = os.path.join(base_path, "code", "images", "")
file_path = os.path.join(base_path, "code", "txt", "")

# color display
nice_cmap_values = np.loadtxt(file_path + 'actc.txt')
nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')

# generate list for odd and even run values:
odd_runs = ["odd_%s" % i for i in object_list]
even_runs = ["even_%s" % i for i in object_list]

# load even and odd run results
all_runs = {}
for i in odd_runs:
    all_runs[i] = np.loadtxt(file_path + i + ".txt")
for i in even_runs:
    all_runs[i] = np.loadtxt(file_path + i + ".txt")


# reshape to 3d images
all_3d = {}
for key, txt in all_runs.iteritems():
    all_3d[key] = np.reshape(txt, (-1, 25, 1))

# save each 3d image as figure
for key, fig in all_3d.iteritems():
    plt.imshow(fig[:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.title("%s" % key)
    plt.savefig(figure_path + "%s.png" % key)
    plt.clf()
plt.close()

# save all 3d images as one compiled figure
fig = plt.figure(figsize=[8.0, 5])
i = 1
for item in object_list:
    plt.subplot(2, 8, i)
    plt.imshow(all_3d["odd_%s" % item][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.title("%s" % item, fontsize=8, weight='bold')
    plt.axis('off')
    i += 1
for item in object_list:
    plt.subplot(2, 8, i)
    plt.imshow(all_3d["even_%s" % item][:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.axis('off')
    i += 1
plt.subplots_adjust(left=0.15, wspace=0.2, hspace=0.1, bottom=0.05, top=0.835)
# label the figure:
fig.text(0.03, 0.625, 'Odd runs', ha='left', weight='bold')
fig.text(0.03, 0.225, 'Even runs', ha='left', weight='bold')
fig.text(0.16, 0.93, 'Average brain images for odd euns / even runs', fontsize=16, weight='bold')
plt.savefig(figure_path + "odd_even_compile.png")
plt.close()

# Run correlation:
all_results = []
print ("correlation analysis:")
for i in odd_runs:
    result = []
    for j in even_runs:
        corr = np.corrcoef(all_runs[i], all_runs[j])
        result.append("%.4f" % corr[0, 1])
        print ("%s vs %s: %.4f" % (i, j, corr[0, 1]))
    all_results.append(result)

table_result = np.array(all_results)

# make table to display the correlation:

fig = plt.figure(figsize=(8, 4))
plt.subplot(111, frameon=False, xticks=[], yticks=[])
table = plt.table(cellText=table_result, colLabels=object_list, rowLabels=object_list, loc='center', cellLoc='center')
plt.subplots_adjust(left=0.3, bottom=0, top=0.95)
fig.text(0.55, 0.75, 'Odd runs', ha='left', fontsize=12)
fig.text(0.05, 0.52, 'Even runs', ha='left', rotation=90, fontsize=12)
fig.text(0.3, 0.85, "Correlation between odd runs and even runs", weight='bold')
table.scale(1.2, 1.2)
plt.savefig(figure_path + "correlation_table.png")

print ("Complete!!!")