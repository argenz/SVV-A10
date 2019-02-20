#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:15:57 2019

@author: PereiraJoao
"""
from IdealizationCoordinates import IdealizationCoordinates
import numpy as np
import matplotlib.pyplot as plt

def Idealization():
    t_sk = 0.0011 #skin thikness
    t_sp = 0.0029 #spar thikness
    h_a = 0.225 #Spar length
    
    #JOINING COORDINATES OF ALL STRINGERS IN TO ONE LIST
    B_coordinatesTopPanel,B_coordinatesTopArc,b_st = IdealizationCoordinates() 
    B_coordinatesTop = B_coordinatesTopPanel + B_coordinatesTopArc 
    B_coordinatesRev = [ [x,y*-1] for [x,y] in B_coordinatesTop[::-1]]
    B_coordinates = B_coordinatesTop + B_coordinatesRev[1:]#stiffner coordinates top half of aileron
    #CALCULATING BOOM AREAS
    A_st = 0.0012*(0.015-0.0012) + (0.02*0.0012) #stiffner area [m]
    B0 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[16][1]/B_coordinates[0][1])+(B_coordinates[16][1]/B_coordinates[1][1])) 
    B1 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[0][1]/B_coordinates[1][1])+(B_coordinates[2][1]/B_coordinates[1][1]))
    B2 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[1][1]/B_coordinates[2][1])+(B_coordinates[3][1]/B_coordinates[2][1]))
    B3 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[2][1]/B_coordinates[3][1])+(B_coordinates[4][1]/B_coordinates[3][1]))
    B4 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[3][1]/B_coordinates[4][1])+(B_coordinates[5][1]/B_coordinates[4][1]))
    B5 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[4][1]/B_coordinates[5][1])+(B_coordinates[6][1]/B_coordinates[5][1]))
    B6 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[5][1]/B_coordinates[6][1])+(B_coordinates[7][1]/B_coordinates[6][1])) + ((t_sp*h_a)/6)*(2+(B_coordinates[10][1]/B_coordinates[6][1]))    
    B7 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[6][1]/B_coordinates[7][1])+(B_coordinates[8][1]/B_coordinates[7][1]))
    B8 = A_st 
    B9 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[8][1]/B_coordinates[9][1])+(B_coordinates[10][1]/B_coordinates[9][1]))
    B10 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[9][1]/B_coordinates[10][1])+(B_coordinates[11][1]/B_coordinates[10][1])) + ((t_sp*h_a)/6)*(2+(B_coordinates[6][1]/B_coordinates[10][1]))   
    B11 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[10][1]/B_coordinates[11][1])+(B_coordinates[12][1]/B_coordinates[11][1]))
    B12 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[11][1]/B_coordinates[12][1])+(B_coordinates[13][1]/B_coordinates[12][1]))
    B13 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[12][1]/B_coordinates[13][1])+(B_coordinates[14][1]/B_coordinates[13][1]))
    B14 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[13][1]/B_coordinates[14][1])+(B_coordinates[15][1]/B_coordinates[14][1]))
    B15 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[14][1]/B_coordinates[15][1])+(B_coordinates[16][1]/B_coordinates[15][1]))
    B16 = A_st + ((t_sk*b_st)/6)*(4+(B_coordinates[15][1]/B_coordinates[16][1])+(B_coordinates[0][1]/B_coordinates[16][1]))
    
    B = [B0,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11,B12,B13,B14,B15,B16] #boom areas [m]
    
    #PLOT TO CHECK THE COORDINATES ARE CORRECT
    #Bplt = np.array(B_coordinates)
    #plt.plot(Bplt[:,0],Bplt[:,1],'*k')
    #plt.show()
    
    return B, B_coordinates


