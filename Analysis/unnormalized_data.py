#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 01:08:53 2018

@author: chloedinh
"""

import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

with open('variblenamesunstandardized.txt', 'r') as inFile: 
    #var name is txt file with variable names
	varNames = inFile.read()
	varComp = re.compile(r'--\s(\w+)')
    #use regular expression to extract var names from string
	varMatch = varComp.findall(varNames)
	df = pd.read_csv('CommViolPredUnnormalizedData.txt',names = varMatch,na_values=['?'])



#remove columns with nans
df = df.dropna(axis='columns',thresh=1994)
df = df.dropna()
colsWNull = df.isnull().sum()[df.isnull().sum() !=0]