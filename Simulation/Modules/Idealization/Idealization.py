#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:15:57 2019

@author: PereiraJoao
"""
from IdealizationCoordinates import IdealizationCoordinates
import numpy as np
import matplotlib.pyplot as plt

t_sk = 0.0011 #skin thikness
t_sp = 0.0029 #spar thikness

B_coordinatesTopPanel,B_coordinatesTopArc,b_st = IdealizationCoordinates() 
B_coordinatesTop = B_coordinatesTopPanel + B_coordinatesTopArc 
B_coordinatesRev = [ [x,y*-1] for [x,y] in B_coordinatesTop[::-1]]
B_coordinates = B_coordinatesTop + B_coordinatesRev[1:]#stiffner coordinates top half of aileron

A_st = 0.0012*(0.015-0.0012) + (0.02*0.0012) #stiffner area [m]

#B0 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[16,1]/B_coordinates[0,1])+(B_coordinates[16,1]/B_coordinates[1,1])) 
#B1 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[0,1]/B_coordinates[1,1])+(B_coordinates[2,1]/B_coordinates[1,1]))
#B2 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[1,1]/B_coordinates[2,1])+(B_coordinates[3,1]/B_coordinates[2,1]))
#B3 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[2,1]/B_coordinates[3,1])+(B_coordinates[4,1]/B_coordinates[3,1]))
#B4 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[3,1]/B_coordinates[4,1])+(B_coordinates[5,1]/B_coordinates[4,1]))
#B5 = 
#B6 = 
#B7 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[16,1]/B_coordinates[0,1])+(B_coordinates[16,1]/B_coordinates[1,1]))


B_coordinates = np.array(B_coordinates)
plt.plot(B_coordinates[:,0],B_coordinates[:,1])
plt.show()