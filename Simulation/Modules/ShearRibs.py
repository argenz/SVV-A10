#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:05:11 2019

@author: PereiraJoao
"""
import math as m
import numpy as np
from FinalShearFlow import FinalShearFL

#GEOMETRIES-----------------
h_a = 0.225
R=h_a/2.
C_a = 0.547
L_p = m.sqrt((C_a-(h_a/2.))**2. +(h_a/2.)**2.) #Top and bottom panel length
L_le = 2*m.pi*(h_a/2.)*(180./360.) #Leading edge arc length
L_tot = 2*L_p + L_le #total perimetry of airfoil


angle_TE = m.atan((h_a/2)/(C_a-(h_a/2.)))
#---------------------------


qs_1, qs_2, qs_3, qs_4, qs_5, q_stiffeners = FinalShearFL()

integral_qs_3 = 0 #Integral for top half of the leading edge arc
for i in range(len(qs_3)):
    integral_qs_3 += qs_3[i] * (h_a/len(qs_3))

Sy = -integral_qs_3 * h_a


integral_pqs_1 = 0 #Integral for top half of the leading edge arc
integral_pqs_4 = 0
theta = np.linspace(0, m.pi/4, len(qs_1))
for i in range(len(qs_1)):
    Theta = theta[i]
    integral_pqs_1 += qs_1[i]*m.sin(Theta) * (L_le/2/len(qs_1)) * (R*m.sin(Theta)+R)
    integral_pqs_4 += qs_4[i]*m.sin(Theta) * (L_le/2/len(qs_4)) * (R - R*m.sin(Theta))

#FOR RIB A
#Cell 1
Rz1 = -1
P1z_1 = -(integral_pqs_1 + integral_pqs_4)/h_a - Rz1*R #ADD EXTERNAL FORCES
#P1z_1 = P2z_1 ...... REDO
P1y_1 = m.tan(angle_TE)*P1z_1
#P1y_1 = P2y_1 ....
sumF = P1y_1*2 + Sy
qrib_1 = sumF/h_a
#Cell 2
#FOR RIB B
#Cell 1
#Cell 2
#FOR RIB C
#Cell 1
#Cell 2
#FOR RIB D
#Cell 1
#Cell 2


print qrib_1


