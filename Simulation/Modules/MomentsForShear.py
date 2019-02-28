#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 15:31:22 2019

@author: FCRA
"""
from math import *
import numpy as np
import matplotlib.pyplot as plt
#from reactionforces import reaction_forces
from MOI import get_Izz, get_Iyy

#DATA 
exec(open("./Data.txt").read())

Izz = get_Izz()
Iyy = get_Iyy()


Rv = 42.514104
Rw = 87.166683
React = sqrt((Rv**2) + (Rw**2))

ang = theta*pi/180

R = h/2

#location x ACTUATOR1
x_a1 = la/2 - xa/2
#location x ACTUATOR2
x_a2 = la/2 + xa/2

marg_act = xa/5              #width of actuator assumed to a fracton of the distance between actuators         

lim1_a1 = x_a1 - marg_act
lim2_a1 = x_a1 + marg_act
lim1_a2 = x_a2 - marg_act
lim2_a2 = x_a2 + marg_act

print x_a1, la, x_a2, lim1_a1, lim2_a1, lim1_a2, lim2_a2

x = np.linspace(0, la, 100)
for i in range(len(x)):
    y = round(x[i], 4)
    x[i] = y

def get_Mx():
    
    M_fx = []
    
    for i in range(len(x)):
    
        if lim1_a1 < x[i] <= lim2_a1: 
            M_x = -q*cos(ang)*(0.25*Ca-R) - P*cos(ang)*R + P*sin(ang)*R
            
    
        elif lim1_a2 < x[i] < lim2_a2:
            M_x = -q*cos(ang)*(0.25*Ca-R) +87.166831*R - 42.5141*R   
            
#        
        else: 
            M_x = -q*cos(ang)*(0.25*Ca-R)
            
        M_fx.append(-M_x)
        
    return M_fx

M_fx = get_Mx()
#
print max(M_fx), min(M_fx)
#        
plt.figure()
plt.plot(x, M_fx)
plt.show()
    
    
