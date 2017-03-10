# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 21:56:43 2017

@author: finn
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(ax,img,channels,title,legend_loc = "upper left"):
    """
    ax: the axis on which you want to plot the histogram
    img: the image to compute the histogram from
    channels: the names fo the channels in the image
              could be ['blue','green','red'] or ['hue','saturation','value'] or ['grey']
    title: the title to give the axis
    """
    plot_settings = {
        "blue":("blue",255),
        "green":("green",255),
        "red":("red",255),
        "hue":("violet",180),
        "saturation":("orange",255),
        "value":("cyan",255),
        "luminosity":("brown",255),
        "grey":("black",255)
        }
    for i,c in enumerate(channels):
        settings = plot_settings.get(c)
        if settings is not None:
            color,channel_max = settings
        else:
            color,channel_max = None,255
            
        hist = cv2.calcHist([img],channels = [i],mask = None, histSize = [channel_max],ranges=[0,channel_max])
        ax.set_xlim(0,channel_max)
        ax.set_title(title)
        ax.plot(hist,color = color,label = c)
    ax.legend(loc=legend_loc)
    return ax
    

def make_hsv(height=179):
    """ 
    create an image with hue in the background.
    returns: hsv image
    """
    hsv = np.zeros((height,179,3),dtype=np.uint8)
    hsv[:,:,0] = np.arange(0,179)
    hsv[:,:,1] = 255
    hsv[:,:,2] = 255
    return hsv

    
def plot_hsv_hist(ax,hsv):
    """ 
    plot counts by hue with the hue colors in the background.
    ax: the axes on which to plot the histogram. 
    hsv: the image to compute the histogram for.
    """
    hist = cv2.calcHist([hsv],channels = [0],mask = None, histSize = [180],ranges=[0,180])
    hist = 180*hist/max(hist)
    ax.set_xlim(0,180)
    ax.set_title("HSV")
    background = cv2.cvtColor(make_hsv(),cv2.COLOR_HSV2RGB)
    ax.tick_params(axis="y",which="both",left="off",labelleft="off")    
    ax.imshow(background,extent=[0,180,0,180])
    ax.plot(hist,color = "black",lw=2)  
   
    
def plot_1d_histograms(img):
    """
    Plot 1d histograms for each channel of rgb, hsv, hls and greyscale.
    """
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hls = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
    grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    fix,ax = plt.subplots(1,4,figsize=(20,4))
    plot_histogram(ax[0],img,["blue","green","red"],"BGR")
    plot_histogram(ax[1],hsv,["hue","saturation","value"],"HSV")
    plot_histogram(ax[2],hls,["hue","luminosity","saturation"],"HLS")
    plot_histogram(ax[3],grey,["grey"],"Greyscale")
    
def hueDifference(hsv,hue, invert=False):
    """
    Returns an image with each pixel proportional to the difference between the image hue channel and specified hue value.
    The difference accounts the fact that hue lies on a cylinder, and resulting values will lie within (0,180).
    hsv: input image in hsv format
    hue: the hue to take the difference from
    invert: if True then invert the image such that closest matching pixels are returned with highest intensity (white)
    """
    hue_channel = np.int16(hsv[:,:,0].copy())  
    diff = np.absolute(hue_channel-hue)
    diff = ((np.minimum(diff,180 - diff))*255/90.0).astype("uint8")
    if invert:
        diff = 255-diff
    return diff

def hsvInRange(hsv,lower,upper):
    """
    An equivelent to inRange that accounts for the fact that hsv loops. 
    So you can pass a range for hue in which lower is higher than upper (for example 170,10 to get red things)
    Returns 255 if the pixel is in the specified range for all channels, 0 otherwise.
    lower: a tuple containing the bottom of the range for each channel
    upper: a tuple containing the upper end of the range for each channel
    """
    hlower,slower,vlower = lower
    hupper,supper,vupper = upper
    if hupper > hlower:
        return cv2.inRange(hsv,lower,upper)
    
    mask1 = cv2.inRange(hsv,np.asarray([hlower,slower,vlower]),np.asarray([180,supper,vupper]))
    mask2 = cv2.inRange(hsv,np.asarray([0,slower,vlower]),np.asarray([hupper,supper,vupper]))
    return np.bitwise_or(mask1,mask2)


    
