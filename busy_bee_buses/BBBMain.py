# BBB (busy bee buses)
# Author: Declan Walsh
# Last Modified: 25/2/2018

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
# 12 - Updated to use api key authentication instead of OAuth2 (as per TfNSW recommendations)
# 13 - Moved the main extraction functions to a separate file

# To Do
# 1 - Add functionality for multiple nearby stops to same destination (e.g. bottom of uni to city)
# 2 - Verify the results (currently some inconsistencies with delays not appearing and buses falling of the lists on refresh)
# 3 - On map display buses route number and different colour for already been/to come
# 4 - Move argument input and checking to a separate file

###########################
# IMPORTS
###########################

# defined functions
from google.transit import gtfs_realtime_pb2 # interpreting gtfs data
import sys

# user made functions
import BBBModules
import BBBNetwork
import BBBCSV
import BBBAnalysis
import BBBDisplay
#import BBBMap

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
    VERBOSE = 1

if(VERBOSE):
    print('Origin: %s') % ORIGIN
    print('Destination: %s') % DESTINATION
    print('Map plot: %d') % MAP_PLOT

if(len(sys.argv) > 5):
    print("Only 4 arguments needed - Excess arguments are ignored")
        
###########################
# MAIN PROGRAM
###########################

# main runtime function
def main():

    # API user information
    # user should insert their own here
    api_key = 'l7xxde410bb18efd4606a34b29ce3439e689'

    # create api key authentication headers
    headers = {'Authorization': 'apikey {}'.format(api_key)} 

    if(VERBOSE == 1):
        print("Headers used are: ")
        print(headers)
    
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

    # extracts the bus data
    busList = BBBAnalysis.extractBusInfo(feedStops, activeStop, VERBOSE)
    
    # not used currently
    #listPosition = BBBAnalysis.extractListPosition(feedTotal, activeStop, VERBOSE)
            
    BBBDisplay.drawBusTable(busList, 'estTime')
        
    # quits program after a single run
    sys.exit()

    
# run the main function
if __name__ == "__main__":

    # run the main program
    main()
