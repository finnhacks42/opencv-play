# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:35:22 2017

@author: finn
"""

import numpy as np
import cv2
cap = cv2.VideoCapture('incredible_machine.avi')
print cap.isOpened()
while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()