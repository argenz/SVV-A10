# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:10:45 2019

@author: Stijn

transform, shearcenter pos.
"""

# Reading data and initializing libraries.
import numpy as np
import matplotlib.pyplot as plt
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shearcenter_pos import *
from sympy import *
exec(open("./Data.txt").read())       

def deflection_torsion(steps):
    theta_rad = np.deg2rad(theta)
    # Calculation of reaction forces.
    Iyy,Izz = get_Iyy(), get_Izz()
    U2,V1,V2,V3,W1,W2,W3,Q_v,Q_w,R_v,R_w,P_v,P_w,YA,YB,ZA,ZB = reaction_forces(Iyy,Izz)
    
    Q_v = -q*np.cos(theta_rad)
    
    # Calculation of the upper aileron length.
    length_upper = 0.25 * np.pi * h + np.sqrt((h/2)**2 + (Ca-h/2)**2)
    
    # Calculate space between stringers.
    spacing = (length_upper - wst * 8.5)/9 
    
    # Initialize array of thicknesses wrt the position. 
    # Length of 35 because 3 + 8*4 = 35
    # Width of 3 because [Start, Stop, Thickness]
    thickness = np.zeros((35,3))
    
    # First 3 sections added. (Half of the stringer at the LE)
    thickness[0] = np.array([0,tst/2,hst + tsk])
    thickness[1] = np.array([thickness[0][1],thickness[0][1] + wst/2 - tst/2 ,tst + tsk])
    thickness[2] = np.array([thickness[1][1],thickness[1][1] + spacing ,tsk])
    
    # Adding the other sections.
    for i in range(3,len(thickness)):
        if i%4 == 0:
            thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + tst/2 ,hst + tsk])
        if i%4 == 1:
            thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + wst/2 - tst/2 ,tst + tsk])
        if i%4 == 2:
            thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + spacing ,tsk])
        if i%4 == 3:
            thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + wst/2 ,tst + tsk])
    
    # Obtaining the location of the shear center. (measured from LE.)
    sc = h/2 - get_shear_center(h,Ca,Izz,tsk)
    
    # Internal torsion as a function of X (x = 0 at hinge 2.)
    def torsion(x):
        x += x2                                                 # Transfer to x = 0 at the root of the aileron.
    
        T_aero = Q_v * x * (0.25*Ca - sc)                       # Torque caused by the aerodynamic load q.
        T_V1   = -V1 * (sc - h/2)                               # Torque caused by V1.
        T_V2   = -V2 * (sc - h/2)                               # Torque caused by V2.
        T_V3   = -V3 * (sc - h/2)                               # Torque caused by V3.
        T_P    = -P_v * sc + P_w * h/2                          # Torque caused by P.
        T_R    = -R_v * sc + R_w * h/2                          # Torque caused by R.
    
        
        # Checking in what section x lies.
        if 0 < x <= x1:                                                             # section 1
            return T_aero
        if x1 < x <= -xa/2 + x2:                                                    # section 2
            return T_aero + T_V1
        if -xa/2 + x2 < x <= x2:                                                    # section 3
            return T_aero + T_V1 + T_R
        if x2 < x <= x2 + xa/2:                                                     # section 4
            return T_aero + T_V1 + T_R + T_V2
        if x2 + xa/2 < x <= x3:                                                     # section 5
            return T_aero + T_V1 + T_R + T_V2 + T_P
        if x3 < x <= la:                                                            # section 6
            return T_aero + T_V1 + T_R + T_V2 + T_P + T_V3
        return 0 
        
    # Area of the two cells, counted from LE to TE.
    Area_I  = 0.5 * np.pi*(h/2)**2
    Area_II = h*(Ca-h/2)
    
    
    
    # Splitting the thickness array into the curved part (a) and straight part (b).
    n = 0
    while thickness[n][1] < 2*np.pi*h/2*0.25:
        thickness_a = thickness[:n+2]
        thickness_b = thickness[n+2:]
        n += 1
    thickness_b = np.row_stack((np.array([2*np.pi*h/2*0.25,thickness_b[0][0],thickness_a[-1][2]]),thickness_b))
    thickness_a[-1][1] = 2*np.pi*h/2*0.25
    
    
    # Calculating the line integrals
    sum_I_arc = 0
    sum_I_spar = 0
    for section in thickness_a:
        sum_I_arc += 2*(section[1]-section[0])/section[2]
    sum_I_spar += h/(tsp)
    
    sum_II_spar = 0
    sum_II_tri  = 0
    
    for section in thickness_b:
        sum_II_tri += 2*(section[1]-section[0])/section[2]
    sum_II_spar += h/(tsp)
    
    # Solving the Torsion formula.
    y_torsion = [0]
    y_angle = [0]
    x = [-x2]
    n = 2772
    for xi in np.linspace(-x2,la-x2,steps):
        d_theta_d_z = sympy.Matrix([[2*Area_I,2*Area_II,0,torsion(xi)],
                                    [1/(2*Area_I*G)*sum_I_arc, -1/(2*Area_I*G)*sum_I_spar,-1,0],
                                    [-1/(2*Area_II*G)*sum_II_spar, 1/(2*Area_II*G)*sum_II_tri,-1,0]])
    
        sol = d_theta_d_z.rref()[0][11]
        x.append(xi)
        y_torsion.append(torsion(xi))
        y_angle.append(y_angle[-1] + np.rad2deg(float(sol))*((-x2-la+x2)/n))
    
    y_torsion = np.array(y_torsion)
    
    i = 0
    while x[i] < 0:
        i+=1
    zero = i
    y_angle = np.array(y_angle)
    y_angle_corrected = y_angle-y_angle[zero]
    
    deflection_v_LE = h/2 * np.sin(y_angle_corrected)
    deflection_w_LE = h/2 * np.cos(y_angle_corrected) - h/2
    deflection_v_TE = (la-h/2) * np.sin(y_angle_corrected)
    deflection_w_TE = (la-h/2) * np.cos(y_angle_corrected) - (la-h/2)

    return def_t_v_LE,def_t_w_LE,def_t_v_TE,def_t_w_TE

#x = [-x2] + [np.linspace(-x2,la-x2,steps)]
#
#fig2 = plt.figure()
#
#ax1 = fig2.add_subplot(221)
#ax1.plot(x,deflection_v_LE)
#
#ax1 = fig2.add_subplot(222)
#ax1.plot(x,deflection_w_LE)
#
#ax1 = fig2.add_subplot(223)
#ax1.plot(x,deflection_v_TE)
#
#ax1 = fig2.add_subplot(224)
#ax1.plot(x,deflection_w_TE)











