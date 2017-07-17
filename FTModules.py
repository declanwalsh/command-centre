# FTModules
# Author: Declan Walsh
# Last Modified: 25/4/2017

# Stores the modules for the flight tracker program

# Changelog
# 1 - Added aircraft class

###########################
# CLASSES
###########################

# class to store aircraft data
class aircraft:
    # variables common to instances of class go here

    # init is called as class constructor whenever new instance of class created
    def __init__(self, departure, arrival, military, engines, distance, ICAO, operator, aircraftModel):
        self.departure = departure # string for where flight originated
        self.arrival = arrival # string for where flight will terminate
        self.military = military # boolean for military status
        self.engines = engines # number of engines
        self.distance = distance # float for distance of A/C from reference in km
        self.ICAO = ICAO # string of ICAO identifier
        self.operator = operator # string of aircraft operator
        self.aircraftModel = aircraftModel # string of aircraft model

    # other functions relevant to class go here

    # prints the class instance information for the user
    def displayAircraftInfo(self):
        print("ICAO: {}\nOperator: {}".format(self.ICAO, self.operator))
        print("Aircraft Type: {}\nEngines: {}".format(self.aircraftModel, self.engines))
        print("Departing from: {}\nArriving at: {}".format(self.departure, self.arrival))
