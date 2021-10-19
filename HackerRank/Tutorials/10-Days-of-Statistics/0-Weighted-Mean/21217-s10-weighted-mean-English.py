#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'weightedMean' function below.
#
# The function accepts following parameters:
#  1. INTEGER_ARRAY X
#  2. INTEGER_ARRAY W
#

def weightedMean(X, W):
    # Write your code here
    # step-by-step
    #lst = list()
    #for i in range(len(X)):
    #    lst.append(X[i]*W[i])
    #lst = list(map(lambda x, y: x*y, X, W))
    #m = round(sum(lst)/sum(W),1)
    #print(m)

    print(round(sum(list(map(lambda x, y: x*y, X, W)))/sum(W),1))
    return

if __name__ == '__main__':
    n = int(input().strip())

    vals = list(map(int, input().rstrip().split()))

    weights = list(map(int, input().rstrip().split()))

    weightedMean(vals, weights)