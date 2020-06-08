from pinballbase.PinballErrand import PinballErrand
from .PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
import Localizer

class DeckHatches(PinballErrand):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DeckHatches')

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.bonusGift = self.board.pointValues['DeckHatchesBonus']
        self.myZone = 0
        self.hatchState = [0, 0, 0]
        self.letterNumber = 0
        self.ballInNotOut = [{}, {}, {}]
        self.totalLettersSpelled = 0
        self.okToRelease = True
        self.pirates = 'PIRATES'
        if Localizer.myLanguage == 'brazilian':
            self.board.beacons['PiratesE'] = Beacon(board.boatModel.find('**/eFlat'), 'piratepinball/art/main_ship/beacons/a.png', rate=1.7)
        else:
            self.board.beacons['PiratesE'] = Beacon(board.boatModel.find('**/eFlat'), 'piratepinball/art/main_ship/beacons/e.png', rate=1.7)
        self.board.beacons['PiratesP'] = Beacon(board.boatModel.find('**/pFlat'), 'piratepinball/art/main_ship/beacons/p.png', rate=1.7)
        self.board.beacons['PiratesI'] = Beacon(board.boatModel.find('**/iFlat'), 'piratepinball/art/main_ship/beacons/i.png', rate=1.75)
        self.board.beacons['PiratesR'] = Beacon(board.boatModel.find('**/rFlat'), 'piratepinball/art/main_ship/beacons/r.png', rate=1.8)
        self.board.beacons['PiratesA'] = Beacon(board.boatModel.find('**/aFlat'), 'piratepinball/art/main_ship/beacons/a.png', rate=1.85)
        self.board.beacons['PiratesT'] = Beacon(board.boatModel.find('**/tFlat'), 'piratepinball/art/main_ship/beacons/t.png', rate=1.65)
        self.board.beacons['PiratesS'] = Beacon(board.boatModel.find('**/sFlat'), 'piratepinball/art/main_ship/beacons/s.png', rate=1.75)
        self.board.beacons['HatchHole1'] = Beacon(board.boatModel.find('**/baconplates:pPlane31'), 'piratepinball/art/main_ship/beacons/hatchIcon.png')
        self.board.beacons['HatchHole2'] = Beacon(board.boatModel.find('**/baconplates:pPlane33'), 'piratepinball/art/main_ship/beacons/hatchIcon.png')
        self.board.beacons['HatchHole3'] = Beacon(board.boatModel.find('**/baconplates:pPlane32'), 'piratepinball/art/main_ship/beacons/hatchIcon.png')
        self.board.beacons['PiratesA'].plane.setBin('flat', 90)
        pos = self.board.beacons['PiratesA'].plane.getPos()
        self.board.beacons['PiratesA'].plane.setPos(pos[0] - 0.02, pos[1], pos[2] - 0.01)
        thelist = []
        for i in range(1, 6):
            thelist.append('piratepinball/art/main_ship/beacons/BoneFrontx%d.png' % i)

        self.board.beacons['Multiplier'] = Beacon(board.boatModel.find('**/BoneFrontx1'), 'piratepinball/art/main_ship/beacons/BoneFront.png', onTextureName=thelist)
        self.hatchCovers = []
        self.hatchCovers.append(board.boatModel.find('**/hatchDeck1'))
        self.hatchCovers.append(board.boatModel.find('**/hatchDeck2'))
        self.hatchCovers.append(board.boatModel.find('**/hatchDeck3'))

    def finishSetup(self):
        pass

    def changeToZone(self, zoneNumber):
        pass

    def reset(self, time=3):
        self.ballInNotOut = [{}, {}, {}]
        hatchMovement = Sequence(name='hatchMovement')
        hatchMove = []
        for y in range(1, 4):
            self.hatchState[y - 1] = 0
            self.board.proxPoints[('HatchHOLE%d' % y)].setActive(False)
            self.board.beacons[('HatchHole%d' % y)].setState(Beacon.OFF)
            self.board.boardObjects[('HatchDropA%d' % y)].drop()
            self.board.boardObjects[('HatchDropB%d' % y)].drop()
            hatchMove.append(self.hatchCovers[(y - 1)].hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeOut'))

        hatchMovement.append(Parallel(*hatchMove))
        hatchMovement.start()
        self.letterNumber = 0
        for i in range(0, 7):
            self.board.beacons[('Pirates%s' % self.pirates[i:i + 1])].setState(Beacon.OFF)

    def refresh(self, time=3, revampActive=0, refreshLetters=True):
        hatchMovement = Sequence(name='hatchMovement')
        hatchMove = []
        for y in range(1, 4):
            if self.hatchState[(y - 1)] == 0:
                if len(self.ballInNotOut[(y - 1)]) != 0:
                    self.board.pbTaskMgr.doMethodLater(0.2, self.refresh, 'refreshBlocked', [time, revampActive + 1])
                    self.notify.debug('\n-- Blocked by full hatch %d ' % y)
                else:
                    self.board.proxPoints[('HatchHOLE%d' % y)].setActive(False)
                    self.board.boardObjects[('HatchDropA%d' % y)].drop()
                    self.board.boardObjects[('HatchDropB%d' % y)].drop()
                    hatchMove.append(self.hatchCovers[(y - 1)].hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeOut'))
                    self.board.beacons[('HatchHole%d' % y)].setState(Beacon.OFF)
            else:
                self.board.proxPoints[('HatchHOLE%d' % y)].setActive(True)
                self.board.beacons[('HatchHole%d' % y)].setState(Beacon.BLINK)
                self.board.boardObjects[('HatchDropA%d' % y)].restore()
                self.board.boardObjects[('HatchDropB%d' % y)].restore()
                hatchMove.append(self.hatchCovers[(y - 1)].hprInterval(time, Point3(0.0, 0.0, -90.0), blendType='easeOut'))

        hatchMovement.append(Parallel(*hatchMove))
        hatchMovement.start()
        if refreshLetters:
            for i in range(0, 7):
                if i >= self.letterNumber:
                    self.board.beacons[('Pirates%s' % self.pirates[i:i + 1])].setState(Beacon.OFF)
                else:
                    self.board.beacons[('Pirates%s' % self.pirates[i:i + 1])].setState(Beacon.ON)

    def start(self, taskInstance=None):
        self.board.beacons['Multiplier'].setState(Beacon.ON)
        self.reset()
        whichHatch = random.randint(1, 3)
        self.hatchState[whichHatch - 1] = 1
        self.board.proxPoints[('HatchHOLE%d' % whichHatch)].setActive(True)
        self.board.beacons[('HatchHole%d' % whichHatch)].setState(Beacon.BLINK)
        self.board.boardObjects[('HatchDropA%d' % whichHatch)].restore()
        self.board.boardObjects[('HatchDropB%d' % whichHatch)].restore()
        hatchMovement = Sequence(name='hatchMovement')
        hatchMovement.append(self.hatchCovers[(whichHatch - 1)].hprInterval(1, Point3(0.0, 0.0, -90.0), blendType='easeOut'))
        hatchMovement.start()

    def pause(self):
        pass

    def resume(self):
        pass

    def wake(self):
        self.okToRelease = True

    def sleep(self):
        ivalMgr.finishIntervalsMatching('hatchMovement')

    def destroy(self):
        ivalMgr.finishIntervalsMatching('hatchMovement')
        PinballErrand.destroy(self)

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        if self.letterNumber == 0:
            return Localizer.ppDeckHatchesNotSpelledAnything
        elif Localizer.myLanguage == 'brazilian':
            theLetter = self.pirates[0:self.letterNumber]
            if self.letterNumber == 6:
                theLetter = 'A'
            return Localizer.ppDeckHatchesPartialSpelling % theLetter
        else:
            return Localizer.ppDeckHatchesPartialSpelling % self.pirates[0:self.letterNumber]
        return

    def getName(self):
        return 'DeckHatches'

    def getBonus(self):
        bonus = self.totalLettersSpelled
        self.totalLettersSpelled = 0
        return (Localizer.ppDeckHatchesBonus, bonus, self.bonusGift)

    def hatchIn(self, ballIndex, args):
        vel = self.board.balls[ballIndex].getODEVel()
        sgode.pyode.dBodySetLinearVel(self.board.balls[ballIndex].body, vel[0] / 2, vel[1] / 2, vel[2] / 2)
        self.notify.debug('\nBall Number %d went in hatch %d' % (ballIndex, args[0]))
        self.ballInNotOut[(args[0] - 1)][ballIndex] = True

    def hatchOut(self, ballIndex, args):
        if ballIndex in self.ballInNotOut[(args[0] - 1)]:
            del self.ballInNotOut[(args[0] - 1)][ballIndex]
        if self.board.balls[ballIndex].getODEPos()[2] > 0:
            sgode.pyode.dGeomSetCollideBits(self.board.balls[ballIndex].geom, 4294967295 ^ DROPPED_CATEGORY)
            self.notify.debug('-- Ball Number %d ALMOST came out hatch %d \n' % (ballIndex, args[0]))
            return
        self.notify.debug('Ball Number %d came out hatch %d \n' % (ballIndex, args[0]))
        whichDialogue = random.randint(0, 1)
        if whichDialogue == 0:
            self.board.dialogueMgr.playDialogue('Hatch')
        elif whichDialogue == 1:
            self.board.dialogueMgr.playDialogue('Arr2')
        self.totalLettersSpelled = self.totalLettersSpelled + 1
        ballMode = self.board.deactivateBall(ballIndex)
        if self.letterNumber == 6:
            self.board.updateScore(self.board.pointValues['SpelledPirates'], 'SpelledPirates')
            self.board.multiplier = self.board.multiplier + 1
            if self.board.multiplier == 5:
                self.board.display.show(Localizer.ppDeckHatchesVictoryFull)
            else:
                self.board.display.show(Localizer.ppDeckHatchesVictory)
            if self.board.multiplier == 6:
                self.board.dialogueMgr.playDialogue('Congratulations')
                self.board.multiplier = 5
                self.board.display.show(Localizer.ppDeckHatchesWrappedMultiplier)
                self.board.updateScore(self.board.pointValues['WrappedMultiplier'], 'WrappedMultiplier')
            else:
                self.board.dialogueMgr.playDialogue('MultiplierAdvances')
            self.board.beacons['Multiplier'].setCurrentOnState(self.board.multiplier - 1)
            self.letterNumber = 0
            for i in range(0, 7):
                self.board.beacons[('Pirates%s' % self.pirates[i:i + 1])].setState(Beacon.BLINK)

            self.multiplierAdvances(ballIndex, args, ballMode)
        else:
            theLetter = self.pirates[self.letterNumber:self.letterNumber + 1]
            if Localizer.myLanguage == 'brazilian':
                if self.letterNumber == 5:
                    theLetter = 'A'
            self.board.display.show(Localizer.ppDeckHatchesSpelledLetter % theLetter)
            self.lightLetter(self.board.beacons[('Pirates%s' % self.pirates[self.letterNumber:self.letterNumber + 1])], self.board.beacons[('HatchHole%d' % args[0])])
            self.letterNumber = self.letterNumber + 1
            self.launchBallFromHatch(hatchNotToUse=args[0] - 1, ballMode=ballMode)

    def launchBallFromHatch(self, hatchNotToUse=-1, closeAfterward=False, fromOutside=False, ballMode=0):
        if hatchNotToUse == -1:
            for i in range(0, 3):
                if self.hatchState[i] == 1:
                    hatchNotToUse = i

        whichHatch = hatchNotToUse
        if len(self.ballInNotOut[hatchNotToUse]) > 0:
            self.board.pbTaskMgr.doMethodLater(0.5, self.launchBallFromHatch, 'launchballagainhatchinuse%d' % hatchNotToUse, [-1, closeAfterward, fromOutside, ballMode])
            return
        while whichHatch == hatchNotToUse:
            whichHatch = random.randint(0, 2)

        self.hatchState = [
         0, 0, 0]
        self.hatchState[whichHatch] = 1
        self.board.pbTaskMgr.doMethodLater(0.4, self.releaseBall, 'releaseBall%d%d' % (hatchNotToUse, fromOutside), [whichHatch, closeAfterward, ballMode])
        self.refresh(0.4, refreshLetters=False)

    def releaseBall(self, whichHatch, closeAfterward=False, ballMode=0):
        if self.board.currentZone != 0 or not self.okToRelease or len(self.ballInNotOut[whichHatch]) > 0:
            self.board.pbTaskMgr.doMethodLater(2, self.releaseBall, 'releaseballlateroutofhatch%d' % whichHatch, [whichHatch, closeAfterward, ballMode])
            return
        whichHatch = whichHatch + 1
        hatchProxPoint = self.board.proxPoints[('HatchHOLE%d' % whichHatch)]
        hatchProxPoint.setActive(False)
        ball = self.board.dropBall(False, tryNumber=0, bx=hatchProxPoint.getPos()[0], by=hatchProxPoint.getPos()[1], bz=0.5, ballMode=ballMode)
        ball.setZone(0)
        sgode.pyode.dBodySetLinearVel(ball.body, 2, -20, 0)
        ball.update()
        if closeAfterward:
            self.hatchState[whichHatch - 1] = 0
            self.refresh(0.4, refreshLetters=False)
        else:
            self.board.pbTaskMgr.doMethodLater(0.4, self.resetHatchActive, 'resetHatchActive%s' % ball.getName(), [whichHatch])

    def resetHatchActive(self, whichHatch):
        hatchProxPoint = self.board.proxPoints[('HatchHOLE%d' % whichHatch)]
        if self.hatchState[(whichHatch - 1)] == 1:
            hatchProxPoint.setActive(True)

    def multiplierAdvances(self, ballIndex, args, ballMode):
        self.board.pbTaskMgr.doMethodLater(3, self.start, 'restartPirates')
        self.launchBallFromHatch(hatchNotToUse=args[0] - 1, closeAfterward=True, ballMode=ballMode)
        self.notify.debug('celebration!!')
        self.board.pirateSounds['DeckHatches_MultiplierAdvances'].play()

    def lightLetter(self, letterBeacon, hatchBeacon):
        self.notify.debug('lighting letter')
        self.board.pirateSounds['DeckHatches_LetterLit'].play()
        letterBeacon.setState(Beacon.BLINK)
        self.board.pbTaskMgr.doMethodLater(2.5, letterBeacon.setState, 'resetLetter%s' % letterBeacon.name, [Beacon.ON])