from libmne import Mne
import argparser
import atexit
import signal

class Daemon(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    mne = Mne()
    atexit.register(lambda: mne.load())


