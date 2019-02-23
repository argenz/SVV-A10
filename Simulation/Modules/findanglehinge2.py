exec(open("./Data.txt").read())
import numpy as np    
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shear_center import *
from Modules.findanglehinge2 import *
from Modules.deflectiondistributedload import *
from Modules.deflectionpointload import *
def deformduetobending():
    #finding centroid
    centroid_original_rf = centroid()

    #finding the inertias in the rotated frame
    Izzrotated=get_Izzrotated(centroid_original_rf[2])
    Iyyrotated=get_Iyyrotated(centroid_original_rf[2])

    #finding the reaction forces
    X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izzrotated)

    #determining the amount of points in discr
    ntotal=10*6
    right=1 #convention
    left=-1 #convention

    #the angles at hinge 2. Values found by first making them zero and
    #then checking the error (see 
    initialthetay=np.deg2rad(-0.03664516776096163)#np.deg2rad(-0.042389290142437454)
    initialthetaz=np.deg2rad(0.08775488757812056)#np.deg2rad(0.08783658335221914)
    
    #z #deflection by forces in z direction, all separated (due to force, and initialangle)
    deflectionlistZ1,x=deflectionpointload(Z1,x2-x1,x2,ntotal,right,Iyyrotated)
    deflectionlistZ2,x=deflectionpointload(Z2,0.0,x2,ntotal,right, Iyyrotated) 
    deflectionlistZ3,xnegativedirection=deflectionpointload(Z3,x3-x2,la-x2,ntotal,left,Iyyrotated)
    deflectionlistP,xnegativedirection=deflectionpointload(P,xa/2.,la-x2,ntotal,left,Iyyrotated)
    deflectionlistR,x= deflectionpointload(R,xa/2.,x2,ntotal,right, Iyyrotated)
    deflectionlistzthetaleft=np.array(xnegativedirection)*(initialthetaz)
    deflectionlistzthetaright=np.array(x)*(initialthetaz)
    
    #y deflection by forces in y direction, all separated (due to force, distr. load and initalangle)
    deflectionlistY1,x=deflectionpointload(Y1,x2-x1,x2,ntotal,right, Izzrotated)
    deflectionlistY2,x=deflectionpointload(Y2,0.0,x2,ntotal,right, Izzrotated) 
    deflectionlistY3,xnegativedirection=deflectionpointload(Y3,x3-x2,la-x2,ntotal,left,Izzrotated)
    deflectionlistq1,x=deflectiondistributedload(q,x2,ntotal,right,Izzrotated)
    deflectionlistq2,xnegativedirection=deflectiondistributedload(q,la-x2,ntotal,left,Izzrotated)
    deflectionlistythetaleft=np.array(xnegativedirection)*(initialthetay)
    deflectionlistythetaright=np.array(x)*(initialthetay)

    #add all deflection on right side and put in list, same for left side. Done for z and y.
    dzright= np.array(deflectionlistZ1)+np.array(deflectionlistR)+deflectionlistzthetaright
    dzleft=np.array(deflectionlistP)+np.array(deflectionlistZ3)+deflectionlistzthetaleft

    dyright=np.array(deflectionlistY1)+np.array(deflectionlistq1)+deflectionlistythetaright
    dyleft=np.array(deflectionlistY3)+np.array(deflectionlistq2)+deflectionlistythetaleft

    #finding the closest discretization x coordinate to points x1 and x3
    xdummy1=x-np.full((1, ntotal+1), (x2-x1))
    xdummy3=xnegativedirection+np.full((1, ntotal+1),(x3-x2))
    x1discr=np.argmin(abs(xdummy1))
    x3discr=np.argmin(abs(xdummy3))

    #finding difference between this discretization and actual deflections (y, z)    
    mistakerighty=dyright[x1discr]+d1
    mistakelefty=dyleft[x3discr]+d3

    mistakerightz=dzright[x1discr]+0
    mistakeleftz=dzleft[x3discr]+0

    #finding the thetas needed to meet the actual case (in degrees)
    thetayleft=np.rad2deg(-mistakelefty/(x3-x2))
    thetayright=np.rad2deg(-mistakerighty/(x2-x1))

    thetazleft=np.rad2deg(-mistakeleftz/(x3-x2))
    thetazright=np.rad2deg(-mistakerightz/(x2-x1))

    #averaging both of them
    thetanewz=(-thetazleft+thetazright)/2
    thetanewy=(-thetayleft+thetayright)/2 #those will be used as input later on to find the actual case

    #merging left and right lists
    xcoordinateslist=np.concatenate((xnegativedirection,x))
    ydeflections=np.concatenate((dyleft,dyright))
    zdeflections=np.concatenate((dzleft,dzright))

    #print testvalues
    print(thetayleft,thetayright,thetazleft,thetazright)
    print(thetanewz,thetanewy)
    print(mistakerighty,mistakelefty,mistakerightz,mistakeleftz)
    return xcoordinateslist,ydeflections,zdeflections



