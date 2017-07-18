# FTADSB
# Author: Declan Walsh
# Last Modified: 17/7/2017

# Capture and processing of ADSB data

# Changelog
# 1 - Moved files from FTMain.py to here
# 2 - Added clean list function to remove unknown entities and position/inSector info to AC classes

import requests # HTTP functions
import json

import FTModules
import FTProcess

##-------------------------------------------------------
## FUNCTIONS
##------------------------------------------------------

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
def parseADSB(data, tri, VERBOSE):

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

        alt = entity['Alt']/1000.0

        pos = FTModules.point(entity['Lat'], entity['Long'])

        inSec = FTProcess.pointInTriangle(pos, tri, VERBOSE)
        
        acListAdd = FTModules.aircraft(dpt, arv, mil, eng, dst, ICAO, op, mdl, alt, pos, inSec)

        if(VERBOSE == 1):
            acListAdd.displayAircraftInfo()
            print("\n")
        
        acList.append(acListAdd)

    return acList

# takes the list of aircraft and removes those with no flight information
def cleanList(data, VERBOSE):

    acListClean = []
    
    for entity in data:
        if (entity.operator != "Unknown" and entity.aircraftModel != "Unknown"):
            acListClean.append(entity) 
        else:
            if(VERBOSE == 1):
                print("Removing: ")
                entity.displayAircraftInfo()
                print("\n")

    return acListClean
