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

# Obtaining the reaction forces and their transform. forces in internal coordinatesystem!!    
U2,V1,V2,V3,W1,W2,W3,Q_v,Q_w,R_v,R_w,P_v,P_w,YA,YB,ZA,ZB = reaction_forces(Iyy,Izz)


print("""X2: {0}
W1,V1: {4},{1}
W2,V2: {5},{2}
W3,V3: {6},{3}

R_v,R_w: {7},{8}""".format(U2/1000,V1/1000,V2/1000,V3/1000,W1/1000,W2/1000,W3/1000,R_v/1000,R_w/1000))

steps = 2772
x = np.linspace(-x2,la-x2,steps)
def_t_v_LE,def_t_w_LE,def_t_v_TE,def_t_w_TE = deflection_torsion(steps)
def_b_v,def_b_w = deformduetobending(steps)

deflection_total_v_LE = def_t_v_LE + def_b_v
deflection_total_v_TE = def_t_v_TE + def_b_v
deflection_total_w_LE = def_t_w_LE + def_b_w
deflection_total_w_TE = def_t_w_TE + def_b_w

fig = plt.figure()

ax1 = fig.add_subplot(221)
ax1.plot(x,deflection_total_v_LE)
ax1.set(title = 'LE', xlabel = 'U', ylabel = 'V')

ax2 = fig.add_subplot(222)
ax2.plot(x,deflection_total_v_TE)
ax2.set(title = 'TE', xlabel = 'U', ylabel = 'V')

ax3 = fig.add_subplot(223)
ax3.plot(x,deflection_total_w_LE)
ax3.set(title = 'LE', xlabel = 'U', ylabel = 'W')

ax4 = fig.add_subplot(224)
ax4.plot(x,deflection_total_w_TE)
ax4.set(title = 'TE', xlabel = 'U', ylabel = 'W')

if True:
    plt.close()    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(x,def_b_v, color = 'r', label = 'Deformed aileron')
    ax.plot([x[0],x[-1]],[0,0],color = 'grey', label = 'Undeformed aileron')
    ax.set(title = 'Deformation due to bending', xlabel = 'U [m]',ylabel = 'V [m]')
    plt.gca().invert_xaxis()
    ax.legend()
    fig.savefig('./Output/Bending_u,v.pdf')
    plt.close()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,def_b_w, color = 'r', label = 'Deformed aileron')
    ax.plot([x[0],x[-1]],[0,0],color = 'grey', label = 'Undeformed aileron')
    
    ax.set(title = 'Deformation due to bending', xlabel = 'U [m]',ylabel = 'W [m]')
    plt.gca().invert_xaxis()
    ax.legend()
    fig.savefig('./Output/Bending_u,w.pdf')

avg = 0
avg += abs(100-(-11.91112471/(W1/1000)*100))	
avg += abs(100-(26.57759392/(V1/1000)*100))
#avg += abs(100-(0.191719995/(W2/1000)*100))	
avg += abs(100-(-36.37587519/(V2/1000)*100))
avg += abs(100-(9.013615578/(W3/1000)*100))	
avg += abs(100-(22.35091127/(V3/1000)*100))

print(avg/5)
















