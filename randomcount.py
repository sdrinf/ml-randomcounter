#!/usr/bin/env python

"""RandomCount.py: Random count generator"""

import random

class RandomNumbers():
    """main class for storing random numbers, and their distributions"""

    def get_number(self):
        """prints a random number with given probability distribution"""
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

    def store_history(self, num):
        """stores a history of the last 100 numbers"""
        if (len(self.items) == 100):
            self.items.pop(0)
        self.items.append(num)

    def get_frequency(self):
        """returns the frequency percentages of numbers given the history"""
        freq = []
        for i in range(0,6):
            freq.append(0)
        for i in self.items:
            freq[i] += 1
        for i in range(0,6):
            freq[i] = (float(freq[i]) / len(self.items))*100
        return freq


    def get_number_store_history(self):
        """returns a random number with probability distribution, and stores it in history"""
        num = self.get_number()
        self.store_history(num)
        print num
        return num

    def __init__(self):
        self.items = []



r = RandomNumbers()
for i in range(0,20000):
    r.get_number_store_history()
print r.get_frequency()
