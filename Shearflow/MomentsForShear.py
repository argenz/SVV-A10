#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 15:31:22 2019

@author: FCRA
"""
from math import *
import numpy as np

#DATA 
exec(open("./Data.txt").read()) 

P = 1
React = 1
q = 1
ang = 1

R = h/2

#location x hinge1
x_h1 = Ca/2 - xa/2
#location x hinge2
x_h2 = Ca/2 + xa/2



x = np.linspace(0, Ca, 100000)

def get_Mx():
    
    if x == x_h1: 
        M_x = -q*cos(ang)*(0.25*Ca-r) -P*cos(ang)*R + P*sin(ang)*R
        
    if x == x_h2:
        M_x = -q*cos(ang)*(0.25*Ca-r) -React*cos(ang)*R + React*sin(ang)*R   
    
    else: 
        M_x = -q*cos(ang)*(0.25*Ca-r)
    return M_x
        
        
    
    