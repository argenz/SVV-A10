exec(open("./Data.txt").read())
import numpy as np    
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shearcenter_pos import *
from Modules.findanglehinge2 import *
from Modules.deflectiondistributedload import *
from Modules.deflectionpointload import *
def deformduetobending():
    #angle of aileron
    theta=0. #26.
    theta_rad = np.deg2rad(theta)

    #Getting the inertias
    Izz=get_Izz()
    Iyy=get_Iyy()

    #finding the reaction forces and angles thetaz and thetay at hinge 2.
    U2,V1,V2,V3,W1,W2,W3,R_v,R_w,P_v,P_w,thetaz,thetay = reaction_forces(Iyy,Izz)

    #determining the amount of points in discr
    ntotal=10*6
    right=1 #convention
    left=-1 #convention
    
    #the angles at hinge 2. Found by flexure formula
    
    initialthetay=thetay
    initialthetaz=thetaz

    ################Z direction
    #z deflection by Z1,Z2,Z3
    deflectionlistW1,x=deflectionpointload(W1,x2-x1,x2,ntotal,right,Iyy)
    deflectionlistW2,x=deflectionpointload(W2,0.0,x2,ntotal,right, Iyy) 
    deflectionlistW3,xnegativedirection=deflectionpointload(W3,x3-x2,la-x2,ntotal,left,Iyy)

    #z deflection by P_w,R_w
    deflectionlistP_w,xnegativedirection=deflectionpointload(P_w,xa/2.,la-x2,ntotal,left,Iyy)
    deflectionlistR_w,x= deflectionpointload(R_w,xa/2.,x2,ntotal,right, Iyy)

    #z deflection by Q_w
    deflectionlistq1_w,x=deflectiondistributedload(Q_w,x2,ntotal,right,Izz)
    deflectionlistq2_w,xnegativedirection=deflectiondistributedload(Q_v,la-x2,ntotal,left,Izz)
    
    #z deflection due to angle
    deflectionlistzthetaleft=np.array(xnegativedirection)*(initialthetaz)
    deflectionlistzthetaright=np.array(x)*(initialthetaz)

    #adding all deflections
    dzright= np.array(deflectionlistW1)+np.array(deflectionlistR_w)+np.array(deflectionlistzthetaright)+np.array(deflectionlistq1_w)
    dzleft=np.array(deflectionlistP_w)+np.array(deflectionlistW3)+np.array(deflectionlistzthetaleft)+np.array(deflectionlistq2_w)

    #merging the 2 lists
    zdeflections=np.concatenate((dzleft,dzright))
    
    ###############Y direction
    #y deflection by Y1,Y2,Y3
    deflectionlistV1,x=deflectionpointload(V1,x2-x1,x2,ntotal,right, Izz)
    deflectionlistV2,x=deflectionpointload(V2,0.0,x2,ntotal,right, Izz) 
    deflectionlistV3,xnegativedirection=deflectionpointload(V3,x3-x2,la-x2,ntotal,left,Izz)

    #y deflection due to P_v and R_v
    deflectionlistP_v,xnegativedirection=deflectionpointload(P_v,xa/2,la-x2,ntotal,left,Izz)
    deflectionlistR_v,x=deflectionpointload(R_v,xa/2,x2,ntotal,right,Izz)

    #y deflection due to Q_v
    deflectionlistq1_v,x=deflectiondistributedload(Q_v,x2,ntotal,right,Izz)
    deflectionlistq2_v,xnegativedirection=deflectiondistributedload(Q_v,la-x2,ntotal,left,Izz)
    
    #y deflection due to angle
    deflectionlistythetaleft=np.array(xnegativedirection)*(initialthetay)
    deflectionlistythetaright=np.array(x)*(initialthetay)

    #adding all deflections
    dyright=np.array(deflectionlistV1)+np.array(deflectionlistq1_v)+np.array(deflectionlistythetaright)+np.array(deflectionlistR_v)
    dyleft=np.array(deflectionlistV3)+np.array(deflectionlistq2_v)+np.array(deflectionlistythetaleft)+np.array(deflectionlistP_v)

    #merging the 2 lists
    ydeflections=np.concatenate((dyleft,dyright))

    #############
    #Merge x coordinates list
    xcoordinateslist=np.concatenate((xnegativedirection,x))
    
    #finding the closest discretization x coordinate to points x1 and x3
    xdummy1=xcoordinateslist-np.full((1, 2(ntotal+1)), (x2-x1))
    xdummy3=xcoordinateslist-np.full((1, 2(ntotal+1)),(x2-x3))
    x1discr=np.argmin(abs(xdummy1))
    x3discr=np.argmin(abs(xdummy3))

    #finding real displacements in new coordinate system
    d1_w = -d1 * np.sin(theta_rad)
    d1_v = d1 * np.cos(theta_rad)
    
    d3_w = -d3 * np.sin(theta_rad)
    d3_v = d3 * np.cos(theta_rad)

    #finding difference between this discr and reality
    dify1=ydeflections[x1discr]-d1_v
    dify3=ydeflections[x3discr]-d3_v

    difz1=zdeflections[x1discr]-d1_w
    difz3=zdeflections[x3discr]-d3_w
    
    #print testvalues
    print(dify1,dify3,difz1,difz3)
    return xcoordinateslist,ydeflections,zdeflections


