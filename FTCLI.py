# FTCLI
# Author: Declan Walsh
# Last Modified: 25/4/2017

# Draws a command line interface for the data obtained

# Changelog
# 1 - Created and output headers
# 2 - Edited to use terminaltables library with AsciiTables

from terminaltables import AsciiTable

def drawTable(data):
    
    table_data = [
        ['ICAO', 'Operator',  'Model', 'Engines', 'From', ' To', 'Military' ]]

    for entity in data:
        table_data.append([entity.ICAO, entity.operator, entity.aircraftModel, entity.engines, entity.departure, entity.arrival, entity.military])

    table = AsciiTable(table_data)
    print table.table
