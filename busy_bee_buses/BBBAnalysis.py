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

