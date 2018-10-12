#
# week3
# COMP450Lab
#
# Created by Nehir Poyraz on 12.10.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.

import random
import numpy as np
from scipy import stats
class Coin(object):
    def __init__(self, pofh=0.5):
        self.face = ['H', 'T']
        self.prob = [pofh, 1 - pofh]

    def toss(self):
        global hcount, tcount
        r = random.random()
        if r >= self.prob[0]:
            #print("Heads", r)
            hcount += 1
            return self.face[0]
        else:
            #print("Tails", r)
            tcount += 1
            return self.face[1]



def start(number):
    result = []
    coin = Coin()
    global hcount, tcount
    hcount, tcount = 0, 0
    for i in range(number):
        result.append(coin.toss())
    print(result)

if __name__ == '__main__':
    count = 10000
    start(count)
    pofh = hcount / count

    poft = 1 - pofh
    pos = stats.binom_test(tcount, count)

    print("Number of HEADS:", hcount, "\tProbability", pofh)
    print("Number of TAILS:", tcount, "\tProbability", poft)
    print("\nFairness:", pos)




