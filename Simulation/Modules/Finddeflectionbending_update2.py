exec(open("./Data.txt").read())
import numpy as np    
from Modules.reactionforces import *
from Modules.centroid import *
from Modules.Tools import *
from Modules.MOI import *
from Modules.shearcenter_pos import *
from Modules.deflectiondistributedload import *
from Modules.deflectionpointload import *
def deformduetobending(steps):
    #angle of aileron
    theta=26. #26.
    theta_rad = np.deg2rad(theta)

    #Getting the inertias
    Izz=get_Izz()
    Iyy=get_Iyy()

    #finding the reaction forces and angles thetaz and thetay on the right side of the beam.
    U2,V1,V2,V3,W1,W2,W3,Q_v,Q_w,R_v,R_w,P_v,P_w,yA,yB,zA,zB = reaction_forces(Iyy,Izz)
    
    #determining the amount of points in discr
    ntotal=steps

    ucoordinates=[]
    vcoordinates=[]
    wcoordinates=[]
    u=0
    n=0
    step=float(la)/float(ntotal-1)
    print(step)
    print(ntotal*step)
    while n<=(ntotal-1):
        if u<=x1:
            v=(1/24*Q_v*u**4+yA*u+yB)/(E*Izz)
            w=(1/24*Q_w*u**4+zA*u+zB)/(E*Iyy)

        elif x1<u<=(x2-xa/2):
            v=(1/24*Q_v*u**4+yA*u+yB+1/6*(u-x1)**3*V1)/(E*Izz)
            w=(1/24*Q_w*u**4+zA*u+zB+1/6*(u-x1)**3*W1)/(E*Iyy)

        elif (x2-xa/2)<u<x2:
            v=(1/24*Q_v*u**4+yA*u+yB+1/6*(u-x1)**3*V1+1/6*(u-x2+xa/2)**3*R_v)/(E*Izz)
            w=(1/24*Q_w*u**4+zA*u+zB+1/6*(u-x1)**3*W1+1/6*(u-x2+xa/2)**3*R_w)/(E*Iyy)
            
        elif x2<u<(x2+xa/2):
            v=(1/24*Q_v*u**4+yA*u+yB+1/6*(u-x1)**3*V1+1/6*(u-x2+xa/2)**3*R_v+1/6*(u-x2)**3*V2)/(E*Izz)
            w=(1/24*Q_w*u**4+zA*u+zB+1/6*(u-x1)**3*W1+1/6*(u-x2+xa/2)**3*R_w+1/6*(u-x2)**3*W2)/(E*Iyy)
            
        elif (x2+xa/2)<u<=x3:
            v=(1/24*Q_v*u**4+yA*u+yB+1/6*(u-x1)**3*V1+1/6*(u-x2+xa/2)**3*R_v+1/6*(u-x2)**3*V2+1/6*(u-x2-xa/2)**3*P_v)/(E*Izz)
            w=(1/24*Q_w*u**4+zA*u+zB+1/6*(u-x1)**3*W1+1/6*(u-x2+xa/2)**3*R_w+1/6*(u-x2)**3*W2+1/6*(u-x2-xa/2)**3*P_w)/(E*Iyy)
            
        elif u>x3:
            v=(1/24*Q_v*u**4+yA*u+yB+1/6*(u-x1)**3*V1+1/6*(u-x2+xa/2)**3*R_v+1/6*(u-x2)**3*V2+1/6*(u-x2-xa/2)**3*P_v+1/6*(u-x3)**3*V3)/(E*Izz)
            w=(1/24*Q_w*u**4+zA*u+zB+1/6*(u-x1)**3*W1+1/6*(u-x2+xa/2)**3*R_w+1/6*(u-x2)**3*W2+1/6*(u-x2-xa/2)**3*P_w+1/6*(u-x3)**3*W3)/(E*Iyy)
            
        ucoordinates.append(u)
        vcoordinates.append(v)
        wcoordinates.append(w)

        u=n*step
        n=n+1
    

    
    
    #finding the closest discretization x coordinate to points x1 and x3   
    xdummy1=ucoordinates-np.full((1, ntotal), x1)
    xdummy3=ucoordinates-np.full((1, ntotal),x3)
    x1discr=np.argmin(abs(xdummy1))
    x3discr=np.argmin(abs(xdummy3))

    #finding real displacements in new coordinate system
    d1_w = -d1 * np.sin(theta_rad)
    d1_v = d1 * np.cos(theta_rad)
    
    d3_w = -d3 * np.sin(theta_rad)
    d3_v = d3 * np.cos(theta_rad)

    #finding difference between this discr and reality
    dify1=vcoordinates[x1discr]-d1_v
    dify3=vcoordinates[x3discr]-d3_v

    difz1=wcoordinates[x1discr]-d1_w
    difz3=wcoordinates[x3discr]-d3_w
    
    #print testvalues
    print(vcoordinates[x1discr],vcoordinates[x3discr],wcoordinates[x1discr],wcoordinates[x3discr])
    print(d1_v,d3_v,d1_w,d3_w)
    print(dify1,dify3,difz1,difz3)
    return vcoordinates,wcoordinates


