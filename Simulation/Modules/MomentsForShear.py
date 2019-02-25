#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 15:31:22 2019

@author: FCRA
"""
from math import *
import numpy as np
import matplotlib.pyplot as plt
from reactionforces import reaction_forces

#DATA 
exec(open("./Data.txt").read()) 


React = reaction_forces()[-1]
ang = theta*pi/180

R = h/2

#location x hinge1
x_h1 = Ca/2 - xa/2
#location x hinge2
x_h2 = Ca/2 + xa/2

marg_act = xa/10             #width of actuator assumed to a fracton of the distance between actuators         

lim1_h1 = x_h1 - marg_act
lim2_h1 = x_h1 + marg_act
lim1_h2 = x_h2 - marg_act
lim2_h2 = x_h2 + marg_act

#print Ca, x_h1, x_h2, lim1_h1, lim2_h1, lim1_h2, lim2_h2


x = np.linspace(0, Ca, 100)
for i in range(len(x)):
    y = round(x[i], 4)
    x[i] = y



def get_Mx():
    
    M_fx = []
    
    for i in range(len(x)):
    
        if lim1_h1 < x[i] <= lim2_h1: 
            M_x = -q*cos(ang)*(0.25*Ca-R) - P*cos(ang)*R + P*sin(ang)*R
            
    
        elif lim1_h2 < x[i] < lim2_h2:
            M_x = -q*cos(ang)*(0.25*Ca-R) -React*cos(ang)*R + React*sin(ang)*R   
            
#        
        else: 
            M_x = -q*cos(ang)*(0.25*Ca-R)
            
        M_fx.append(M_x)
        
    return M_fx

M_fx = get_Mx()

print len(M_fx), len(x)
        
plt.figure()
plt.plot(x, M_fx)
plt.show()
#    
    