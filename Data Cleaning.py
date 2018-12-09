#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 23:10:37 2018

@author: mkonig and cdinh
"""

import re
import pandas as pd

with open('variable names.txt', 'r') as inFile:
	varNames = inFile.read()
	varComp = re.compile(r'--\s(\w+)')
	varMatch = varComp.findall(varNames)
	df = pd.read_csv('communities.csv',names = varMatch)


