# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: MultiBall.py
from pinballbase.PinballErrand import PinballErrand
from .PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
import Localizer

class MultiBall(PinballErrand):
    __module__ = __name__

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.bonusGift = self.board.pointValues['MultiBallBonus']
        self.myZone = 0
        self.multiBallMode = 0
        self.totalMultiBalls = 0

    def finishSetup(self):
        pass

    def changeToZone(self, zoneNumber):
        pass

    def reset(self, time=1):
        self.multiBallMode = 0

    def refresh(self, time=1):
        pass

    def onlyOneBall(self):
        self.multiBallMode = 0

    def start(self, permission=0):
        if permission == 0:
            return
        self.multiBallMode = permission
        self.board.musicMgr.playMusic('SkullBall')
        self.board.errands['DeckHatches'].hatchState = [
         1, 1, 1]
        if self.multiBallMode == 2:
            self.board.dialogueMgr.playDialogue('SuperSkullball')
            self.totalMultiBalls = self.totalMultiBalls + 3
            self.board.display.show(Localizer.ppMultiBallSuperSkullBall)
            self.board.pbTaskMgr.doMethodLater(0.7, self.board.errands['DeckHatches'].releaseBall, 'releaseBall1', [0, False, 1])
        else:
            self.board.dialogueMgr.playDialogue('SkullMultiball')
            self.board.display.show(Localizer.ppMultiBallSkullBall)
            self.totalMultiBalls = self.totalMultiBalls + 1
            self.board.pbTaskMgr.doMethodLater(0.7, self.board.errands['DeckHatches'].releaseBall, 'releaseBall1', [0, False, 0])
        self.board.pbTaskMgr.doMethodLater(0.8, self.board.errands['DeckHatches'].releaseBall, 'releaseBall2', [1, True, 1])
        self.board.pbTaskMgr.doMethodLater(0.9, self.board.errands['DeckHatches'].releaseBall, 'releaseBall3', [2, True, 1])
        self.board.errands['DeckHatches'].refresh(0.7)

    def morphBall(self, ballMode):
        for b in self.board.balls:
            if b.getBallMode != 1:
                b.setBallMode(1)
                self.board.pirateSounds['TopDeck_HelmThread'].play()

    def pause(self):
        pass

    def resume(self):
        pass

    def destroy(self):
        PinballErrand.destroy(self)

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        if self.multiBallMode == 0:
            return Localizer.ppMultiBallNotYet
        elif self.multiBallMode == 1:
            return Localizer.ppMultiBallDuring
        else:
            return Localizer.ppMultiBallDuringSuper
        return

    def getName(self):
        return 'Skull Ball'

    def getBonus(self):
        bonus = self.totalMultiBalls
        self.totalMultiBalls = 0
        return (Localizer.ppMultiBallBonus, bonus, self.bonusGift)