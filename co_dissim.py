# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:38:52 2021

@author: Suraj
"""
# The following script calculates the dissimilarity index values of each congressional district 
# in a state. 

import geopandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read in the distr_contrib layer of the co.gpkg file. Trim the result, set the
# index to "CD116FP" and rename the index to "Congressional District".

co_distr=geopandas.read_file("co.gpkg",layer="distr_contrib")
co_distr=co_distr.set_index("CD116FP")
co_distr=co_distr.drop(columns=["GEOID","MTFCC","FUNCSTAT","LSAD","CDSESSN","AWATER","NAMELSAD"])
co_distr.index.name="Congressional District"

#Read in the zip_pieces_contrib.csv file previously created and set the index 
# to the "zipcode" column and rename the "CD116FP" column to "Cong_Distr".

zip_pieces_contrib=pd.read_csv("zip_pieces_contrib.csv")
zip_pieces_contrib=zip_pieces_contrib.set_index("zipcode")
zip_pieces_contrib=zip_pieces_contrib.rename(columns={"CD116FP":"Cong_Distr"})

# Now calculate the dissimilarity index value for each congressional district.
# Use the zip pieces contributions in each district to calcuate the index. 
# Append each district's dissimilarity index value to an empty dictionarty. 

grouped=zip_pieces_contrib.groupby(["Cong_Distr"])
dict={}

for distrnum, group in grouped:
    print(distrnum)
    print(group)
    zip_d_share=group["DEM"]/group["DEM"].sum()
    zip_r_share=group["REP"]/group["REP"].sum()
    zip_dissim=0.5*((zip_d_share-zip_r_share).abs()).sum()
    dict[distrnum]=(zip_dissim)
    
# Transform the dictionary to a DataFrame, set its index to "Congressional District", 
# and rename the column "0" to "dissim". 

distr_dissim=pd.DataFrame.from_dict(dict,orient="index")
distr_dissim.index.name="Congressional District"
distr_dissim=distr_dissim.rename(columns={0:"dissim"})

#Calculate the average dissimilarity value across the state's congressional 
# districts, and modify the index's format to match the index format of the co_distr DataFrame.

dissim_avg=distr_dissim["dissim"].mean()
distr_dissim.index=distr_dissim.index.map("{:02}".format)

# In order to spatially draw the district dissimilarity index values in GIS, merge distr_dissim on co_distr.

dissim_gis=co_distr.merge(distr_dissim,on="Congressional District",how="outer",validate="1:1",indicator=True)

# Drop irrelevant columns and write the result to a new dissim.gpkg geopackage file. 

dissim_gis=dissim_gis.drop(columns=["STATEFP","ALAND","DEM","REP","total","d_share","_merge"])
dissim_gis.to_file("dissim.gpkg",driver="GPKG")

# Create a bar plot indicating each district's dissimilarity value as well as the state's average dissimilarity value. 

ax1=distr_dissim.plot(kind="bar")
ax1.axhline(dissim_avg,color="green",linewidth=3)
ax1.set_title("Dissimilarity of CO Congressional Districts")
ax1.set_ylabel("Dissimilarity")

# Save the plot to a png file.

ax1.get_figure().savefig('co_dissim.png')
