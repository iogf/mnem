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


        self.conn.execute('''CREATE TABLE IF NOT EXISTS REGCMD
        (CMD TEXT, MSG TEXT);''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS DATETIME
        (TIME INT, REGCMD_ID INT, 
        FOREIGN KEY(REGCMD_ID) REFERENCES REGCMD(ROWID)
        ON DELETE CASCADE);''')

        self.conn.commit()

    def add_note(self, cmd, msg, years, months, days, hours, minutes):
        # months  = xrange(1, 12) if not months else months
        # hours   = xrange(1, 24) if not hours else hours
        # minutes = xrange(1, 12) if not minutes else minutes
        # days = range(1, monthrange(years, months)[1]) 

        dates  = product(years, months, days, hours, minutes)
        query0 = '''INSERT INTO REGCMD (CMD, MSG) 
        VALUES ('{cmd}', '{msg}');'''

        cursor = self.conn.execute(query0.format(cmd=cmd, msg=msg))
        self.conn.commit()
        query1 = '''INSERT INTO DATETIME (TIME, REGCMD_ID) 
        VALUES ({time}, {regcmd_id});'''

        for ind in dates:
            tval = time.mktime(datetime(year=ind[0], month=ind[1], 
                day=ind[2], hour=ind[3], minute=ind[4], second=0).timetuple())
            self.conn.execute(query1.format(time=tval, regcmd_id=cursor.lastrowid))
        self.conn.commit()

    def del_note(self, regex):
        pass

    def find(self, regex):
        pass

    def process(self):
        now = datetime.now()
        query0 = '''SELECT MSG, DATETIME.ROWID FROM REGCMD INNER JOIN DATETIME
        ON DATETIME.TIME <= {time} AND REGCMD.ROWID = DATETIME.REGCMD_ID;
        '''

        tval = time.mktime(datetime(year=now.year, month=now.month, 
        day=now.day, hour=now.hour, minute=now.minute).timetuple())
        query0  = query0.format(time=tval)
        cursor  = self.conn.execute(query0)
        records = cursor.fetchall()

        for ind in records:
            self.display_and_update(ind)
        print(records)

    def display_and_update(self, record):
        query0 = 'DELETE FROM DATETIME WHERE ROWID <= {rowid};'
        dzen = Dzen2()
        dzen(record[0])
        self.conn.execute(query0.format(rowid=record[1]))
        self.conn.commit()

    def mainloop(self):
        while True:
            time.sleep(5); self.process()

class Dzen2:
    def __call__(self, msg):
        lines = msg.count('\n') + 1
        cmd   = "echo '%s' | dzen2 -p -bg %s -fg %s -l %s -fn %s" % \
                (msg, self.background, self.foreground, lines, self.font)     
        call(cmd, shell=True)

    def __init__(self, background='yellow', foreground='black', font='fixed'):
        self.background = background
        self.foreground = foreground
        self.font       = font

