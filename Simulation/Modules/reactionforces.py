# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:53:09 2019

@author: Stijn
"""
import numpy as np
import sympy

exec(open("../Data.txt").read())
I = 1E-10

R = 0#(-q*la*(0.25*Ca-0.5*h)-P)/(np.cos(theta)*0.5*h)
y_force = sympy.Matrix([[(1/6)*(x2-x1)**3, 0, 0, x2, 1, (1/24)*q*x2**4],
                          [0, 0, 0, x1, 1, d1*E*I + (1/24)*q*x1**4],
                          [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3, 0, x3, 1, d3*E*I + (1/24)*q*x3**4],
                          [x2-x1, 0, -x3+x2, 0, 0, 0.5*q*x2**2 - 0.5*q*(x3-x2)**2],
                          [1, 1, 1, 0, 0, la*q]])

z_force = sympy.Matrix([[1,1,1,0,0,-R-P],
                        [x2-x1,0,x2-x3,0,0,-0.5*xa*(R-P)],
                        [0,0,0,x1,1,0],
                        [-(1/6)*(x2-x1)**3,0,0,x2,1,(1/6)*(0.5*xa)**3*R],
                        [-(1/6)*(x3-x1)**3,-(1/6)*(x3-x2)**3,0,x3,1,-(1/6)*(x3-(x2-0.5*xa))**3*R -(1/6)*(x3-(x2+0.5*xa))**3*P]])


rrefy = y_force.rref()[0]
rrefz = z_force.rref()[0]

y1, y2, y3, yA, yB = rrefy[5], rrefy[11], rrefy[17], rrefy[23], rrefy[29]
z1, z2, z3, zA, zB = rrefz[5], rrefz[11], rrefz[17], rrefz[23], rrefz[29]

def test_reactionforcesy():
    margin = 0.0001
    assert -margin <= y1 + y2 + y3 -la*q <= margin
    assert -margin <= int((x2-x1)*y1 - (x3-x2)*y3 - 0.5*q*x2**2 + 0.5*q*(x3-x2)**2) <= margin
    assert -margin <= - d1 * E * I - (1/24)*q*x1**4 + yA*x1+ yB <= margin
    assert -margin <= - (1/24)*q*x2**4 + (1/6)*(x2-x1)**3*y1 + yA*x2 + yB <= margin
    assert -margin <= - d3*E*I - (1/24)*q*x3**4 + (1/6)*(x3-x1)**3*y1 + (1/6)*(x3-x2)**3*y2 + yA*x3 + yB <= margin
    
test_reactionforcesy()