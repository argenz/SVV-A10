# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:42:03 2019

@author: A10

Main function to calculate delfection and shear flow of A320 aileron
"""
# Reading data and initializing libraries and other functions.
import numpy as np    
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shear_center import *
exec(open("./Data.txt").read())    
  
# Obtaining the location of centroid.
centroid_original_rf = centroid()

# Obtaining the MOI.
Izz = get_Izz()
Iyy = get_Iyy(centroid_original_rf[2])
Iyz = get_Iyz(centroid_original_rf[2])

# Obtaining the location of the shear center.
shear_center = get_ShearCenter(Izz,tsk,h,Ca)

# Obtaining the reaction forces and their transform.      
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izzrotated)
X2,Y1,Y2,Y3,Z1,Z2,Z3,R_y,R_z,P_y,P_z,Q_y,Q_z = transform(X2,Y1,Y2,Y3,Z1,Z2,Z3,R,P,q,theta)

""" Maybe use this naming of the internal rf?"""
#U2,V1,V2,V3,W1,W2,W3,R_v,R_w,P_v,P_w,Q_v,Q_w = transform(X2,Y1,Y2,Y3,Z1,Z2,Z3,R,P,q,theta)