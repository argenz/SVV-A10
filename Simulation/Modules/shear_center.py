# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from math import *
import numpy as np
import scipy.integrate as integrate
from Modules.MOI import *

#Chord c
#aileron height h

exec(open("./Data.txt").read()) 


def get_ShearCenter (Izz,t,h,c): #shear center calculation (Moment of inertia, thickness, enclosed area, aileron height)
    #Gt assumed constant, thin wall assumption

    #Known
    r=h/2
    d=sqrt(r*r+(c-r)*(c-r))
    diam=r*pi+2*d #int ds
    theta=atan(r/(c-r))
    
    #qs0
    qs012=integrate.dblquad(lambda s, s1: t*r*sin(s/r), 0, r*pi/2, lambda s: 0, lambda s: s)
    qs023=integrate.dblquad(lambda s, s2: t*(d-s)*sin(theta), 0, d, lambda s: 0, lambda s: s)
    qs0=(2/Izz/diam)*(qs012[0]+qs023[0])
    
    #distance to point in 12 follows sqrt((r*sin(s1*180/r/pi))^2+(r*cos(s1*180/r/pi))^2)
    
    #contribution to moment coming from qs0
    qs0mom=integrate.quad(lambda s1: qs0*sqrt((r*sin(s1/r))*(r*sin(s1/r))+(r*cos(s1/r))*(r*cos(s1/r))), 0, r*pi/2)[0]
    
    #contribution to moment coming from qb12
    qb12mom=(-1/Izz)*integrate.dblquad(lambda s, s1: sqrt((r*sin(s1/r))*(r*sin(s1/r))+(r*cos(s1/r))*(r*cos(s1/r)))*t*r*sin(s1/r), 0, r*pi/2, lambda s: 0, lambda s: s)[0]
    
    #Shear center by moment equilibrium
    ShearCenter=2*(qs0mom+qb12mom)-c
    
    return ShearCenter

h=10.
c=13.
#Izz=0.002
t=0.05

#print(ShearCenter(calc_Izz(),tsk,h,Ca))
