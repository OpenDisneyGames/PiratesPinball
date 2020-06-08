# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: TopDeck.py
from pinballbase.PinballErrand import PinballErrand
from .PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
from pinballbase.Cheater import Cheater
import Localizer, random

class TopDeck(PinballErrand):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TopDeck')

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.bonusGift = self.board.pointValues['GoldenBarrelBonus']
        self.myZone = 0
        self.totalBarrelsGotten = 0
        self.seagullStatus = [
         [
          0, 0], [0, 0], [0, 0]]
        self.perchStatus = [
         0, 0, 0, 0, 0]
        self.barrelBonus = [0, 0, 0]
        self.cameraMovement = None
        self.rampOpen = True
        self.barrelFade = None
        self.goldenBarrelDialogueAllowed = True
        self.seagullNoise = True
        self.cheater = Cheater('crows', self.crowsCallBack)
        self.board.beacons['RampArrowBeacon'] = Beacon(board.boatModel.find('**/baconplates:pPlane38'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png', onTextureName=['piratepinball/art/main_ship/beacons/redArrowLit.png', 'piratepinball/art/main_ship/beacons/BoneXLit.png'])
        self.board.beacons['HelmBeacon'] = Beacon(board.boatModel.find('**/baconplates:pPlane35'), 'piratepinball/art/main_ship/beacons/RedLight.png')
        self.board.beacons['TopDeckSkullBeacon'] = Beacon(board.boatModel.find('**/baconplates:pPlane54'), 'piratepinball/art/main_ship/beacons/Skullflat.png')
        self.board.beacons['SeaGull1'] = Beacon(board.boatModel.find('**/baconplates:pPlane49'), 'piratepinball/art/main_ship/beacons/hatchIcon.png')
        self.board.beacons['SeaGull2'] = Beacon(board.boatModel.find('**/baconplates:pPlane43'), 'piratepinball/art/main_ship/beacons/RedLight.png')
        self.board.beacons['SeaGull3'] = Beacon(board.boatModel.find('**/baconplates:pPlane48'), 'piratepinball/art/main_ship/beacons/hatchIcon.png')
        self.rampBlockerFlat = board.boatModel.find('**/noEntranceStairs')
        self.rampBlockerFlat.setTransparency(1)
        self.rampBlockerFlat.setColor(1, 1, 1, 0)
        self.blockerParent = self.rampBlockerFlat.getParent()
        self.rampBlockerFlat.reparentTo(hidden)
        self.prop = ODESpinner(Point3(2.5, 0.5, 0.5), Point3(0, 27, 4.3), Point3(0, 0, -90), 50, Point3(0, 27, 4.5), Point3(0, 1, 0), 35, self.board.odeWorld, self.board.odeSpace, 'TheHelmSpinner')
        self.prop.loadModel('piratepinball/art/main_ship/wheel', Point3(0.2, 0.0, 0.0), Point3(-90.0, 0.0, 0.0))
        self.prop.setCallback(self.spinnerSpun, [])
        self.prop.reparentTo(render)
        self.prop.setActive(False)
        self.board.movables.append(self.prop)
        return

    def finishSetup(self):
        self.seagullPath = {}
        for r in range(4):
            for t in range(r + 1, 5):
                self.seagullPath['Path%d-%d' % (r, t)] = Actor('piratepinball/art/main_ship/BirdAnim_%d-%d' % (r, t), {'fly': 'piratepinball/art/main_ship/BirdAnim_%d-%d' % (r, t)})
                self.seagullPath[('Path%d-%d' % (r, t))].setHpr(-90.0, 0.0, 0.0)
                self.seagullPath[('Path%d-%d' % (r, t))].setPos(0.0, -9.44, 0.0)
                self.seagullPath[('Path%d-%d' % (r, t))].setScale(12)
                self.seagullPath[('Path%d-%d' % (r, t))].reparentTo(render)
                self.seagullPath[('Path%d-%d' % (r, t))].pose('fly', 0)
                self.seagullPath[('Path%d-%d' % (r, t))].find('**/+GeomNode').setTransparency(1)
                self.seagullPath[('Path%d-%d' % (r, t))].find('**/+GeomNode').setColor(0, 0, 0, 0)
                self.seagullPath['Node%d-%d' % (r, t)] = render.attachNewNode('seagullNode%d-%d' % (r, t))
                self.seagullPath[('Path%d-%d' % (r, t))].exposeJoint(self.seagullPath[('Node%d-%d' % (r, t))], 'modelRoot', 'joint')
                self.seagullPath[('Node%d-%d' % (r, t))].reparentTo(self.seagullPath[('Path%d-%d' % (r, t))])
                self.seagullPath[('Path%d-%d' % (r, t))].fixBounds()

        self.seagulls = []
        for i in range(0, 3):
            seagullActor = Actor('piratepinball/art/main_ship/seagull', {'idle': 'piratepinball/art/main_ship/seagullIdle', 'flap': 'piratepinball/art/main_ship/seagullFlap'})
            self.seagulls.append(seagullActor)
            self.seagulls[i].setScale(0.4)
            self.seagulls[i].setPos(-0.01, 0, 0.01)
            self.seagulls[i].setHpr(180, 0, 0)
            self.seagulls[i].setPlayRate(0.5, 'flap')
            self.seagulls[i].reparentTo(render)
            whichPerch = random.randint(0, 3)
            while self.perchStatus[whichPerch] > 0:
                whichPerch = random.randint(0, 3)

            self.perchStatus[whichPerch] = 2
            self.seagulls[i].reparentTo(self.seagullPath[('Node%d-4' % whichPerch)])
            self.notify.debug('selected nodepath = Node%d-4' % whichPerch)
            self.seagullStatus[i] = [whichPerch, 0]

        self.updateSpecialBarrels()

    def changeToZone(self, zoneNumber):
        pass

    def reset(self, time=1):
        for i in range(1, 4):
            self.board.beacons[('SeaGull%d' % i)].setState(Beacon.OFF)

        self.board.beacons['RampArrowBeacon'].setState(Beacon.OFF)
        self.board.beacons['HelmBeacon'].setState(Beacon.OFF)
        self.board.beacons['TopDeckSkullBeacon'].setState(Beacon.OFF)
        self.openUpRamp()

    def refresh(self, time=1):
        pass

    def crowsCallBack(self):
        if self.seagullNoise:
            self.seagullNoise = False
        else:
            self.seagullNoise = True
        if self.seagullNoise:
            self.board.pirateSounds['TopDeck_SeagullStartle'].play()
        else:
            self.board.pirateSounds['TopDeck_Bird'].play()

    def start(self):
        self.openUpRamp()
        self.board.beacons['RampArrowBeacon'].setState(Beacon.BLINK)
        for i in range(1, 4):
            self.board.beacons[('SeaGull%d' % i)].setState(Beacon.OFF)

        self.board.beacons['HelmBeacon'].setState(Beacon.OFF)
        self.board.beacons['TopDeckSkullBeacon'].setState(Beacon.OFF)
        self.seagullStatus = [
         [
          0, 0], [0, 0], [0, 0]]
        self.perchStatus = [0, 0, 0, 0, 0]
        for i in range(len(self.seagulls)):
            whichPerch = random.randint(0, 3)
            while self.perchStatus[whichPerch] > 0:
                whichPerch = random.randint(0, 3)

            self.perchStatus[whichPerch] = 2
            self.seagulls[i].reparentTo(self.seagullPath[('Node%d-4' % whichPerch)])
            self.seagullStatus[i] = [whichPerch, 0]
            self.seagulls[i].stop()
            self.seagulls[i].loop('idle')

        self.updateSpecialBarrels()

    def pause(self):
        if self.cameraMovement != None and self.cameraMovement.isPlaying():
            self.cameraMovement.pause()
        return

    def resume(self):
        if self.cameraMovement != None and self.cameraMovement.getState() == CInterval.SPaused:
            self.cameraMovement.resume()
        return

    def wake(self):
        self.cheater.wake()
        for s in self.seagulls:
            s.show()
            s.loop('idle')

    def sleep(self):
        self.cheater.sleep()
        if self.cameraMovement != None and self.cameraMovement.isPlaying():
            self.cameraMovement.finish()
        if self.barrelFade != None and self.barrelFade.isPlaying():
            self.barrelFade.finish()
        ivalMgr.finishIntervalsMatching('seagullMovement*')
        for s in self.seagulls:
            s.hide()
            s.stop()

        return

    def destroy(self):
        if self.cameraMovement != None and self.cameraMovement.isPlaying():
            self.cameraMovement.finish()
        if self.barrelFade != None and self.barrelFade.isPlaying():
            self.barrelFade.finish()
        for j in range(4):
            i = ivalMgr.getInterval('seagullMovement%d' % j)
            if i != None:
                ivalMgr.removeInterval(i)

        PinballErrand.destroy(self)
        return

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        return Localizer.ppTopDeckVisit

    def getName(self):
        return 'TopDeck'

    def getBonus(self):
        bonus = self.totalBarrelsGotten
        self.totalBarrelsGotten = 0
        return (Localizer.ppTopDeckBonus, bonus, self.bonusGift)

    def helmCenterIn(self, ballIndex, args):
        self.board.updateScore(self.board.pointValues['HelmCenter'], 'HelmCenter')
        self.board.beacons['HelmBeacon'].setState(Beacon.ONCE, 3)
        self.board.display.show(Localizer.ppTopDeckCenter)
        self.board.pirateSounds['TopDeck_HelmThread'].play()

    def helmIn(self, ballIndex, args):
        pass

    def flyTo(self, currentPerch, whichPerch, seagullNumber):
        self.perchStatus[whichPerch] = 1
        self.updateSpecialBarrels()
        if whichPerch == -1:
            finalPos = self.board.refPoints['FarSeagull'].getPos()
            finalHpr = self.board.refPoints['FarSeagull'].getHpr()
        else:
            finalPos = self.board.refPoints[('SeagullRef%d' % whichPerch)].getPos()
            finalHpr = self.board.refPoints[('SeagullRef%d' % whichPerch)].getHpr()
        perchPos = []
        perchHpr = []
        usedTargets = [0, 0, 0, 0]
        for i in range(2):
            whichTarget = random.randint(0, 3)
            while usedTargets[whichTarget] > 0:
                whichTarget = random.randint(0, 3)

            usedTargets[whichTarget] = 1
            perchPos.append(self.board.refPoints[('SeagullFlyTarget%d' % whichTarget)].getPos())
            perchHpr.append(self.board.refPoints[('SeagullFlyTarget%d' % whichTarget)].getHpr())

        seagullMovement = Sequence(name='seagullMovement%d' % seagullNumber)
        seagullMovement.append(Func(self.seagulls[seagullNumber].stop))
        seagullMovement.append(Func(self.seagulls[seagullNumber].loop, 'flap'))
        self.getCorrectFlightPlan(seagullNumber, seagullMovement, currentPerch, whichPerch)
        if whichPerch == -1:
            seagullMovement.append(Func(self.seagulls[seagullNumber].reparentTo, hidden))
        else:
            seagullMovement.append(Func(self.checkInToPerch, whichPerch, seagullNumber))
        seagullMovement.append(Func(self.seagulls[seagullNumber].stop))
        seagullMovement.append(Func(self.seagulls[seagullNumber].loop, 'idle'))
        seagullMovement.start()

    def checkInToPerch(self, whichPerch, seagullNumber):
        self.notify.debug('Seagull %d checking in to perch %d' % (seagullNumber, whichPerch))
        self.seagullStatus[seagullNumber][0] = whichPerch
        self.perchStatus[whichPerch] = 2
        self.updateSpecialBarrels()

    def getCorrectFlightPlan(self, seagullNumber, flightPlan, startPerch, endPerch):
        self.notify.debug('Seagull Number %d wants to go to perch %d from perch %d' % (seagullNumber, endPerch, startPerch))
        backwards = False
        if 'Path%d-%d' % (startPerch, endPerch) not in self.seagullPath:
            if 'Path%d-%d' % (endPerch, startPerch) in self.seagullPath:
                temp = startPerch
                startPerch = endPerch
                endPerch = temp
                backwards = True
            else:
                self.notify.warning("getCorrectFlightPlan: !!!!!!! holy crap, there's a problem !!!!!!!!!!!!!!!!")
                return
        self.seagulls[seagullNumber].reparentTo(self.seagullPath[('Node%d-%d' % (startPerch, endPerch))])
        if backwards:
            self.seagullPath[('Path%d-%d' % (startPerch, endPerch))].pose('fly', self.seagullPath[('Path%d-%d' % (startPerch, endPerch))].getNumFrames('fly'))
            flightPlan.append(self.seagullPath[('Path%d-%d' % (startPerch, endPerch))].actorInterval('fly', playRate=-1.0))
        else:
            self.seagullPath[('Path%d-%d' % (startPerch, endPerch))].pose('fly', 0)
            flightPlan.append(self.seagullPath[('Path%d-%d' % (startPerch, endPerch))].actorInterval('fly', playRate=1.0))

    def seagullIn(self, ballIndex, args):
        if args[0] > 0 and args[0] < 4:
            if self.barrelBonus[(args[0] - 1)] > 0:
                self.totalBarrelsGotten += 1
                self.board.display.show(Localizer.ppTopDeckBarrelBonus)
                self.board.updateScore(self.barrelBonus[(args[0] - 1)], 'GoldenBarrel')
                self.board.beacons['TopDeckSkullBeacon'].setState(Beacon.ONCE)
                self.board.pirateSounds['TopDeck_Barrel'].play()
        if self.perchStatus[args[0]] == 0 or self.perchStatus[args[0]] == 1:
            return
        if args[0] > 0 and args[0] < 4:
            self.board.beacons['SeaGull2'].setState(Beacon.ONCE)
        elif args[0] == 0:
            self.board.beacons['SeaGull1'].setState(Beacon.ONCE)
        else:
            self.board.beacons['SeaGull3'].setState(Beacon.ONCE)
        for i in range(len(self.seagullStatus)):
            if self.seagullStatus[i][0] == args[0]:
                self.board.display.show(Localizer.ppTopDeckStartle)
                self.board.updateScore(self.board.pointValues['HitSeagull'], 'HitSeagull')
                if self.seagullNoise:
                    self.board.pirateSounds['TopDeck_SeagullStartle'].play()
                    self.board.pirateSounds['TopDeck_SeagullFlap'].play()
                else:
                    self.board.pirateSounds['TopDeck_Bird'].play()
                self.seagullStatus[i][1] = self.seagullStatus[i][1] + 1
                self.notify.debug('\nPicking a new perch for seagull %d ' % i)
                whichPerch = random.randint(0, 4)
                while self.perchStatus[whichPerch] > 0:
                    whichPerch = random.randint(0, 4)

                self.seagullStatus[i][0] = -1
                self.flyTo(args[0], whichPerch, i)
                self.perchStatus[args[0]] = 0
                self.updateSpecialBarrels()
                break

    def seagullsReturn(self, taskInstance=None):
        self.board.display.show(Localizer.ppTopDeckIncoming)
        self.seagullStatus = [[0, 0], [0, 0], [0, 0]]
        self.perchStatus = [0, 0, 0, 0, 0]
        for i in range(len(self.seagulls)):
            self.seagulls[i].reparentTo(render)
            whichPerch = random.randint(0, 4)
            while self.perchStatus[whichPerch] > 0:
                whichPerch = random.randint(0, 4)

            self.perchStatus[whichPerch] = 1
            self.flyTo(0, whichPerch, i)
            self.seagullStatus[i] = [whichPerch, -1]

    def updateSpecialBarrels(self, taskInstance=None):
        if self.perchStatus[1] < 2 and self.perchStatus[2] < 2 and self.perchStatus[3] < 2:
            if self.barrelBonus[0] == 0 and self.goldenBarrelDialogueAllowed:
                self.goldenBarrelDialogueAllowed = False
                self.board.dialogueMgr.playDialogue('GoldenBarrel')
            self.barrelBonus = [
             self.board.pointValues['GoldenBarrel'], self.board.pointValues['GoldenBarrel'], self.board.pointValues['GoldenBarrel']]
            for i in range(0, 3):
                self.board.boardObjects[('TopBarrel%d' % i)].setColor(1, 1, 0, 1)

        else:
            self.barrelBonus = [
             0, 0, 0]
            for i in range(0, 3):
                self.board.boardObjects[('TopBarrel%d' % i)].setColor(1, 1, 1, 1)

    def spinnerSpun(self, args):
        if not self.board.gameOver:
            self.board.updateScore(self.board.pointValues['HelmSpun'], 'HelmSpun')

    def rampLogic(self, ballIndex, args):
        if args[0] == 'top':
            campos = 'topDeck'
            startT = 1
            endT = 0
            time = 1.5
            self.goldenBarrelDialogueAllowed = True
            self.prop.setActive(True)
        elif args[0] == 'bottom':
            self.prop.setActive(False)
            campos = 'main'
            startT = 0
            endT = 1
            time = 1.5
        if self.board.currentCameraPosition == campos:
            return
        if args[1]:
            self.board.pauseBalls()
        self.cameraMovement = Sequence(name='cameraTopDeckMovement')
        if args[0] == 'top':
            self.board.pbTaskMgr.doMethodLater(1, self.board.dialogueMgr.playDialogue, 'playseagulldialogue', ['ScareSeagulls'])
            flippers = []
            for flipper in self.board.allFlippers:
                if flipper.name == 'LeftTopDeckFlipper' or flipper.name == 'RightTopDeckFlipper':
                    flippers.append(flipper)

            self.board.flipperFlash(flippers)
        self.cameraMovement.append(Func(self.board.bumpManager.disable))
        camera1stMove = []
        camera1stMove.append(camera.posInterval(time, self.board.getCameraPos(campos), blendType='easeOut'))
        camera1stMove.append(camera.hprInterval(time, self.board.getCameraHpr(campos), blendType='easeOut'))
        camera1stMove.append(LerpColorInterval(self.board.frontMast, time, Vec4(1, 1, 1, endT), blendType='easeOut'))
        camera1stMove.append(LerpColorInterval(self.board.rearSail, time, Vec4(1, 1, 1, endT), blendType='easeOut'))
        camera1stMove.append(LerpColorInterval(self.board.frontSail, time, Vec4(1, 1, 1, endT), blendType='easeOut'))
        camera1stMove.append(LerpColorInterval(self.board.rearMast, time, Vec4(1, 1, 1, endT), blendType='easeOut'))
        camera1stMove.append(LerpColorInterval(self.board.crowsNest, time, Vec4(1, 1, 1, endT), blendType='easeOut'))
        self.cameraMovement.append(Parallel(*camera1stMove))
        self.cameraMovement.append(Func(self.board.bumpManager.enable))
        self.cameraMovement.start()

    def rampLogicTimer(self, ballIndex, args):
        if not self.board.gamePaused:
            self.board.pauseBalls(False)

    def closeRamp(self):
        self.rampOpen = False
        self.board.boardObjects['RampBumper'].restore()
        self.rampBlockerFlat.setColor(1, 1, 1, 0)
        self.rampBlockerFlat.reparentTo(self.blockerParent)
        barrelFade = LerpColorInterval(self.rampBlockerFlat, 1, Vec4(1, 1, 1, 1))
        barrelFade.start()
        self.board.beacons['RampArrowBeacon'].setCurrentOnState(1)
        self.board.beacons['RampArrowBeacon'].setState(Beacon.ON)

    def openUpRamp(self):
        if not self.board.gameOver and not self.rampOpen:
            self.board.pbTaskMgr.doMethodLater(2, self.board.dialogueMgr.playDialogue, 'playRampdialogue', ['AimRamp'])
        self.rampOpen = True
        self.board.boardObjects['RampBumper'].drop()
        self.barrelFade = Sequence(name='barrelFadeGone')
        self.barrelFade.append(LerpColorInterval(self.rampBlockerFlat, 1, Vec4(1, 1, 1, 0)))
        self.barrelFade.append(Func(self.rampBlockerFlat.reparentTo, hidden))
        self.barrelFade.start()
        self.board.beacons['RampArrowBeacon'].setCurrentOnState(0)
        self.board.beacons['RampArrowBeacon'].setState(Beacon.BLINK)