#!/usr/bin/env python

"""RandomCount.py: Random count generator"""

import random
import datetime
import Queue
import threading
import time


class LogWriter():
    """reads the most recently generated random number and the current time and writes them both to disk on one line"""
    """runs in a different thread; consumes logs via a priority queue to ensure chronological order"""

    def workerlog(self):
        """main queue processing worker"""
        lastnum = datetime.datetime(1900,1,1)
        while True:
            item = self.queue.get()
            (timestamp, num) = item
            # testing for strictly incremental chronological order
            if (lastnum > timestamp):
                print "Items written in non-chronological order"
                print lastnum, timestamp
            lastnum = timestamp
            with open("logfile.txt", "a") as logfile:
                logfile.write("Log at "+timestamp.__str__()+" :"+num.__str__()+"\n" )
            self.queue.task_done()
        return True

    def enqueue(self, timestamp, num):
        """queues up a new item"""
        # order is provided by PriorityQueue, which is thread-aware
        self.queue.put( (timestamp, num) )

    def wait_for_worker_finish(self):
        """returns when the worker has finished with all the tasks"""
        print "waiting for items:"+self.queue.qsize().__str__()
        self.queue.join()
        return True

    def __init__(self):
        self.queue = Queue.PriorityQueue()
        self.thread = threading.Thread(target=self.workerlog)
        self.thread.daemon = True
        self.thread.start()

log = LogWriter()

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
        """returns a random number with probability distribution, stores it in history, and writes it to log"""
        num = self.get_number()
        self.store_history(num)
        return num

    def __init__(self):
        self.items = []

class RandomNumberGenerator():
    """Dedicates thread for random number generation"""

    def stop_generator(self):
        self.running = False

    def generator(self):
        while (self.running):
            num = self.numgenerator.get_number_store_history()
            log.enqueue(datetime.datetime.now(), num)

    def __init__(self):
        self.numgenerator = RandomNumbers()
        self.running = True
        self.thread = threading.Thread(target=self.generator)
        self.thread.daemon = True
        self.thread.start()


allthreads = []
for i in range(0,5):
    allthreads.append(RandomNumberGenerator())
while True:
    log.wait_for_worker_finish()

