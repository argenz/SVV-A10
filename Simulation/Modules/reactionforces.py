# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:53:09 2019

@author: Stijn

This function calculated the forces on the aileron in the internal coordinate system x,y,z <> u,v,w
"""
# Reading data and initializing libraries.
import numpy as np
import sympy
from Modules.Tools import *
#from Modules.MOI import *
exec(open("./Data.txt").read())
theta = 0
def reaction_forces(I):
    theta_rad = np.deg2rad(theta)
    # Calculation of R, just a moment equation around the hingeline to solve for R.
    R =  (-q*la*(0.25*Ca-0.5*h)*np.cos(theta_rad))/(h*0.5*np.sqrt(2)*np.sin(np.pi*0.25-theta_rad)) - P
    
    # Calculation or X2, just sum of forces in the x direction, one force hence X2 equals zero
    X2 = 0
    
    d1_w = -d1 * np.sin(theta_rad)
    d1_v = d1 * np.cos(theta_rad)
    
    d3_w = -d3 * np.sin(theta_rad)
    d3_v = d3 * np.cos(theta_rad)
    
    X2,Y1,Y2,Y3,Z1,Z2,Z3,R_v,R_w,P_v,P_w,Q_v,Q_w = transform(0,0,0,0,0,0,0,-R,-P,-q,theta)
    
    
    # Calculation for Y1,Y2,Y3. This is done by using moment equation around hinge 2, sum of forces in y,
    # and 3 compatibility equations using the known deflections of hinges 1,2 and 3. 
    y_force = sympy.Matrix([[(1/6)*(x2-x1)**3, 0, 0, x2, 1, (1/24)*Q_v*x2**4 - 1/6 * (xa/2) * R_v],#Bending hinge 2
                              [0, 0, 0, x1, 1, d1_v*E*Izz + (1/24)*Q_v*x1**4],#Bending hinge 1
                              [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3, 0, x3, 1, d3_v*E*Izz + (1/24)*Q_v*x3**4 - 1/6 * (x3 - x2 + xa/2) * R_v - 1/6 * (x3 - x2 - xa/2) * P_v],#Bending hinge 3
                              [x1-x2, 0, x3-x2, 0, 0, Q_v*la*(la/2 - x2) - R_v * xa/2 + P_v * xa/2],#external moment hinge 2
                              [1, 1, 1, 0, 0, la*Q_v + R_v + P_v]])#sum of forces
    
    # Calculation for Z1,Z2,Z3. This is done by using moment equation around hinge 2, sum of forces in z,
    # and 3 compatibility equations using the known deflections of hinges 1,2 and 3. 
    z_force = sympy.Matrix([[-1,-1,-1,0,0,R+P],
                            [x1-x2,0,x3-x2,0,0, -0.5*xa*(P-R)],
                            [0,0,0,x1,1,0],
                            [(1/6)*(x2-x1)**3,0,0,x2,1,-(1/6)*(-0.5*xa)**3*R],
                            [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3,0,x3,1, -(1/6)*(x3-(x2-0.5*xa))**3*R - (1/6)*(x3-(x2+0.5*xa))**3*P]])
    
    # Row reducing the two matrices to solve for the forces.
    rrefy = y_force.rref()[0]
    rrefz = z_force.rref()[0]
    
    # Extracting the results.
    Y1, Y2, Y3, yA, yB = rrefy[5], rrefy[11], rrefy[17], rrefy[23], rrefy[29]
    Z1, Z2, Z3, zA, zB = rrefz[5], rrefz[11], rrefz[17], rrefz[23], rrefz[29]
    
    return float(X2), float(Y1),float(Y2),float(Y3),float(Z1),float(Z2),float(Z3),R
    # In order to test the results, comment out the return statement.
    
    # Below are the equation used for the calculations.
    def test_reactionforcesy():
        margin = 0.0001
        assert -margin <= Y1 + Y2 + Y3 -la*q <= margin
        assert -margin <= -(x2-x1)*Y1 + (x3-x2)*Y3 - q*la*(x2-la/2) <= margin
        assert -margin <= - d1 * E * Izz - (1/24)*q*x1**4 + yA*x1+ yB <= margin
        assert -margin <= - (1/24)*q*x2**4 + (1/6)*(x2-x1)**3*Y1 + yA*x2 + yB <= margin
        assert -margin <= - d3*E*Izz - (1/24)*q*x3**4 + (1/6)*(x3-x1)**3*Y1 + (1/6)*(x3-x2)**3*Y2 + yA*x3 + yB <= margin
        
    test_reactionforcesy()
    
    def test_reactionforcesz():
        margin = 0.0001
        assert -margin <= Z1 + Z2 + Z3 + R + P <= margin
        assert -margin <= -(x3-x2)*Z3+(x2-x1)*Z1+0.5*xa*(R-P)<= margin
        assert -margin <= zA*x1+zB <= margin
        assert -margin <= zA*x2+zB  + (1/6)*(x2-x1)**3*Z1 + (1/6)*(-0.5*xa)**3*R <= margin
        assert -margin <= zA*x3+zB + (1/6)*(x3-x1)**3*Z1 + (1/6)*(x3-(x2-0.5*xa))**3*R + (1/6)*(x3-x2)**3*Z2 + (1/6)*(x3-(x2+0.5*xa))**3*P <= margin
    
    def test_R():
        margin = 0.0001
        assert -margin <= (q*la*(0.25*Ca - 0.5*h)*np.cos(theta_rad)) + (R + P) * (0.5*np.sqrt(2)*h*np.sin(0.25*np.pi - theta_rad)) <= margin
      
    test_reactionforcesy()
    test_reactionforcesz()
    test_R()
    
    
Izz = 1.25180748944789E-5



X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izz)

print("""X2: {0}
Z1,Y1: {4},{1}
Z2,Y2: {5},{2}
Z3,Y3: {6},{3}

R: {7}""".format(X2/1000,Y1/1000,Y2/1000,Y3/1000,Z1/1000,Z2/1000,Z3/1000,R/1000))

