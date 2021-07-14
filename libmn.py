from datetime import datetime, timedelta
from subprocess import call
from itertools import product
from calendar import monthrange
import sqlite3
from time import mktime, time, sleep
import os

class Mnem:
    def __init__(self, dbpath, handle=lambda *args: None):
        self.dbpath = dbpath
        self.handle = handle
        self.conn   = sqlite3.connect(dbpath)
        self.conn.execute(''' CREATE TABLE IF NOT EXISTS REGCMD
        (CMD TEXT, MSG TEXT); ''')

        self.conn.execute(''' CREATE TABLE IF NOT EXISTS DATETIME
        (TIME INT, YEAR INT, MONTH INT, DAY INT, HOUR INT, MINUTE INT, 
        REGCMD_ID INT, FOREIGN KEY(REGCMD_ID) REFERENCES REGCMD(ROWID)
        ON DELETE CASCADE); ''')

        self.conn.execute(''' CREATE TRIGGER 
        IF NOT EXISTS CLEAN AFTER DELETE ON DATETIME
        WHEN (SELECT COUNT(*) FROM DATETIME WHERE REGCMD_ID = OLD.REGCMD_ID) = 0
        BEGIN
        DELETE FROM REGCMD WHERE ROWID = OLD.REGCMD_ID;
        END;''')

        self.conn.commit()

    def add_note(self, cmd, msg, dates):
        dates = [(date, mktime(datetime(*date, 
        second=0).timetuple())) for date in dates]

        for ind in range(0, len(dates)):
            if dates[ind][1] < time():
                del dates[ind]
        else:
            if bool(dates) is False: 
                return dates

        query0 = ''' INSERT INTO REGCMD (CMD, MSG) 
        VALUES (?, ?); '''

        cursor = self.conn.execute(query0, (cmd, msg))
        self.conn.commit()

        query1 = ''' INSERT INTO DATETIME 
        (TIME, YEAR, MONTH, DAY, HOUR, MINUTE, REGCMD_ID) 
        VALUES  (?, ?, ?, ?, ?, ?, ?) ; '''

        for date, tval in dates:
            self.conn.execute(query1, 
                ((tval, ) + date + (cursor.lastrowid, )))
        self.conn.commit()
        return dates

    def expand_dates(self, years, months, days, hours, minutes):
        months  = months if months else range(1, 13)
        hours   = hours if  hours else range(0, 24) 
        minutes = minutes if minutes else range(0, 59) 

        if bool(days) is True :
            return product(years, months, days, hours, minutes)
        else:
            return self.date_range(years, months, hours, minutes)

    def date_range(self, years, months, hours, minutes):
        dates = product(years, months)
        for year, month in dates:
            yield from product((year,), (month,), range(1, 
                monthrange(year, month)[1] + 1), hours, minutes) 

    def del_notes(self, ids):
        query = 'DELETE FROM REGCMD WHERE ROWID IN {rowids};'
        ids = '(%s)' % ', '.join((str(ind) for ind in ids))

        query = query.format(rowids=ids)
        print(query)
        self.conn.execute(query)
        self.conn.commit()

    def find(self, msg, years, months, days, hours, minutes, index):
        query = '''SELECT DISTINCT CMD, TIME, REGCMD_ID FROM REGCMD 
        INNER JOIN DATETIME ON REGCMD.ROWID = DATETIME.REGCMD_ID AND {cond}
        '''

        years = ', '.join((str(ind) for ind in years))
        months = ', '.join((str(ind) for ind in months))
        days = ', '.join((str(ind) for ind in days))
        hours = ', '.join((str(ind) for ind in hours))
        minutes = ', '.join((str(ind) for ind in minutes))
        index = ', '.join((str(ind) for ind in index))

        cond0 = ('DATETIME.YEAR IN (%s)' % years) if years else ''
        cond1 = ('DATETIME.MONTH IN (%s)' % months) if months else ''
        cond2 = ('DATETIME.DAY IN (%s)' % days) if days else ''
        cond3 = ('DATETIME.HOUR IN (%s)' % hours) if hours else ''
        cond4 = ('DATETIME.MINUTE IN (%s)' % minutes) if minutes else ''
        cond4 = ('DATETIME.REGCMD_ID IN (%s)' % index) if index else ''

        cond5 = "REGCMD.MSG LIKE '%{msg}%'".format(msg = (msg if msg else ''))

        conds = (ind for ind in (cond0, cond1, 
        cond2, cond3, cond4, cond5) if ind)

        query = query.format(cond=' AND '.join(conds))
        print('Sql:', query)
        cursor  = self.conn.execute(query)
        records = cursor.fetchall()
        return records

    def process(self):
        # now = datetime.now()
        query0 = '''SELECT MSG, DATETIME.ROWID FROM REGCMD INNER JOIN DATETIME
        ON DATETIME.TIME <= {time} AND REGCMD.ROWID = DATETIME.REGCMD_ID;
        '''

        # tval = mktime(datetime(year=now.year, month=now.month, 
        # day=now.day, hour=now.hour, minute=now.minute).timetuple())
        tval    = time()
        query0  = query0.format(time=tval)
        cursor  = self.conn.execute(query0)
        records = cursor.fetchall()

        for ind in records:
            self.display_and_update(ind)

    def display_and_update(self, record):
        query0 = 'DELETE FROM DATETIME WHERE ROWID = ?;'
        self.handle(record[0])
        # dzen = Dzen2()
        # dzen(record[0])
        print('Msg:', record[1], 'Id:', record[0])
        self.conn.execute(query0, (record[1], ))
        self.conn.commit()

    def mainloop(self):
        while True:
            sleep(5); self.process()

    def reload_conn(self):
        self.conn.close()
        self.conn = sqlite3.connect(dbpath)

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

