# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 18:59:15 2021

@author: Suraj
"""

import pandas as pd

# Read in the contrib_clean.pkl and com_cand_info.csv files from the G-19 
# folder found in the repository. 
# The first file lists contributions made to specific committees of U.S 
# Presidential candidates and their respective political party.
# The second file lists contributions to specific committees of U.S 
# Presidential candidates by zipcode.

contrib=pd.read_pickle("contrib_clean.pkl")
com_cand=pd.read_csv("com_cand_info.csv")

# Merge the two datasetss using a many-to-one inner join, based on their shared
# "CMTE_ID" column. 
# This will then list contributions made to a candidate or party on a zip code
# level in all U.S states.

merged=contrib.merge(com_cand,on="CMTE_ID",how="inner",validate="m:1")

# Rename the "CAND_PTY_AFFILIATION" column in the Data Frame to a more conscise
# name. 

merged=merged.rename(columns={"CAND_PTY_AFFILIATION":"party"})

# Use a query method to select the state of interest to analyze. In this 
#script, the zip code contributions in Colorado will be selected. 

co=merged.query("STATE=='CO'")

# Use the groupby method to group the "co" Data Frame based on the "zip" and 
#"party" columns. 

grouped=co.groupby(["zip","party"])

# Calculate the sum of contributions made to each political party in each zip 
#code.

amount=grouped["amt"].sum()

# Fill in a value of 0 where $0 contributions were made to a party.

amount=amount.where(amount>0,0)

# Unstack the "amount" Series so that one can clearly visualize the 
# contributions made to each party in a zip code. Fill in a 0 value when $0 in
# contributions were made to a party.  
 
wide=amount.unstack(level="party")
wide.fillna(0,inplace=True)

# Calculate the total amount of contributions made in each zip code, and 
# calculate the share of contributions made to Democrats. 
wide["total"]=wide.sum(axis="columns")
wide["d_share"]=wide["DEM"]/wide["total"]

# Write out the resulting data into a csv file.
wide.to_csv("CO_by_party.csv")
