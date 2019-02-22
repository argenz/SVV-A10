#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 14:43:10 2019

@author: PereiraJoao
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt

def Coordinates():
    C_a = 0.547
    h_a = 0.225
    n_st = 17
    
    L_p = m.sqrt((C_a-(h_a/2.))**2. +(h_a/2.)**2.) #Top and bottom panel length
    L_le = 2*m.pi*(h_a/2.)*(180./360.) #Leading edge arc length
    L_tot = 2*L_p + L_le #total perimetry of airfoil
    b = L_tot/(n_st+1) #Stringer spacing
    Theta_p = m.atan((h_a/2)/(C_a-(h_a/2.))) #angle (radians) of airfoil top and bottom panel with respect to chordline
    
    
    # STRINGER COORDINATES FOR TOP PANEL----------
    B_coordinatesTP = list()
    y_B = 0#starting y coordinate
    z_B = -1#srandom initalization z coordinate 
    n = 0#staring stringer
    while True:
        n = n+1
        y_B = m.sin(Theta_p)*(n*b)# y-coordinate stringer top panel
        z_B = -(C_a-(h_a/2.))  + m.cos(Theta_p)*(n*b) # x-coordinate stringer top panel
        if z_B > 0.: #condition for first panel
            break
        B_coordinatesTP.append([z_B,y_B])
    
    #STRINGER COORDINATES FOR LEADING EDGE ARC top half------------
    B_coordinatesA = list()
    l_arc = b-(abs(B_coordinatesTP[-1][0])/m.cos(Theta_p)) #starting length along LE arc
    arc_angle = 0          
    while True:
        arc_angle = 360*(l_arc/(2*m.pi*(h_a/2))) * (m.pi/180) #radians
        z_B = m.sin(arc_angle)*(h_a/2)
        y_B = m.cos(arc_angle)*(h_a/2)
        l_arc = l_arc + b
        if y_B < 10**-4:
           y_B = 0
        B_coordinatesA.append([z_B,y_B])
        if arc_angle > 90*(m.pi/180):
            break
        
    #PUTTING ALL COORDINATES TOGETHER 
    B_coordinatesT = B_coordinatesTP + B_coordinatesA 
    B_coordinatesRev = [ [x,y*-1] for [x,y] in B_coordinatesT[::-1]]
    B_coordinates = B_coordinatesT + B_coordinatesRev[1:]#stiffner coordinates top half of aileron
    
    #PLOT TO CHECK THE COORDINATES ARE CORRECT
    Bplt = np.array(B_coordinates)
    plt.plot(Bplt[:,0],Bplt[:,1],'*k')
    plt.show()  

    return B_coordinates, b

testcoordinates, btest = Coordinates()
