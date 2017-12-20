#!/usr/bin/python
#coding:utf-8
import Image
import sys
from PyQt4.QtGui import QApplication,QPixmap
from PyQt4.QtCore import Qt
import os

def generateThumb(path,tinypath,height_thumbnail,width_thumbnail):
   print path
   image=Image.open(path)
   image.thumbnail((height_thumbnail,width_thumbnail))
   image.save(tinypath)

# def generateThumb(path,tinypath,thumbWidth,thumbHeight):
#
#     print path
#     maptif = QPixmap(path)
#     maptif.scaled(thumbWidth,thumbHeight)
#     maptif.save(tinypath)
if __name__=="__main__":

    #for f in os.listdir("/opt/Aatt_ObjectDection_fin/images/"):
    #    if "tif" in f:
    #        print f
    f="/opt/Aatt_ObjectDection_fin/images/IPIU_IMAGE_1_9.tif"
    tinyf="/opt/Aatt_ObjectDection_fin/images_tiny/IPIU_IMAGE_1_9.tif"
    #        app = QApplication(sys.argv)
    generateThumb(f,tinyf,576,324)
    #app = QApplication(sys.argv)
    #generateThumb("/opt/Aatt_ObjectDection_fin/images/IPIU_IMAGE_1_6.tif","/opt/Aatt_ObjectDection_fin/images_tiny/IPIU_IMAGE_1_6.tif",324,576)