import sys
import os
import json
import xml.etree.ElementTree as ET

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

if len(sys.argv) == 2:
    classes = {}
    with open(os.path.dirname(os.path.abspath(__file__))+"/data/predefined_classes.txt", "r") as f:
        num = 0
        for line in f:
            classes[line[:-1]] = num
            num += 1
    with open(sys.argv[1]+'/visim_project.json', 'r') as data:
        intrinsics = json.load(data)
    height = int(intrinsics["cameras"][0]["height"])
    width = int(intrinsics["cameras"][0]["width"])
    ldir = sys.argv[1]+"/output/3_labelimg"
    for name in os.listdir(ldir):
        if name.endswith(".xml"):
            yolo = open(ldir+"/"+name.split(".")[0]+".txt", "w")
            tree = ET.parse(ldir+"/"+name)
            root = tree.getroot()
            for obj in root.findall("object"):
                cname = obj[0].text
                umin = int(obj[4][0].text)
                vmin = int(obj[4][1].text)
                umax = int(obj[4][2].text)
                vmax = int(obj[4][3].text)
                bb = convert((width,height), (umin, umax, vmin, vmax))
                yolo.write(str(classes[cname])+" "+ " ".join([str(a) for a in bb]) + '\n')
            yolo.close()
else:
    print("Script needs exactly one argument -- the path to the top level directory of the project")
