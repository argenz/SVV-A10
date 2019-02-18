# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:53:09 2019

@author: Stijn
"""
import numpy as np
import sympy

exec(open("../Data.txt").read())
x = 5
E,I = 1,1

y_force = sympy.Matrix([[(1/6)*(x2-x1)**3, 0, 0, x2, 1, (1/24)*q*x2**4],
                          [0, 0, 0, x1, 1, d1*E*I + (1/24)*q*x1**4],
                          [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3, 0, x3, 1, d3*E*I + (1/24)*q*x3**4],
                          [x2-x1, 0, -x3+x2, 0, 0, 0.5*q*x2**2 - 0.5*q*(x3-x2)**2],
                          [1, 1, 1, 0, 0, la*q]])

rref = y_force.rref()[0]
y1, y2, y3, A, B = rref[5], rref[11], rref[17], rref[23], rref[29]

def test_reactionforces():
    margin = 0.0001
    assert -margin <= y1 + y2 + y3 -la*q <= margin
    assert -margin <= int((x2-x1)*y1 - (x3-x2)*y3 - 0.5*q*x2**2 + 0.5*q*(x3-x2)**2) <= margin
    assert -margin <= - d1 * E * I - (1/24)*q*x1**4 + A*x1+ B <= margin
    assert -margin <= - (1/24)*q*x2**4 + (1/6)*(x2-x1)**3*y1 + A*x2 + B <= margin
    assert -margin <= - d3*E*I - (1/24)*q*x3**4 + (1/6)*(x3-x1)**3*y1 + (1/6)*(x3-x2)**3*y2 + A*x3 + B <= margin
    
test_reactionforces()