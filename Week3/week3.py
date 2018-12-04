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

            return self.face[0]
        else:
            #print("Tails", r)

            return self.face[1]



def start(number):

    coin = Coin()
    global hcount
    global tcount
    global hhcount
    global htcount
    global ttcount
    global thcount
    hcount, tcount = 0, 0
    hhcount, htcount, ttcount, thcount = 0, 0, 0, 0
    """result = []
    for i in range(number):
        result.append(coin.toss())
    print(result)"""

    global probhgivent, probtgivenh, probhgivenh, probtgivent
    global probhgiventh, probhgiventt, probhgivenhh, probhgivenht, probtgivenhh, probtgiventh, probtgivenht, probtgiventt
    probhgivent, probtgivenh, probhgivenh, probtgivent = 0, 0, 0, 0
    probhgiventh, probhgiventt, probhgivenhh, probhgivenht = 0, 0, 0, 0
    probtgivenhh, probtgiventh, probtgivenht, probtgiventt = 0, 0, 0, 0

    prev = ''
    prev2 = ''
    for i in range(number):
        toss = dataset[i]
        if toss == 'H':
            hcount += 1
            if prev == 'H':
                probhgivenh += 1
                if prev2 == 'H':
                    hhcount += 1
                    probhgivenhh += 1
                elif prev2 == 'T':
                    htcount += 1
                    probhgivenht += 1

            elif prev == 'T':
                probhgivent += 1
                if prev2 == 'H':
                    thcount += 1
                    probhgiventh += 1
                elif prev2 == 'T':
                    ttcount += 1
                    probhgiventt += 1


        elif toss == 'T':
            tcount += 1
            if prev == 'H':
                probtgivenh += 1
                if prev2 == 'H':
                    hhcount += 1
                    probtgivenhh += 1
                elif prev2 == 'T':
                    htcount += 1
                    probtgivenht += 1
            elif prev == 'T':
                probtgivent += 1
                if prev2 == 'H':
                    thcount += 1
                    probtgiventh += 1
                elif prev2 == 'T':
                    ttcount += 1
                    probtgiventt += 1
        prev2 = prev
        prev = toss





    global pofheads
    global poftails
    pofheads = hcount / count

    poftails = 1 - pofheads
    pos = stats.binom_test(tcount, count)

    print("Number of HEADS:", hcount, "\tProbability", pofheads)
    print("Number of TAILS:", tcount, "\tProbability", poftails)
    print("\nFairness:", pos)
    probhgivent = probhgivent / hcount
    probhgivenh = probhgivenh / hcount
    probtgivent = probtgivent / tcount
    probtgivenh = probtgivenh / tcount

    probhgivenhh = probhgivenhh / hcount
    probhgivenht = probhgivenht / hcount
    probhgiventt = probhgivenhh / hcount
    probhgiventh = probhgiventh / hcount

    probtgivenhh = probtgivenhh / tcount
    probtgivenht = probtgivenht / tcount
    probtgivenhh = probtgivenhh / tcount
    probtgiventh = probtgiventh / tcount

    #print("P(H|T):", probhgivent)
    #print("P(H|H):", probhgivenh)
    #print("P(T|T):", probtgivent)
    #print("P(T|H):", probtgivenh)
    print("P(H|TT)", probhgiventt)
    print("P(H|TH)", probhgiventh)
    print("P(T|HH)", probtgivenhh)

    bayestest(probtgivenh, probhgivent, poftails, pofheads)
    bayestest(probhgivent, probtgivenh, pofheads, poftails)
    bayestest(probtgivent, probtgivent, poftails, poftails)
    bayestest(probhgivenh, probhgivenh, pofheads, pofheads)
    bayestest(probhgiventt, probtgiventh, probtgivenh, poftails)
    bayestest(probhgiventh, probtgivenhh, probhgivenh, poftails)
    bayestest(probtgivenhh, probhgiventh, probtgivenh, pofheads)


def bayestest(posterior, likelihood, prior, mlikelihood):
    calcpost = likelihood * prior / mlikelihood

    if round(posterior, 2) == round(calcpost, 2):
        print("Bayes rule checks")
        print("Posterior", posterior, "is equal to calculated posterior", calcpost)
    else:
        print("Posterior", posterior, "is different from the calculated posterior", calcpost)




if __name__ == '__main__':
    dataset = []
    for i in range(3000):
        for j in range(5):
            dataset.append('H')
        for k in range(5):
            dataset.append('T')
    print(dataset)
    count = len(dataset)
    start(count)

