# FTModules
# Author: Declan Walsh
# Last Modified: 17/7/2017

# Stores the modules for the flight tracker program

# Changelog
# 1 - Added aircraft class
# 2 - Added point and tri class

###########################
# CLASSES
###########################

# class to store aircraft data
class aircraft:
    
    # variables common to instances of class go here

    # init is called as class constructor whenever new instance of class created
    def __init__(self, departure, arrival, military, engines, distance, ICAO, operator, aircraftModel, altitude, position, inSector):
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
        
    # other functions relevant to class go here

    # prints the class instance information for the user
    def displayAircraftInfo(self):
        print("ICAO: {}\nOperator: {}".format(self.ICAO, self.operator))
        print("Aircraft Type: {}\nEngines: {}".format(self.aircraftModel, self.engines))
        print("Departing from: {}\nArriving at: {}".format(self.departure, self.arrival))

# class to store points (latitude and longitude assumed to be 2D)
class point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # prints the class instance information for the user
    def displayPointInfo(self):
        print("x: {}\ny: {}\n".format(self.x, self.y))

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
