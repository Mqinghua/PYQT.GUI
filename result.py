#!/usr/bin/python
#coding:utf-8

print "图像处理完毕"
runtime = "???unknown"
plane = 0
ship = 0
def traversalfile():
    global plane,ship,runtime
    Number(plane,"plane")
    Number(ship,"ship")
def Number(number,kind):    
    labels = []
    for f in os.listdir("/opt/Aatt_ObjectDection_fin/pre_deal_image/"+kind+"/"):
        if "png" in f:
            labels.append(f)
    number = len(labels)
     


