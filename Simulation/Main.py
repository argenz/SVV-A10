# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:42:03 2019

@author: Stijn
"""
import numpy as np
<<<<<<< HEAD
from Modules.reactionforces import reaction_forces
from Modules.centroid import centroid
from Modules.MOI import Izz, Iyy, Iyz
=======
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shear_center import *
>>>>>>> cfa26dd348350bb7ecc98ed78e802006a7cf0e7a

exec(open("./Data.txt").read())    
Izz = get_Izz()
Iyy = get_Iyy()
Iyz = get_Iyz()

<<<<<<< HEAD
exec(open("./Data.txt").read())       
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izz())
centroid_original_rf = centroid()

Izz = Izz()
Iyy = Iyy(centroid_original_rf[2])
Iyz = Iyz(centroid_original_rf[2])
=======
centroid_location = centroid()
shear_center = get_ShearCenter(Izz,tsk,h,Ca)
   
X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izz)
X2,Y1,Y2,Y3,Z1,Z2,Z3,R_y,R_z,P_y,P_z,Q_y,Q_z = transform(X2,Y1,Y2,Y3,Z1,Z2,Z3,R,P,q,theta)
>>>>>>> cfa26dd348350bb7ecc98ed78e802006a7cf0e7a
