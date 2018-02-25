# BBBCSV
# Author: Declan Walsh
# Last Modified: 8/11/2016

# busy_bee_buses functions relating to reading from and writing to csv's

# Changelog
# 1 - Moved csv reading program from main to here
# 2 - Added verbose options and printing stops functions

###########################
# CONSTANTS
###########################

COL_STOP_ID = 0
COL_ROUTE_NAME = 1
COL_BUSES = 2
COL_ROUTE_DESC = 3
COL_ORIGIN = 4
COL_DESTINATION = 5

import csv # for reading from and writing to CSVs
import BBBModules

# function for reading a CSV in a known format to obtain the bus information
def readCSV (filename, ORIGIN, DESTINATION, VERBOSE):

    # used to determine if stop in database (0 for specified stop not in database and 1 if it is)
    found = 0

    with open(filename, 'rb') as csvfile:
        next(csvfile)
        readerFile = csv.reader(csvfile, delimiter=',', quotechar = '"')
        for row in readerFile:
            ORIGIN_ROW = row[COL_ORIGIN]
            DESTINATION_ROW = row[COL_DESTINATION]
            if (ORIGIN_ROW==ORIGIN and DESTINATION_ROW==DESTINATION):
                
                stopID = row[COL_STOP_ID]
                routeName = row[COL_ROUTE_NAME]
                busList = row[COL_BUSES]
                routeDesc = row[COL_ROUTE_DESC]
                routeOrigin = row[COL_ORIGIN]
                routeDestination = row[COL_DESTINATION]

                busActive = BBBModules.busStop(stopID, routeName, busList, routeDesc, routeOrigin, routeDestination)

                found = 1
                break # stop loop once stop is found

    if(found == 0):
        print('ERROR - No route found - Check inputs and csv directory')
        printStopsCSV(filename)
        exit()
    elif(found == 1 & VERBOSE == 1):
        print('Route found')

    return busActive

# function for printing the stops in the CSV
def printStopsCSV(filename):

    print("Stops included in the database currently include:")
    
    with open(filename, 'rb') as csvfile:
        next(csvfile) # skip header row
        readerFile = csv.reader(csvfile, delimiter=',', quotechar = '"')
        for row in readerFile:
            origin = row[COL_ORIGIN]
            dest = row[COL_DESTINATION]

            print("Origin: {} - Destination: {}".format(origin, dest))

    print("If your desired stop is not included, add it to the CSV")
            
# function to setup the CSV settings for the CSV library
def setupCSVDialects ():

    return
