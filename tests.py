from libmn import Mnem
from time import mktime, time, sleep
from os.path import join, expanduser
from datetime import datetime, timedelta
import unittest
from unittest import mock
import sqlite3

class TestMnem(unittest.TestCase):
    def setUp(self):
        self.mnem  = Mnem(join(expanduser('~'), 
        'mnem-tests.db'), self.handle)

    def handle(self, msg):
        print('Displaying:', msg)

    def test0(self):
        """
        Test Mnem.expand_dates method. Check whether it is expanding
        dates accordingly.
        """

        dates = self.mnem.expand_dates([1], [2], [3], [], [5])
        dates = list(dates)
        self.assertEqual(len(dates), 24)
        self.assertIn((1, 2, 3, 0, 5), dates)
        self.assertIn((1, 2, 3, 23, 5), dates)
        
        dates = self.mnem.expand_dates([1], [], [3], [], [5])
        dates = list(dates)
        self.assertEqual(len(dates), 12 * 24)
        self.assertIn((1, 1, 3, 0, 5), dates)
        self.assertIn((1, 12, 3, 23, 5), dates)

        dates = self.mnem.expand_dates([2021], [], [], [23], [5])
        dates = list(dates)
        self.assertEqual(len(dates), 365)
        self.assertIn((2021, 1, 3, 23, 5), dates)
        self.assertIn((2021, 2, 28, 23, 5), dates)

    def test1(self):
        """
        Test Mnem.add_note superficially. It fakes time in order
        to have registers created then it checks the DB structure to
        be according to what it is expexted.
        """
        dates = self.mnem.expand_dates([2021], [7], [12], [13], [55])
        tval = mktime(datetime(year=2021, month=7, 
        day=12, hour=13, minute=55).timetuple())
        mval = mock.MagicMock(return_value=tval)

        with mock.patch('libmn.time', mval) as mocktime:
            records0 = self.mnem.add_note('''mnem Test 
                    -y 2021 -m 7 -d 12 -u 13 -i 55''', 'Test', dates)

        self.assertTrue(len(records0), 1)
        query0 = """SELECT CMD, MSG FROM REGCMD 
        WHERE MSG LIKE '%Test%'"""

        cursor = self.mnem.conn.execute(query0)
        records1 = cursor.fetchall()
        self.assertTrue(len(records1), 1)
        query1 = 'SELECT * FROM DATETIME WHERE TIME = ?'

        cursor = self.mnem.conn.execute(query1, (tval,))

        records2 = cursor.fetchall()
        self.assertTrue(len(records1), 1)

        query2 = 'SELECT * FROM REGCMD WHERE ROWID = ?'

        cursor = self.mnem.conn.execute(query2, (records2[0][-1],))
        records3 = cursor.fetchall()
        self.assertTrue(len(records3), 1)

        with mock.patch('libmn.time', mval) as mocktime:
            self.mnem.process()
        query3 = 'SELECT * FROM REGCMD WHERE ROWID = ?'
        cursor = self.mnem.conn.execute(query3, (records2[0][-1],))

if __name__ == '__main__':
    unittest.main()