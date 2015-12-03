import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import colors

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
    all_runs[i] = np.loadtxt(file_path + i +".txt")
for i in even_runs:
    all_runs[i] = np.loadtxt(file_path + i +".txt")

#
# even_bottle = np.loadtxt(file_path + "even_bottle.txt")
# even_cat = np.loadtxt(file_path + "even_cat.txt")
# even_chair = np.loadtxt(file_path + "even_chair.txt")
# even_face = np.loadtxt(file_path + "even_face.txt")
# even_house = np.loadtxt(file_path + "even_house.txt")
# even_scissors = np.loadtxt(file_path + "even_scissors.txt")
# even_scrambledpix = np.loadtxt(file_path + "even_scrambledpix.txt")
# even_shoe = np.loadtxt(file_path + "even_shoe.txt")
# odd_bottle = np.loadtxt(file_path + "odd_bottle.txt")
# odd_cat = np.loadtxt(file_path + "odd_cat.txt")
# odd_chair = np.loadtxt(file_path + "odd_chair.txt")
# odd_face = np.loadtxt(file_path + "odd_face.txt")
# odd_house = np.loadtxt(file_path + "odd_house.txt")
# odd_scissors = np.loadtxt(file_path + "odd_scissors.txt")
# odd_scrambledpix = np.loadtxt(file_path + "odd_scrambledpix.txt")
# odd_shoe = np.loadtxt(file_path + "odd_shoe.txt")

# reshape to 3d images
all_3d = {}
for key, txt in all_runs.iteritems():
    all_3d[key] = np.reshape(txt, (-1, 25, 1))

# even_bottle_3d = np.reshape(even_bottle, (-1, 25, 1))
# even_cat_3d = np.reshape(even_cat, (-1, 25, 1))
# even_chair_3d = np.reshape(even_chair, (-1, 25, 1))
# even_face_3d = np.reshape(even_face, (-1, 25, 1))
# even_house_3d = np.reshape(even_house, (-1, 25, 1))
# even_scissors_3d = np.reshape(even_scissors, (-1, 25, 1))
# even_scrambledpix_3d = np.reshape(even_scrambledpix, (-1, 25, 1))
# even_shoe_3d = np.reshape(even_shoe, (-1, 25, 1))
# odd_bottle_3d = np.reshape(odd_bottle, (-1, 25, 1))
# odd_cat_3d = np.reshape(odd_cat, (-1, 25, 1))
# odd_chair_3d = np.reshape(odd_chair, (-1, 25, 1))
# odd_face_3d = np.reshape(odd_face, (-1, 25, 1))
# odd_house_3d = np.reshape(odd_house, (-1, 25, 1))
# odd_scissors_3d = np.reshape(odd_scissors, (-1, 25, 1))
# odd_scrambledpix_3d = np.reshape(odd_scrambledpix, (-1, 25, 1))
# odd_shoe_3d = np.reshape(odd_shoe, (-1, 25, 1))

# generate list for 3d images:
# all_3d = ["odd_%s_3d" % i for i in object_list] + ["even_%s_3d" % i for i in object_list]

# save each 3d image as figure
for key, fig in all_3d.iteritems():
    plt.imshow(fig[:, :, 0], interpolation="nearest", cmap=nice_cmap)
    plt.title("%s" % key)
    plt.savefig(figure_path + "%s.png" % key)

    plt.clf()
plt.close()

# Run correlation:
print ("correlation analysis:")
for i in odd_runs:
    for j in even_runs:
        corr = np.corrcoef(all_runs[i], all_runs[j])
        print ("%s vs %s: %.4f" %(i, j, corr[0, 1]))

print ("Complete!!!")