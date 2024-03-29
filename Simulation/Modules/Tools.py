# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:23:29 2019

@author: Stijn

This file contains all kinds of usefull functions, such as the transform function
to transfer to the internal coordinate system.
"""
# Reading data and initializing libraries.
import numpy as np
exec(open("./Data.txt").read()) 

# General transform function.
def transform(X2,Y1,Y2,Y3,Z1,Z2,Z3,R,P,Q,theta):
    # Function to transform a force in y-direction.
    def transformy(Yxx,theta):
        theta_rad = np.deg2rad(theta)
        Yxx_y = Yxx * np.cos(theta_rad)
        Yxx_z = -Yxx * np.sin(theta_rad)
        return Yxx_y, Yxx_z
    
    # Function to transform a force in z-direction.
    def transformz(Zxx,theta):
        theta_rad = np.deg2rad(theta)
        Zxx_y = Zxx * np.sin(theta_rad)
        Zxx_z = -Zxx * np.cos(theta_rad)
        return Zxx_y, Zxx_z
    
    # Transforming the forces in y-direction.
    Y1_y,Y1_z = transformy(Y1,theta)
    Y2_y,Y2_z = transformy(Y2,theta)
    Y3_y,Y3_z = transformy(Y3,theta)
    
    # Transforming the forces in z-direction.
    Z1_y,Z1_z = transformz(Z1,theta)
    Z2_y,Z2_z = transformz(Z2,theta)
    Z3_y,Z3_z = transformz(Z3,theta)
    
    # Superimposing the forces at the hinges.
    Y1_new = Y1_y + Z1_y
    Y2_new = Y2_y + Z2_y
    Y3_new = Y3_y + Z3_y
    
    Z1_new = Y1_z + Z1_z
    Z2_new = Y2_z + Z2_z
    Z3_new = Y3_z + Z3_z
    
    # Transforming the actuator forces.
    P_y, P_z = transformz(P,theta)
    R_y, R_z = transformz(R,theta)
    
    # Transforming the q force.
    Q_y, Q_z = transformy(Q,theta)
    
    return X2,Y1_new,Y2_new,Y3_new,Z1_new,Z2_new,Z3_new,-R_y,R_z,-P_y,P_z,Q_y,Q_z

# Test function to test transform.
def test_transform():
    assert transform(0,1,1,1,0,0,0,0,0,0,90) == (0, 6.123233995736766e-17, 6.123233995736766e-17, 6.123233995736766e-17, 1.0, 1.0, 1.0, -0.0, 0.0, -0.0, 0.0, 0.0, 0.0)
    assert transform(0,0,0,0,1,1,1,0,0,0,90) == (0, 1.0, 1.0, 1.0, 6.123233995736766e-17, 6.123233995736766e-17, 6.123233995736766e-17, -0.0, 0.0, -0.0, 0.0, 0.0, 0.0)
    assert transform(0,0,0,0,0,0,0,1,1,1,90) == (0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 6.123233995736766e-17, -1.0, 6.123233995736766e-17, 6.123233995736766e-17, 1.0)

#test_transform()

