#!/usr/bin/python
#coding:utf-8

#from PIL import Image
#import numpy as np
#import matplotlib.pyplot as plt
#img=np.array(Image.open('../images/IPIU_IMAGE_0_1.tif'))  

import cv2

picheight=""
picwidth=""
def get(path):
    global picheight,picwidth
    img = cv2.imread(path)
    try:
       sp = img.shape
    except AttributeError:
       sp=[0,0]
       sp[0]=11651*11
       sp[1]=7767*15
    picheight = '%d' % sp[0]  # height(rows) of image
    picwidth = '%d' % sp[1]  # width(colums) of image
#get('../images/IPIU_IMAGE_0_1.tif')