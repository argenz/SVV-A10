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
from Modules.Torsion_displacement import *

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


print("""X2: {0}
W1,V1: {4},{1}
W2,V2: {5},{2}
W3,V3: {6},{3}

R_v,R_w: {7},{8}""".format(U2/1000,V1/1000,V2/1000,V3/1000,W1/1000,W2/1000,W3/1000,R_v/1000,R_w/1000))

steps = 2772
def_t_v_LE,def_t_w_LE,def_t_v_TE,def_t_w_TE = deflection_torsion(steps)
x = [-x2] + [np.linspace(-x2,la-x2,steps)]

#ucoordinates,vdefbend,wdefbend,x1discr,x3discr=deformduetobending()
#ucoordinates=ucoordinates[::-1]
#vdefbend=vdefbend[::-1]
#wdefbend=wdefbend[::-1]
#
#plt.plot(ucoordinates,wdefbend)
#plt.show()


