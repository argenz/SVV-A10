exec(open("./Data.txt").read())

def deflectiondistributedload(q,L_total,ntotal,direction):    
    #positive load q is negative direction z    
    #internal moment for distributed load q
    #right side. L_total is total distance from hinge 2 to the end of beam. ntotal is the amount of discretizations
    #direction: to right (1), to left (-1)
    I=1 #### MOMENT OF INERTIA TO BE IMPLEMENTED
    
    dx=L_total/float(ntotal) #discretization distances
    thetatotal=0 #initial theta
    deftotal=0 #initial deflection
    
    deflectionlist=[0.0]
    xcoordinateslist=[0.0]    
    n=1 #starting value
    while n<=ntotal: #while before force
        F = q*(L_total-n*dx)        
        M0 = -q*(L_total-n*dx)*(L_total-n*dx)/2 #internal moment
        defshear= -F*dx**3/(3*E*I) #deformation due to force 
        defmoment= M0*dx**2/(2*E*I) #deformation due to internal moment
        defq=-q*L**4/(8*E*I) #deformation due to distributed load
        defangle= dx*thetatotal #deformation due to already existing angle
        deftotal = deftotal+defangle+defshear+defmoment+defq #summation
        thetashear= -P*L**2/(2*E*I) #theta due to force
        thetamoment= M0*L/(E*I) #theta due to moment
        thetaq=-q*L**3/(6*E*I) #angle due to distributed load
        thetatotal = thetashear +thetamoment + thetatotal +thetaq #theta summation
        deflectionlist.append(deftotal) #append to list
        xcoordinateslist.append(n*dx) #append to list of x coordinates
        n=n+1 #next
    
    xcoordinateslist=xcoordinateslist*direction
    return deflectionlist, xcoordinateslist