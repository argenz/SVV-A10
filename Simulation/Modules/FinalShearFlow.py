#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 16:29:55 2019

@author: PereiraJoao
"""

from BaseShears import get_baseshear
from ShearMomentEquation import MomentEqShear
from ShearTwistRateEq import TwistEqForShear
from StiffnerShear import StiffnerContribution
from SolveComplimentaryShear import SolveCompShear
from MomentsForShear import get_Mx

Sz = 1
Sy = 1

q_extra_stiff = StiffnerContribution(Sz, Sy)
qb_1, qb_2, qb_3, qb_4, qb_5 = get_baseshear()
M_ext = get_Mx()

qs01, qs02 = SolveCompShear(MomentEqShear(qb_1, qb_2, qb_4, qb_5, M_ext), TwistEqForShear(qb_1, qb_2, qb_3, qb_4, qb_5))

#IF NO STIFFENER
#qs = qs0 + qb
qs_1 = [i+qs01 for i in qb_1] #NOT SURE ABOUT THE SIGNS
qs_2 = [i+qs02 for i in qb_1]
qs_3 = [i+qs01+qs02 for i in qb_1]
qs_4 = [i+qs01 for i in qb_1]
qs_5 = [i+qs02 for i in qb_1]

#IF STIFFENER
#qs = qs0 + qb + qstiffener

#FOR EACH STIFFENER
    #FOR EACH SEPERATE SECTION
        #FOR THE CLOSESR qs TO THE STIFFENER 
            #q_stiffener = qs + q_extra_sf