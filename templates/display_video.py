# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:44:27 2017

@author: finn
"""

import cv2
import sys
import cvutil as u

cap = u.source_video(sys.argv)

while(True):
    _, frame = cap.read()

    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break
    
cv2.destroyAllWindows()
