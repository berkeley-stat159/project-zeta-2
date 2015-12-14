# import important packages
import os

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