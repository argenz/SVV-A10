#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:05:06 2019

@author: PereiraJoao
"""

C_a = 0.547 #chord length
h_a = 0.225 #Spar height
R = h_a/2. # Radius arc (half the length of spar)
A1 = (m.pi*R**2)/2 #Area cell leading 
A2 = ((C_a-R)*R)/2 #Area cell trailing 
G = 28*(10**9) #Shear modulus [Gpa]  

# TWIST RATE EQUATION FOR CELL 1 (FORWARD CELL)----------------------

#Terms from the base shear flows
intqb_1 = 0
for i in range(len(qb_1)):
    

#Terms for complimentary shear flows

# TWIST RATE EQUATION FOR CELL 2 (AFT CELL)--------------------------

#Terms from the base shear flows

#Terms for complimentary shear flows