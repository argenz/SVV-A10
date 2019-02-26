#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 16:29:55 2019

@author: PereiraJoao
"""
import math as m
import matplotlib.pyplot as plt

from Modules.BaseShears import get_baseshear
from Modules.ShearMomentEquation import MomentEqShear
from Modules.ShearTwistRateEq import TwistEqForShear
from Modules.StiffnerShear import StiffnerContribution
from Modules.SolveComplimentaryShear import SolveCompShear
from Modules.MomentsForShear import get_Mx
from Modules.StiffnerCoordinates import Coordinates

#VARIABLES --> Sz, Sy and xpos for moments

#REMBER Sy AND Sz HAVE TO MATCH THE POSITION AT WHICH THE M_ext IS ALSO SELECTED
#FOR HINGE 1:
#Sz = -84.8127*1000 + 4.53*1000*m.sin(26*m.pi/180) #P = 91.7 * 1000, Q = 4.53 * 1000
#Sy =  26.53*1000 - 4.53*1000*m.cos(26*m.pi/180)
#FOR ACTUATOR 1:
#Sz =  -42.5*1000*m.cos(26*m.pi/180) + 4.53*1000*m.sin(26*m.pi/180)
#Sy = -42.5*1000*m.sin(26*m.pi/180) - 4.53*1000*m.cos(26*m.pi/180)
#FOR ACTUATOR 2: 
#Sz = -91.7*1000*m.cos(26*m.pi/180) + 4.53*1000*m.sin(26*m.pi/180)
#Sy = -91.7*1000*m.sin(26*m.pi/180) - 4.53*1000*m.cos(26*m.pi/180)
#FOR HINGE 3
Sz = -51.787*1000 + 4.53*1000*m.sin(26*m.pi/180)
Sy = -51.787*1000 - 4.53*1000*m.cos(26*m.pi/180)
   
def FinalShearFL():
    q_extra_stiff = StiffnerContribution(Sz, Sy)
    qb_1, qb_2, qb_3, qb_4, qb_5 = get_baseshear(Sz,Sy)
    M_ext = get_Mx()
    
    xpos = 0 #Position along the x such that the moment_external is for that position
    qs01, qs02 = SolveCompShear(MomentEqShear(qb_1, qb_2, qb_4, qb_5, M_ext[22]), TwistEqForShear(qb_1, qb_2, qb_3, qb_4, qb_5))
    
    #CALCULATING FINAL SHEAR FLOW VALUES----------------------------------------------
    #IF NO STIFFENER-------------------
    #qs = qs0 + qb
    qs_1 = [-i+qs01 for i in qb_1] #NOT SURE ABOUT THE SIGNS, IF THERE IS A ERROR IT IS PROBABLY HERE
    qs_2 = [i+qs02 for i in qb_2]
    qs_3 = [-i+qs01-qs02 for i in qb_3]
    qs_4 = [i+qs01 for i in qb_4]
    qs_5 = [-i+qs02 for i in qb_5]
    
    #IF STIFFENER-----------------------
    C_a = 0.547
    h_a = 0.225
    n_st = 17

    L_p = m.sqrt((C_a-(h_a/2.))**2. +(h_a/2.)**2.) #Top and bottom panel length
    L_le = 2*m.pi*(h_a/2.)*(180./360.) #Leading edge arc length
    
    qs_for_sf = qs_2+qs_1[::-1]+qs_4+qs_5[::-1] #for use in  this part only
    
    L_tot = 1.2510850095818462 #aileron perimetry
    
    s_coor, s_spacing = Coordinates() #Important part is stiffener spacing
    
    position = 0
    q_stiffeners = []

    #FOR EACH STIFFENER
    for j in range(len(q_extra_stiff)):
        #FOR EACH SECTION OF THE CORSS SECTION
            #FOR THE CLOSESt qs TO THE STIFFENER 
                #q_stiffener = qs0 + qb + qstiffener
        if j<6:
            iter_spacing2 = L_p/len(qs_2)
            cum_n =[] #cumelative itteration spacing
            for s in range(len(qs_2)):
                cum_n.append(s*iter_spacing2)
            position = min(range(len(cum_n)), key=lambda i: abs(cum_n[i]-((j+1)*s_spacing)))
            q_stiffeners.append(q_extra_stiff[j]+qs_2[position])
        if 5<j<9:
            iter_spacing1 = L_le/2/len(qs_1)
            cum_n =[] #cumelative itteration spacing
            for s in range(len(qs_1)):
                cum_n.append((s_spacing*6)+s*iter_spacing1)
            position = min(range(len(cum_n)), key=lambda i: abs(cum_n[i]-((j+1)*s_spacing)))
            qs_1Rev = qs_1[::-1]
            q_stiffeners.append(q_extra_stiff[j]+qs_1Rev[position])
        if 8<j<11:
            iter_spacing4 = L_le/2/len(qs_4)
            cum_n =[] #cumelative itteration spacing
            for s in range(len(qs_4)):
                cum_n.append((s_spacing*9)+s*iter_spacing4)
            position = min(range(len(cum_n)), key=lambda i: abs(cum_n[i]-((j+1)*s_spacing)))
            q_stiffeners.append(q_extra_stiff[j]+qs_4[position])   
        if 10<j:
            iter_spacing5 = L_p/len(qs_5)
            cum_n =[] #cumelative itteration spacing
            for s in range(len(qs_5)):
                cum_n.append((s_spacing*10)+s*iter_spacing5)
            position = min(range(len(cum_n)), key=lambda i: abs(cum_n[i]-((j+1)*s_spacing)))
            qs_5Rev = qs_5[::-1]
            q_stiffeners.append(q_extra_stiff[j]+qs_5Rev[position]) 
            
    return qs_1, qs_2, qs_3, qs_4, qs_5, q_stiffeners

qs_1, qs_2, qs_3, qs_4, qs_5, q_stiffeners = FinalShearFL()

#Tests
qb_1, qb_2, qb_3, qb_4, qb_5 = get_baseshear(Sz,Sy)
M_ext = get_Mx()
qs01, qs02 = SolveCompShear(MomentEqShear(qb_1, qb_2, qb_4, qb_5, M_ext[0]), TwistEqForShear(qb_1, qb_2, qb_3, qb_4, qb_5))