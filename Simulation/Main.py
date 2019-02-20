# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:42:03 2019

@author: Stijn
"""
import numpy as np
from Modules.reactionforces import reaction_forces
from Modules.centroid import centroid
from Modules.MOI import Izz, Iyy, Iyz


exec(open("./Data.txt").read())       
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izz())
centroid_original_rf = centroid()

Izz = Izz()
Iyy = Iyy(centroid_original_rf[2])
Iyz = Iyz(centroid_original_rf[2])
