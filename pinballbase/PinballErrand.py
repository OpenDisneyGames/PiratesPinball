# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: PinballErrand.py
from direct.directnotify import DirectNotifyGlobal

class PinballErrand:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballErrand')

    def __init__(self, board):
        self.board = board
        self.seenTutorial = False

    def finishSetup(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement finishSetup')

    def changeToZone(self, newZone, oldZone):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement changeToZone')

    def reset(self, time=3):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement reset')

    def refresh(self, time=3):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement refresh')

    def tutorial(self, interactiveMode=True):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement tutorial')

    def continueOn(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement continueOn')

    def skip(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement skip')

    def start(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement start')

    def nextBall(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement nextBall')

    def pause(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement pause')

    def resume(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement resume')

    def wake(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement wake')

    def sleep(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement sleep')

    def destroy(self):
        del self.board
        self.notify.debug(self.getName() + ' calling destroy just fine.')

    def getStatus(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement getStatus')

    def getName(self):
        self.notify.debug('You should implement getName')

    def getBonus(self):
        self.notify.debug(self.getName())
        self.notify.debug('You should implement getBonus')

    def __str__(self):
        return self.getStatus()

    def __repr__(self):
        return self.getStatus()