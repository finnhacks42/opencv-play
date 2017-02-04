# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:44:27 2017

@author: finn
"""

import cv2
from matplotlib import pyplot as plt

# Load an color image in grayscale
#cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
#cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
#cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel
target = cv2.imread('../images/ship.jpg',cv2.IMREAD_COLOR)
cv2.imshow('image',target)

xmin,ymin,xmax,ymax = 0,0,40,300
roi = target[ymin:ymax,xmin:xmax]

 # calculating object histogram
hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
channels = [0,2]
nbins = [180,180]
ranges = [0,180,0,180]
roihist = cv2.calcHist(images = [hsv],channels = channels, mask = None, histSize = nbins, ranges = ranges )

color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([hsv],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()


plt.imshow(roihist,interpolation = 'nearest')
plt.show()
# normalize histogram and apply backprojection
cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsvt],channels,roihist,ranges,1)              
cv2.imshow("diff",dst)


# threshold and binary AND
#ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
#ret,thresh = cv2.threshold(dst,1,255,cv2.THRESH_BINARY)
#thresh = cv2.merge((thresh,thresh,thresh))
#res = cv2.bitwise_and(target,thresh)

#res = np.dstack((target,thresh,res))
#cv2.imshow('res',thresh)


cv2.waitKey(0) # close when any key pressed
cv2.destroyAllWindows()

