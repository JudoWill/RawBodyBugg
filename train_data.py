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
from scipy.optimize import fminbound, fmin, anneal, brute, fmin_tnc, leastsq
import numpy as np
from copy import deepcopy

def group_data(lines, windows):
    
    lines = list(lines)
    groups = []
    
    for bot, top in windows:
        groups.append([x for x in lines if x['EPOCH'] > bot and x['EPOCH'] < top])

    return groups

def mean(rows, key):
    return sum(x[key] for x in rows)/len(rows)

def integrate(rows, key):
    return np.trapz([x[key] for x in rows], x = [x['EPOCH'] for x in rows])

def calculate_features(group):
    #MOVTSKIN	MOVACCTR	MOVACCLO	MOVACCFW	MOVTCOV	MADACCTR	
    #MADACCLO	COMPGSR	PEDO3	PLATEAU	TRPEAKS	MOVTHETA	MADTHETA	
    #TCOUNT	LOGSWEEP	LCOUNT	T0CROSS	L0CROSS	PEDO3TOE	LOPEAKS	
    #MOVVBAT	MADACCFW	FCOUNT	F0CROSS	FWPEAKS	MOVGSR	EE
    allowed_features = set(['EE', 'MOVTSKIN', 'T0CROSS'])
    mods = (('max', lambda rows,key: max(x[key] for x in rows)),
            ('min', lambda rows,key: min(x[key] for x in rows)),
            ('mean', mean),
            ('int', integrate))
            
    res = {}
    for (name, fun), key in product(mods, allowed_features):
        res[name+'-'+key] = fun(group, key)
    return res


def process_data(in_list):
    
    for item in in_list:
        for key in item.keys():
            try:
                item[key] = int(item[key])
            except:
                item.pop(key)

    return in_list

def objfun(in_guess, training_data, calories, ret_cals = False):

    if ret_cals:
        return np.sum((np.sum(training_data*in_guess,1)-calories)**2)**(1/2)
    else:
        return np.sum(training_data*in_guess,1)-calories
        

def tmp_iter(groups):

    for x in groups:
        feats = calculate_features(x)
        for key, val in sorted(feats.items()):
            yield val
        yield 1


def multi_train(nfeats, calories, cutoff = 0.01):

    start = np.fromiter((0 for x in xrange(nfeats.shape[1])), np.float)
    minscore = objfun(start, nfeats, calories, ret_cals = True)
    skip = np.zeros(nfeats.shape[1], dtype = np.bool)
    miter = 0
    while miter < 100:
        miter += 1
        tstart = start[~skip]
        tfeats = nfeats[:,~skip]
        res = leastsq(objfun, tstart, args = (tfeats, calories))
        score = objfun(res[0], tfeats, calories, ret_cals = True)
        if score <= minscore:
            minscore = score
            minskip = deepcopy(skip)
            minres = res[0]
            skip |= res[0] < cutoff
        else:
            break

    return minres, minskip


def main(train_file, data_file):
    

    all_data = list(csv.DictReader(open(data_file), delimiter = '\t'))
    train_data = list(csv.DictReader(open(train_file), delimiter = '\t'))

    all_data = process_data(all_data)
    train_data = process_data(train_data)

    group_boundaries = [(x['Start-Time'], x['End-Time']) for x in train_data]
    groups = group_data(all_data, group_boundaries)

    nfeats = np.fromiter(tmp_iter(groups), np.float)
    nfeats = np.reshape(nfeats, (len(groups), -1))
    calories = np.fromiter((x['Calories'] for x in train_data), np.float)
    start = [0 for x in xrange(nfeats.shape[1])]
    bounds = [(-2,2) for x in xrange(nfeats.shape[1])]
    weights, skip = multi_train(nfeats, calories)
    print weights, skip

    #res = leastsq(objfun, start, args = (nfeats, calories))
    #print 'dine'
    #print res[0], res[1]
    #print objfun(res[0], nfeats, calories, ret_cals = True)

    

    
    


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="""A function for training results to match 
    between the BodyBugg website and the armband.""")
    
    parser.add_argument('--trainingFile', type = str, required = True)
    parser.add_argument('--dataFile', type = str, required = True)
    
    args = parser.parse_args()    
      
    main(args.trainingFile, args.dataFile)

