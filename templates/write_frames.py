# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:44:27 2017

@author: finn
"""

import cv2
import sys
import cvutil as u


cap = u.source_video(sys.argv)

count = 0
while(count < 10):
    count +=1
    _, frame = cap.read()
    cv2.imshow('frame',frame)
    cv2.imwrite("../videos/frames/frame_{0}.png".format(count),frame)
    
cv2.destroyAllWindows()
