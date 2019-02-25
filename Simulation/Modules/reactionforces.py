# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:53:09 2019

@author: Stijn

This function calculated the forces on the aileron in the original(fixed to the wing) coordinate system
"""
# Reading data and initializing libraries.
import numpy as np
import sympy
from Modules.MOI import *
exec(open("./Data.txt").read())
theta = 0
def reaction_forces(I):
    theta_rad = np.deg2rad(theta)
    # Calculation of R, just a moment equation around the hingeline to solve for R.
    R =  (-q*la*(0.25*Ca-0.5*h)*np.cos(theta_rad))/(h*0.5*np.sqrt(2)*np.sin(np.pi*0.25-theta_rad)) - P
    
    # Calculation or X2, just sum of forces in the x direction, one force hence X2 equals zero
    X2 = 0
    
    # Calculation for Y1,Y2,Y3. This is done by using moment equation around hinge 2, sum of forces in y,
    # and 3 compatibility equations using the known deflections of hinges 1,2 and 3.
    #[y1,y2,y3,sinthetay,Mly,Mry,Vly,Vry, integration constant 1, integration constant 2, ANSWER], same for z
    y_direction = sympy.Matrix([[1,1,1,0,0,0,0,0,0,0,la*q],
                            [(x1-x2),0,(x3-x2),0,0,0,0,0,0,0,-q*la*(x2-0.5*la)],
                            [0,(1/6)*(x2-x1)**3,0,E*I*(x2-x1),0,(1/2)*(x2-x1)**2,0,-1/6(x2-x1)**3,(x2-x1),0,d1*E*I+1/24*(x2-x1)**4*q],
                            [0,1/6*(x3-x2)**3,0,-E*I*(x3-x2),1/2*(x3-x2)**2,0,1/6*(x3-x2)**3,0,0,(x3-x2),d3*E*I+1/24*(x3-x2)**4*q],
                            [0,0,0,0,1,1,0,0,0,0,0],
                            [0,0,0,0,0,0,1,1,0,0,0],
                                [-1,0,0,0,0,0,1,0,0,0,-q*(la-x2)],
                                [0,0,-1,0,0,0,0,1,0,0,-q*x2],
                                
    
    # Calculation for Z1,Z2,Z3. This is done by using moment equation around hinge 2, sum of forces in z,
    # and 3 compatibility equations using the known deflections of hinges 1,2 and 3. 
    z_direction = sympy.Matrix([[-1,-1,-1,0,0,0,0,0,0,0,R+P],
                            [x1-x2,0,x3-x2,0,0,0,0,0,0,0, 0.5*xa*(R-P)],
                            []
    
    # Row reducing the two matrices to solve for the forces.
    rrefy = y_direction.rref()[0]
    rrefz = z_direction.rref()[0]
    
    # Extracting the results.
    Y1, Y2, Y3, sinthetay = rrefy[10], rrefy[20], rrefy[30], rrefy[40]
    Z1, Z2, Z3, sinthetaz = rrefz[10], rrefz[20], rrefz[30], rrefz[40]
    
    return float(X2), float(Y1),float(Y2),float(Y3),float(Z1),float(Z2),float(Z3),R,sinthetay,sinthetaz
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
    
    
Izz = Izz()1.25180748944789E-5

Iyy = Iyy()#9.93425176458821E-5
Iyz = Iyz()#0

Izzrotated=Izzrotated(Izz,Iyy,Iyz)


X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izzrotated)

print("""X2: {0}
Z1,Y1: {4},{1}
Z2,Y2: {5},{2}
Z3,Y3: {6},{3}

R: {7}""".format(X2/1000,Y1/1000,Y2/1000,Y3/1000,Z1/1000,Z2/1000,Z3/1000,R/1000))

