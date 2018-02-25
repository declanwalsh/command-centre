# BBBModules
# Author: Declan Walsh
# Last Modified: 3/11/2016

# Stores the classes for the busy_bee_buses program

# Changelog
# 1 - Added busStop class
# 2 - Added bus class

###########################
# CLASSES
###########################

# class to store bus stops for comparision to data from site
class busStop:
    # variables common to instances of class go here

    # init is called as class constructor whenever new instance of class created
    def __init__(self, ID, name, bus, descriptor, origin, destination):
        self.ID = ID # unique ID for bus stop
        self.name = name # readable user-set identifier for route
        self.bus = bus # list of strings of buses
        self.descriptor = descriptor # string description of stop
        self.origin = origin # string of state of route
        self.destination = destination # string of destination of route   

    # other functions relevant to class go here

    # prints the class instance information for the user
    def displayStopInfo(self):
        print("Stop Name: {}\nStop ID: {}\nStop Buses: {}".format(self.name, self.ID, self.bus))
        print("Stop Description: {}".format(self.descriptor))
        print("The route is from {} to {}".format(self.origin, self.destination))

# class to store bus data        
class bus:

    def __init__(self, ID, number, position, delay, estTime):
        self.ID = ID # unique bus ID
        self.number = number # 3 digit normal bus number
        self.position = position #lat/long/bearing/speed
        self.delay = delay # delay in system
        self.estTime = estTime # estimated time to arriving at specified stop

    # prints the class infomation for user
    def displayBusInfo(self):
        print("Bus Number: {}".format(self.number))
        print("Delay: {}\nEstimated Time to Arrival: {}".format(self.delay, self.estTime))
        print(self.position)
