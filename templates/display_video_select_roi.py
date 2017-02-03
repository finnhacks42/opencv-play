#!/usr/bin/env python

'''
Camshift tracker
================

This is a demo that shows mean-shift based tracking
You select a color objects such as your face and it tracks it.
This reads from video camera (0 by default, or the camera number the user enters)

http://www.robinhewitt.com/research/track/camshift.html

Usage:
------
    camshift.py [<video source>]

    To initialize tracking, select the object with mouse

Keys:
-----
    ESC   - exit
    b     - toggle back-projected probability visualization
'''

# Python 2/3 compatibility
from __future__ import print_function
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2


# TODO consider making this a utility class that works for images or video    

class App(object):
    def __init__(self, video_src,window_name = "frame",roi_name = "roi"):
        self.cap = cv2.VideoCapture(video_src)
        ret, self.frame = self.cap.read()
        self.window_name = window_name
        self.roi_name = roi_name
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.onmouse)

        self.selection = None
        self.drag_start = None


    def onmouse(self, event, x, y, flags, param):
        """ gets called evertime a mouse button is clicked or the mouse is moved over the image"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
 
        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])
            self.selection = (xmin, ymin, xmax, ymax)
            
        if event == cv2.EVENT_LBUTTONUP:
            self.drag_start = None
            
    
    def draw_roi(self,img):
        """ 
        draws a blue rectange around the selected region onto the input image: img.
        Note: modifies img 
        """
        
        if self.selection:
            xmin,ymin,xmax,ymax = self.selection
            cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(255,0,0),2)
             
    def get_roi(self,img):
        if self.selection:
            xmin,ymin,xmax,ymax = self.selection
            return img[ymin:ymax, xmin:xmax]
        
            
    def run(self):
        """ Runs a loop, repeatedly getting video/images and displaying them and any selected region of interest """
        
        while True:
            ret, self.frame = self.cap.read()
            vis = self.frame.copy()
            
            # draw the a rectangle around the roi
            self.draw_roi(vis)
            
            
            # obtain the roi and display it in a new window 
            roi = self.get_roi(vis)
            if roi is not None: 
                height = roi.shape[0]
                width = roi.shape[1]
                if height > 0 and width > 0:
                    cv2.imshow(self.roi_name,roi)
               
            
            # show the full image
            cv2.imshow(self.window_name, vis)

            # check to see if a key has been pressed and if its a 'q' then exit the run loop
            ch = cv2.waitKey(5)
            if ch == ord('q'):
                break
            
        cv2.destroyAllWindows()


if __name__ == '__main__':
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print(__doc__)
    App(video_src).run()
