from random import randint
from datetime import datetime, timedelta
from os.path import expanduser, join, exists
from itertools import product
import pickle

class Mne(object):
    def __init__(self):
        self.pool = {}
        
    def add(self, action, years, months, days, hours, minutes):
        for ind in product(years, months, days, hours, minutes):
            time = datetime(*ind)
            if time > datetime.today():
                self.register(time, action)

    def process(self):
        for indi, indj in self.pool.iteritems():
            if datetime.today() > indi: 
                self.dispatch(indi, indj)

    def register(self, action, time):
        if time < datetime.today(): return
        actions = self.pool.setdefault(time, [])
        actions.append(action)

    def dispatch(self, time, actions):        
        for ind in actions[:]:
            ind(time)
        del self.pool[time]

    def load(self, filename):
        fd   = open(filename, 'r')
        pool = pickle.load(fd)
        fd.close()
        self.pool.update(pool)

    def save(self, filename):
        fd = open(self.filename, 'w')
        pickle.dump(self.pool, fd)
        fd.close()

class Dzen2(object):
    pass





