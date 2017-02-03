# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:30:49 2017

@author: finn
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io

cv2.namedWindow('bgr')
cv2.namedWindow('hsv')
img = cv2.imread('blocks2.jpg')
#img = cv2.medianBlur(img,5)
img = cv2.GaussianBlur(img,(5,5),0)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

segments = slic(h, n_segments = 100, sigma = 5)
 
# show the output of SLIC
fig = plt.figure("Superpixels -- %d segments" % (100))
ax = fig.add_subplot(1, 1, 1)
ax.imshow(mark_boundaries(img, segments))
plt.axis("off")
plt.show()

# think about the fact that h is a circle. 
# plot a histogram/kde of intensity. 
#hist = cv2.calcHist([hsv], [0],mask = None, histSize=[180],ranges=[0,180])
#plt.plot(hist)
#plt.xlim([0,256])
#plt.show()

cv2.imshow('bgr',img)
cv2.imshow('hsv',h)

cv2.waitKey(0)
cv2.destroyAllWindows()


#    last_gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
#    last_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#    while(True):
#        ret, frame = cap.read()
#        cv2.imshow('frame',frame)   
#        if not ret:
#            break
#        
#        key = cv2.waitKey(1) & 0xFF
#        
#        if key == ord('c'):
#            last_gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
#            last_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#        
#        if key == ord('a'):
#            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#            print('hsv shape',hsv.shape)
#            #diff = hsv_diff(hsv,last_hsv,h,s,v) 
#            #diff = cv2.bitwise_not(diff)
#            
#            diff = cv2.absdiff(gray, last_gray)
#            cv2.imshow('difference',diff)
#            
#            cframe = cv2.bilateralFilter(diff, 10, 50, 50)
#        
#            while(True):
#                cnts = outline_finder.find_outlines(cframe)
#                key = cv2.waitKey(3) & 0xFF
#                if key == ord('q'):
#                    break
#                elif key == ord('s'):
#                    outline_finder.save_outlines(frame,cnts)
#                    break
#            last_gray = gray
#            last_hsv = hsv
#                    
#        elif key == ord('q'):
#            print("quitting")
#            break
#    
#    # When everything done, release the capture
#    cap.release()
#    cv2.destroyAllWindows()