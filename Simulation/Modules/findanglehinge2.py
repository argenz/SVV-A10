exec(open("../Data.txt").read())
from deflectiondistributedload import *
from deflectionpointload import *
from reactionforces import *
from MOI import Izzrotated
from MOI import Iyyrotated
import numpy as np

X2,Y1,Y2,Y3,Z1,Z2,Z3,R = reaction_forces(Izzrotated())

ntotal=10000
right=1
left=-1
initialthetay=0
initialthetaz=np.deg2rad(-0.08783658335221914)

#deflectionlist1,xlist= deflectiondistributedload(q,la,ntotal,right,initialtheta)
#deflectionlist2,xlist2= deflectionpointload(P,L_force,la,ntotal,right,initialtheta)

#z 
deflectionlistZ1,x=deflectionpointload(Z1,x2-x1,x2,ntotal,right, initialthetaz,Iyyrotated())
deflectionlistZ2,x=deflectionpointload(Z2,0.0,x2,ntotal,right, 0,Iyyrotated()) 
deflectionlistZ3,xnegativedirection=deflectionpointload(Z3,x3-x2,la-x2,ntotal,left, -initialthetaz,Iyyrotated())
deflectionlistP,xnegativedirection=deflectionpointload(P,xa/2.,la-x2,ntotal,left,0 ,Iyyrotated())
deflectionlistR,x= deflectionpointload(R,xa/2.,x2,ntotal,right, 0,Iyyrotated())

#y
deflectionlistY1,x=deflectionpointload(Y1,x2-x1,x2,ntotal,right, initialthetay,Izzrotated())
deflectionlistY2,x=deflectionpointload(Y2,0.0,x2,ntotal,right, 0,Izzrotated()) 
deflectionlistY3,xnegativedirection=deflectionpointload(Y3,x3-x2,la-x2,ntotal,left, -initialthetay,Izzrotated())
deflectionlistq1,x=deflectiondistributedload(q,x2,ntotal,right,0,Izzrotated())
deflectionlistq2,xnegativedirection=deflectiondistributedload(q,la-x2,ntotal,left, 0,Izzrotated())

dzright= np.array(deflectionlistZ1)+np.array(deflectionlistR)
dzleft=np.array(deflectionlistP)+np.array(deflectionlistZ3)

dyright=np.array(deflectionlistY1)+np.array(deflectionlistq1)
dyleft=np.array(deflectionlistY3)+np.array(deflectionlistq2)

mistakerighty=dyright[8806]+d1
mistakelefty=dyleft[9396]+d3

mistakerightz=dzright[8806]+0
mistakeleftz=dzleft[9396]+0

thetayleft=np.rad2deg(mistakelefty/(x3-x2))
thetayright=np.rad2deg(mistakerighty/(x2-x1))

thetazleft=np.rad2deg(mistakeleftz/(x3-x2))
thetazright=np.rad2deg(mistakerightz/(x2-x1))

print(thetayleft,thetayright,thetazleft,thetazright)


