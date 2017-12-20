#!/usr/bin/python
#coding:utf-8
import os
print "获得时间图片数等"
runtime = "how to get time?"
plane = 0
ship = 0
def traversalfile():
    global plane,ship,runtime
    Number("plane")
    Number("ship")
def Number(kind):    
    global plane,ship,runtime
    labels = []
    for f in os.listdir("/opt/Aatt_ObjectDection_fin/pre_deal_image/"+kind+"/"):
        if "png" in f:
            labels.append(f)
    if kind=="plane":
        plane = len(labels)
    else:
        ship = len(labels)



