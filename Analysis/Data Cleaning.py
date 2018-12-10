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


df[df['ViolentCrimesPerPop'] >= dangerThreshold]

df.to_csv('cleaned_data.csv', index = False)

sns.pairplot(df)



stateAvgRace = df.groupby('state_abv')['ViolentCrimesPerPop', 'racepctblack', 'racePctWhite', 'racePctAsian', 'racePctHisp'].mean()
stateAvgRace = pd.DataFrame(stateAvgRace).reset_index()

def graph(xVar, yVar, title, xLabel, yLabel, imgName):
	tempData = df.groupby('state_abv')[xVar, yVar].mean()
	ax = sns.regplot(xVar, yVar, data = tempData)
	ax.set(title = title, xlabel = xLabel, ylabel = yLabel)
	plt.savefig(imgName + '.png', dpi = 300)
	plt.show()
	print(tempData.corr())

graph('ViolentCrimesPerPop', 'racepctblack', 'Violent Crimes per Pct of African American Population',
	'Violent Crimes Per Population', 'Percentage of Pop African American', 'crimeVSblackpctpop')

#create graph for racepct black versus violent crimes per pop
ax = sns.regplot('ViolentCrimesPerPop','racepctblack', data=df.groupby('state_abv')['ViolentCrimesPerPop', 'racepctblack'].mean())
ax.set(title = 'Violent Crimes per Pct of African American Population', xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop African American')
plt.savefig('crimeVSblackpctpop.png', dpi = 300)
plt.show()
df.groupby('state_abv')['ViolentCrimesPerPop', 'racepctblack'].mean().corr()

#create graph for racepct white versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','racePctWhite', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop White')
plt.savefig('crimeVSwhitepctpop.png', dpi = 300)

#create graph for racepct asian versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','racePctAsian', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Asian')
plt.savefig('crimeVSasianpctpop.png', dpi = 300)

#create graph for racepct Hisp versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','racePctHisp', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Hisp')
plt.savefig('crimeVShisppctpop.png', dpi = 300)

#create graph for racepct black versus violent crimes per pop
ax = sns.regplot('ViolentCrimesPerPop','racepctblack', data = df, line_kws={"color": "red"})
plt.show()
df.corr()
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop African American')
plt.savefig('crimeVSblackpctpop.png', dpi = 300)

#create graph for racepct white versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','racePctWhite', data = df)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop White')
plt.savefig('crimeVSwhitepctpop.png', dpi = 300)

#create graph for racepct asian versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','racePctAsian', data = df)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Asian')
plt.savefig('crimeVSasianpctpop.png', dpi = 300)

#create graph for racepct Hisp versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','racePctHisp', data = df)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Hisp')
plt.savefig('crimeVShisppctpop.png', dpi = 300)


stateAvgRace = df.groupby('state_abv')['ViolentCrimesPerPop', 'agePct12t21', 'agePct12t29', 'agePct16t24', 'agePct65up'].mean()
stateAvgRace = pd.DataFrame(stateAvgRace).reset_index()

#create graph for racepct black versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','agePct12t21', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop African American')
plt.savefig('crimeVSblackpctpop.png', dpi = 300)

#create graph for racepct white versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','agePct12t29', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop White')
plt.savefig('crimeVSwhitepctpop.png', dpi = 300)

#create graph for racepct asian versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','agePct16t24', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Asian')
plt.savefig('crimeVSasianpctpop.png', dpi = 300)

#create graph for racepct Hisp versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','agePct65up', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Hisp')
plt.savefig('crimeVShisppctpop.png', dpi = 300)

stateAvgRace = df.groupby('state_abv')['ViolentCrimesPerPop', 'NumInShelters', 'NumStreet', 'PctUnemployed', 'PctEmploy'].mean()
stateAvgRace = pd.DataFrame(stateAvgRace).reset_index()

#create graph for racepct black versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','NumInShelters', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop African American')
plt.savefig('crimeVSblackpctpop.png', dpi = 300)

#create graph for racepct white versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','NumStreet', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop White')
plt.savefig('crimeVSwhitepctpop.png', dpi = 300)

#create graph for racepct asian versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','PctUnemployed', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Asian')
plt.savefig('crimeVSasianpctpop.png', dpi = 300)

#create graph for racepct Hisp versus violent crimes per pop
ax = sns.scatterplot('ViolentCrimesPerPop','PctEmploy', data=stateAvgRace)
ax.set(xlabel='Violent Crimes Per Population', ylabel='Percentage of Pop Hisp')
plt.savefig('crimeVShisppctpop.png', dpi = 300)

ax = sns.scatterplot(data = df.groupby('state_abv')['population'].sum())

