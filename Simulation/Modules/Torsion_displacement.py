# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:10:45 2019

@author: Stijn
"""
import numpy as np
import matplotlib.pyplot as plt
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shear_center import *
from sympy import *

exec(open("./Data.txt").read())       
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(1E-10)
X2,Y1,Y2,Y3,Z1,Z2,Z3,R_y,R_z,P_y,P_z,Q_y,Q_z = transform(X2,Y1,Y2,Y3,Z1,Z2,Z3,R,P,q, theta)

length_upper = 0.25 * np.pi * h + np.sqrt((h/2)**2 + (Ca-h/2)**2)

spacing = (length_upper - wst * 8.5)/9 
thickness = np.zeros((35,3))

thickness[0] = np.array([0,tst/2,hst + tsk])
thickness[1] = np.array([thickness[0][1],thickness[0][1] + wst/2 - tst/2 ,tst + tsk])
thickness[2] = np.array([thickness[1][1],thickness[1][1] + spacing ,tsk])

for i in range(3,len(thickness)):
    if i%4 == 2:
        thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + spacing ,tsk])
    if i%4 == 1:
        thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + wst/2 - tst/2 ,tst + tsk])
    if i%4 == 0:
        thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + tst/2 ,hst + tsk])
    if i%4 == 3:
        thickness[i] = np.array([thickness[i-1][1],thickness[i-1][1] + wst/2 ,tst + tsk])
        


shear_center = 0.03 #get_ShearCenter(get_Izz(),tsk,h,Ca)
def torsion(x):
    x += x2

    T_aero = ((0.25*Ca - h/2) - shear_center) * Q_y * x
    T_Y1   = Y1 * (shear_center)
    T_Y2   = Y2 * (shear_center)
    T_Y3   = Y3 * (shear_center)
    T_P_y  = P_y * (h/2 - shear_center)
    T_R_y  = R_y * (h/2 - shear_center)
    T_P_z  = P_z * (h/2)
    T_R_z  = R_z * (h/2)
    
    if 0 < x <= x1:
        return T_aero
    if x1 < x <= -xa/2 + x2:
        return T_aero + T_Y1
    if -xa/2 + x2 < x <= x2:
        return T_aero + T_Y1 + T_R_y + T_R_z
    if x2 < x <= x2 + xa/2:
        return T_aero + T_Y1 + T_R_y + T_R_z + T_Y2
    if x2 + xa/2 < x <= x3:
        return T_aero + T_Y1 + T_R_y + T_R_z + T_Y2 + T_P_y + T_P_z
    if x3 < x <= la:
        return T_aero + T_Y1 + T_R_y + T_R_z + T_Y2 + T_P_y + T_P_z + T_Y3
    return 0 
    
Area_I  = 0.5 * np.pi*(h/2)**2
Area_II = h*(Ca-h/2)



n = 0
#split_thickness
while thickness[n][1] < 2*np.pi*h/2*0.25:
    thickness_a = thickness[:n+2]
    thickness_b = thickness[n+2:]
    n += 1
thickness_b = np.row_stack((np.array([2*np.pi*h/2*0.25,thickness_b[0][0],thickness_a[-1][2]]),thickness_b))
thickness_a[-1][1] = 2*np.pi*h/2*0.25



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

plt.plot(x,angle,color = 'r')
plt.gca().invert_xaxis()












#x,y = [],[]
#for xi in np.linspace(-x2,la-x2,1000):
#    x.append(xi)
#    y.append(torsion(xi))
#    
#plt.scatter(x,y,color = 'r')
#plt.gca().invert_xaxis()
#
#x = 2.771

#
#
#
#
#m = (P_z + P_y + R_z + R_y)*(h/2) + Q_y*la * (0.25*Ca-h/2)
















