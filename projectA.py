#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project A Template


"""
import math

from simVis1 import visualize




def main():
    
    # initialize parameters
    
    radius = 0.15
    dt =.2
    
    # simulation steps
    simSteps = 800
    

    # Default is Ax1xmin= 0,Ax1xmax = 1, Ax1ymin = 0, Ax1ymax = 1
    vis = visualize() 
    

    x1 = 0.2
    y1 = 0
    
    v1x = -0.05
    v1y = 0
    
    x2 = 0.7
    y2 = 0.7
    
    
    v2x = 0.05
    v2y = 0.05
    
    
    # run simulation
    simulate(simSteps,vis,x1,y1,x2,y2,v1x,v1y,v2x,v2y,dt,radius)
    


# DO NOT CHANGE THIS FUNCTION
def boundary_locations(vis,radius):
    
    """
    Calculate the boundary locations within the visualization window.
    This function calculates the boundary coordinates for a containing box 
    within the visualization window to ensure that particles 
    do not exceed these boundaries.

    Parameters
    ----------
    vis : visualization object
        The visualization object used for determining window boundaries.
    radius : float
        The radius of the particles.

    Returns
    -------
    xLow : float
        The lower bound of the containing box's threshold to hit the vertical left wall.
    yLow : float
        The lower bound of the containing box's threshold to hit the horizontal bottom wall.
    xHigh : float
        The upper bound of the containing box's threshold to hit the vertical right wall.
    yHigh : float
        The upper bound of the containing box's threshold to hit the horizontal top wall.

    """
    
    # Adjust the boundary according to the 
    # circle radius and display window size
    # Assume circles have the same radius.
    xLow = vis.Ax1xmin + radius 
    xHigh = vis.Ax1xmax - radius 
    
    yLow = vis.Ax1ymin + radius 
    yHigh = vis.Ax1ymax - radius 
    
    return xLow, yLow, xHigh, yHigh
    
    


def updateX(x,vx,dt):
    
    # updates x element of circle's position on x,y plane
    
    x = x + vx * dt
    return round(x,3)

def updateY(y,vy,dt):
    
    # updates y element of circle's position on x,y plane
    
   y = y + vy * dt
   return round(y,3)

def boxCollision(x,y,vx,vy,xLow,xHigh,yLow,yHigh):
    
    # Determines if x or y position of circle has gone past the bounds of the
    # box
    # Updates the coordinates to match the bounds
    # Reverses the speed to mimic collision with the wall
    
   
    if x < xLow or x > xHigh:
        vx = -vx
        if x < xLow:
            x = xLow
        else:
            x = xHigh
    
    if y < yLow or y > yHigh:
        vy = -vy
        if y < yLow:
            y = yLow
        else:
            y = yHigh
    
    
    return x,y,vx,vy

def Overlap(x1,y1,radius1,x2,y2,radius2):
    
    # Determines if the circles are overlapping using the distance bewteen
    # their centers and each circle's radius
    
    distance = get_distance(x1, y1, x2, y2)
    
    radius_sum = round(radius1 + radius2,3)
    
    if distance < radius_sum:
        return True
    else:
        return False

def get_unit_direction(x1,y1,x2,y2):
    
    # Determines the a unit vector in the direction from one circle's radius
    # to another
    
    if get_distance(x1, y1, x2, y2) == 0:
        return (math.nan, math.nan)
    
    else:
        x_unit = (x1 - x2) / get_distance(x1, y1, x2, y2)
        y_unit = (y1 - y2) / get_distance(x1, y1, x2, y2)
        
        unit_direction = (x_unit, y_unit)
        return unit_direction

def get_distance(x1,y1,x2,y2):
    
    # Calculates the distance between the two circles' centers using the
    # distance formula
    
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2)
    return round(distance,3)
    
def dot_product(x1,y1,x2,y2):
    
    # Returns the dot product of two vectors (x1, y1) and (x2, y2)
    
    result = x1 * x2 + y1 * y2
    return result

def update_collision_velocity(x1,y1,v1x,v1y, x2,y2,v2x,v2y):
    
    # Checks if cirlces are fully overlapped, in which case their velocities are 
    # flipped in both cases
    # In other cases, calculates the new velocites after a collision between
    # circles
    
    if get_distance(x1, y1, x2, y2) == 0:
        
        v1x = -v1x
        v1y = -v1y
        v2x = -v2x
        v2y = -v2y
        
        return v1x, v1y, v2x, v2y
        
    else:
        new_v1x = round(v1x - (dot_product(v1x - v2x, v1y - v2y, x1 - x2, y1 - y2) / \
                 ((get_distance(x1, y1, x2, y2)) ** 2)) * (x1 - x2), 3)
        new_v1y = round(v1y - (dot_product(v1x - v2x, v1y - v2y, x1 - x2, y1 - y2) / \
                 ((get_distance(x1, y1, x2, y2)) ** 2)) * (y1 - y2), 3)
        new_v2x = round(v2x - (dot_product(v2x - v1x, v2y - v1y, x2 - x1, y2 - y1) / \
                 ((get_distance(x1, y1, x2, y2)) ** 2)) * (x2 - x1), 3)
        new_v2y = round(v2y - (dot_product(v2x - v1x, v2y - v1y, x2 - x1, y2 - y1) / \
                 ((get_distance(x1, y1, x2, y2)) ** 2)) * (y2 - y1), 3)
        return new_v1x, new_v1y, new_v2x, new_v2y
        

    
    
    

def circleCollision(x1,y1,radius1,v1x, v1y, x2,y2,radius2,v2x,v2y):
    
    # Checks if circles are touching each other first
    # If so, calls update_collision_velocity to find new velocities
    # Updates new x and y positions for first circle
    
    if Overlap(x1, y1, radius1, x2, y2, radius2):
        v1x, v1y, v2x, v2y = update_collision_velocity(x1, y1, v1x, v1y, x2, y2, v2x, v2y)
    
        distance = get_distance(x1, y1, x2, y2)
        
        x_unit, y_unit = get_unit_direction(x1, y1, x2, y2)
        
        if (x_unit, y_unit) == (math.nan, math.nan):
            x_unit, y_unit = 0.707, 0.707
        
        displacement = round(radius1 + radius2 - distance,3)
        
        x1 = round((x1 + x_unit * displacement),3)
        y1 = round((y1 + y_unit * displacement),3)
        
    return x1, y1, v1x, v1y, x2, y2, v2x, v2y

# DON NOT CHANGE THIS FUNCTION
def simulate(simSteps,vis,x1,y1,x2,y2,v1x,v1y,v2x,v2y,dt,radius):
    
    """
    Run a particle simulation for a specified number of time steps.

    Parameters
    ----------
    simSteps : int
        Number of time steps to run the simulation.
    vis : visualize
        An instance of the 'visualize' class for visualization.
    x1 : float
        Initial x-coordinate of the center of circle 1.
    y1 : float
        Initial y-coordinate of the center of circle 1.
    x2 : float
        Initial x-coordinate of the center of circle 2.
    y2 : float
        Initial y-coordinate of the center of circle 2.
    v1x : float
        Initial x-component of the velocity of circle 1.
    v1y : float
        Initial y-component of the velocity of circle 1.
    v2x : float
        Initial x-component of the velocity of circle 2.
    v2y : float
        Initial y-component of the velocity of circle 2.
    dt : float
        Time step size for the simulation.
    radius : float
        Radius of both particles.

    Returns
    -------
    None

    """
    
    # This function runs a two-particle simulation for a specified number of 
    # time steps. It updates the positions of two circles and checks for 
    # their collisions with both the container boundary and each other. 
    # The simulation is visualized using the'visualize' class instance 
    # provided as 'vis'.
    
    
    # Identify the boundary location for the containing window
    # Assumption: both particles have the same radius.
    xLow,yLow,xHigh, yHigh = boundary_locations(vis,radius) 
    
    for i in range(simSteps):
        
            
    
    
        # update x, y position of particles
        x1 = updateX(x1,v1x,dt)
        y1 = updateY(y1,v1y,dt)
        
        x2 = updateX(x2,v2x,dt)
        y2 = updateY(y2,v2y,dt)
            
        
                    
        # Check for box and circle collisions
        
        x1,y1,v1x,v1y = boxCollision(x1,y1,v1x,v1y,xLow,xHigh,yLow,yHigh)
        
        
        
        x2,y2,v2x,v2y = boxCollision(x2,y2,v2x,v2y,xLow,xHigh,yLow,yHigh)
        
        
        x1,y1,v1x,v1y, x2,y2,v2x,v2y = circleCollision\
                                      (x1,y1,radius,v1x, \
                                        v1y, x2,y2,radius,v2x,v2y)
                    
        
                    
        # draw circles
        vis.circle(x1, y1, radius, 0)
        vis.circle(x2, y2, radius, 1)
        
                    
        # pause plots and clear window axis 1
        vis.plotPause()
        
        
        vis.axis1Clear()
    
    # redraw circles after last iteration
    vis.circle(x1, y1, radius, 0)
    vis.circle(x2, y2, radius, 1)
        
if __name__ == '__main__': 
    
    # Call the main function to excute the simulation
    # For testing purpose comment main() and call another 
    # function.
    main()
    
    
    