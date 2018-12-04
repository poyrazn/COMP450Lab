#
# week5
# COMP450Lab
#
# Created by Nehir Poyraz on 26.10.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.


import pandas as pd
import numpy as np


def probability(val, mean, var):

    p = (np.exp(-(((val-mean)**2)/(2*var))))/np.sqrt(2*np.pi*var)
    return p


female, male = 0, 1
data = pd.read_csv('dataset.csv')
mean = data.groupby('Person').mean().values
variance = data.groupby('Person').var().values

test = pd.read_csv('test_dataset.csv').values
count = 0
for sample in test:
    pmale, pfemale = 1, 1
    for i in range(1, len(sample)):
        pmale *= probability(sample[i], mean[male][i-1], variance[male][i-1])
        pfemale *= probability(sample[i], mean[female][i-1], variance[female][i-1])

    if pmale >= pfemale:
        person = 'male'
        print("Male with probability", pmale)
    else:
        person = 'female'
        print("Female with probability", pfemale)
    if sample[0] == person:
        count += 1

print("Accuracy:", count*100/len(test))
