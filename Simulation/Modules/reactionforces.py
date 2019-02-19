# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:53:09 2019

@author: Stijn
"""
import numpy as np
import sympy

exec(open("./Data.txt").read())

#R = (-q*la*(0.25*Ca-0.5*h)-P)/(np.cos(theta)*0.5*h)
def reaction_forces(I):
    R =  (-q*la*(0.25*Ca-0.5*h)*np.cos(np.deg2rad(theta)))/(h*0.5*np.sqrt(2)*np.sin(np.pi*0.25-np.deg2rad(theta))) - P
    
    y_force = sympy.Matrix([[(1/6)*(x2-x1)**3, 0, 0, x2, 1, (1/24)*q*x2**4],
                              [0, 0, 0, x1, 1, d1*E*I + (1/24)*q*x1**4],
                              [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3, 0, x3, 1, d3*E*I + (1/24)*q*x3**4],
                              [x2-x1, 0, -x3+x2, 0, 0, 0.5*q*x2**2 - 0.5*q*(x3-x2)**2],
                              [1, 1, 1, 0, 0, la*q]])
    
    z_force = sympy.Matrix([[-1,-1,-1,0,0,R+P],
                            [x1-x2,0,x3-x2,0,0, -0.5*xa*(P-R)],
                            [0,0,0,x1,1,0],
                            [(1/6)*(x2-x1)**3,0,0,x2,1,-(1/6)*(-0.5*xa)**3*R],
                            [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3,0,x3,1, -(1/6)*(x3-(x2-0.5*xa))**3*R - (1/6)*(x3-(x2+0.5*xa))**3*P]])
    
    
    rrefy = y_force.rref()[0]
    rrefz = z_force.rref()[0]
    
    y1, y2, y3, yA, yB = rrefy[5], rrefy[11], rrefy[17], rrefy[23], rrefy[29]
    z1, z2, z3, zA, zB = rrefz[5], rrefz[11], rrefz[17], rrefz[23], rrefz[29]
    
    def test_reactionforcesy():
        margin = 0.0001
        assert -margin <= y1 + y2 + y3 -la*q <= margin
        assert -margin <= (x2-x1)*y1 - (x3-x2)*y3 - 0.5*q*x2**2 + 0.5*q*(x3-x2)**2 <= margin
        assert -margin <= - d1 * E * I - (1/24)*q*x1**4 + yA*x1+ yB <= margin
        assert -margin <= - (1/24)*q*x2**4 + (1/6)*(x2-x1)**3*y1 + yA*x2 + yB <= margin
        assert -margin <= - d3*E*I - (1/24)*q*x3**4 + (1/6)*(x3-x1)**3*y1 + (1/6)*(x3-x2)**3*y2 + yA*x3 + yB <= margin
        
    test_reactionforcesy()
    
    def test_reactionforcesz():
        margin = 0.0001
        assert -margin <= z1 + z2 + z3 + R + P <= margin
        assert -margin <= -(x3-x2)*z3+(x2-x1)*z1+0.5*xa*(R-P)<= margin
        assert -margin <= zA*x1+zB <= margin
        assert -margin <= zA*x2+zB  + (1/6)*(x2-x1)**3*z1 + (1/6)*(-0.5*xa)**3*R <= margin
        assert -margin <= zA*x3+zB + (1/6)*(x3-x1)**3*z1 + (1/6)*(x3-(x2-0.5*xa))**3*R + (1/6)*(x3-x2)**3*z2 + (1/6)*(x3-(x2+0.5*xa))**3*P <= margin
    
    def test_R():
        margin = 0.0001
        assert -margin <= (q*la*(0.25*Ca - 0.5*h)*np.cos(np.deg2rad(theta))) + (R + P) * (0.5*np.sqrt(2)*h*np.sin(0.25*np.pi - np.deg2rad(theta))) <= margin
      
    test_reactionforcesy()
    test_reactionforcesz()
    test_R()
    
    return float(y1),float(y2),float(y3),float(z1),float(z2),float(z3),R


#print("""y1: {0}
#y2: {1}
#y3: {2}
#z1: {3}
#z2: {4}
#z3: {5}
#R : {6}
#""".format(y1,y2,y3,z1,z2,z3,R))
    
