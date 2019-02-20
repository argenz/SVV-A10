def beamdeflection(P,L_force,L_total,ntotal):    
    #internal moment for force P placed at distance L_force from hinge 2
    #right side. L_total is total distance to end of beam. ntotal is the amount of discretizations

    L_straight = L_total - L_force #length where beam will be straight
    
    I=1 #### MOMENT OF INERTIA TO BE IMPLEMENTED
    
    dx=L_total/float(ntotal) #discretization distances
    thetatotal=0 #initial theta
    deftotal=0 #initial deflection
    
    deflectionlist=[0.0]
    xcoordinateslist=[0.0]    
    n=1 #starting value
    while n*dx<L_force: #while before force
        M0 = -F*(L_force-n*dx) #internal moment
        defshear= -F*dx**3/(3*E*I) #deformation due to force 
        defmoment= M0*dx**2/(2*E*I) #deformation due to internal moment
        defangle= dx*thetatotal #deformation due to already existing angle
        deftotal = deftotal+defangle+defshear+defmoment #summation
        thetashear= -P*L**2/(2*E*I) #theta due to force
        thetamoment= M0*L/(E*I) #theta due to moment
        thetatotal = thetashear +thetamoment + thetatotal #theta summation
        deflectionlist.append(deftotal) #append to list
        xcoordinateslist.append(n*dx) #append to list of x coordinates
        n=n+1 #next
            
    while n<=ntotal: #while after force but before end of beam
        deftotal = deftotal + thetatotal*dx #total deflection updated
        deflectionlist.append(deftotal) #append to list
        xcoordinateslist.append(n*dx) #append to list of x coordinates
        n=n+1 #next
    
    return deflectionlist, xcoordinateslist