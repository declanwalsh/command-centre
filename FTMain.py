# FT (Flight Tracker)
# Author: Declan Walsh
# Last Modified: 18/7/2017

# Main FT Program

# Changelog
# 1 - Added basic adsbexchange API functionality, aircraft class and printing to terminal
# 2 - Added terminaltables library to make terminal printing more effective

# external libaries
import time # clock and time functions
import requests # HTTP functions
import sys
import json
import csv
from csv import DictWriter

# other files in the program
import FTModules
import FTCLI

##-------------------------------------------------------
## CONSTANTS
##-------------------------------------------------------
LATITUDE = -33.909887
LONGITUDE = 151.247162
MAX_ALT = 100000 # feet - high enough to capture all through traffic
MIN_ALT = 200 # feet - high enough to filter out ground aircraft at airport
MAX_DISTANCE = 20 # km
MIN_DISTANCE = 0 #km

UPDATE_INTERVAL = 60 # inteval in seconds between updating A/C information
KB = 1024 # conversion factor from bytes to kb

STATUS_OK = 200
STATUS_UNAUTH = 401
STATUS_INT_ERROR  =500

VERBOSE = 0

##-------------------------------------------------------
## FUNCTIONS
##-------------------------------------------------------

# checks the status code of the returned HTTP request
# prints debug based on status code
def checkRequestStatus( status_code ):
    
    if(status_code == STATUS_OK):
        print('Status %d = OK') % status_code
    elif(status_code == STATUS_UNAUTH):
        print('Status %d = Unauthorized Access: Check API key or Limits Reached') % status_code
    elif(status_code == STATUS_INT_ERROR):
        print('Status %d = Internal Error: Check API key') % status_code
    else:
        print('Status %d = Error: Unknown Status Returned') % status_code

    return

# retrieves json of data from given ADSB Exchange URL
# returns the json from data
def retrieveADSB( parameters, VERBOSE ):

    URL = "http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json"
    URL_GET = "%s?%s" % (URL, parameters)

    if(VERBOSE == 1):
        print("\nRetrieving information")
        print("URL being GET: {}").format(URL_GET)
        
    # collect data with GET HTTP request
    data = requests.get(URL_GET)
    
    if(VERBOSE == 1):
        # check status code
        checkRequestStatus(data.status_code)
        print("Retrieved information")
        print("Retrieved {} kilobytes\n").format(len(data.content)/KB)

    return data

# takes the json of data and converts it to a dict and makes it into a readable class
# return the classes
def parseADSB(data, VERBOSE):

    acList = [] # list that will store aircraft in defined class

    dicts = json.loads(data.content) # convert to a dictionary to parse easier
    acListDicts = dicts['acList'] # data has an acList property that stores all A/C data

    if(VERBOSE == 1):
        print("{} aircraft have been detected in the nearby airspace\n".format(len(acListDicts)))

    for entity in acListDicts:

        # see http://www.virtualradarserver.co.uk/Documentation/Formats/AircraftList.aspx
        # for a full list of properties in the data

        # not all aircraft file a flight plan
        # need to still have values to prevent errors in processing
        if 'From' in entity:
            dpt = entity['From']
            arv = entity['To']
        else:
            dpt = "Route Unknown"
            arv = "Route Unknown"
            
        mil = entity['Mil']

        if 'Engines' in entity:
            eng = entity['Engines']
        else:
            eng = "Unknown"
            
        dst = entity['Dst']
        ICAO = entity['Icao']

        if 'Op' in entity:
            op = entity['Op']
        else:
            op = "Unknown"

        if 'Mdl' in entity:
            mdl = entity['Mdl']
        else:
            mdl = "Unknown"
            
        acListAdd = FTModules.aircraft(dpt, arv, mil, eng, dst, ICAO, op, mdl)

        if(VERBOSE == 1):
            acListAdd.displayAircraftInfo()
            print("\n")
        
        acList.append(acListAdd)

    return acList
        
##-------------------------------------------------------
# MAIN PROGRAM
##-------------------------------------------------------

def main():

    QUERY_STRING = "lat=%s&lng=%s&fDstL=%s&fDstU=%s&fAltL=0&fAltL=%s&fAltU=%s" % (LATITUDE, LONGITUDE, MIN_DISTANCE, MAX_DISTANCE, MIN_ALT, MAX_ALT)

    if(VERBOSE == 1):
        print("Query String is: {}").format(QUERY_STRING)

    rawData = retrieveADSB(QUERY_STRING, VERBOSE)

    cleanData = parseADSB(rawData, VERBOSE)

    FTCLI.drawTable(cleanData)
    
# run the main function
if __name__ == "__main__":

    # run the main program
    main()



