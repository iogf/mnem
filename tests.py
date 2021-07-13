from libmn import Mnem
from os.path import join, expanduser
from datetime import datetime, timedelta
import unittest
# from unittest import mock
import sqlite3
import time

class TestMnem(unittest.TestCase):
    def setUp(self):
        self.mnem  = Mnem(join(expanduser('~'), 
        'mnem-tests.db'), self.handle_display)

    def handle_display(self):
        pass

    def test0(self):
        """
        Test Mnem.expand_dates method.
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
        dates = self.mnem.expand_dates([2021], [7], [12], [13], [55])

        records = self.add_note('mnem Test -i 55', 'Test', dates)
        with mock.patch('__main__.time', 
            mock.MagicMock(return_value=12345)) as mocktime:

if __name__ == '__main__':
    unittest.main()