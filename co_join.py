# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 19:33:41 2021

@author: Suraj
"""

import pandas as pd
import geopandas
import numpy as np

# Read in the "CO_by_party.csv" file previously created. Specify that the "zip"
# column variables are treated as strings.
 
contrib=pd.read_csv("CO_by_party.csv",dtype={"zip":str})

# Read in the U.S states Census shapefile and select the fips code for the 
# state of interest. In this script, values for Colorado will be selected. 

states=geopandas.read_file("zip://tl_2019_us_state.zip")
co_state=states.query("STATEFP=='08'")

# Read in a zip code shapefile for the state of interest. In this script, the 
# shapefile for Colorado zip codes will be inputted.
 
co_zip=geopandas.read_file("zip://colorado_zip.zip")

# Write the states Census shapefile to a geopackage file. Put the data into a 
# layer called states.

co_state.to_file("co.gpkg",layer="state",driver="GPKG")

# Write the Colorado zip code shapefile to the above geopackage file. Put the
# data into a layer called zip.

co_zip.to_file("co.gpkg",layer="zip",driver="GPKG")

# Read the zip layer of the geopackage file into a variable called geo_zip.

geo_zip=geopandas.read_file("co.gpkg",layer="zip")

# Join the geo_zip and contrib Data Frames and drop the "_merge" column. This 
# will allow the data to be displayed in QGIS. 

joined=geo_zip.merge(contrib,left_on="ZCTA5CE10",right_on="zip",how="left",validate="1:1",indicator=True)    
joined=joined.drop(columns=["_merge"])

# Write the new merged data to the "zip" layer in the co.gpkg geopackage file.
             
joined.to_file("co.gpkg",layer="zip_by_party",driver="GPKG")
