#!/usr/bin/env python

"""RandomCount.py: Random count generator"""

import random

def random_number():
    t = random.random()
    if (t <= .5):
        return 1
    elif (t <= .75):
        return 2
    elif (t <= 90):
        return 3
    elif (t <= 95):
        return 4
    return 5


for x in range(0,100):
    print random_number()
