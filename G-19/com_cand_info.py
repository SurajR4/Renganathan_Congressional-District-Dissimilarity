# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 17:12:09 2021

@author: Suraj
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


contrib=pd.read_pickle("contrib_clean.pkl")
com_total=pd.read_csv("com_total.csv")
com_info=pd.read_csv("committees.csv",dtype=str)

list= ["CMTE_ID","CMTE_NM","CMTE_PTY_AFFILIATION","CAND_ID"]
com_info=com_info[list]

com_merged=com_info.merge(com_total,how="right",validate="m:1",indicator=True)

print(com_merged["_merge"].value_counts())

com_merged=com_merged.drop(columns=["_merge"])

numcan=com_info.groupby("CMTE_ID").size()

print( numcan[ numcan>1 ] )

pres=pd.read_csv("candidates.csv",dtype=str)
is_pres=pres["CAND_OFFICE"]=="P"
is_2020=pres["CAND_ELECTION_YR"]=="2020"

keep=is_pres & is_2020
pres=pres[keep]
pres=pres.drop(columns=["CAND_OFFICE","CAND_ELECTION_YR"])

com_cand=com_merged.merge(pres,how="left",validate="m:1",indicator=True)
print(com_cand["_merge"].value_counts())
list=com_cand["_merge"]=="both"
com_cand=com_cand[list]
com_cand=com_cand.drop(columns=["_merge"])
com_cand.to_csv("com_cand_info.csv",index=False)

