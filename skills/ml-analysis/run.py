#!/usr/bin/env python3
"""ml-analysis: full chain on water_treatment.csv -> branded HTML report.
Modes: honest | flawed | variant. Offline; see SKILL.md."""
import argparse, json, numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
TARGET='DBO-S'; FEATS=['Q-E','PH-E','DBO-E','DQO-E','SS-E','SED-E','COND-E']
ap=argparse.ArgumentParser(); ap.add_argument('--mode',default='honest',choices=['honest','flawed','variant'])
a=ap.parse_args()
df=pd.read_csv('water_treatment.csv').dropna(subset=[TARGET])
X=df[FEATS].copy(); y=df[TARGET].values
if a.mode=='variant': X['load']=(df['DBO-E'].fillna(df['DBO-E'].median())/190)*(df['SS-E'].fillna(df['SS-E'].median())/220)
if a.mode=='flawed':  X['DQO-S_leak']=df['DQO-S'].fillna(df['DQO-S'].median())
if a.mode=='flawed':
    Xtr,Xte,ytr,yte=train_test_split(X.fillna(X.median()),y,test_size=.2,random_state=0); split='random shuffle (WRONG for time series)'
else:
    k=int(len(df)*.8); Xi=X.fillna(X.iloc[:k].median())
    Xtr,Xte,ytr,yte=Xi.iloc[:k],Xi.iloc[k:],y[:k],y[k:]; split='time-aware (last 20% of days)'
m=LinearRegression().fit(Xtr,ytr); p=m.predict(Xte)
res=dict(mode=a.mode,split=split,mae=round(mean_absolute_error(yte,p),2),
         r2=round(r2_score(yte,p),3),base=round(mean_absolute_error(yte,np.full_like(yte,ytr.mean())),2))
print(json.dumps(res,indent=1))
print('For the styled report, see the precomputed ml_report_%s.html (regenerate off-stage only).'%a.mode)
