# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 13:05:26 2021

@author: Suraj
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

contrib=pd.read_csv("contrib_by_zip.csv",dtype=str)
contrib["amt"]=contrib["amt"].astype(float)

po=pd.read_csv("pocodes.csv")
po=po.drop(columns=["Name"])

contrib=contrib.merge(po,left_on="STATE",right_on="PO",how="outer",validate="m:1",indicator=True)
print(contrib["_merge"].value_counts())

state_bad=contrib["_merge"]!="both"
contrib=contrib.drop(columns=["PO","_merge"])

bad_recs = contrib[state_bad].groupby('STATE')
state_bad_amt=bad_recs["amt"].sum()
print("\n",state_bad_amt)
print("\n",state_bad_amt.sum())

contrib=contrib[state_bad==False]

num_zip=pd.to_numeric(contrib["zip"],errors="coerce")
zip_bad=num_zip.isna()

bad_recs=contrib[zip_bad].groupby("zip")
zip_bad_amt=bad_recs["amt"].sum()
print("\n",zip_bad_amt)
print("\n",zip_bad_amt.sum())


contrib=contrib[zip_bad==False]

contrib.to_pickle("contrib_clean.pkl")

by_com=contrib.groupby("CMTE_ID")
com_total=by_com["amt"].sum()
com_total.name = 'total_amt'

com_total.to_csv("com_total.csv")
