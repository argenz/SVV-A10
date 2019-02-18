import numpy as np
#centroid calculation
#assume same material density
#we use the rotating coordinate system (XYZ)'

#z'
#y', because of symmetry y'_centroid = 0
#x', because of symmetry x'_centroid = 0

#centroid formula= SUM(area * distance) / SUM(area)

#Data
Ca = 0.547                  #m   Chord length aileron Ca
la = 2.771                  #m   Span of the aileron 
x1 = 0.153                  #m   x-location of hinge 1
x2 = 1.281                  #m   x-location of hinge 2 
x3 = 2.681                  #m   x-location of hinge 3 
xa = 28.0 / 100             #m   Distance between actuator 1 and 2 
h = 22.5  / 100             #m   Aileron height 
tsk = 1.1 / 1000            #m   Skin thickness 
tsp = 2.9 / 1000            #m   Spar thickness 
tst = 1.2 / 1000            #m   Thickness of Stiffener 
hst = 1.5 / 100             #m   Height of stiffener 
wst = 2.0 / 100             #m   Width of stiffener 
nst = 17                    #    Number of stiffeners 
d1 = 1.103 / 100            #m   Vertical displacement hinge 1 
d3 = 1.642 / 100            #m   Vertical displacement hinge 3 
theta = 26                  #deg Maximum upward deflection 
P = 91.7 * 1000             #N   Load in actuator 2 
q = 4.53 * 1000             #N/m Net aerodynamic load

#things used
l_sk_str = np.sqrt((Ca-h/2)**2+(h/2)**2)            #length straight skin
theta_sk = np.arctan((h/2)/(Ca-h/2))                #angle between straight skin and z' axis
circ_tot = l_sk_str*2+np.pi*h/2                     #circumference aileron
l_stiff = circ_tot /(nst+1)                         #stiffener pitch
nst_str = int(l_sk_str / l_stiff)                   #number of stiffeners in straight part ONE side
nst_le = nst - nst_str*2                            #total number of stiffeners in LE BOTH sides
theta_le = l_stiff/(h/2)                            #angle between stiffeners leading edge

#area
a_st = nst * (hst*tst + wst*tst)                    #area total stringers
a_st_one = (hst*tst + wst*tst)                      #area one stringer
a_sp = h * tsp                                      #area spar
a_le = np.pi*(h/2) * tsk                            #area leading edge circular section
a_sk_str = 2*l_sk_str * tsk                         #area total straight skin
a_tot = a_st + a_sp + a_le + a_sk_str               #sum of area

#centre of mass of coordinates components
z_sk_str = -((Ca-h/2)-l_sk_str/2*np.cos(theta_sk))                  #z' straight skin
z_le = h/np.pi                                                      #z' leading edge
z_st_str = -((Ca-h/2)-(nst_str/2+0.5)*l_stiff*np.cos(theta_sk))     #z' stiffeners straight part
z_st_le_close = np.cos(theta_le)*(h/2)                              #z' of 2 stiffeners close to edge
z_st_le_far = np.cos(2*theta_le)*(h/2)                              #z' of 2 stiffeners further from edge

#area times distance
a_tot_dis = z_st_str * nst_str * 2 * a_st_one + z_st_le_close * 2 * a_st_one + z_st_le_far * 2 * a_st_one + z_le * a_le + z_sk_str * a_sk_str

#finalize
z = a_tot_dis/a_tot
