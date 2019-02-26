#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:05:06 2019

@author: PereiraJoao
"""
import math as m

def TwistEqForShear(qb_1, qb_2, qb_3, qb_4, qb_5):
    
    #INPUTS AND GENERAL INFO ON GEOMETRIES------------------------------    
    C_a = 0.547 #chord length
    h_a = 0.225 #Spar height
    R = h_a/2. # Radius arc (half the length of spar)
    A1 = (m.pi*R**2)/2 #Area cell leading 
    A2 = ((C_a-R)*R)/2 #Area cell trailing 
    G = 28*(10**9) #Shear modulus [Gpa]  
    t_skin = 0.0011 #skin thikness [m]
    t_spar = 0.0029 #spar thikness [m]
    
    l_arc = 2*m.pi*(R)*(90./360.) #half the length of the leading edge arc
    l_panel = m.sqrt((C_a-(R))**2. + (R)**2.) #airfoil panel length
    
    # TWIST RATE EQUATION FOR CELL 1 (FORWARD CELL)----------------------
    
    #Terms from the base shear flows
    intqb_1 = 0 #Integral for top half of the leading edge arc
    for i in range(len(qb_1)):
        intqb_1 += qb_1[i] * (l_arc/len(qb_1)) / t_skin
 
    intqb_4 = 0 #Integral for the bottom half of the leading edge arc
    for i in range(len(qb_4)):
        intqb_4 += qb_4[i] * (l_arc/len(qb_4)) / t_skin
 
    intqb_3 = 0 #Integral for the spar
    for i in range(len(qb_3)):
        intqb_3 += qb_3[i] * (h_a/len(qb_3)) / t_spar

    sum_int_cell1 = (1/(2*A1*G)) * (intqb_1 + intqb_3 - intqb_4)
    
    #Terms for complimentary shear flows
    C11 = (1/(2*A1*G)) * ((l_arc*2)/t_skin + h_a/t_spar)
    C12 = (1/(2*A1*G)) * (h_a/t_spar)
    
    # TWIST RATE EQUATION FOR CELL 2 (AFT CELL)--------------------------
    
    #Terms from the base shear flows
    intqb_2 = 0 #Integral for the top panel 
    for i in range(len(qb_2)):
        intqb_2 += qb_2[i] * (l_panel/len(qb_2)) / t_skin

    intqb_5 = 0 #Integral for the bottom panel
    for i in range(len(qb_5)):
        intqb_5 += qb_5[i] * (l_panel/len(qb_5)) / t_skin
  
    #intqb_3 ---> this integral is used again, it is the same as calculated for cell1
    
    sum_int_cell2 = (1/(2*A2*G)) * (-intqb_2 + intqb_5 - intqb_3) #before -+
    
    #Terms for complimentary shear flows
    C21 = (1/(2*A2*G)) * (2*l_panel/t_skin + h_a/t_spar)
    C22 = (1/(2*A2*G)) * (h_a/t_spar)
    
    #OBTAINING ALL TWIST EQUATION COEFFICIENTS WHEN THE 2 EQUATIONS (FOR CELL 1 & 2) ARE EQUALIZED
    
    D1 = C11-C21
    D2 = C12 - C22
    D0 =  sum_int_cell1 - sum_int_cell2
    D = [D0, D1, D2]  #coefficients in the form 0 = D1*qs01 + D2*qs02 + D0                                                         
    
    return D
                                                                
                                                                