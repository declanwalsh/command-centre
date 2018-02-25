# BBB (busy bee buses)
# Author: Declan Walsh
# Last Modified: 8/11/2016

# Main busy_bee_buses program

# Changelog
# 1 - Added basic opendata API functionality from http://nbviewer.jupyter.org/gist/timbennett/7ec739fc619459316859d3875b76a76b/notebook.ipynb
# 2 - Extended to search realtime timetables for buses
# 3 - Added busStop class and created Network and Module function files
# 4 - Added csv reader support for importing data
# 5 - Moved csv reader to another file
# 6 - Added delay functionality
# 7 - Created bus class and added sorting of the resultant list to optimise choice
# 8 - Added analysis file for functions
# 9 - Added arguments passed into main program
# 10 - Added verbose option
# 11 - Fixed map with plot option and all route number cases

# To Do
# 1 - Add functionality for multiple nearby stops to same destination (e.g. bottom of uni to city)
# 2 - Verify the results (currently some inconsistencies between refreshes and )
# 3 - On map display buses route number and different colour for already been/to come
# 4 - Move argument input and checking to a separate file

###########################
# IMPORTS
###########################

# defined functions
import time # clock and time functions
from google.transit import gtfs_realtime_pb2 # interpreting gtfs data
import sys

# user made functions
import BBBModules
import BBBNetwork
import BBBCSV
import BBBAnalysis
import BBBMap

###########################
# ARGUMENTS
###########################

if(len(sys.argv) < 3):
    print("Must set an origin AND destination")
    sys.exit()

# strings for origin and destination
ORIGIN = sys.argv[1]
DESTINATION = sys.argv[2]

if(len(sys.argv) > 3):
    # integer of 1 (to display map) or otherwise to not display additional information
    MAP_PLOT = sys.argv[3]

    if MAP_PLOT == '1':
        MAP_PLOT = 1
    else:
        MAP_PLOT = 0
else:
    MAP_PLOT = 0

if(len(sys.argv) > 4):
    # integer of 1 (to display) or otherise (to not display) additional information (for testing)
    VERBOSE = sys.argv[4]
    if VERBOSE == '1':
        VERBOSE = 1
    else:
        VERBOSE = 0
else:
    VERBOSE = 0

if(len(sys.argv) > 5):
    print("Only 4 arguments needed - Excess arguments are ignored")
        
###########################
# MAIN PROGRAM
###########################

# main runtime function
def main():

    # API user information
    api_key = 'l7xxde410bb18efd4606a34b29ce3439e689'
    shared_secret = '79c1f1b9af3b4682ae4cc780ca75b952'

    # retrieve security headers
    headers = BBBNetwork.authentication(api_key, shared_secret, VERBOSE)

    # retrieve real time bus positions
    feedTotal = BBBNetwork.retrieveDataGTFS('https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses', headers, VERBOSE)

    # read in the stop information
    if(VERBOSE == 1):
        print("START - stop data")
        
    activeStop = BBBCSV.readCSV('stopDatabase.csv', ORIGIN, DESTINATION, VERBOSE) 

    if(VERBOSE == 1):
        activeStop.displayStopInfo()
        print("END - stop data\n")
    
    # https://developers.google.com/transit/gtfs-realtime/reference/VehiclePosition
    # entity.vehicle referes to the vehiclePosition set of data
            
    # retrieve realtime timetable data
    feedStops = BBBNetwork.retrieveDataGTFS('https://api.transport.nsw.gov.au/v1/gtfs/realtime/buses', headers, VERBOSE) 
            
    busList = []
    listRelevant = []
    
    # for every bus trip, checks all bus stops to see if the stop ID is in there
    for entity in feedStops.entity:
        for stop_time_update in entity.trip_update.stop_time_update:
            if(stop_time_update.stop_id in activeStop.ID): # filters out buses not going to stop
                if(entity.trip_update.trip.route_id[5:] in  activeStop.bus): # filters out buses at stop not in list of buses                
                    # gets current unix time and compares to bus arrival unix time
                    currentTime = int(time.time())
                    busArrivalTime = stop_time_update.arrival.time
                    totalSecToArrive = busArrivalTime - currentTime
                    timeToArrive = BBBAnalysis.formatTime(totalSecToArrive)
                    
                    # pulls bus number from realtime timetable
                    busID = entity.trip_update.trip.route_id[5:]
                    
                    # gets reported delay of bus according to online
                    reportedDelay = stop_time_update.arrival.delay
                    delay = BBBAnalysis.formatDelay(reportedDelay)
                    
                    busPosition = '111'
                    
                    # adds bus to list of buses leaving from stop going to destination
                    busListAdd = BBBModules.bus('111', busID, busPosition, reportedDelay, totalSecToArrive)
                    busList.append(busListAdd)

                    listRelevant.append(entity.trip_update.trip.trip_id)

                    if(VERBOSE == 1):
                        busListAdd.displayBusInfo()

    # stores the trip id's of all buses that have positions and correct route number
    listPosition = []

    # adds the trip_id of buses with relevant route numbers to a list
    for entity in feedTotal.entity:
        if(entity.vehicle.trip.route_id[5:] in activeStop.bus):

            if(VERBOSE == 1):
                print(entity.vehicle.position)
       
            listPosition.append(entity.vehicle.position)

           # if contains(busList, lambda entity:entity.vehicle.trip.trip_id 
            
    # sorts the buses based on the estimtated time of arrival
    sortedBusList = sorted(busList, key=lambda bus:bus.estTime)
    
    # prints the bus list
    for bus in sortedBusList:
        print("{} - {} - {}".format(bus.number, BBBAnalysis.formatTime(bus.estTime), BBBAnalysis.formatDelay(bus.delay)))

    if(MAP_PLOT == 1):
        BBBMap.mapCreate(listPosition)
        
    # quits program after a single run
    sys.exit()
    
# run the main function
if __name__ == "__main__":

    # run the main program
    main()
