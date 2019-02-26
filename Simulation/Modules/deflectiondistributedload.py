exec(open("./Data.txt").read())
import numpy as np
def deflectiondistributedload(q,L_total,ntotal,direction,I):    
    #positive load q is positive downwards 
    #internal moment for distributed load q
    #right side. L_total is total distance from hinge 2 to the end of beam. ntotal is the amount of discretizations
    #direction: to right (1), to left (-1). Deformation is positive UPwards
    
    dx=L_total/float(ntotal) #discretization distances
    thetatotal=0 #initial theta
    deftotal=0 #initial deflection
    
    deflectionlist=[0.0]
    xcoordinateslist=[0.0]    
    n=1 #starting value
    while n<=ntotal: # while along the beam 

        #internal moment of force due to q at the cut
        F = -q*(L_total-n*dx)
        M0 = q*(L_total-n*dx)*(L_total-n*dx)/2

        #deformation due to the internal shear and moment, the distributed load and the already existing angle
        defshear= -F*dx**3/(3*E*I)  
        defmoment= M0*dx**2/(2*E*I)
        defq=q*dx**4/(8*E*I) 
        defangle= dx*thetatotal

        # The new deformation is the deformation of the previous point plus all new deformations
        deftotal = deftotal+defangle+defshear+defmoment+defq 

        #theta for the 3 different components again...
        thetashear= -F*dx**2/(2*E*I) #theta due to force
        thetamoment= M0*dx/(E*I) #theta due to moment
        thetaq=q*dx**3/(6*E*I) #angle due to distributed load

        #add theta from previous point plus all the new thetas
        thetatotal = thetashear +thetamoment + thetatotal +thetaq #theta summation

        deflectionlist.append(deftotal) #append results to list
        xcoordinateslist.append(n*dx) #append x coordinates to list
        n=n+1 #next
    
    xcoordinateslist=np.array(xcoordinateslist)*direction #to the left is negative, to the right positive
    return deflectionlist, xcoordinateslist

