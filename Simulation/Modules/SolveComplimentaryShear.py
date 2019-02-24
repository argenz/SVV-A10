#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 15:53:22 2019

@author: PereiraJoao
"""

import numpy as np

def SolveCompShear(MomentEquationCoefficietns, TwistEquationCoefficietns):
    C = MomentEquationCoefficietns #from equation in the form C0 + C1*qso1 + C2*qso2 = 0
    D = TwistEquationCoefficietns#from equation in the form D0 + D1*qso1 + D2*qso2 = 0
    
    a = np.array([[C[1],C[2]],[D[1],D[2]]])
    b = np.array([-C[0],-D[0]])
    qs0np = np.linalg.solve(a,b) #Solving for qs01 and qs02 
    qs0 = qs0np.tolist() #--> qs0 = [qs01, qs02]
    
    return qs0[0], qs0[1] # its returning qs01, qs02