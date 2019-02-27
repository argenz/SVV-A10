# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:42:03 2019

@author: A10

Main function to calculate delfection and shear flow of A320 aileron
"""
# Reading data and initializing libraries and other functions.
import numpy as np
import matplotlib.pyplot as plt
import numpy as np    
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shearcenter_pos import *
from Modules.Finddeflectionbending_update2 import *
from Modules.deflectiondistributedload import *
from Modules.deflectionpointload import *

exec(open("./Data.txt").read())    
  
# Obtaining the location of centroid.
centroid_original_rf = centroid()

# Obtaining the MOI.
Izz = get_Izz()
Iyy = get_Iyy()
Iyz = get_Iyz()

# Obtaining the location of the shear center.
shear_center = get_shear_center(Izz,tsk,h,Ca)

# Obtaining the reaction forces and their transform. forces in internal coordinatesystem!!    
U2,V1,V2,V3,W1,W2,W3,Q_v,Q_w,R_v,R_w,P_v,P_w,YA,YB,ZA,ZB = reaction_forces(Iyy,Izz)

""" Maybe use this naming of the internal rf?"""

ucoordinates,vdefbend,wdefbend,x1discr,x3discr=deformduetobending()
ucoordinates=ucoordinates[::-1]
vdefbend=vdefbend[::-1]
wdefbend=wdefbend[::-1]

plt.plot(ucoordinates,wdefbend)
plt.show()

