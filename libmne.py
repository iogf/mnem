from random import randint
from datetime import datetime, timedelta
from os.path import expanduser, join, exists
from itertools import product
from re import search
import pickle

class Mne(object):
    def __init__(self, filename, show):
        self.filename = filename
        self.pool     = {}
        self.show     = show

        try:
            self.load(self.filename)
        except IOError:
            pass

    def add(self, msg, years, months, days, hours, minutes):
        for ind in product(years, months, days, hours, minutes):
            time = datetime(*map(int, ind))
            if time > datetime.today():
                self.register(msg, time)
        self.save()

    def remove(self, regex):
        for indi, indj in self.pool.iteritems():
            for indz in indj[:]:
                if search(regex, indz):
                    indj.remove(indz)
        self.save()

    def find(self, regex):
        for indi, indj in self.pool.iteritems():
            for indz in indj:
                if search(regex, indz):
                    yield indi, indz

    def process(self):
        for indi, indj in self.pool.items():
            if datetime.today() > indi: 
                self.dispatch(indj, indi)

    def register(self, msg, time):
        if time < datetime.today(): return
        msgs = self.pool.setdefault(time, [])
        msgs.append(msg)

    def dispatch(self, msgs, time):        
        for ind in msgs[:]:
            self.show(ind, time)
        del self.pool[time]
        self.save()

    def load(self, filename):
        fd   = open(filename, 'r')
        pool = pickle.load(fd)
        fd.close()
        self.pool.update(pool)

    def save(self):
        fd = open(self.filename, 'w')
        pickle.dump(self.pool, fd)
        fd.close()




