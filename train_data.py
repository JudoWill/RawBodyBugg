#!/usr/bin/env python
# encoding: utf-8
from __future__ import division
"""
train_data.py

Created by William Dampier on 2011-05-07.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import argparse
import csv
import numpy as np
from itertools import product

def group_data(lines, windows):
    
    lines = list(lines)
    groups = []
    
    for bot, top in windows:
        groups.append([x for x in lines if x['EPOCH'] > bot and x['EPOCH'] < top])

    return groups

def mean(rows, key):
    return sum(x[key] for x in rows)/len(rows)

def integrate(rows, key):
    
    return np.trapz((x[key] for x in rows), x = (x['EPOCH'] for x in rows))

def calculate_features(group):
    
    mods = (('max', lambda rows,key: max(x[key] for x in rows)),
            ('min', lambda rows,key: min(x[key] for x in rows)),
            ('mean', mean),
            ('int', integrate))
            
    res = {}
    for (name, fun), key in product(mods, group[0].keys()):
        res[name+'-'+key] = fun(group)
    return res

def main():
    pass


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="""A function for training results to match 
    between the BodyBugg website and the armband.""")
    
    parser.add_argument('--training-file', type = str, required = True)
    parser.add_argument('--data-file', type = str, required = True)
    
    
    
    
    main()

