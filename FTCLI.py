# FTCLI
# Author: Declan Walsh
# Last Modified: 4/9/2017

# Draws a command line interface for the data obtained

# Changelog
# 1 - Created output headers, footer and data
# 2 - Edited to use terminaltables library with AsciiTables
# 3 - Added bearing and range to print and added ability to sort

from terminaltables import SingleTable
from datetime import datetime
import operator

def drawTable(unsortedData, sortKey):

    LENGTH_SHORT = 20
    
    table_data = [
        ['Call', 'Operator',  'Model', 'Engines', 'From', ' To', 'Altitude', 'Range', 'Bearing', 'Sector' ]]

    data = sorted(unsortedData, key=operator.attrgetter(sortKey))

    listInSector = []
    listOutSector = []
    
    for entity in data:
        if entity.inSector == True:
            listInSector.append(entity)
        else:
            listOutSector.append(entity)
            
    for entity in listInSector:
        reducedOp = info = (entity.operator[:LENGTH_SHORT] + '..') if len(entity.operator) > LENGTH_SHORT else entity.operator
        reducedDep = info = (entity.departure[:LENGTH_SHORT] + '..') if len(entity.departure) > LENGTH_SHORT else entity.departure
        reducedArr = info = (entity.arrival[:LENGTH_SHORT] + '..') if len(entity.arrival) > LENGTH_SHORT else entity.arrival
        table_data.append([entity.call, reducedOp, entity.aircraftModel, entity.engines, reducedDep, reducedArr, entity.altitude, round(entity.dist, 1), round(entity.bearing, 1), entity.inSector])

    for entity in listOutSector:
        reducedOp = info = (entity.operator[:LENGTH_SHORT] + '..') if len(entity.operator) > LENGTH_SHORT else entity.operator
        reducedDep = info = (entity.departure[:LENGTH_SHORT] + '..') if len(entity.departure) > LENGTH_SHORT else entity.departure
        reducedArr = info = (entity.arrival[:LENGTH_SHORT] + '..') if len(entity.arrival) > LENGTH_SHORT else entity.arrival
        table_data.append([entity.call, reducedOp, entity.aircraftModel, entity.engines, reducedDep, reducedArr, entity.altitude, round(entity.dist, 1), round(entity.bearing, 1), entity.inSector])
        
    tableComplete = SingleTable(table_data)

    timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    titleStr = "A/C Information: " + timeStr
    
    tableComplete.title = titleStr
    print tableComplete.table
