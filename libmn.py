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

        self.conn.execute(''' CREATE TABLE IF NOT EXISTS REGCMD
        (CMD TEXT, MSG TEXT); ''')

        self.conn.execute(''' CREATE TABLE IF NOT EXISTS DATETIME
        (TIME INT, YEAR INT, MONTH INT, DAY INT, HOUR INT, MINUTE INT, 
        REGCMD_ID INT, FOREIGN KEY(REGCMD_ID) REFERENCES REGCMD(ROWID)
        ON DELETE CASCADE); ''')

        self.conn.execute(''' create trigger 
        if not exists clean after delete on datetime
        when (select count(*) from datetime where regcmd_id = OLD.regcmd_id) = 0
        
        begin
        delete from regcmd where rowid = OLD.regcmd_id;
        end;''')

        self.conn.commit()

    def add_note(self, cmd, msg, dates):
        query0 = ''' INSERT INTO REGCMD (CMD, MSG) 
        VALUES ('{cmd}', '{msg}'); '''

        cursor = self.conn.execute(query0.format(cmd=cmd, msg=msg))
        self.conn.commit()

        for ind in dates:
            self.mk_qdate(ind, cursor.lastrowid)
        self.conn.commit()

    def mk_qdate(self, date, regcmd_id):
        query = ''' INSERT INTO DATETIME 
        (TIME, YEAR, MONTH, DAY, HOUR, MINUTE, REGCMD_ID) 
        VALUES %s ; '''

        tval = time.mktime(datetime(*date, second=0).timetuple())
        query = query % str((tval, ) + date + (regcmd_id, ))
        self.conn.execute(query)

    def exp_dates(self, years, months, days, hours, minutes):
        months  = months if months else range(1, 12)
        hours   = hours if  hours else range(1, 24) 
        minutes = minutes if minutes else range(1, 12) 

        if bool(days) is True :
            return product(years, months, days, hours, minutes)
        else:
            return self.date_range(years, months, hours, minutes)

    def date_range(self, years, months, hours, minutes):
        dates = product(years, months)
        for year, month in dates:
            yield from product((year,), (month,), range(1, 
                monthrange(year, month)[1]), hours, minutes) 

    def del_note(self, regex):
        pass

    def find(self, msg, years, months, days, hours, minutes):
        query = '''SELECT DISTINCT CMD, TIME FROM REGCMD INNER JOIN DATETIME ON
        REGCMD.ROWID = DATETIME.REGCMD_ID AND {cond}
        '''

        years = ', '.join((str(ind) for ind in years))
        months = ', '.join((str(ind) for ind in months))
        days = ', '.join((str(ind) for ind in days))
        hours = ', '.join((str(ind) for ind in hours))
        minutes = ', '.join((str(ind) for ind in minutes))

        cond0 = ('DATETIME.YEAR IN (%s)' % years) if years else ''
        cond1 = ('DATETIME.MONTH IN (%s)' % months) if months else ''
        cond2 = ('DATETIME.DAY IN (%s)' % days) if days else ''
        cond3 = ('DATETIME.HOUR IN (%s)' % hours) if hours else ''
        cond4 = ('DATETIME.MINUTE IN (%s)' % minutes) if minutes else ''
        cond5 = "REGCMD.MSG LIKE '%{msg}%'".format(msg = (msg if msg else ''))

        conds = (ind for ind in (cond0, cond1, 
        cond2, cond3, cond4, cond5) if ind)

        query = query.format(cond=' AND '.join(conds))
        print('Query:', query)
        cursor  = self.conn.execute(query)
        records = cursor.fetchall()
        return records

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

