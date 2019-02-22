#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 14:43:21 2019

@author: FCRA
"""
import numpy as np
from math import *
from Modules.centroid import centroid
#from scipy.integrate import quad

################### Area Moment of Inertia Tools ###########################
#Data

exec(open("../Data.txt").read())

#to find the area moments of inertia we decompose the cross section in 3 parts:
#the thin walled semi circle, and the two rectangles 
#most dimenstion are given above except a few which are calculate below:

#derived dimensions
a_r = sqrt((h/2)**2 + Ca**2)                #lenght of rectangle
beta_r = acos(Ca/a_r)                       #inclination of rectangle
d_cr = (a_r/2)*sin(beta_r)                  #distance from rectangle's centroid to the z axis
r = h/2



############ AREA MOMENTS OF INERTIA IN ZZ
#Izz_r1, moment of the first rectangle including steiner
#Izz_r2, moment of second rectangle including steiner

def get_Izz():
    Izz_r1 = tsk*(a_r**3)*(sin(beta_r)**2)/12 + a_r*tsk*(d_cr)**2
    Izz_r2 = Izz_r1                             #because only parameters changing sign are squared so no difference 
   
    Izz_sm = r**3*tsk*pi/2                      #no steiner because symmetry with respect to z
    
    Izz = Izz_r1 + Izz_r2 + Izz_sm
    return float(Izz)



############ AREA MOMENTS OF INERTIA IN YY
    

ctrd_r_z = -(Ca - r - a_r/2*cos(beta_r))   #projection of z location of rectangle's centroid on z axis
                                           #minus to respect coordinate system

#Calculating Centroid of thin walled semicircle
R1 = r
R2 = r - tsk

z1 = 4*R1/(3*pi)
A1 = pi*(R1**2)/2

z2 = 4*R2/(3*pi)
A2 = - pi*(R2**2)/2

cntrd_sm = ((A1*z1)+(A2*z2))/(A1+A2)


def get_Iyy(ctrd_z):
    Iyy_r1 = tsk*(a_r**3)*(cos(beta_r)**2)/12 + a_r*tsk*(ctrd_r_z-ctrd_z)**2
    Iyy_r2 = Iyy_r1                            #Only thing varying is beta and it's cos so same value for negative angle
    
    
    
    Iyy_sm = r**3*tsk*pi/2 + (A1+A2)*(cntrd_sm - ctrd_z)**2
    
    Iyy = Iyy_r1 + Iyy_r2 + Iyy_sm
    return float(Iyy)

############ AREA MOMENTS OF INERTIA IN YZ

def get_Iyz(ctrd_z):
    Iyz_r1 = tsk*(a_r**3)*sin(beta_r)*cos(beta_r)/(12) + a_r*tsk*(d_cr)*(ctrd_r_z-ctrd_z)
    Iyz_r2 = tsk*(a_r**3)*sin(-beta_r)*cos(-beta_r)/(12) + a_r*tsk*(-d_cr)*(ctrd_r_z-ctrd_z)
    
    Iyz_sm = 0 + 0 #second distance to the centroid is zero 
    Iyz = Iyz_r1 + Iyz_r2 + Iyz_sm
    return float(Iyz)

#transform moments of inertias 
def Izzrotated():
    angle=np.deg2rad(26)
    Izzrotated=0.5*(Izz()+Iyy())+0.5*cos(2*angle)*(Izz()-Iyy())-Iyz()*sin(2*angle)
    return float(Izzrotated)
def Iyyrotated():
    angle=np.deg2rad(26) 
    Iyyrotated=0.5*(Izz()+Iyy())-0.5*cos(2*angle)*(Izz()-Iyy())+Iyz()*sin(2*angle)
    return float(Iyyrotated)









