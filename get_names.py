# This script should be placed in the top level folder in which the labelmefacade dataset is
import os

path = os.getcwd()+"/"
# where segmented images and .txt files with bounding box info are
label_folder = "cam0_segmented/"
# where original images are
image_folder = "cam0_original/"
postfix="\n"

label_names = os.listdir(path+label_folder)
image_names = os.listdir(path+image_folder)
for name in label_names:
    name = name.split(".")[0]
for name in image_names:
    name = name.split(".")[0]
valid_names = set(label_names).intersection(set(image_names))

ftest = open(path+"test.txt", "wt")
ftrain = open(path+"train.txt", "wt")
iter = 0

for name in valid_names:
    if iter < 100:
        ftest.write(path+image_folder+name+postfix)
        iter += 1
    else:
        ftrain.write(path+image_folder+name+postfix)

ftest.close()
ftrain.close()
