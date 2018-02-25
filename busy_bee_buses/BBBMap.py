# BBBMap
# Author: Declan Walsh
# Last Modified: 8/11/2016

# functions related to mapping

# Changelog
# 1 - Added basic dictionary and functionality from http://nbviewer.jupyter.org/gist/timbennett/7ec739fc619459316859d3875b76a76b/notebook.ipynb
# 2 - Fixed functionality for the broken API key
# 3 - Got basic case of displaying buses on map working (all buses with route numbers)

###########################
# IMPORTS
###########################

import json
from bokeh.plotting import save
from bokeh.io import (output_file, show)
from bokeh.models import ( GeoJSONDataSource, GMapPlot, GMapOptions, ColumnDataSource, Circle, 
                           DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, HoverTool)

def mapCreate(busList):
    
    # create the dictionary
    feature_collection = {}
    feature_collection['type'] = "FeatureCollection"
    feature_collection['features'] = []

    mapsAPI = "AIzaSyB_TQyPnJCd3MTNaBCY9umf709N_rvVWnI"
    
   # for bus in busList:
      #  this_object = {"type":"Feature",
               #        "geometry":{"type":"Point",
              #                     "coordinates": [bus.position.longitude, bus.position.latitude]
       #                },
             #          "properties": {"route":bus.name}
       # }
       # }

    for bus in busList:
        this_object = {"type":"Feature",
                       "geometry":{"type":"Point",
                                   "coordinates": [bus.longitude, bus.latitude]
                       },
                       "properties": {"route" : "111"}
        }
        feature_collection['features'].append(this_object)

    bus_geojson = json.dumps(feature_collection)
            
    # print('Result: "{}..."'.format(bus_geojson)) # print a little bit of the result; you could also write to a file

    map_options = GMapOptions(lat=-33.87, lng=151.1, map_type="roadmap", zoom=11)

    geo_source = GeoJSONDataSource(geojson=bus_geojson)
    circle = Circle(x="x", y="y", size=6, fill_color="blue", fill_alpha=0.8, line_color=None)
    
    plot = GMapPlot(
        x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, 
        plot_width=900, plot_height=900, api_key = mapsAPI
    )

    plot.add_glyph(geo_source, circle)
    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

    output_file('bus-positions.html')
    save(plot)

    show(plot)
