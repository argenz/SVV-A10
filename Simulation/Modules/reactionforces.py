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
from Modules.MOI import *
exec(open("./Data.txt").read())
def reaction_forces(Iyy,Izz):
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
    y_force = sympy.Matrix([[1, 1, 1, 0, 0, -la*Q_v - R_v - P_v], #sum of forces
                            [x1-x2, 0, x3-x2, 0, 0, -Q_v*la*(la/2 - x2) + R_v * xa/2 - P_v * xa/2], #external moment hinge 2
                            [0, 0, 0, x1, 1, d1_v*E*Izz - (1/24)*Q_v*x1**4],#Bending hinge 1
                            [(1/6)*(x2-x1)**3, 0, 0, x2, 1, -(1/24)*Q_v*x2**4 - 1/6 * (xa/2)**3 * R_v],#Bending hinge 2
                            [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3, 0, x3, 1, d3_v*E*Izz - (1/24)*Q_v*x3**4 - 1/6 * (x3 - x2 + xa/2)**3 * R_v - 1/6 * (x3 - x2 - xa/2)**3 * P_v]])#Bending hinge 3

    
    # Calculation for Z1,Z2,Z3. This is done by using moment equation around hinge 2, sum of forces in z,
    # and 3 compatibility equations using the known deflections of hinges 1,2 and 3. 
    z_force = sympy.Matrix([[1,1,1,0,0,-Q_w*la-P_w-R_w], #sum of forces
                            [x1-x2,0,x3-x2,0,0, 0.5*xa*(R_w-P_w)+Q_w*la*(x2-la/2)], #external moment hinge 2.
                            [0,0,0,x1,1,E*Iyy*d1_w-1/24*Q_w*x1**4], #Bending hinge 1
                            [(1/6)*(x2-x1)**3,0,0,x2,1,-(1/6)*(0.5*xa)**3*R_w-1/24*Q_w*x2**4], #Bending hinge 2
                            [(1/6)*(x3-x1)**3, (1/6)*(x3-x2)**3,0,x3,1, E*Iyy*d3_w - (1/6)*(x3-x2+0.5*xa)**3*R_w - (1/6)*(x3-x2-0.5*xa)**3*P_w - 1/24*Q_w*x3**4]])
    
    # Row reducing the two matrices to solve for the forces.
    rrefy = y_force.rref()[0]
    rrefz = z_force.rref()[0]
    
    # Extracting the results.
    Y1, Y2, Y3 ,YA, YB = rrefy[5], rrefy[11], rrefy[17], rrefy[23], rrefy[29]
    Z1, Z2, Z3, ZA, ZB = rrefz[5], rrefz[11], rrefz[17], rrefz[23], rrefz[29]

    #finding the angle at hinge 2 for y and z
    theta_x0_z=ZB/(E*Iyy)
    theta_x0_y=YB/(E*Izz)
    
    # In order to test the results, comment out the return statement.
    
    # Below are the equation used for the calculations.
    def test_reactionforcesy():
        margin = 0.0001
        assert -margin <= Y1 + Y2 + Y3 + la*Q_v + R_v + P_v <= margin
        assert -margin <= -(x2-x1)*Y1 + (x3-x2)*Y3 + Q_v*la*(la/2-x2) - R_v * xa/2 + P_v * xa/2 <= margin
        assert -margin <= - d1_v*E*Izz + (1/24)*Q_v*x1**4 + YA*x1 + YB <= margin
        assert -margin <=  (1/24)*Q_v*x2**4 + (1/6)*(x2-x1)**3*Y1 + 1/6*(xa/2)**3 * R_v + YA*x2 + YB <= margin
        assert -margin <= - d3_v*E*Izz + (1/24)*Q_v*x3**4 + (1/6)*(x3-x1)**3*Y1 + (1/6)*(x3-x2)**3*Y2 + 1/6*(x3-x2+xa/2)**3 * R_v + 1/6*(x3-x2-xa/2)**3 * P_v + YA*x3 + YB <= margin
        
    test_reactionforcesy()
    
    def test_reactionforcesz():
        margin = 0.0001
        assert -margin <= Z1 + Z2 + Z3 + R_w + P_w + Q_w * la <= margin
        assert -margin <= (x2-x1)*Z1 + R_w * xa/2 - P_w * xa/2 - Z3*(x3-x2) + Q_w*la*(x2-la/2) <= margin
        assert -margin <= - E*Iyy*d1_w + 1/24*Q_w*x1**4 + ZA*x1 + ZB <= margin
        assert -margin <= 1/6*(x2-x1)**3*Z1 + 1/24*Q_w*x2**4 + 1/6*(xa/2)**3*R_w + ZA*x2 + ZB <= margin
        assert -margin <= -E*Iyy*d3_w + 1/6*(x3-x1)**3*Z1 + 1/6*(x3-x2)**3*Z2 + 1/24*Q_w*x3**4 + 1/6*(x3-x2+(xa/2))**3*R_w + 1/6*(x3-x2-(xa/2))**3*P_w + ZA * x3 + ZB <= margin
    
    def test_R():
        margin = 0.0001
        assert -margin <= (q*la*(0.25*Ca - 0.5*h)*np.cos(theta_rad)) + (R + P) * (0.5*np.sqrt(2)*h*np.sin(0.25*np.pi - theta_rad)) <= margin
      
    test_reactionforcesy()
    test_reactionforcesz()
    test_R()
    

    return (float(X2), float(Y1),float(Y2),float(Y3),float(Z1),float(Z2),float(Z3),Q_v,Q_w,R_v,R_w,P_v,P_w,float(theta_x0_z),float(theta_x0_y))


Izz=get_Izz()
Iyy=get_Iyy()
#Izz = 1.25180748944789E-5
#Iyy = 9.93425176458821E-5

U2,V1,V2,V3,W1,W2,W3,Q_v,Q_w,R_v,R_w,P_v,P_w,thetaz,thetay = reaction_forces(Iyy,Izz)

print("""X2: {0}
Z1,Y1: {4},{1}
Z2,Y2: {5},{2}
Z3,Y3: {6},{3}

R: {7},{8}""".format(U2/1000,V1/1000,V2/1000,V3/1000,W1/1000,W2/1000,W3/1000,R_v/1000,R_w/1000))

