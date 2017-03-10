# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:44:27 2017

@author: finn
"""

import cv2
import sys

args = sys.argv
if len(args) > 1:
    source = args[1]
else:
    source = 0

cap = cv2.VideoCapture(source)
while(True):

    _, frame = cap.read()
    cv2.imshow('frame',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break
    
cv2.destroyAllWindows()
