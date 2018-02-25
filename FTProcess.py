# FTProcess
# Author: Declan Walsh
# Last Modified: 4/9/2017

# Functions for distance and position calculations

# Changelog
# 1 - Added triangle creation, vincey's method of calculating lat and long and barycentric co-ordinate method of calculating position in triangle
# 2 - Changed to Haversine's method for calculating range and bearing

from math import radians, cos, sin, asin, sqrt, atan2, degrees
import math
import FTModules

SEMI_MAJOR_AXIS = 6378137.0 # length of semi-major axis of the ellipsoid (radius at equator) from WGS-84
FLATTENING = 1/298.257223563 # flattening of ellipsoid from WGS-84
KILO = 1000 # conversion from metres to kilometers

# calculates the bearing and range given two lat, long co-ordinates
# returns the resultant vector
# code from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(origin, target):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """

    lon1 = origin.lon
    lat1 = origin.lat
    lon2 = target.lon
    lat2 = target.lat
    
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = SEMI_MAJOR_AXIS/KILO

    bearing = atan2(sin(lon2-lon1)*cos(lat2), cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360

    vectorHaversine = FTModules.vector(c*r, bearing)
    
    return vectorHaversine

# checks if a vector lies within a sector (angle boundaries)
# units need to be consistent (all angles or radians)
def pointInSector(vector, angleMin, angleMax):

    inSector = False
    
    if vector.angle < angleMax and vector.angle > angleMin:
        inSector = True

    return inSector

# forms a triangle object from an origin, two angles and the distance of the two points from the origin
def calculateTrianglePoints(originX, originY, angleLimit1, angleLimit2, maxDistance, VERBOSE):
    
    origin = FTModules.point(originX, originY)

    p1 = vinc_pt(FLATTENING, SEMI_MAJOR_AXIS, originX, originY, angleLimit1, maxDistance*KILO)
    point1 = FTModules.point(p1[2], p1[1])

    p2 = vinc_pt(FLATTENING, SEMI_MAJOR_AXIS, originX, originY, angleLimit2, maxDistance*KILO)
    point2 = FTModules.point(p2[2], p2[1])
    
    tri = FTModules.triangle(origin, point1, point2)

    if(VERBOSE == 1):
        print("Triangle points are:\n")
        tri.displayTriInfo()
   
    return tri

# checks if a point lies within a triangle
def pointInTriangle(acPos, tri, VERBOSE):

    insideTriangle = False
    
    denom = ((tri.p2.y - tri.p3.y)*(tri.p1.x - tri.p3.x) + (tri.p3.x - tri.p2.x)*(tri.p1.y - tri.p3.y))
    
    alpha = ((tri.p2.y - tri.p3.y)*(acPos.x - tri.p3.x) + (tri.p3.x - tri.p2.x)*(acPos.y - tri.p3.y))/denom
    beta = ((tri.p3.y - tri.p1.y)*(acPos.x - tri.p3.x) + (tri.p1.x - tri.p3.x)*(acPos.y - tri.p3.y)) /denom
    gamma = 1.0 - alpha - beta

    if (alpha < 1.0 and alpha > 0.0 and beta < 1.0 and beta > 0.0 and gamma < 1.0 and gamma > 0.0):
         insideTriangle = True

    if(VERBOSE == 1):
        print("Alpha: {}, Beta: {}, Gamma: {}\n".format(alpha, beta, gamma))

    return insideTriangle
