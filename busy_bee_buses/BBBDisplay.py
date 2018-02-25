# BBBDisplay
# Author: Declan Walsh
# Last Modified: 3/11/2016

# busy_bee_buses functions for displaying the data in tables

# Changelog
# 1 - Created

###########################
# IMPORTS
###########################

from terminaltables import SingleTable
from datetime import datetime
import operator
import BBBAnalysis

###########################
# FUNCTIONS
###########################

# draws a neatly formatted table of data
def drawBusTable(unsortedData, sortKey):
    
    table_data = [
        ['Bus Number', 'Est. Time',  'Delay']]

    # sorts the buses based on specified key (normally arrival time)
    data = sorted(unsortedData, key=operator.attrgetter(sortKey))

    for entity in data:
        table_data.append([entity.number, BBBAnalysis.formatTime(entity.estTime), BBBAnalysis.formatDelay(entity.delay)])
        
    tableComplete = SingleTable(table_data)

    timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    titleStr = "Bus Information: " + timeStr
    
    tableComplete.title = titleStr
    print tableComplete.table
