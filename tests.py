from mnem import Mnem
import unittest
import sqlite3

class TestMnem(unittest.TestCase):
    def setUP(self):
        pass

    def test0(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test1(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()