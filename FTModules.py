# FTModules
# Author: Declan Walsh
# Last Modified: 4/9/2017

# Stores the modules for the flight tracker program

# Changelog
# 1 - Added aircraft class
# 2 - Added point and tri class
# 3 - Added vector class

###########################
# CLASSES
###########################

# class to store aircraft data
class aircraft:
    
    # variables common to instances of class go here

    # init is called as class constructor whenever new instance of class created
    def __init__(self, departure, arrival, military, engines, distance, ICAO, operator, aircraftModel, altitude, position, inSector, dist, bearing, call):
        self.departure = departure # string for where flight originated
        self.arrival = arrival # string for where flight will terminate
        self.military = military # boolean for military status
        self.engines = engines # number of engines
        self.distance = distance # float for distance of A/C from reference in km
        self.ICAO = ICAO # string of ICAO identifier
        self.operator = operator # string of aircraft operator
        self.aircraftModel = aircraftModel # string of aircraft model
        self.altitude = altitude # altitude of aircraft in feet
        self.position = position # position of aircraft (latitude, longitude in point class)
        self.inSector = inSector # boolean for in sector
        self.dist = dist # distance from origin
        self.bearing = bearing # angle from north
        self.call = call # callsign (may be - if blank)
        
    # other functions relevant to class go here

    # prints the class instance information for the user
    def displayAircraftInfo(self):
        print("ICAO: {}\nOperator: {}\nCallsign: {}\n".format(self.ICAO, self.operator, self.call))
        print("Aircraft Type: {}\nEngines: {}".format(self.aircraftModel, self.engines))
        print("Departing from: {}\nArriving at: {}".format(self.departure, self.arrival))
        print("Angle from origin: {}\nDistance from origin: {}\n".format(self.dist, self.bearing))

# class to store points (latitude and longitude assumed to be 2D)
class point:

    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    # prints the class instance information for the user
    def displayPointInfo(self):
        print("Longitude: {}\nLatitude: {}\n".format(self.lon, self.lat))

# stores length and angle of a bearing
class vector:

    def __init__(self, length, angle):
        self.length = length
        self.angle = angle

    # prints the class instance information for the user
    def displayVectorInfo(self):
        print("Length: {}\nAngle: {}\n".format(self.length, self.angle))
        
# each element in the class is a point class
class triangle:

    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    # prints the class instance information for the user
    def displayTriInfo(self):
        self.p1.displayPointInfo()
        self.p2.displayPointInfo()
        self.p3.displayPointInfo()
