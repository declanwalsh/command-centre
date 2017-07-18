# FTCLI
# Author: Declan Walsh
# Last Modified: 17/7/2017

# Draws a command line interface for the data obtained

# Changelog
# 1 - Created output headers, footer and data
# 2 - Edited to use terminaltables library with AsciiTables

from terminaltables import AsciiTable

def drawTable(data):
    
    table_data = [
        ['ICAO', 'Operator',  'Model', 'Engines', 'From', ' To', 'Altitude', 'Sector' ]]

    for entity in data:
        table_data.append([entity.ICAO, entity.operator, entity.aircraftModel, entity.engines, entity.departure, entity.arrival, entity.altitude, entity.inSector])

    table = AsciiTable(table_data)
    print table.table
