#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:13:48 2019

@author: PereiraJoao
"""
import math as m

def MomentEqShear(qb1, qb2, qb4, qb5, Mext):
    #INPUTS AND GENERAL INFO ON GEOMETRIES -----------------------------------
    M_ext = Mext #External moment about the hinge
    
    qb_1 = qb1 #Base Shear flow list top arc
    qb_2 = qb2 #Base Shear flow list top panel
    #Base Shear flow list spar (qb_3) NOT USED AS IT DOSENT CREAT A MOMENT ABOUT THE HINGE
    qb_4 = qb4 #Base Shear flow list bottom arc
    qb_5 = qb5 #Base Shear flow list bottom panel
    
    h_a = 0.225 #Spar height
    R = h_a/2. # Radius arc (half the length of spar)
    C_a = 0.547 #chord length
    l_arc = 2*m.pi*(R)*(90./360.) #half the length of the leading edge arc
    l_panel = m.sqrt((C_a-(R))**2. + (R)**2.) #airfoil panel length
    Theta_p = m.atan((R)/(C_a-(R))) #angle (radians) of airfoil top and bottom panel with respect to chordline
    R_perp = m.sin(Theta_p) * (C_a - R) #Moment arm for top and bottom panels
    
    #CALCULATING MOMENT CONTRIBUTIONS FOR BASE SHEAR FLOWS (Numerical Integration)----------
    
    integral_pqb_1 = 0 #Integral for top half of the leading edge arc
    for i in range(len(qb_1)):
        integral_pqb_1 += qb_1[i] * (l_arc/len(qb_1)) * R
    
    integral_pqb_4 = 0 #Integral for the bottom half of the leading edge arc
    for i in range(len(qb_4)):
        integral_pqb_4 += qb_4[i] * (l_arc/len(qb_4)) * R
    
    integral_pqb_2 = 0 #Integral for to panel
    for i in range(len(qb_2)):
        integral_pqb_2 += qb_2[i] * (l_panel/len(qb_1)) * R_perp
                              
    integral_pqb_5 = 0 #Integral for bottom panel
    for i in range(len(qb_5)):
        integral_pqb_5 += qb_5[i] * (l_panel/len(qb_1)) * R_perp
    
    #CALCULATING MOMENT CONTRIBUTIONS FOR COMPLIMENTARY SHEAR FLOWS--------------------
    
    A1 = (m.pi*R**2)/2 #Area cell leading 
    A2 = ((C_a-R)*R)/2 #Area cell trailing 
    
    qs0_1_coefficient = 2*A1 #front cell complimentary q contribution
    qs0_2_coefficient = 2*A2 #back cell complimentary q contribution
    
    #OBTAINING all MOMENT EQUATION COEFFICIENTS-------------------------------
    
    C_0 = -integral_pqb_1 + integral_pqb_4 + integral_pqb_2 - integral_pqb_5 - M_ext
    C_1 = qs0_1_coefficient
    C_2 = qs0_2_coefficient
    C = [C_0, C_1, C_2] #Coeeficients in the form: 0 = C_0 + C_1*qso_1 + C_2*qso_2

    return C