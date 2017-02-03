# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 19:29:24 2017

@author: finn
"""

import cv2

img = cv2.imread('cow1.jpg')
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()