# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:53:09 2019

@author: Stijn

This function calculated the forces on the aileron in the original(fixed to the wing) coordinate system
"""
# Reading data and initializing libraries.
import numpy as np
import sympy
exec(open("./Data.txt").read())

def reaction_forces(Izz):
    # Calculation of R, just a moment equation around the hingeline to solve for R.
    R =  (-q*la*(0.25*Ca-0.5*h)*np.cos(np.deg2rad(theta)))/(h*0.5*np.sqrt(2)*np.sin(np.pi*0.25-np.deg2rad(theta))) - P
    
    # Calculation or X2, just sum of forces in the x direction, one force hence X2 equals zero
    X2 = 0
    
    # Calculation for Y1,Y2,Y3. This is done by using moment equation around hinge 2, sum of forces in y,
    # and 3 compatibility equations using the known deflections of hinges 1,2 and 3. 
    y_force = sympy.Matrix([[(1/6)*(x2-x1)**3, 0, 0, x2, 1, (1/24)*q*x2**4],
                              [0, 0, 0, x1, 1, d1*E*Izz + (1/24)*q*x1**4],
                              [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3, 0, x3, 1, d3*E*Izz + (1/24)*q*x3**4],
                              [x2-x1, 0, -x3+x2, 0, 0, 0.5*q*x2**2 - 0.5*q*(x3-x2)**2],
                              [1, 1, 1, 0, 0, la*q]])
    
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
        assert -margin <= (x2-x1)*Y1 - (x3-x2)*Y3 - 0.5*q*x2**2 + 0.5*q*(x3-x2)**2 <= margin
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
        assert -margin <= (q*la*(0.25*Ca - 0.5*h)*np.cos(np.deg2rad(theta))) + (R + P) * (0.5*np.sqrt(2)*h*np.sin(0.25*np.pi - np.deg2rad(theta))) <= margin
      
    test_reactionforcesy()
    test_reactionforcesz()
    test_R()
