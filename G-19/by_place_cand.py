# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 18:09:07 2021

@author: Suraj
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

contrib=pd.read_pickle("contrib_clean.pkl")
com_cand=pd.read_csv("com_cand_info.csv")

merged=contrib.merge(com_cand,on="CMTE_ID",validate="m:1",indicator=True)

print(merged["_merge"].value_counts())

merged=merged.drop(columns=["_merge"])

group_by_place_cand=merged.groupby(["STATE","zip","CAND_NAME"])
by_place_cand=group_by_place_cand["amt"].sum()
by_place_cand.to_csv("by_place_cand.csv")

mil=by_place_cand.sum(level=["STATE","CAND_NAME"])/1e6

by_cand=mil.sum(level="CAND_NAME")
top_cand=by_cand.sort_values()
top_cand=top_cand[-10:]
print(top_cand)

by_state=mil.sum(level="STATE")
top_state=by_state.sort_values()
top_state=top_state[-10:]
print(top_state)

fig,(ax1,ax2)=plt.subplots(1,2,dpi=300)
fig.suptitle("Top Candidates and States, Millions of Dollars")
top_cand.plot.barh(ax=ax1,fontsize=7)
ax1.set_ylabel("")
top_state.plot.barh(ax=ax2,fontsize=7)
ax2.set_xlabel("State")
fig.tight_layout()
fig.savefig('top.png')

reset=mil.reset_index()
keep_cand=reset["CAND_NAME"].isin(top_cand.index)
keep_state=reset["STATE"].isin(top_state.index)
keep=keep_cand &  keep_state
sub=reset[keep]

grouped=sub.groupby(["STATE","CAND_NAME"])
summed=grouped["amt"].sum()
grid=summed.unstack("STATE")

fig,ax1=plt.subplots(dpi=300)
fig.suptitle("Contributions in Millions")
sns.heatmap(grid,annot=True,fmt=".0f",ax=ax1)
ax1.set_xlabel("State")
ax1.set_ylabel("Candidate")
fig.tight_layout()
fig.savefig('heatmap.png')


