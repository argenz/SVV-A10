# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:42:03 2019

@author: A10

Main function to calculate delfection and shear flow of A320 aileron
"""
# Reading data and initializing libraries and other functions.
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shearcenter_pos import *
from Modules.Finddeflectionbending_update2 import *
from Modules.deflectiondistributedload import *
from Modules.deflectionpointload import *
#from Modules.FinalShearFlow import *
from Modules.Torsion_displacement import *

exec(open("./Data.txt").read())    
theta_rad = np.deg2rad(theta)
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

# Numerical deflections.
steps = 2772
x = np.linspace(-x2,la-x2,steps)
def_t_v_LE,def_t_w_LE,def_t_v_TE,def_t_w_TE = deflection_torsion(steps)
def_b_v,def_b_w = deformduetobending(steps)

deflection_total_v_LE = def_t_v_LE + def_b_v
deflection_total_v_TE = def_t_v_TE + def_b_v
deflection_total_w_LE = def_t_w_LE + def_b_w
deflection_total_w_TE = def_t_w_TE + def_b_w

# Validation data.
TEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheetname=0)         #X,Y,Z,dY values of columns
LEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheetname=1)
HINGEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheetname=2)

TEDY = TEDY.values/1000                                                     #to get everything in meters
LEDY = LEDY.values/1000
HINGEDY = HINGEDY.values/1000

TEDY[:,0] = TEDY[:,0]-x2                                                  #to match x-coordinates to ours
LEDY[:,0] = LEDY[:,0]-x2
HINGEDY[:,0] = HINGEDY[:,0]-x2

# Deflections in local rf.
d1_w = -d1 * np.sin(theta_rad)
d1_v = d1 * np.cos(theta_rad)

d3_w = -d3 * np.sin(theta_rad)
d3_v = d3 * np.cos(theta_rad)

if True:
    plt.close()    
    fig0 = plt.figure()
    ax = fig0.add_subplot(111)    
    ax.plot(x,def_b_v, color = 'r', label = 'Numerical solution')
    ax.plot([x[0],x[-1]],[0,0],color = 'grey', label = 'Undeformed aileron')
    ax.plot(HINGEDY[:,0],HINGEDY[:,3], color = 'blue', label = 'Validation data')
    #ax.plot(HINGEDY[:,0][::-1],HINGEDY[:,3])
    ax.scatter([(x1-x2),0,(x3-x2)],[d1_v,0,d3_v],label = 'Hinge deflections')
    ax.set(title = 'Deformation due to bending', xlabel = 'U [m]',ylabel = 'V [m]')
    plt.gca().invert_xaxis()
    ax.legend()
    fig0.savefig('./Output/Bending_u,v.pdf')
    
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.plot(x,def_b_w, color = 'r', label = 'Deformed aileron')
    ax.plot([x[0],x[-1]],[0,0],color = 'grey', label = 'Undeformed aileron')
    ax.scatter([(x1-x2),0,(x3-x2)],[d1_w,0,d3_w],label = 'Hinge deflections')
    ax.set(title = 'Deformation due to bending', xlabel = 'U [m]',ylabel = 'W [m]')
    plt.gca().invert_xaxis()
    ax.legend()
    fig1.savefig('./Output/Bending_u,w.pdf')


    fig2 = plt.figure()    
    ax1 = fig2.add_subplot(221)
    ax1.plot(LEDY[:,0],LEDY[:,3])
    ax1.plot(x,deflection_total_v_LE)
    #ax1.plot(HINGEDY[:,0],HINGEDY[:,3])
    ax1.set(title = 'LE', xlabel = 'U', ylabel = 'V')
    
    ax2 = fig2.add_subplot(222)
    ax2.plot(x,deflection_total_v_TE)
    ax2.plot(TEDY[:,0],TEDY[:,3])
    ax2.set(title = 'TE', xlabel = 'U', ylabel = 'V')
    
    ax3 = fig2.add_subplot(223)
    ax3.plot(x,deflection_total_w_LE)
    ax3.set(title = 'LE', xlabel = 'U', ylabel = 'W')
    
    ax4 = fig2.add_subplot(224)
    ax4.plot(x,deflection_total_w_TE)
    ax4.set(title = 'TE', xlabel = 'U', ylabel = 'W')
    fig2.savefig('./Output/deflections_LE_TE.pdf')








