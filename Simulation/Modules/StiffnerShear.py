#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 12:00:53 2019

@author: PereiraJoao
"""
from StiffnerCoordinates import Coordinates
from MOI  import Izz, Iyy

def StiffnerContribution(Sz, Sy): # inputs are the vertical and horizontal forces acting on the corss section
    
    I_zz = Izz()
    I_yy = Iyy()
    Qz = Sz/I_yy 
    Qy = Sy/I_zz
    Astiffner = 0.0012*(0.015-0.0012) + (0.02*0.0012) #stiffner area [m]
    
    Stif_coor, Spacing = Coordinates() # (z,y) coordinates for stiffners and spacing (spacing is not used here)
    
    #CALCULATING STIFFNER CONTRIBUTION TO BASE SHEAR FLOW
    StiffnerContribution = []
    for c in Stif_coor:
        qb_st_contribution = -Qz * Astiffner * c[0] - Qy * Astiffner * c[1]
        StiffnerContribution.append(qb_st_contribution)
    
    return StiffnerContribution