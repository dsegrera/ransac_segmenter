import cv2
from os.path import join
import os
import json
import sys
from random import shuffle
from random import randint

#import torch

imgs_path = sys.argv[1]
json_dir = sys.argv[2]
out_dir = sys.argv[3]
option = sys.argv[4]

ranges = [join(json_dir, flnm) for flnm in os.listdir(json_dir) if 'json' in flnm]
shuffle(ranges)
for flnm in ranges:
    imgnum = flnm.split('/')[-1].split('.')[0]
    with open(flnm) as f:
        columns = json.load(f)
    in_img_path = (imgs_path + imgnum + '.jpg')
    img = cv2.imread(in_img_path)
    try:
        if option == "ranges":
            for column in columns['corners']:
                for cell in column:
                    red = randint(0, 255)
                    green = randint(0, 255)
                    blue = randint(0, 255)
                    img[cell[3] - 5:cell[3], cell[0]:cell[1]] = (red, green, blue)
                    img[cell[2]:cell[2] + 5, cell[0]:cell[1]] = (red, green, blue)
                    img[cell[2]:cell[3], cell[0]:cell[0] + 5] = (red, green, blue)
                    img[cell[2]:cell[3], cell[1] - 5:cell[1]] = (red, green, blue)

        elif option == "points":
            for cell in columns['corners']:
                img[int(cell[1])-1:int(cell[1])+1, int(cell[0])-1:int(cell[0])+1] = (0, 255, 0)

    except KeyError:
        print("Key Error: reading " + flnm)
    out_img_path = out_dir + 'test_' + imgnum + '.jpg'
    cv2.imwrite(out_img_path, img)
