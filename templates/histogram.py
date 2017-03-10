# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 14:58:36 2017

@author: finn
"""

# need details about HSV and the ranges of the values that it can contain. 



import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("../images/cow3.jpg")

cv2.imshow("image",img)

HSL
HSV



def plot_1Dhistogram(img,nbins):
    # plot 1D histograms for each chanel
    nbins = 256
    color = ('blue','green','red')
    for i,c in enumerate(color):
        hist = cv2.calcHist([img],[i],None,[nbins],[0,256]) # range is the range of values you care about - pixels outside this range get ignored.
        plt.plot(hist,color=c,label = c)
    plt.legend(loc="upper right")
    plt.show(block=False)



# plot 2d histograms





cv2.waitKey(0)
cv2.destroyAllWindows()