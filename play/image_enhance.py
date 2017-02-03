# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 14:50:18 2017

@author: finn
"""

import numpy as np
import cv2
import math
from os import listdir
import random
from lxml import etree as et
    
def rotate(src,angle, scale=1.0):
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians    
    # now calculate new image width and height - these don't seem right at the momment.
    nw = int(math.ceil((abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale))
    nh = int(math.ceil((abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale))
    print(w,h,nw,nh)
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    print(rot_mat)
    rotated = cv2.warpAffine(src, rot_mat, (nw, nh), flags=cv2.INTER_LANCZOS4)
    return (rotated,nw,nh)
    
def add_object(background,obj,obj_name,number,outfolder,minscale = .4,maxscale=.5):
    #cv2.namedWindow('image')
    img = cv2.imread(background)
    obj = cv2.imread(foreground,cv2.IMREAD_UNCHANGED)
    angle = np.random.randint(0,45)
    scale = np.random.uniform(minscale,maxscale)    
    obj,nw,nh = rotate(obj,angle,scale = scale)
    
    # translate to somewhere it still fits
    xnew = np.random.randint(0,img.shape[1] - nw)
    ynew = np.random.randint(0,img.shape[0] - nh)
    
    rows,cols,channels = obj.shape    
    rgb,alpha = obj[:,:,0:3],obj[:,:,3]
    alpha = alpha*1.0/np.max(alpha)
    alpha = np.dstack((alpha,alpha,alpha))
    
    img[0+ynew:rows+ynew,0+xnew:cols+xnew] = rgb*alpha + img[0+ynew:rows+ynew,0+xnew:cols+xnew]*(1-alpha)
    #cv2.rectangle(img,(xnew,ynew),(xnew+nw,ynew+nh),(255,0,0),2) # write image and associated xml metadata    
    #cv2.imshow('image',img)
    
    return img,xnew,ynew,nw,nh
    
import os
def generate_labeled_set(backgrounds,foreground,forground_name,name,outfolder,n = 100):
    background_images = listdir(backgrounds)
    dataset = et.Element("dataset")
    images = et.SubElement(dataset, "images")
    et.SubElement(dataset,"name").text = name
    for i in range(n):
        background = backgrounds+random.choice(background_images)
        img,left,top,width,height = add_object(background,foreground,forground_name,i,outfolder)
        filename = '{obj}_{set_name}{num}.jpg'.format(obj = forground_name,set_name = name,num=i)
        cv2.imwrite(os.path.join(outfolder, filename),img)
        image = et.SubElement(images,"image",file=filename)
        et.SubElement(image,"box",top=str(top),left=str(left),width=str(width),height=str(height))
    
    #tree = et.ElementTree(dataset)
    header = "<?xml version='1.0' encoding='ASCII'?>\n<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>\n"
    
    outfile = outfolder+name+".xml"
    with open(outfile,'w') as out:
        out.write(header)
        out.write(et.tostring(dataset,pretty_print=True))
    #tree.write(outfolder+name+".xml",pretty_print=True,xml_declaration=True)
 
backgrounds = "images/"   
foreground = "rgba3.png"
fname = "croc"
foldername = "crocs/"
generate_labeled_set(backgrounds,foreground,fname,"training",foldername,n=100)
generate_labeled_set(backgrounds,foreground,fname,"testing",foldername,n=50)

