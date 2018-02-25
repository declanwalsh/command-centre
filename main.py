# FT (Flight Tracker)
# Author: Declan Walsh
# Last Modified: 4/9/2017

# Main FT Program

# Changelog
# 1 - Added basic adsbexchange API functionality, aircraft class and printing to terminal
# 2 - Added terminaltables library to make terminal printing more effective
# 3 - Added cleaning of data to remove unknown entities and triangle calculation
# 4 - Complete functionality - v1 complete - working sector detection and printing

# To Do
# Detect whether runway 25 is in use (check for mutiple trues in sector above altitudes)
# Highlighting of four engine planes

# external libaries
import time # clock and time functions
import sys
import csv
from csv import DictWriter

# other files in the program
import FTCLI
import FTADSB
import FTProcess
import FTModules

##-------------------------------------------------------
## CONSTANTS
##-------------------------------------------------------
LATITUDE = -33.909887
LONGITUDE = 151.247162
MAX_ALT = 100000 # feet - high enough to capture all through traffic
MIN_ALT = 300 # feet - high enough to filter out ground aircraft at airport
MAX_DISTANCE = 40 # km
MIN_DISTANCE = 0 #km

# angle of sector in degrees
ANGLE_SECTOR_1 = 10
ANGLE_SECTOR_2 = 170

UPDATE_INTERVAL = 60 # interval in seconds between updating A/C information
KB = 1024 # conversion factor from bytes to kb

STATUS_OK = 200
STATUS_UNAUTH = 401
STATUS_INT_ERROR  =500

VERBOSE = 0

        
##-------------------------------------------------------
# MAIN PROGRAM
##-------------------------------------------------------

def main():

    QUERY_STRING = "lat=%s&lng=%s&fDstL=%s&fDstU=%s&fAltL=0&fAltL=%s&fAltU=%s" % (LATITUDE, LONGITUDE, MIN_DISTANCE, MAX_DISTANCE, MIN_ALT, MAX_ALT)

    if(VERBOSE == 1):
        print("Query String is: {}").format(QUERY_STRING)

    origin = FTModules.point(LONGITUDE, LATITUDE)
    
    rawData = FTADSB.retrieveADSB(QUERY_STRING, VERBOSE)

    cleanData = FTADSB.parseADSB(rawData, origin, VERBOSE, ANGLE_SECTOR_1, ANGLE_SECTOR_2)
    
    filteredData = FTADSB.cleanList(cleanData, VERBOSE)

    # FTCLI.drawTable(cleanData)
    FTCLI.drawTable(filteredData, 'dist')
    
# run the main function
if __name__ == "__main__":

    # run the main program
    main()



