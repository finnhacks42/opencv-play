# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 14:55:42 2016

@author: finn
"""

# Divide the entire image up into squares. Calculate the mean and standard deviation of the hue in each square. 
# Merge squares with means within the standard deviation
# Complete ..

# cluster pixels via kmeans (for example)

#retvel, t_minus_thresh = cv2.threshold(t_minus, 0, 255, cv2.THRESH_OTSU)
#t_minus_dilate = cv2.dilate(t_minus_thresh, es)

import numpy as np
import cv2


class OutlineFinder(object):
    def __init__(self):
        self.threshold = 0
        self.min_contour_area = 0
    
    def find_outlines(self,filtered_diff):
        cframe = filtered_diff.copy()
        _,cframe = cv2.threshold(cframe,self.threshold,255,cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(cframe.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = []
        for i, cnt in enumerate(contours):
            if hierarchy[0,i,3] == -1 and cv2.contourArea(cnt) > self.min_contour_area:
                cnts.append(cnt)

        backtorgb = cv2.cvtColor(cframe,cv2.COLOR_GRAY2RGB)     
        cv2.drawContours(backtorgb, cnts, -1, (0, 255, 0), 2)
        cv2.imshow('diffed',backtorgb)        
        return cnts
    
    def save_outlines(self,frame,cnts):
        mask = np.zeros(frame.shape[0:-1],np.uint8)
        cv2.drawContours(mask, cnts, -1, (1, 1, 1), -1) # setting linewidth to -1 leads to filled contours
        b_channel, g_channel, r_channel = cv2.split(frame)
        img_RGBA = cv2.merge((b_channel, g_channel, r_channel, mask*255))
        for indx,cnt in enumerate(cnts):   
            x,y,w,h = cv2.boundingRect(cnt)
            crop = img_RGBA[y:(y + h), x:(x + w)]
            cv2.imwrite('rgba'+str(indx)+".png",crop) # make this a section
            
    def set_threshold(self,thresh):
        self.threshold = thresh
    
    def set_min_contour_area(self,area):
        self.min_contour_area = area
    

def hsv_diff(frame, last_frame,h,s,v):
    """ compute a difference that puts most emphasis on changes in color """
    total = float(h+s+v)
    if total == 0:
        h,s,v = 1/3.0,1/3.0,1/3.0
    else:
        h = h/total
        s = s/total
        v = v/total
    
    fh,fs,fv = cv2.split(frame)
    lh,ls,lv = cv2.split(last_frame)
    dh,ds,dv = fh - lh, fh - lh, fv - lv

#    cv2.imshow('h',dh)
#    cv2.imshow('s',ds)
#    cv2.imshow('v',dv)
    
    return dh #h*dh+s*ds+v*dv
    
h = 1
s = 1
v = 1
    
def set_h(x):
    global h
    h = x

def set_s(x):
    global s
    s = x

def set_v(x):
    global v
    v = x

def main(): 
    outline_finder = OutlineFinder()
    cap = cv2.VideoCapture(0)
   
    cv2.namedWindow('frame')
    cv2.namedWindow('diffed')
    cv2.namedWindow('difference')
#    cv2.namedWindow('h')
#    cv2.namedWindow('s')
#    cv2.namedWindow('v')
#    cv2.createTrackbar('h','difference',0,100,set_h)
#    cv2.createTrackbar('s','difference',0,100,set_s)
#    cv2.createTrackbar('v','difference',0,100,set_v)

    cv2.createTrackbar('threshold','diffed',0,255,lambda x:outline_finder.set_threshold(x))
    cv2.createTrackbar('minimum area','diffed',0,1000,lambda x:outline_finder.set_min_contour_area(x))
    frame = cap.read()[1]
    last_gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    last_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    while(True):
        ret, frame = cap.read()
        cv2.imshow('frame',frame)   
        if not ret:
            break
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('c'):
            last_gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            last_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        
        if key == ord('a'):
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            print('hsv shape',hsv.shape)
            #diff = hsv_diff(hsv,last_hsv,h,s,v) 
            #diff = cv2.bitwise_not(diff)
            
            diff = cv2.absdiff(gray, last_gray)
            cv2.imshow('difference',diff)
            
            cframe = cv2.bilateralFilter(diff, 10, 50, 50)
        
            while(True):
                cnts = outline_finder.find_outlines(cframe)
                key = cv2.waitKey(3) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    outline_finder.save_outlines(frame,cnts)
                    break
            last_gray = gray
            last_hsv = hsv
                    
        elif key == ord('q'):
            print("quitting")
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


main()
 

 
 

