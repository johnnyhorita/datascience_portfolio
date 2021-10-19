#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'stdDev' function below.
#
# The function accepts INTEGER_ARRAY arr as parameter.
#

def stdDev(arr):
    # Print your answers to 1 decimal place within this function
    larr = len(arr)
    m = sum(arr)/larr
    lst = list()
    
    for e in arr:
        item = (e-m)**2
        lst.append(item)
    
    print(round(math.sqrt(sum(lst)/larr),1))
    return

if __name__ == '__main__':
    n = int(input().strip())

    vals = list(map(int, input().rstrip().split()))

    stdDev(vals)