# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 14:24:53 2017

@author: finn
"""

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os


def get_soup(url):
    return BeautifulSoup(requests.get(url).text)

image_type = "messy_table_top"
query = "messy+table+top"
url = "http://www.bing.com/images/search?q=" + query + "&qft=+filterui:imagesize-large&FORM=R5IR3" #+filterui:color2-bw

soup = get_soup(url)
images = [a['src'] for a in soup.find_all("img", {"src": re.compile("mm.bing.net")})]

for img in images:
    raw_img = urllib2.urlopen(img).read()
    cntr = len([i for i in os.listdir("images") if image_type in i]) + 1
    f = open("images/" + image_type + "_"+ str(cntr), 'wb')
    f.write(raw_img)
    f.close()