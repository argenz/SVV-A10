# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:10:45 2019

@author: Stijn
"""

# Reading data and initializing libraries.
import numpy as np
import matplotlib.pyplot as plt
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shear_center import *
from sympy import *
exec(open("./Data.txt").read())       

# Calculation of reaction forces.
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(1E-10)
X2,Y1,Y2,Y3,Z1,Z2,Z3,R_y,R_z,P_y,P_z,Q_y,Q_z = transform(X2,Y1,Y2,Y3,Z1,Z2,Z3,R,P,q, theta)

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

# Obtaining the location of the shear center.
shear_center = 0.001 #get_ShearCenter(get_Izz(),tsk,h,Ca)

# Internal torsion as a function of X (x = 0 at hinge 2.)
def torsion(x):
    x += x2                                                 # Transfer to x = 0 at the root of the aileron.

    T_aero = ((0.25*Ca - h/2) - shear_center) * Q_y * x     # Torque caused by the aerodynamic load q.
    T_Y1   = Y1 * (shear_center)                            # Torque caused by Y1.
    T_Y2   = Y2 * (shear_center)                            # Torque caused by Y2.
    T_Y3   = Y3 * (shear_center)                            # Torque caused by Y3.
    T_P_y  = P_y * (h/2 - shear_center)                     # Torque caused by P_y.
    T_R_y  = R_y * (h/2 - shear_center)                     # Torque caused by R_y.
    T_P_z  = P_z * (h/2)                                    # Torque caused by P_z.
    T_R_z  = R_z * (h/2)                                    # Torque caused by R_z.
    
    # Checking in what section x lies.
    if 0 < x <= x1:                                                             # section 1
        return T_aero
    if x1 < x <= -xa/2 + x2:                                                    # section 2
        return T_aero + T_Y1
    if -xa/2 + x2 < x <= x2:                                                    # section 3
        return T_aero + T_Y1 + T_R_y + T_R_z
    if x2 < x <= x2 + xa/2:                                                     # section 4
        return T_aero + T_Y1 + T_R_y + T_R_z + T_Y2
    if x2 + xa/2 < x <= x3:                                                     # section 5
        return T_aero + T_Y1 + T_R_y + T_R_z + T_Y2 + T_P_y + T_P_z
    if x3 < x <= la:                                                            # section 6
        return T_aero + T_Y1 + T_R_y + T_R_z + T_Y2 + T_P_y + T_P_z + T_Y3
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
angle = [0]
x = [-x2]
n = 1000
for xi in np.linspace(-x2,la-x2,n):
    d_theta_d_z = sympy.Matrix([[2*Area_I,2*Area_II,0,torsion(xi)],
                                [1/(2*Area_I*G)*sum_I_arc, -1/(2*Area_I*G)*sum_I_spar,-1,0],
                                [-1/(2*Area_II*G)*sum_II_spar, 1/(2*Area_II*G)*sum_II_tri,-1,0]])

    sol = d_theta_d_z.rref()[0][11]
    x.append(xi)
    angle.append(angle[-1] + np.rad2deg(float(sol))*((-x2-la+x2)/n))

# Plotting the angle over the length of the aileron.
#plt.plot(x,angle,color = 'r')
#plt.gca().invert_xaxis()












x,y = [],[]
for xi in np.linspace(-x2,la-x2,1000):
    x.append(xi)
    y.append(torsion(xi))
    
plt.scatter(x,y,color = 'r', s = 1)
#plt.gca().invert_xaxis()

x = 2.771

#
#
#
#
#m = (P_z + P_y + R_z + R_y)*(h/2) + Q_y*la * (0.25*Ca-h/2)
















