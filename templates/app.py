#!/usr/bin/env python

'''

'''

# Python 2/3 compatibility
from __future__ import print_function
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2

   

class App(object):
    def __init__(self,input_source,window_name = "frame",roi_name = "roi"):
        if isinstance(input_source,str):
            self.video = False
            self.img = cv2.imread(input_source,cv2.IMREAD_COLOR)

        else:
            self.video = True
            self.cap = cv2.VideoCapture(video_src)
#        ret, self.frame = self.cap.read()
        self.window_name = window_name
        self.roi_name = roi_name
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.onmouse)

        self.selection = None
        self.drag_start = None

    def read_frame(self):
        if self.video:
            _,frame = self.cap.read()
            return frame
        else:
            return self.img
        


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
            self.frame = self.read_frame()
            vis = self.frame.copy()
            
            # draw the a rectangle around the roi
            self.draw_roi(vis)
            
            
            # obtain the roi and display it in a new window 
            roi = self.get_roi(self.frame)
            if roi is not None: 
                height = roi.shape[0]
                width = roi.shape[1]
                if height > 0 and width > 0:
                    cv2.imshow(self.roi_name,roi)

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
