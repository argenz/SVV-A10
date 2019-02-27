exec(open("./Data.txt").read())
import numpy as np    
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shearcenter_pos import *
from Modules.deflectiondistributedload import *
from Modules.deflectionpointload import *
def deformduetobending():
    #angle of aileron
    theta=26. #26.
    theta_rad = np.deg2rad(theta)

    #Getting the inertias
    Izz=get_Izz()
    Iyy=get_Iyy()

    #finding the reaction forces and angles thetaz and thetay on the right side of the beam.
    U2,V1,V2,V3,W1,W2,W3,Q_v,Q_w,R_v,R_w,P_v,P_w,thetaz,thetay = reaction_forces(Iyy,Izz)
    
    #determining the amount of points in discr
    ntotal=10**3
    right=1 #convention
    left=-1
    
    ################Z direction
    #z deflection by Z1,Z2,Z3
    deflectionlistW1,x=deflectionpointload(W1,x1,la,ntotal,left,Iyy)
    deflectionlistW2,x=deflectionpointload(W2,x2,la,ntotal,left, Iyy) 
    deflectionlistW3,x=deflectionpointload(W3,x3,la,ntotal,left,Iyy)

    #z deflection by P_w,R_w
    deflectionlistP_w,x=deflectionpointload(P_w,x2+xa/2,la,ntotal,left,Iyy)
    deflectionlistR_w,x= deflectionpointload(R_w,x2-xa/2,la,ntotal,left, Iyy)

    #z deflection by Q_w
    deflectionlistq_w,x=deflectiondistributedload(Q_w,la,ntotal,left,Izz)
    
    #z deflection due to angle
    deflectionlistthetaz=np.array(x)*(thetaz)
    
    #adding all deflections
    zdeflections= np.array(deflectionlistW1)+np.array(deflectionlistW2)+np.array(deflectionlistW3)+np.array(deflectionlistP_w)+np.array(deflectionlistR_w)+np.array(deflectionlistq_w)+np.array(deflectionlistthetaz)
        
    ###############Y direction
    #y deflection by Y1,Y2,Y3
    deflectionlistV1,x=deflectionpointload(V1,x1,la,ntotal,left, Izz)
    deflectionlistV2,x=deflectionpointload(V2,x2,la,ntotal,left, Izz) 
    deflectionlistV3,x=deflectionpointload(V3,x3,la,ntotal,left,Izz)

    #y deflection due to P_v and R_v
    deflectionlistP_v,xnegativedirection=deflectionpointload(P_v,x2+xa/2,la,ntotal,left,Izz)
    deflectionlistR_v,x=deflectionpointload(R_v,x2-xa/2,la,ntotal,left,Izz)

    #y deflection due to Q_v
    deflectionlistq_v,x=deflectiondistributedload(Q_v,la,ntotal,left,Izz)
    
    #y deflection due to angle
    deflectionlistthetay=np.array(x)*(thetay)

    #adding all deflections
    ydeflections=np.array(deflectionlistV1)+np.array(deflectionlistV2)+np.array(deflectionlistV3)+np.array(deflectionlistP_v)+np.array(deflectionlistR_v)+np.array(deflectionlistq_v)+np.array(deflectionlistthetay)
    
    #finding the closest discretization x coordinate to points x1 and x3   
    xdummy1=x-np.full((1, (ntotal+1)), x1)
    xdummy3=x-np.full((1, (ntotal+1)),x3)
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
    #print(ydeflections[x1discr],ydeflections[x3discr],zdeflections[x1discr],zdeflections[x3discr])
    #print(d1_v,d3_v,d1_w,d3_w)
    #print(dify1,dify3,difz1,difz3)
    return x,ydeflections,zdeflections,x1discr,x3discr


