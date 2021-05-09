# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:22:05 2021

@author: Suraj
"""

import geopandas

# Read in the zip layer and zip_pieces_area layer of the co.gpkg file. 
zip_area=geopandas.read_file("co.gpkg",layer="zip_pieces_area")

zip_party=geopandas.read_file("co.gpkg",layer="zip_by_party")

# Rename columns
zip_party=zip_party.rename(columns={"ZCTA5CE10":"zipcode"})

# Rename columns
zip_area=zip_area.rename(columns={"ZCTA5CE10":"zipcode"})

# Select a subset of columns and set the index to the "zipcode" column
zip_party_trim=zip_party[["zipcode","DEM","REP","total"]]
zip_party_trim=zip_party_trim.set_index(["zipcode"])

# Select a subset of columns and set the index to the "zipcode" and "NAMELSAD 
# columns
zip_area_trim=zip_area[["zipcode","CD116FP","NAMELSAD","area"]]
zip_area_trim=zip_area_trim.set_index(["zipcode","NAMELSAD"])

# Group the zip_area_trim Data Frame by zipcode and calculate the total area of
# each zip code.This is a useful verfication step to ensure that calculated zip
# code areas actually match the zip code areas as published by the Census.

grouped=zip_area_trim.groupby(["zipcode"])
total_area=grouped["area"].sum()

# Calcualte the area proportion each zip piece comprises in relation to the 
# larger zip code. 

zip_area_trim["area_prop"]=zip_area_trim["area"].div(total_area)

# Join zip_party_trim on zip_area_trim and make a copy of the result. 
# Subsequently, allocate the Democratic and Republican contributions in each 
# zip code to its respective zip pieces according to each zip piece's area proportion. 

merged=zip_area_trim.merge(zip_party_trim,on="zipcode",how="outer",validate="m:1",indicator=True)
merged2=merged.copy()
merged2["DEM"]=merged2["DEM"]*merged2["area_prop"]
merged2["REP"]=merged2["REP"]*merged2["area_prop"]
merged2["total"]=merged2["total"]*merged2["area_prop"]

# Drop the "_merge" column in the resulting Data Frame and write it out as a csv file.

merged2=merged2.drop(columns=["_merge"])
merged2.to_csv("zip_pieces_contrib.csv")

# Now calculate the contributions made to Democrats and Republicans in each 
# congressional district. Group merged2 by "CD116FP", which is the 
# district number a zip piece belongs to, and aggregate the DEM, REP, and total
# columns as a sum. The grouped2 variable illustrates contributions made to 
# Democrats, Republicans, and in total for each congressional district in a state. 

grouped2=merged2.groupby(["CD116FP"],as_index=False).agg({"DEM":"sum","REP":"sum","total":"sum"})

# Set the index for grouped2 to "CD116FP" and calculate the share of contributions in each district made to Democrats. 

grouped2=grouped2.set_index(["CD116FP"])
grouped2["d_share"]=grouped2["DEM"]/grouped2["total"]

# Read in the U.S Congressional Distrct Census shapefile. Use a query method to
# select the congressional district for the state of interest (in this case CO).

distr=geopandas.read_file("zip://tl_2019_us_cd116.zip")
co_distr=distr.query("STATEFP=='08'").copy()

# Merge the grouped2 on the Congressional District shapefile. This will provide
# a new shapefile with information regarding each district's contributions. 

distr_contrib=co_distr.merge(grouped2,on="CD116FP",how="outer",validate="1:1",indicator=True)

# Set the index to "CD116FP" and drop the "_merge" column.
distr_contrib=distr_contrib.set_index(["CD116FP"])
distr_contrib=distr_contrib.drop(columns=["_merge"])

# Write the resulting data to the distr_contrib layer of the co.gpkg geopackage file. 
distr_contrib.to_file("co.gpkg",layer="distr_contrib",driver="GPKG")
