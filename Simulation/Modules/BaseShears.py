#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:29:10 2019

@author: FCRA
"""
from math import *  
import numpy as np
from centroid import centroid
from MOI import Izz, Iyy, Iyz
import matplotlib.pyplot as plt


########### Calculation of base shears #########

#INPUTS:
exec(open("./Data.txt").read())   
R = h/2

zneg = Ca - R
gamma = atan(R/zneg)

Izz = Izz()
Iyy = Iyy()
Iyz = Iyz()

niter = 100

#defining coordinates for first cell
theta = np.linspace(0, pi/4, niter)
zcoor14 = R*np.cos(theta)
ycoor14 = R*np.sin(theta)

def get_baseshear(Sz, Sy):
#Base shear flow 1, from cut at LE on z axis to y axis above hinge line
    L_le = 2*pi*(h/2.)*(180./360.) 
    s_le = L_le/2/niter
    qb_1 =[]
    qb_1iter = 0
    for i in range(niter):
        qb_1iter = qb_1iter - Sz/Iyy * (tsk*R*cos(theta[i])*s_le) - Sy/Izz*(tsk*R*sin(theta[i])*s_le)
        qb_1.append(qb_1iter)
    qb_1 = np.array(qb_1)

##plotting of shear to check
#plt.figure()
#plt.plot(zcoor14, qb_1)
#plt.show() 

#Base shear flow 4, from cut at LE on z axis to y axis below hinge line

    qb_4 =[]
    qb_4iter = 0
    for i in range(niter):
        qb_4iter = qb_4iter - Sz/Iyy * (tsk*R*cos(theta[i])*s_le) - Sy/Izz*(tsk*R*sin(theta[i])*s_le)
        qb_4.append(qb_4iter)
    qb_4 = np.array(qb_4)   

##plotting of shear to check
#plt.figure()
#plt.plot(zcoor14, qb_4)
#plt.show()     
    
#defining coordinates for second cell
    s2tot = sqrt(R**2 + zneg**2)
    s2 = np.linspace(0, s2tot, niter)
    space = s2tot/niter
    zcoor25 = s2*cos(gamma)
    ycoor25 = s2*sin(gamma)

#Base shear flow 2, from cut at TE on z axis to y axis above hinge line
    qb_2 = []
    qb_2iter = 0
    for i in range(niter): 
        qb_2iter =  qb_2iter - Sz/Iyy*(tsk*zcoor25[i]*space) - Sy/Izz*(tsk*ycoor25[i]*space)
        qb_2.append(qb_2iter)
    qb_2 = np.array(qb_2)
    
##plotting of shear to check
#plt.figure()
#plt.plot(zcoor25, qb_2)
#plt.show()     

#Base shear flow 5, from cut at TE on z axis to y axis below hinge line 
    qb_5 = []
    qb_5iter = 0
    for i in range(niter):
        qb_5iter =  qb_5iter - Sz/Iyy*(tsk*zcoor25[i]*space) - Sy/Izz*(tsk*ycoor25[i]*space)
        qb_5.append(qb_5iter)
    qb_5 = np.array(qb_5)

##plotting of shear to check
#plt.figure()
#plt.plot(zcoor25, qb_5)
#plt.show()     

#defining coordinates for spar
    yspar = np.linspace(h/2, -h/2, 100)
    
    #Base shear flow 3 on y axis 
    qb_3part = qb_1[-1] + qb_2[-1]
    qb_3 = []
    qb_3iter = qb_3part
    qb_3.append(qb_3iter)
    for i in range(niter):
        qb_3iter = qb_3iter - Sy/Izz*(tsp*yspar[i]*(h/niter))
        qb_3.append(qb_3iter)
    
    qb_3 = np.array(qb_3)
    
    return qb_1, qb_2, qb_3, qb_4, qb_5
#plotting of shear to check
#plt.figure()
#plt.plot(yspar, qb_3)
#plt.show() 
