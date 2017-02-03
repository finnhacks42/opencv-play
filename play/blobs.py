# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 10:11:32 2016

@author: finn
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(1)
#cv2.namedWindow('blobs')

# Set up the detector with parameters.
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 0
params.maxThreshold = 200
params.thresholdStep = 30
params.minDistBetweenBlobs = 50
params.filterByArea = False
#params.minArea = 1500
params.filterByCircularity = False
#params.minCircularity = 0.1
params.filterByConvexity = False
#params.minConvexity = 0.87
params.filterByInertia = False
#params.minInertiaRatio = 0.01
detector = cv2.SimpleBlobDetector_create(params)


        
while(True):
    frame = cv2.imread('blob_frames/blob.png',0)
    #frame = cv2.bitwise_not(frame)
    frame = cv2.bilateralFilter(frame, 10, 50, 50)
    #_, frame = cv2.threshold(frame,200,255,cv2.THRESH_BINARY)
    _, frame = cv2.threshold(frame,70,255,cv2.THRESH_BINARY)
    #frame = cv2.Canny(frame, 30, 200)

    im2, contours, hierarchy = cv2.findContours(frame.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    top_level = []
    for i in range(len(contours)):
        if hierarchy[0,i,3] == -1:
            top_level.append(contours[i])
    
    
    cnts = sorted(top_level, key = cv2.contourArea, reverse = True)[:]
    
    backtorgb = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(backtorgb, cnts, -1, (0, 255, 0), 3)
    
    cv2.imshow("frame", backtorgb)
   
    key = cv2.waitKey(1) & 0xFF   
    if key == ord('q'):
        print("quitting")
        break
    