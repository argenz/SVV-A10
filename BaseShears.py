#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:29:10 2019

@author: FCRA
"""

import math
import numpy as np
from Modules.centroid import centroid
from Modules.MOI import Izz, Iyy, Iyz


########### Calculation of base shears #########

#INPUTS:
exec(open("./Data.txt").read())   
R = h/2
Sz = 1
Sy = 1
gamma = 1
Izz = Izz()
Iyy = Iyy(centroid_original_rf[2])
Iyz = Iyz(centroid_original_rf[2])

theta = np.linspace(0,pi/4, 100)
qb_1list =[]

for i in range(len(theta)):
    qb_1 = - Sz/Iyy * (tsk*R**2*cos(theta[i])) - Sy/Izz*(tsk*R**2*sin(theta[i]))
    qb_1list.append(qb_1)

print theta
print qb_1list
    

    