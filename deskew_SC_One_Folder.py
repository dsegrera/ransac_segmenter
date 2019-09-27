#!/bin/bash
import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
from glob import glob
import math
import sys
from time import time



def get_angle(image):
    
    deg = 4000
    blur = cv2.GaussianBlur(image,(5,5),0)
    edges = cv2.Canny(blur, 100, 200)
    
    '''cv2.imshow('eto', blur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    
    thresh = 1500
    while True:
        lines = cv2.HoughLines(edges,1,np.pi/1000,thresh)
        if lines is not None:
            break
        thresh = thresh - 50
        
    for line in lines:
        for rho,theta in line: 
            """
            a = np.cos(theta)
            b = np.sin(theta)

            x0 = a*rho
            y0 = b*rho
            
            x1 = int(x0 + 3000*(-b))
            y1 = int(y0 + 3000*(a))
            x2 = int(x0 - 3000*(-b))
            y2 = int(y0 - 3000*(a))
            cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
            """
            #cv2.imwrite("Lines" + strnum +".jpg", image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            degrees = math.degrees(theta) 
            #print(degrees)
            if degrees > 170 and degrees < 190:
                deg = 180. - degrees     
            if degrees > 80 and degrees < 100:
                deg = 90. - degrees     
            if degrees > 350 or degrees < 10:
                deg = 360. - degrees
            if degrees > 260 and degrees < 280:
                deg = 270. - degrees
            """
            if deg == 4000:
                deg = degrees
                break
            """
    return deg
    

def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def deskew(image):
    
    #cv2.imshow("Rotated" + strnum +".jpg", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    deg = get_angle(image)
    #print (deg)
    deg = -deg
    #print (deg)
    result = rotateImage(image, deg)
    
    """
    deg = -deg
    rows = image.shape[0]
    cols = image.shape[1]
    
    print(deg)
    
    matrix = cv2.getRotationMatrix2D((cols,rows),deg,1)
    rotated = cv2.warpAffine(image,matrix,(cols,rows))
    """
     
    #cv2.imshow('eto', image)
    #cv2.imwrite("lines" + strnum +".jpg", image)

    cv2.imwrite("/fslhome/coryhunt/fsl_groups/fslg_handwriting/compute/cropped_1930_full/" + "Rotated_" + strnum +".jpg", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

               

if __name__ == "__main__":   
    os.chdir("full_1930_set/004949546")
    #num = 1
    for file in glob('*.jpg'):
        start_loop = time()
        #strnum = file + str(num)
        strnum = os.path.splitext(file)[0]
        image = cv2.imread(file)
        deskew(image)

    
        #num = num + 1