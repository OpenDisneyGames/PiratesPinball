# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: SkullAlleys.py
from pinballbase.PinballErrand import PinballErrand
from .PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
import Localizer

class SkullAlleys(PinballErrand):
    __module__ = __name__

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.bonusGift = self.board.pointValues['SkullAlleyBonus']
        self.myZone = 0
        self.totalLaneSavesActivated = 1
        self.alleyState = [False, False, False, False]
        self.laneSaves = [False, False, False]
        self.board.beacons['alleyBeacon1'] = Beacon(board.boatModel.find('**/PirateDropFlat2'), 'piratepinball/art/main_ship/beacons/PirateBand2.png', onTextureName=['pinballbase/blank.png'])
        self.board.beacons['alleyBeacon2'] = Beacon(board.boatModel.find('**/PirateDropFlat1'), 'piratepinball/art/main_ship/beacons/PirateBand3.png', onTextureName=['pinballbase/blank.png'])
        self.board.beacons['alleyBeacon3'] = Beacon(board.boatModel.find('**/PirateDropFlat'), 'piratepinball/art/main_ship/beacons/PirateBand4.png', onTextureName=['pinballbase/blank.png'])
        self.board.beacons['alleyBeacon4'] = Beacon(board.boatModel.find('**/PirateDropFlat3'), 'piratepinball/art/main_ship/beacons/PirateBand5.png', onTextureName=['pinballbase/blank.png'])
        self.board.beacons['alleyBeacon1'].plane.setBin('transparent', 3)
        self.board.beacons['alleyBeacon2'].plane.setBin('transparent', 3)
        self.board.beacons['alleyBeacon3'].plane.setBin('transparent', 3)
        self.board.beacons['alleyBeacon4'].plane.setBin('transparent', 3)
        board.boatModel.find('**/RedLight').setPos(-0.075, 0, 0)
        self.board.beacons['laneBeacon2'] = Beacon(board.boatModel.find('**/RedLight'), 'piratepinball/art/main_ship/beacons/RedLight.png')
        self.board.beacons['laneBeacon1'] = Beacon(board.boatModel.find('**/RedLight1'), 'piratepinball/art/main_ship/beacons/RedLight.png')
        self.board.beacons['laneBeacon3'] = Beacon(board.boatModel.find('**/baconplates:pPlane22'), 'piratepinball/art/main_ship/beacons/RedLight.png')
        self.hatchCovers = []
        self.hatchCovers.append(board.boatModel.find('**/leftOutlaneHatchNew'))
        self.hatchCovers.append(None)
        self.hatchCovers.append(board.boatModel.find('**/rightOutlaneHatchNew'))
        self.ballsInSave = 0
        return

    def finishSetup(self):
        pass

    def changeToZone(self, zoneNumber):
        pass

    def reset(self, time=1):
        self.alleyState = [False, False, False, False]
        self.laneSaves = [False, False, False]
        for i in range(1, 5):
            self.board.beacons[('alleyBeacon%d' % i)].setState(Beacon.OFF)

        self.ballsInSave = 0
        hatchMovement = Sequence(name='hatchMovement')
        hatchMove = []
        self.board.myBallSaveManager.setBeaconInUse(False)
        for i in range(1, 4):
            self.board.beacons[('laneBeacon%d' % i)].setState(Beacon.OFF)
            self.board.boardObjects[('outLaneDrop%d' % i)].drop()
            self.board.proxPoints[('outLaneHOLE%d' % i)].setActive(False)
            if self.hatchCovers[(i - 1)] != None:
                print(self.hatchCovers[(i - 1)])
                hatchMove.append(self.hatchCovers[(i - 1)].hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeOut'))

        print(hatchMove)
        hatchMovement.append(Parallel(*hatchMove))
        hatchMovement.start()
        return

    def refresh(self, time=1):
        hatchMovement = Sequence(name='hatchMovement')
        hatchMove = []
        for i in range(1, 4):
            if self.laneSaves[(i - 1)]:
                self.board.boardObjects[('outLaneDrop%d' % i)].restore()
                if self.hatchCovers[(i - 1)] != None:
                    hatchMove.append(self.hatchCovers[(i - 1)].hprInterval(time, Point3(0.0, 0.0, 90.0), blendType='easeOut'))
                self.board.beacons[('laneBeacon%d' % i)].setState(Beacon.ON)
                if i == 2:
                    self.board.myBallSaveManager.setBeaconInUse(True)
                self.board.proxPoints[('outLaneHOLE%d' % i)].setActive(True)
            else:
                self.board.boardObjects[('outLaneDrop%d' % i)].drop()
                if self.board.myBallSaveManager.isSaved() and i == 2:
                    pass
                else:
                    self.board.beacons[('laneBeacon%d' % i)].setState(Beacon.OFF)
                self.board.proxPoints[('outLaneHOLE%d' % i)].setActive(False)
                if self.hatchCovers[(i - 1)] != None:
                    hatchMove.append(self.hatchCovers[(i - 1)].hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeOut'))

        hatchMovement.append(Parallel(*hatchMove))
        hatchMovement.start()
        for i in range(1, 5):
            if self.alleyState[(i - 1)]:
                self.board.beacons[('alleyBeacon%d' % i)].setState(Beacon.ON)
            else:
                self.board.beacons[('alleyBeacon%d' % i)].setState(Beacon.OFF)

        return

    def start(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def sleep(self):
        ivalMgr.finishIntervalsMatching('hatchMovement')

    def destroy(self):
        ivalMgr.finishIntervalsMatching('hatchMovement')
        PinballErrand.destroy(self)

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        alleyCount = 0
        for i in self.alleyState:
            if i:
                alleyCount = alleyCount + 1

        laneCount = 0
        for i in self.laneSaves:
            if i:
                laneCount = laneCount + 1

        status = ''
        if alleyCount == 0:
            status = status + Localizer.ppSkullAlleysNoneLitMessage
        else:
            status = status + Localizer.ppSkyllAlleysSomeLitMessage % alleyCount
        return status

    def getName(self):
        return 'SkullAlleys'

    def getBonus(self):
        bonus = self.totalLaneSavesActivated
        self.totalLaneSavesActivated = 1
        return (Localizer.ppSkullAlleysBonus, bonus, self.bonusGift)

    def getLaneSaveState(self, laneNumber):
        return self.laneSaves[laneNumber]

    def cycleLeft(self):
        self.alleyState.append(self.alleyState.pop(0))
        self.refresh(0)

    def cycleRight(self):
        self.alleyState.insert(0, self.alleyState.pop())
        self.refresh(0)

    def alleyIn(self, ballIndex, alleyNumber):
        allLanesLit = False
        if not self.alleyState[(alleyNumber[0] - 1)]:
            self.board.beacons[('alleyBeacon%d' % alleyNumber[0])].setState(Beacon.ON)
            self.alleyState[alleyNumber[0] - 1] = True
            allLanesLit = True
            lanesLit = 0
            for i in self.alleyState:
                if not i:
                    allLanesLit = False
                else:
                    lanesLit += 1

            if lanesLit == 1:
                self.board.dialogueMgr.playDialogue('SkullLanes')
            else:
                whichDialogue = random.randint(0, 2)
                if whichDialogue == 0:
                    self.board.dialogueMgr.playDialogue('Arr1')
                elif whichDialogue == 1:
                    self.board.dialogueMgr.playDialogue('Arr2')
                elif whichDialogue == 2:
                    self.board.dialogueMgr.playDialogue('Arr3')
        self.getPoint(allLanesLit)

    def getPoint(self, allLanesLit):
        if allLanesLit:
            self.board.musicMgr.playJingle('Music_Success1', musicContinue=True)
            self.totalLaneSavesActivated = self.totalLaneSavesActivated + 1
            self.board.display.show(Localizer.ppSkullAlleysAllLitMessage)
            self.board.updateScore(self.board.pointValues['AllAlleysActive'], 'AllAlleysActive')
            self.board.pirateSounds['SkullAlleys_SavesActivated'].play()
            self.alleyState = [False, False, False, False]
            self.laneSaves = [True, True, True]
            self.board.dialogueMgr.playDialogue('LaneSaves')
            self.refresh(time=1)
        else:
            self.board.updateScore(self.board.pointValues['AlleyLit'], 'AlleyLit')
            self.board.pirateSounds['SkullAlleys_LightAlley'].play()

    def removeOneFromSave(self):
        self.ballsInSave -= 1

    def laneSaveIn(self, ballIndex, args):
        self.board.display.show(Localizer.ppSkullAlleysBallSaved)

    def laneSaveOut(self, ballIndex, args):
        ballMode = self.board.deactivateBall(ballIndex)
        self.ballsInSave += 1
        self.board.pbTaskMgr.doMethodLater(2.1, self.removeOneFromSave, 'removeOneFromSave%d' % ballIndex)
        self.laneSaves[args[0] - 1] = False
        if args[0] == 2:
            self.board.myBallSaveManager.setBeaconInUse(False)
        self.refresh(time=1)
        self.board.dialogueMgr.playDialogue('BallSaved')
        self.board.pbTaskMgr.doMethodLater(2, self.board.errands['DeckHatches'].launchBallFromHatch, 'launchfromsave%d' % ballIndex, [-1, False, True, ballMode])