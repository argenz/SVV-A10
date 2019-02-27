# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from math import *
import numpy as np
import scipy.integrate as integrate

#Values in meters
#h=0.225
#c=0.547
#Izz=0.00000764
#t=0.0011


def get_shear_center(h,c,Izz,t):
    
    #Qb determination
    r=h/2
    alpha=atan(h/2/(c-r))
    diagonal=sqrt((c-r)*(c-r)+r*r)

    #qb12=int(1/Izz*t*s1) 0, s1
    #qb23=int(1/Izz*t*r*sin(pi/2-s2/r)) 0, s2
    #qb52=int(1/Izz*t*s5*sin(alpha)) 0, s5
    #qb21=int(1/Izz*t*(r-s4)), 0, s4 

    #Perimeters
    p_cell_1=h+r*pi
    p_cell_2=h+2*diagonal

    #qb integrated around cell 1
    qb12int=integrate.dblquad(lambda s, s1: 1/Izz*t*s1, 0, r, lambda s:0, lambda s: s)
    qb23int=integrate.dblquad(lambda s, s2: 1/Izz*t*r*sin(pi/2-s2/r), 0, r*pi/2, lambda s:0, lambda s: s)
    qbint1=2*qb12int[0]+2*qb23int[0]

    #qb integrated around cell 2. 
    qb52int=integrate.dblquad(lambda s, s5: 1/Izz*t*s5*sin(alpha), 0, diagonal, lambda s:0, lambda s: s)
    qbint2=2*(-qb12int[0])+2*qb52int[0]

    #Qs0 determination
    #qs0I
    qs0I=1/(p_cell_1-h**2/p_cell_2)*(-qbint1-h/p_cell_2*qbint2)
    #qs0II
    qs0II=(-qbint2+qs0I*h)/p_cell_2

    #Moments NOTE: moments taken about TE, CCW pos
    spar_mom=(c-r)*(-2*qb12int[0]+qs0II-2*qb12int[0]-qs0I)
    arc_mom_qb=-2*integrate.dblquad(lambda s, s2: 1/Izz*t*r*sin(s2/r)*sqrt((r*sin(s/r))**2+(c-r+r*cos(s/r))**2), 0, r*pi/2, lambda s:0, lambda s: s)[0]
    arc_mom_qs0=-2*integrate.quad(lambda s2: qs0I*sqrt((r*sin(s2/r))**2+(c-r+r*cos(s2/r))**2), 0, r*pi/2)[0]

    #print(qb12int,qb23int,qb52int,qs0I,qs0II)
    shear_cent=spar_mom+arc_mom_qb+arc_mom_qs0
    #print(spar_mom, arc_mom_qb, arc_mom_qs0)
    print(shear_cent)
    #Transformation to system coordinates
    shear_cent=r-(c+shear_cent)


    return(shear_cent)

