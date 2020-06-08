# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: StairCase.py
from pinballbase.PinballErrand import PinballErrand
from PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
from direct.interval.IntervalGlobal import LerpFunc
import Localizer

class StairCase(PinballErrand):
    __module__ = __name__

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.bonusGift = self.board.pointValues['SecretStaircaseBonus']
        self.myZone = 0
        self.inStairCase = False
        self.rollSoundPlaying = False
        self.rollSoundInt = None
        self.totalTimesDown = 0
        self.ballModeInStairs = 0
        return

    def finishSetup(self):
        pass

    def changeToZone(self, zoneNumber):
        pass

    def reset(self, time=3):
        self.inStairCase = False

    def refresh(self, time=3):
        pass

    def start(self, taskInstance=None):
        pass

    def pause(self):
        if self.rollSoundPlaying and self.rollSoundInt != None:
            self.rollSoundInt.pause()
        return

    def resume(self):
        if self.rollSoundPlaying and self.rollSoundInt != None:
            self.rollSoundInt.resume()
        return

    def sleep(self):
        if self.rollSoundInt != None and self.rollSoundPlaying:
            self.rollSoundInt.finish()
        return

    def destroy(self):
        if self.rollSoundInt != None and self.rollSoundPlaying:
            self.rollSoundInt.finish()
        PinballErrand.destroy(self)
        return

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        if self.inStairCase or self.board.currentZone == 1:
            return Localizer.ppStairCaseInIt
        else:
            return Localizer.ppStairCaseNotInIt
        return

    def getName(self):
        return 'StairCase'

    def getBonus(self):
        bonus = self.totalTimesDown
        self.totalTimesDown = 0
        return (Localizer.ppStairCaseBonus, bonus, self.bonusGift)

    def stairCaseIn(self, ballIndex, args):
        self.board.display.show(Localizer.ppStairCaseAchieved)
        self.board.updateScore(self.board.pointValues['SecretStaircase'], 'SecretStaircase')
        self.board.pirateSounds['StairCase_Found'].play()
        self.board.myTransition.fadeOut(1.5)
        self.board.musicMgr.playJingle('Music_Success2', musicContinue=True)
        for b in self.board.balls:
            if b.active:
                sgode.pyode.dBodyDisable(b.body)
                sgode.pyode.dGeomDisable(b.geom)

        sgode.pyode.dBodyEnable(self.board.balls[ballIndex].body)
        sgode.pyode.dGeomEnable(self.board.balls[ballIndex].geom)
        self.board.bumpManager.disable()

    def stairCaseOut(self, ballIndex, args):
        sgode.pyode.dBodyDisable(self.board.balls[ballIndex].body)

    def stairCaseRelease(self, ballIndex, args):
        self.totalTimesDown = self.totalTimesDown + 1
        self.board.boatModel.reparentTo(hidden)
        self.board.brigModel.reparentTo(render)
        base.setBackgroundColor(0, 0, 0)
        self.board.changeToZone(1)
        self.board.errands['BoneBrig'].showFlippers()
        self.board.waterEffects.turnOff()
        self.board.setCameraPosition('boneBrig')
        self.board.balls[ballIndex].setODEPos(self.board.proxPoints['BoneBrigAlleyTop'].getPos()[0], self.board.proxPoints['BoneBrigAlleyTop'].getPos()[1], 0.5)
        self.board.balls[ballIndex].setZone(1)
        sgode.pyode.dBodySetLinearVel(self.board.balls[ballIndex].body, 0, 0, 0)
        sgode.pyode.dGeomSetCollideBits(self.board.balls[ballIndex].geom, 4294967295 ^ DROPPED_CATEGORY)
        sgode.pyode.dBodyDisable(self.board.balls[ballIndex].body)
        self.board.balls[ballIndex].update()
        self.board.balls[ballIndex].reparentTo(render)
        sgode.pyode.dWorldSetGravity(self.board.odeWorld, 0, -10, -32)
        self.board.myTransition.fadeIn(1.5)

    def alleyTopIn(self, ballIndex, args):
        print 'entering bone brig alley with ball %d' % ballIndex

    def alleyTopTimer(self, ballIndex, args):
        sgode.pyode.dBodyEnable(self.board.balls[ballIndex].body)
        sgode.pyode.dGeomEnable(self.board.balls[ballIndex].geom)
        self.board.pirateSounds['StairCase_Wind'].play()
        self.rollSoundInt = SoundInterval(self.board.pirateSounds['StairCase_Roll'])
        self.rollSoundInt.start()
        self.rollSoundPlaying = True
        self.board.pirateSounds['StairCase_Roll'].setVolume(1)
        self.board.pirateSounds['StairCase_Wind'].setVolume(1)

    def alleyBottomIn(self, ballIndex, args):
        print 'exiting bonebrig alley'
        self.board.myTransition.fadeOut(1.5)
        self.board.pbTaskMgr.doMethodLater(1.5, self.resetFromBoneBrig, 'resetFromBoneBrig', [ballIndex])
        self.volDown = LerpFunc(self.changeRollVol, duration=1.0, fromData=1.0, toData=0.0)
        self.volDown.start()

    def changeRollVol(self, newVol):
        self.board.pirateSounds['StairCase_Roll'].setVolume(newVol)
        self.board.pirateSounds['StairCase_Wind'].setVolume(newVol)

    def resetFromBoneBrig(self, ballIndex):
        self.board.boatModel.reparentTo(render)
        self.board.brigModel.reparentTo(hidden)
        self.ballModeInStairs = self.board.deactivateBall(ballIndex)
        self.board.myTransition.fadeIn(1.5)
        self.board.setCameraPosition('main')
        self.board.waterEffects.turnOn()
        self.rollSoundPlaying = False
        base.setBackgroundColor(0.3, 0.3, 0.7)
        self.board.changeToZone(0)
        self.board.errands['BoneBrig'].hideFlippers()

    def alleyBottomTimer(self, ballIndex, args):
        self.board.errands['DeckHatches'].launchBallFromHatch(ballMode=self.ballModeInStairs)
        for b in self.board.balls:
            if b.active:
                sgode.pyode.dBodyEnable(b.body)
                sgode.pyode.dGeomEnable(b.geom)

        self.board.bumpManager.enable()