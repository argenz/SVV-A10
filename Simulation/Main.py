# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:42:03 2019

@author: Stijn
"""
import numpy as np
from Modules.reactionforces import reaction_forces


exec(open("./Data.txt").read())       
y1,y2,y3,z1,z2,z3,R = reaction_forces(1E-10)
