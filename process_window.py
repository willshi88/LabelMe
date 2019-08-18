# This script should be placed in the top level folder in which the labelmefacade dataset is

import os
import numpy as np
import cv2

path = os.getcwd()+"/"
# where the segmented images are stored
seg_folder = "cam0_segmented/"
# where the .txt files with bounding box info are
label_folder = "cam0_segmented/"

# the conversion function is taken from the darknet repo
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

names = os.listdir(path+seg_folder)
for name in names:
    img = cv2.imread(path+seg_folder+name)
    # pay attention to element order given by .shape!
    height, width, channel = img.shape
    # convert RGB to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # apply threshold so only window/blue sections in the segmented image are left
    blue_lower = np.array([110,150,0])
    blue_upper = np.array([130,255,255])
    mask=cv2.inRange(hsv,blue_lower,blue_upper)

    # find all window/blue sections
    img, contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    out_file = open(path+label_folder+"%s.txt"%(name.split(".")[0]), 'w')
 
    # output the bounding boxed associated with the contours
    for contour in contours:
        [x,y,w,h] = cv2.boundingRect(contour)
        b = (float(x), float(x+w), float(y), float(y+h))
        bb = convert((width,height), b)
        out_file.write("0 " + " ".join([str(a) for a in bb]) + '\n')
