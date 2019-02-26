#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:05:11 2019

@author: PereiraJoao
"""
import math as m
import numpy as np
from FinalShearFlow import FinalShearFL
#from reactionforces import reaction_forces

#THE SHEAR FLOWS CALULATED BEFORE HAVE TO BE AT THE CONDTIONS OF THE CORRESPONDING HINGER LOCATION

RIB_NUMBER = 4 #RIB A = 1, B = 2, C = 3, D = 4

#GEOMETRIES & FORCES-----------------
h_a = 0.225
R=h_a/2.
C_a = 0.547
L_p = m.sqrt((C_a-(h_a/2.))**2. +(h_a/2.)**2.) #Top and bottom panel length
L_le = 2*m.pi*(h_a/2.)*(180./360.) #Leading edge arc length
L_tot = 2*L_p + L_le #total perimetry of airfoil
Airfoil_Theta = 26*m.pi/180

Q = 4.53 * 1000

angle_TE = m.atan(R/(C_a-(R)))

#SOME VALUES THAT WILL BE NEEDED---------------------------

qs_1, qs_2, qs_3, qs_4, qs_5, q_stiffeners = FinalShearFL()

integral_qs_3 = 0 #Integral for top half of the leading edge arc
for i in range(len(qs_3)):
    integral_qs_3 += qs_3[i] * (h_a/len(qs_3))

Sy = -integral_qs_3 * h_a


integral_pqs_1 = 0 #Integral of the moment from leading edge arcs around bottom point
integral_pqs_4 = 0
theta = np.linspace(0, m.pi/4, len(qs_1))
for i in range(len(qs_1)):
    Theta = theta[i]
    integral_pqs_1 += qs_1[i]*m.sin(Theta) * (L_le/2/len(qs_1)) * (R*m.sin(Theta)+R)
    integral_pqs_4 += qs_4[i]*m.sin(Theta) * (L_le/2/len(qs_4)) * (R - R*m.sin(Theta))

integral_pqs_2 = 0 #Integral for momemnts from top panel around bottom point
R_perp = m.sin(angle_TE) * (C_a - R)
for i in range(len(qs_2)):
    integral_pqs_2 += qs_2[i] * (L_p/len(qs_2)) * R_perp
#-------------------------------

#FOR RIB A
if RIB_NUMBER == 1:
    #Cell 1
    Rz1 = -84.812734 *1000
    P1z_1 = (integral_pqs_1 + integral_pqs_4 + Rz1*R)/h_a 
    P2z_1 = P1z_1 + Rz1
    P1y_1 = m.tan(angle_TE)*P1z_1
    P2y_1 = m.tan(angle_TE)*P2z_1
    sumF_1 = P1y_1 + P2y_1 + Sy
    qrib_1 = sumF_1/h_a
    #Cell 2
    P1z_2 = -(integral_pqs_2 + Q*m.sin(Airfoil_Theta)*R - Q*m.cos(Airfoil_Theta)*(0.25*C_a - R))/h_a
    P2z_2 = Q*m.sin(angle_TE)-P1z_2
    P1y_2 = m.tan(angle_TE)*P1z_2 
    P2y_2 = m.tan(angle_TE)*P2z_2 
    sumF_2 = P2y_2 - P1y_2 + Sy - Q*m.cos(Airfoil_Theta)
    qrib_2 = sumF_2/h_a
#FOR RIB B
if RIB_NUMBER == 2:
    #Cell 1
    Preact = -42.5141042*1000
    P1z_1 = (integral_pqs_1 + integral_pqs_4 + Preact*m.cos(Airfoil_Theta)*h_a - Preact*m.sin(Airfoil_Theta)*R)/h_a
    P2z_1 = P1z_1 + Preact*m.cos(Airfoil_Theta)
    P1y_1 = m.tan(angle_TE)*P1z_1
    P2y_1 = m.tan(angle_TE)*P2z_1
    sumF_1 = P1y_1 + P2y_1 + Sy + Preact*m.sin(Airfoil_Theta)
    qrib_1 = sumF_1/h_a
    #Cell 2
    P1z_2 = -(integral_pqs_2 + Q*m.sin(angle_TE)*R - Q*m.cos(angle_TE)*(0.25*C_a - R))/h_a
    P2z_2 = Q*m.sin(angle_TE)-P1z_2
    P1y_2 = m.tan(angle_TE)*P1z_2 
    P2y_2 = m.tan(angle_TE)*P2z_2 
    sumF_2 = P2y_2 - P1y_2 + Sy - Q*m.cos(angle_TE)
    qrib_2 = sumF_2/h_a
#FOR RIB C
if RIB_NUMBER == 3:
    #Cell 1
    P = 91.7 * 1000
    P1z_1 = (integral_pqs_1 + integral_pqs_4 + P*m.cos(Airfoil_Theta)*h_a - P*m.sin(Airfoil_Theta)*R)/h_a
    P2z_1 = P1z_1 + P*m.cos(Airfoil_Theta)
    P1y_1 = m.tan(angle_TE)*P1z_1
    P2y_1 = m.tan(angle_TE)*P2z_1
    sumF_1 = P1y_1 + P2y_1 + Sy + P*m.sin(Airfoil_Theta)
    qrib_1 = sumF_1/h_a    
    #Cell 2
    P1z_2 = -(integral_pqs_2 + Q*m.sin(angle_TE)*R - Q*m.cos(angle_TE)*(0.25*C_a - R))/h_a
    P2z_2 = Q*m.sin(angle_TE)-P1z_2
    P1y_2 = m.tan(angle_TE)*P1z_2 
    P2y_2 = m.tan(angle_TE)*P2z_2 
    sumF_2 = P2y_2 - P1y_2 + Sy - Q*m.cos(angle_TE)
    qrib_2 = sumF_2/h_a
#FOR RIB D
if RIB_NUMBER == 4:
    #Cell 1
    Rz1 = -51.787 *1000
    P1z_1 = (integral_pqs_1 + integral_pqs_4 + Rz1*R)/h_a 
    P2z_1 = P1z_1 + Rz1
    P1y_1 = m.tan(angle_TE)*P1z_1
    P2y_1 = m.tan(angle_TE)*P2z_1
    sumF_1 = P1y_1 + P2y_1 + Sy
    qrib_1 = sumF_1/h_a
    #Cell 2
    P1z_2 = -(integral_pqs_2 + Q*m.sin(Airfoil_Theta)*R - Q*m.cos(Airfoil_Theta)*(0.25*C_a - R))/h_a
    P2z_2 = Q*m.sin(angle_TE)-P1z_2
    P1y_2 = m.tan(angle_TE)*P1z_2 
    P2y_2 = m.tan(angle_TE)*P2z_2 
    sumF_2 = P2y_2 - P1y_2 + Sy - Q*m.cos(Airfoil_Theta) 
    qrib_2 = sumF_2/h_a

