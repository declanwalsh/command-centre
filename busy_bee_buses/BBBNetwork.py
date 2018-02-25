# BBBNetwork
# Author: Declan Walsh
# Last Modified: 25/2/2018

# Functions related to network procedures

# Changelog
# 1 - Added checkStatus functions and authentication/data retrieval functions
# 2 - Added VERBOSE options
# 3 - Modified to use the apikey header authentatication instead of Oauth2

import requests # HTTP functions
from google.transit import gtfs_realtime_pb2 # interpreting gtfs data

STATUS_OK = 200
STATUS_BADREQUEST = 400
STATUS_UNAUTH = 401
STATUS_INT_ERROR  =500
KB = 1024

# checks the status code of the returned HTTP request
# prints debug based on status code
def checkRequestStatus( status_code ):
    
    if(status_code == STATUS_OK):
        print('Status %d = OK') % status_code
    elif(status_code == STATUS_BADREQUEST):
        print('Status %d = Bad request')% status_code
    elif(status_code == STATUS_UNAUTH):
        print('Status %d = Unauthorized Access: Check API key or Limits Reached') % status_code
    elif(status_code == STATUS_INT_ERROR):
        print('Status %d = Internal Error: Check API key') % status_code
    else:
        print('Status %d = Error: Unknown Status Returned') % status_code

    return

# retrieves GTFS data from a given openTransportData URL
# returns GTFS feed from data
def retrieveDataGTFS( URL, headers, VERBOSE ):

    if(VERBOSE == 1):
        print("Retrieving information")
        
    # collect data with GET HTTP request
    data = requests.get(URL, headers=headers)

    if(VERBOSE == 1):
        # check status code
        checkRequestStatus(data.status_code)
        print("Retrieved information")
        print("Retrieved {} kilobytes\n").format(len(data.content)/KB)

    # convert data into GTFS feeed object 
    feedData = gtfs_realtime_pb2.FeedMessage()
    feedData.ParseFromString(data.content)
    
    return feedData
