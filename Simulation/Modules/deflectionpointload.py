exec(open("./Data.txt").read())
import numpy as np
def deflectionpointload(P,L_force,L_total,ntotal,direction,I):    
    #positive load P is negative direction z   
    
    #internal moment for force P DOWN placed at distance L_force from hinge 2
    #right side. L_total is total distance from hinge 2 to the end of beam. ntotal is the amount of discretizations
    #direction: to right (1), to left (-1). Deformation is positive UPwards
    
    dx=L_total/float(ntotal) #discretization distances
    thetatotal=0. #initial theta
    deftotal=0. #initial deflection
    
    deflectionlist=[0.0]
    xcoordinateslist=[0.0]    
    n=1 #starting value
    while n*dx<=L_force: # for the part in front of the force, the beam is bending 
        M0 = -P*(L_force-n*dx) #internal moment caused by force at the cut (positive anti clockwise)

        #deformations bu the shear, moment and the already existing angle of the beam:
        defshear= -P*dx**3/(3*E*I) 
        defmoment= M0*dx**2/(2*E*I)
        defangle= dx*thetatotal

        #total deformation is the deformation of the previous point + the new found displacements
        deftotal = deftotal+defangle+defshear+defmoment

        #angle theta caused by the moment and the shear force
        thetashear= -P*dx**2/(2*E*I)
        thetamoment= M0*dx/(E*I)

        #sum all the components, add the already existing angle from previous step: thetatotal
        thetatotal = thetashear +thetamoment + thetatotal #theta summation
        
        deflectionlist.append(deftotal) #append to list
        xcoordinateslist.append(n*dx) #append x coordinates to list
        n=n+1 #next
            
    while n<=ntotal: #behind the applied force, the beam is straight from this point onwards
        deftotal = deftotal + thetatotal*dx #add contribution from angle to deformation
        deflectionlist.append(deftotal) #append results to list
        xcoordinateslist.append(n*dx) #append x coordinates to list
        n=n+1 #next
        
    xcoordinateslist=np.array(xcoordinateslist)*direction #take negative x coordinates for running to the left
    return deflectionlist, xcoordinateslist



