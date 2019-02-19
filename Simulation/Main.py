# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:42:03 2019

@author: Stijn
"""
import numpy as np
from Modules.reactionforces import reaction_forces
from Modules.centroid import centroid


exec(open("./Data.txt").read())       
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(1E-10)
centroid_original_rf = centroid()
