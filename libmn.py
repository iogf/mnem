from datetime import datetime, timedelta
from subprocess import call
from itertools import product
from calendar import monthrange
import sqlite3
import time
import os

class Mnem:
    def __init__(self, dbpath, handle=lambda *args: None):
        self.dbpath = dbpath
        self.handle = handle
        self.conn   = sqlite3.connect(dbpath)

        self.conn.execute('''CREATE TABLE IF NOT EXISTS DATETIME
        (MSG       TEXT,
        TIME      INT);
        ''')
        self.conn.commit()

    def add_note(self, msg, years, months, days, hours, minutes):
        dates = product([msg], years, months, days, hours, minutes)

        query = '''INSERT INTO DATETIME (MSG, TIME) 
        VALUES ('{msg}', {time});'''

        for ind in dates:
            tval = time.mktime(datetime(year=ind[1], month=ind[2], 
                day=ind[3], hour=ind[4], minute=ind[5], second=0).timetuple())
            self.conn.execute(query.format(msg=ind[0], time=tval))
        self.conn.commit()

    def del_note(self, regex):
        pass

    def find(self, regex):
        pass

    def process(self):
        now = datetime.now()
        query0 = '''SELECT MSG FROM DATETIME 
        WHERE TIME <= {time};
        '''
        tval = time.mktime(datetime(year=now.year, month=now.month, 
        day=now.day, hour=now.hour, minute=now.minute).timetuple())
        query0  = query0.format(time=tval)
        cursor  = self.conn.execute(query0)
        records = cursor.fetchall()

        for ind in records:
            Dzen2()(ind[0], str(now))

        query1 = 'DELETE FROM DATETIME WHERE TIME <= {time};'
        cursor.execute(query1.format(time=tval))
        self.conn.commit()
        print(records)

    def mainloop(self):
        while True:
            time.sleep(5); self.process()

class Dzen2:
    def __call__(self, msg, time):
        lines = msg.count('\n') + 1
        cmd   = "echo '%s' | dzen2 -p -bg %s -fg %s -l %s -fn %s" % \
                (msg, self.background, self.foreground, lines, self.font)     
        call(cmd, shell=True)

    def __init__(self, background='yellow', foreground='black', font='fixed'):
        self.background = background
        self.foreground = foreground
        self.font       = font

