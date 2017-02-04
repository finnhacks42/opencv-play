# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:44:27 2017

@author: finn
"""

import cv2


# Load an color image in grayscale
#cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
#cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
#cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel
img = cv2.imread('../images/ship.jpg',cv2.IMREAD_COLOR)
cv2.imshow('image',img)

xmin,ymin,xmax,ymax = 0,0,40,300
roi = img[ymin:ymax,xmin:xmax]


 # calculating object histogram
                    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
                    roihist = cv2.calcHist(images = [hsv],channels = [0, 1,2], mask = None, histSize = [180, 256,180], ranges = [0, 180, 0, 256,0,180] )
                    hsvt = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
 
                    # normalize histogram and apply backprojection
                    cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
                    dst = cv2.calcBackProject([hsvt],[0,1,2],roihist,[0,180,0,256,0,180],1)
                    #disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
                    #cv2.filter2D(dst,-1,disc,dst)
                    cv2.imshow("diff",dst)

                    target = self.frame.copy()

                    # threshold and binary AND
                    #ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
                    ret,thresh = cv2.threshold(dst,1,255,cv2.THRESH_BINARY)
                    thresh = cv2.merge((thresh,thresh,thresh))
                    res = cv2.bitwise_and(target,thresh)

                    #res = np.dstack((target,thresh,res))
                    cv2.imshow('res',thresh)


cv2.waitKey(0) # close when any key pressed
cv2.destroyAllWindows()

