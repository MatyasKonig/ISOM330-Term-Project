#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 23:10:37 2018

@author: mkonig and cdinh
"""

import re
import pandas as pd


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

#define threshold for dangerous cities that are in the .95 quantile 
dangerThreshold = df['ViolentCrimesPerPop'].quantile(.90)


df[df['ViolentCrimesPerPop'] >= dangerThreshold]

df.to_csv('cleaned_data.csv', index = False)