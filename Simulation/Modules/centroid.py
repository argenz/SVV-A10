import numpy as np
import matplotlib.pyplot as plt
"""centroid calculation, assume same material density
RETURNS centroid in (XYZ) original
 

we use the rotating coordinate system (XYZ)' to find centroid and then transform
z'
y', because of symmetry y'_centroid = 0
x', because of symmetry x'_centroid = 0

centroid formula= SUM(area * distance) / SUM(area)
"""
#Data
exec(open("./Data.txt").read())

def centroid():
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
    
    #finalize in (XYZ)' coordinates
    x_trans = 0
    y_trans = 0
    z_trans = a_tot_dis/a_tot          #z' of centroid
    
    #transform back to orginial XYZ
    x = x_trans
    y = -z_trans * np.sin(np.deg2rad(theta))
    z = z_trans * np.cos(np.deg2rad(theta))
    
    return float(x_trans),float(y_trans),float(z_trans)





















    fig = plt.figure(figsize = (12,6))
    ax = fig.add_subplot(1,1,1)
    n = 100
    
    angle = np.linspace(np.pi/2,3*np.pi/2,n)
    circ_x = 0.5*h*np.cos(angle) 
    circ_y = 0.5*h*np.sin(angle)
    aileron_profile_x = (np.concatenate((np.array([0     , Ca - 0.5*h , 0      ]),circ_x)))*-1
    aileron_profile_y = (np.concatenate((np.array([0.5*h , 0          , -0.5*h ]),circ_y)))
    
    ax.plot(aileron_profile_x,aileron_profile_y)
    ax.scatter(z_trans,0)
    ax.set_aspect('equal')
    plt.grid()
    plt.gca().invert_xaxis()


