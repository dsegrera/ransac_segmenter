import os
import json
import random
import cv2


# this script just randomly samples outputs from the segmenter and creates
# visualization images so we can see if the segmenter is working correctly.
"""
dirs = ['outs/' + flnm for flnm in os.listdir('outs')]
files = []
for dir in dirs:
    fs = [flnm.split('.')[0] for flnm in os.listdir(dir) if 'json' in flnm]
    fs = [flnm.split('_')[0] + '/' + flnm for flnm in fs]
    random.shuffle(fs)
    fs = fs[:5]
    files += fs

random.shuffle(files)
"""
files = ['004952321/004952321_00007']
for flnm in files:
    no_f_flnm = flnm.split('/')[-1] + '.jpg'
    img_name = os.path.join('full_1930_set', flnm + '.jpg')
    points_name = os.path.join('outs', flnm + '.json')
    with open(points_name) as f:
        pts = json.load(f)
        if pts == {}:
            continue
        pts = pts['corners']
    img = cv2.imread(img_name)
    for pt in pts:
        img[pt[1]-6:pt[1]+7, pt[0]-6:pt[0]+7] = (0, 255, 0)
    cv2.imwrite(os.path.join('random_samples', no_f_flnm), img)

