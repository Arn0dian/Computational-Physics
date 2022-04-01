import os
from time import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pi = 3.14159265359
g = 9.8
time_diff = 0.001 # time difference choosen as per accuracy requirement

# Degree to radian conversion
def degtorad(degree):
    return (degree * (pi / 180))

# Time of flight
def timeofflg(velocity,degree):
    return(((2*velocity*np.sin(degtorad(degree)))/g))

# Range of the projectile
def rnge(velocity,degree):
    rg = velocity**2
    rg *= np.sin(2*degtorad(degree))
    rg /= g
    return(rg)

# Maximum Height of the projectile
def maxheights(velocity,degree):
    hg = velocity**2
    hg *= (np.sin(degtorad(degree)))**2
    hg /= (2*g)
    return(hg)

# X-cordinate of the projectile at a given time
def xposatt(velocity,degree,time):
    return(velocity*time*np.cos(degtorad(degree)))

# Y-cordinate of the projectile at a given time
def yposatt(velocity,degree,time):
    y = ((velocity*time)*(np.sin(degtorad(degree)))) - ((g*(time**2))/2)
    return(y)

# (x,y) ordered pair position of the projectile at a given time
def postionattime(velocity,degree,time):
    return(xposatt(velocity,degree,time),yposatt(velocity,degree,time))

# This function is used to calculate the trajectory of the projectile with drag
def projectileDrag(velocity,degree,mass,cd):
    x = [0]                      
    y = [0]

    vx = [velocity*np.cos(degree/180*np.pi)]
    vy = [velocity*np.sin(degree/180*np.pi)]
    t = [0]
    drag=cd*velocity**2  # Drag force

    ax = [-(drag*np.cos(degree/180*np.pi))/mass]
    ay =  [(-g-(drag*np.sin(degree/180*np.pi))/mass)]

    while(x[-1]<rnge(velocity,degree) and y[-1]>=0):
        vx.append(vx[-1] + ax[-1]*time_diff)
        vy.append(vy[-1] + ay[-1]*time_diff)
        t.append(t[-1]+time_diff)
        vel = np.sqrt(vx[-1]**2 + vy[-1]**2) 
        drag = cd*vel**2
        ax.append(-(drag*np.cos(degree/180*np.pi))/mass)     
        ay.append(-g-(drag*np.sin(degree/180*np.pi)/mass))
        x.append(x[-1]+time_diff*vx[-1])    
        y.append(y[-1]+time_diff*vy[-1]) 
    
    # plt.subplot(2,1,1)
    # plt.plot(t,y)
    # plt.title('Time vs Y-Position')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Height (m)')
    # plt.subplot(2,1,2)
    # plt.plot(t,x)
    # plt.title('Time vs X-Position')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Distance (m)')
    list_dict = {'Time':t,'X':x, 'Y':y, 'X-velocity':vx, 'Y-velocity':vy}
    df=pd.DataFrame(list_dict) 
    # This creates a csv file of all the points of the trajectory with given time step and stores it locally in same directory as this script file
    if(os.stat("trajectory_points_with_drag.csv").st_size == 0):
        df.to_csv('trajectory_points_with_drag.csv')
    else: 
        os.remove("trajectory_points_with_drag.csv")
        df.to_csv('trajectory_points_with_drag.csv')

    plt.plot(x,y)
    plt.title('Trajectory of projectile motion under drag') 
    plt.xlabel('X-Position (m)')
    plt.ylabel('Y-Position (m)')
    # Produces a plot of the trajectory of the projectile with drag
    plt.show()

# This function is used to calculate the trajectory of the projectile without drag
def projectileNoDrag(velocity,degree):
    x = np.arange(0, rnge(velocity,degree),0.1)
    y = (x*np.tan(degtorad(degree))) - ((g*(x**2))/(2*(velocity**2)*((np.cos(degtorad(degree)))**2)))
    plt.plot(x, y)
    i = 0
    yp = np.array([]) 
    xp = np.array([])
    while i < timeofflg(velocity,degree):      
        xp = np.append(xp, xposatt(velocity,degree,i))
        yp = np.append(yp, yposatt(velocity,degree,i))
        i += time_diff
    list_dict = {'X':xp, 'Y':yp} 
    df=pd.DataFrame(list_dict) 
    # This creates a csv file of all the points of the trajectory with given time step and stores it locally in same directory as this script file
    if(os.stat("trajectory_points.csv").st_size == 0):
        df.to_csv('trajectory_points.csv')
    else: 
        os.remove("trajectory_points.csv")
        df.to_csv('trajectory_points.csv')
    # Produces a plot of the trajectory of the projectile
    plt.title('Trajectory of projectile motion') 
    plt.xlabel('X-Position (m)')
    plt.ylabel('Y-Position (m)')
    plt.show()

# Driver Code
print("Choose Your Projectile Type:")
print("1. Projectile with Drag")
print("2. Projectile without Drag")
choice = int(input("Enter your choice: "))
if(choice == 1):
    print("Enter the following details:")
    velocity = float(input("Enter the velocity of the projectile: "))
    degree = float(input("Enter the angle of the projectile: "))
    mass = float(input("Enter the mass of the projectile: "))
    cd = float(input("Enter the drag coefficient of the projectile: "))
    projectileDrag(velocity,degree,mass,cd)
elif(choice == 2):
    print("Enter the following details:")
    velocity = float(input("Enter the velocity of the projectile: "))
    degree = float(input("Enter the angle of the projectile: "))
    projectileNoDrag(velocity,degree)   




        
