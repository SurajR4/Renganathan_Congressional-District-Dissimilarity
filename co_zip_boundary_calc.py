# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:12:00 2021

@author: Suraj
"""

import geopandas
# This script appends total area values to the Colorado zip code shapefile. 
# The shapefile as downloaded does not include this information.

# Read in the Colorado zip code shapefile. 

co_state=geopandas.read_file("zip://colorado_zip.zip")

# Build a projected version of the shapefile using the projection recommended 
# for the state of Colorado: UTM Zone 13N, which is also known as EPSG:32613.

co_state=co_state.to_crs(epsg=32613)

# Calculate the area of each zip code, set the index to "ZCTA5CE10" and rename 
# the index to "zipcode".

co_state["total area"]=co_state.area
co_state=co_state.set_index("ZCTA5CE10")
co_state.index.name="zipcode"

# Write out the result to a new geopackage file entitled "co_zip_boundaries.gpkg"

co_state.to_file("co_zip_boundaries.gpkg",driver="GPKG")
