# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:10:45 2019

@author: Stijn
"""
import numpy as np
import matplotlib.pyplot as plt
from Modules.reactionforces import reaction_forces
from Modules.centroid import centroid
from Modules.Tools import transform
exec(open("./Data.txt").read())       
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(1E-10)
X2,Y1,Y2,Y3,Z1,Z2,Z3,R_y,R_z,P_y,P_z,Q_y,Q_z = transform(X2,Y1,Y2,Y3,Z1,Z2,Z3,R,P,q)

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
        
        
#thickness = np.row_stack((thickness[::-1],thickness))
#integral = 0
#for section in thickness:
#    integral += (section[1]-section[0])/section[2]

Area_II = h*(Ca-h/2)

















plt.scatter(thickness[:,0],thickness[:,2],color = 'r')
plt.scatter(thickness[:,1],thickness[:,2],color = 'r')

plt.scatter(length_upper,tsk, color = 'b')