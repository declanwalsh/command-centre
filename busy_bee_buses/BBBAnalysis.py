# BBBAnalysis
# Author: Declan Walsh
# Last Modified: 3/11/2016

# busy_bee_buses functions for parsing data

# Changelog
# 1 - Added existing functions

###########################
# IMPORTS
###########################

import math
import BBBModules
import time # clock and time functions

###########################
# FUNCTIONS
###########################

# input time in unix
def formatTime (totalSeconds):

    minute = math.fabs(math.floor(totalSeconds/60))
    second = totalSeconds%60

    return "{0:.0f}:{1:02d}".format(minute, second)

# input reported delay in seconds to classify the delay and output as formatted string
def formatDelay (reportedDelay):

    # convert seconds to formatted time
    timeDelay = formatTime(reportedDelay)
    
    if(reportedDelay > 0):
        return "Delay of {}".format(timeDelay)
    elif(reportedDelay == 0):
        return "On time"
    else:
        return "Early by {}".format(timeDelay)

# extracts bus info into usable form
def extractBusInfo(feedStops, activeStop, VERBOSE):

    busList = []
    listRelevant = [] # unused currently
    
    # for every bus trip, checks all bus stops to see if the stop ID is in there
    for entity in feedStops.entity:    
        for stop_time_update in entity.trip_update.stop_time_update:
            if(stop_time_update.stop_id in activeStop.ID): # filters out buses not going to stop
                if(entity.trip_update.trip.route_id[5:] in  activeStop.bus): # filters out buses at stop not in list of buses                
                    # gets current unix time and compares to bus arrival unix time
                    currentTime = int(time.time())
                    busArrivalTime = stop_time_update.arrival.time
                    totalSecToArrive = busArrivalTime - currentTime
                    timeToArrive = formatTime(totalSecToArrive)
                    
                    # pulls bus number from realtime timetable
                    busID = entity.trip_update.trip.route_id[5:]
                    
                    # gets reported delay of bus according to online
                    reportedDelay = stop_time_update.arrival.delay
                    delay = formatDelay(reportedDelay)

                    # placeholder
                    busPosition = '111'
                    
                    # adds bus to list of buses leaving from stop going to destination
                    busListAdd = BBBModules.bus('111', busID, busPosition, reportedDelay, totalSecToArrive)
                    busList.append(busListAdd)

                    # adds trip ID to list of relevant IDs
                    listRelevant.append(entity.trip_update.trip.trip_id)

                    # prints all the bus info data parsed
                    if(VERBOSE == 1):
                        busListAdd.displayBusInfo()

    return busList


def extractListPosition(feedTotal, activeStop, VERBOSE):
    
    # stores the trip id's of all buses that have positions and correct route number
    listPosition = []

    # adds the trip_id of buses with relevant route numbers to a list
    for entity in feedTotal.entity:
        if(entity.vehicle.trip.route_id[5:] in activeStop.bus):

            if(VERBOSE == 1):
                print(entity.vehicle.position)
       
            listPosition.append(entity.vehicle.position)

    return listPosition
