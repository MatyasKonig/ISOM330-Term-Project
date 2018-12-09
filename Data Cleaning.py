#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 23:10:37 2018

@author: mkonig and cdinh
"""

import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

with open('variable names.txt', 'r') as inFile: 
    #var name is txt file with variable names
	varNames = inFile.read()
	varComp = re.compile(r'--\s(\w+)')
    #use regular expression to extract var names from string
	varMatch = varComp.findall(varNames)
	df = pd.read_csv('communities.csv',names = varMatch,na_values=['?'])


#remove columns with nans
df = df.dropna(axis='columns')

#import state code file
dfState = pd.read_csv('state.txt',sep='|',header=0)
#remove two unwanted columns
dfState = dfState.drop(['STATE_NAME','STATENS'],axis=1)
dfState.columns = ['state','state_abv']

df = pd.merge(df,dfState[['state','state_abv']],on='state',how='left')

#remove DC because it might be outlier/error
df = df.drop(1044)

#define threshold for dangerous cities that are in the .95 quantile 
dangerThreshold = df['ViolentCrimesPerPop'].quantile(.90)
df[df['ViolentCrimesPerPop'] >= dangerThreshold]


#get the state's avg crime rate 
stateAvgCrime = df.groupby('state_abv')['ViolentCrimesPerPop'].mean()
stateAvgCrime = pd.DataFrame(stateAvgCrime).reset_index()

#plot the state's avg crime
#fig, ax = plt.subplots(figsize=(18,4))
#sns.swarmplot(x='state_abv',y='ViolentCrimesPerPop',data=df)
sns.catplot('state_abv','ViolentCrimesPerPop',data=stateAvgCrime,
            kind='strip')

sns.pairplot(df)


stateAvgBlack = df.groupby('state_abv')['ViolentCrimesPerPop','racepctblack'].mean()
stateAvgBlack = pd.DataFrame(stateAvgBlack).reset_index()

#create graph for racepct black versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','racepctblack',data=stateAvgBlack)
ax.set(xlabel='Violent Crimes Per Population',ylabel='Percentage of Pop African American')
plt.savefig('crimeVSblackpctpop.png')