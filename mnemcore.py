from datetime import datetime, timedelta
from subprocess import call
from itertools import product
from re import search
from lockfile import LockFile
from calendar import monthrange
import pickle
import time
import os

class Mnem(object):
    def __init__(self, filename, handle=lambda *args: None):
        self.filename = filename
        self.pool     = {}
        self.handle   = handle

        if not os.path.exists(self.filename):
            self.create_db()

        self.lock = LockFile(self.filename)

    def add(self, msg, years, months, days, hours, minutes):
        months  = xrange(1, 12) if not months else months
        hours   = xrange(1, 24) if not hours else hours
        minutes = xrange(1, 12) if not minutes else minutes
        prod    = product(years, months, hours, minutes)

        for indi in prod:
            for indj in self.get_days_range(indi[0], indi[1], days):
                time = datetime(int(indi[0]), int(indi[1]), 
                int(indj) ,int(indi[2]), int(indi[3]))
                if time > datetime.today():
                    self.register(msg, time)
        self.save()

    def get_days_range(self, year, month, days):
        return xrange(1, monthrange(
        year, month)[1]) if not days else days

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
            self.handle(ind, time)
        del self.pool[time]
        self.save()

    def load(self):
        self.lock.acquire()
        fd   = open(self.filename, 'r')
        pool = pickle.load(fd)
        fd.close()
        self.pool.update(pool)
        self.lock.release()

    def mainloop(self):
        while True:
            time.sleep(5); self.process()

    def save(self):
        self.lock.acquire()
        self.create_db()
        self.lock.release()

    def create_db(self):
        """
        Dump into a file the contents of pool. This
        method is not using a file lock.
        """

        fd = open(self.filename, 'w')
        pickle.dump(self.pool, fd)
        fd.close()

class Dzen2(object):
    def __call__(self, msg, time):
        lines = msg.count('\n') + 1
        cmd   = "echo '%s' | dzen2 -p -bg %s -fg %s -l %s -fn %s" % \
                (msg, self.background, self.foreground, lines, self.font)     
        call(cmd, shell=True)

    def __init__(self, background='yellow', foreground='black', font='fixed'):
        self.background = background
        self.foreground = foreground
        self.font       = font





