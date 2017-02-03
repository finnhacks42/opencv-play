# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 20:29:37 2016

@author: finn
"""



def foo(func):
    func(42)
    
def bar(x,y):
    x[0] = y

def main():
    x = [3]
    foo(lambda y:bar(x,y))
    print x
    
main()
    

