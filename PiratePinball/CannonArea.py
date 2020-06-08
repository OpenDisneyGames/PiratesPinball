# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: CannonArea.py
from pinballbase.PinballErrand import PinballErrand
from PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
from pinballbase.odeConstructs import *
import Localizer
from EvilShipFSM import EvilShipFSM
import copy
from pandac.PandaModules import *

class CannonArea(PinballErrand):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratePinball.CannonArea')

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.myMouseWatcher = base.mouseWatcher.node()
        self.bonusGift = self.board.pointValues['SeaSerpentBonus']
        self.totalSeaSerpentsHit = 0
        self.myZone = 2
        self.ast = 80
        self.aet = 110
        self.islandHitCount = -1
        self.myBalls = None
        self.readySequence = None
        self.tutorialSequence = None
        self.seaSerpentSequence = None
        self.cannonBlockerFade = None
        self.seaSerpentWiggle = None
        self.saidEnemies = False
        self.stopBattle = False
        self.numberOfVictories = 0
        self.board.beacons['CannonArrowBeacon'] = Beacon(board.boatModel.find('**/baconplates:pPlane30'), onTextureName='piratepinball/art/main_ship/beacons/redArrowLit.png')
        self.firingCannon = board.boatModel.find('**/cannon02Barrel')
        self.otherCannon = board.boatModel.find('**/cannon01Barrel')
        self.inCannonArea = False
        self.shipsApproaching = False
        self.underAttack = False
        self.boarded = False
        self.pauseFlight = False
        self.dontHonorEnter = False
        self.serpentCanGetHit = True
        self.cannonOpen = True
        self.myExplosionManager = BillboardManager(name='cannonarea', howManyAtOnce=3, textureName='piratepinball/art/explosions/HitShip', numberOfTextures=6, seconds=0.3, scale=2.0)
        self.seaSerpentCrossTime = 40
        self.wSpeed = 1
        self.numberOfEvilShips = 4
        self.shipReports = []
        self.timeBetweenShipLaunches = 3
        self.numberOfShipsToEnd = 8
        self.courseStatus = [
         0, 0, 0, 0]
        self.maxTurnSpeed = 150.0
        self.turnAccelMagnitude = 500.0
        self.minHeading = -110
        self.maxHeading = -70
        self.cannonBase = NodePath('CannonBase')
        self.turnHelper = NodePath('CannonTurnHelper')
        self.raiseHelper = NodePath('CannonRaiseHelper')
        self.cannonBase.setScale(12)
        self.cannonBase.setHpr(270, 0, 0)
        self.cannonBase.setPos(-8.1, 0.0, 1.0)
        self.cannonBase.reparentTo(render)
        self.firingCannon.reparentTo(self.cannonBase)
        self.inverted = False
        self.minPitch = -60
        self.maxPitch = -10
        self.cannonPower = 6
        self.makeSerpent()
        self.annoyingFlat = self.board.boatModel.find('**/pPlane24')
        self.annoyingFlat.setBin('flat', 10)
        self.cannonBlockerFlat = board.boatModel.find('**/noEntrancePlank')
        self.cannonBlockerFlat.setTransparency(1)
        self.cannonBlockerFlat.setColor(1, 1, 1, 0)
        self.cannonBlockerFlat.setPos(-1.11, -0.76, 0.055)
        self.cannonBlockerFlat.setHpr(70, 265, 195)
        self.cannonBlockerFlat.setScale(0.25, 0.24, 0.16)
        self.cannonBlockerFlat.setBin('flat', 50)
        self.cannonBlockerFlat.stash()
        return

    def finishSetup(self):
        self.skullIsland = loader.loadModelCopy('piratepinball/art/skull_island/SkullIsland')
        self.skullIsland.setScale(11)
        self.skullIsland.setPos(-150, 2, -4)
        self.skullIsland.reparentTo(render)
        self.skullIsland.node().setAttrib(LightAttrib.makeAllOff())
        self.evilShipFSMs = []
        for i in range(self.numberOfEvilShips):
            self.evilShipFSMs.append(EvilShipFSM('EvilShip%d' % i, self.board, self, i))
            self.evilShipFSMs[i].request('Docked')

    def wake(self):
        self.cannonBase.reparentTo(render)
        self.islandHitCount = -1
        self.myExplosionManager.wake()
        for i in self.evilShipFSMs:
            i.wake()

    def sleep(self):
        self.dockTheShips()
        if self.cannonBlockerFade != None and self.cannonBlockerFade.isPlaying():
            self.cannonBlockerFade.pause()
            self.cannonBlockerFade.finish()
        for i in self.evilShipFSMs:
            i.sleep()

        ivalMgr.finishIntervalsMatching('cannonAreaSeaSerpentSinkSequence')
        self.cannonBase.reparentTo(hidden)
        self.myExplosionManager.sleep()
        if self.readySequence != None and not self.readySequence.isStopped():
            self.readySequence.finish()
        if self.tutorialSequence != None and not self.tutorialSequence.isStopped():
            self.tutorialSequence.finish()
        if self.seaSerpentSequence != None and not self.seaSerpentSequence.isStopped():
            self.seaSerpentSequence.finish()
        if self.seaSerpentWiggle != None and not self.seaSerpentWiggle.isStopped():
            self.seaSerpentWiggle.finish()
        self.board.display.invertCheckButton.reparentTo(hidden)
        self.firingCannon.setScale(1)
        self.inCannonArea = False
        self.underAttack = False
        self.shipsApproaching = False
        self.dontHonorEnter = False
        self.board.myTransition.noFade()
        props = base.win.getProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        sgode.pyode.dWorldSetGravity(self.board.odeWorld, self.board.gravX, self.board.gravY, self.board.gravZ)
        self.board.display.compass.setHpr(0, 0, 45)
        self.board.display.skullIsland.setColor(1, 1, 1, 0)
        return

    def destroy(self):
        while self.evilShipFSMs != []:
            i = self.evilShipFSMs.pop()
            i.destroy()

        ivalMgr.finishIntervalsMatching('cannonAreaSeaSerpentSinkSequence')
        if self.cannonBlockerFade != None and self.cannonBlockerFade.isPlaying():
            self.cannonBlockerFade.pause()
            self.cannonBlockerFade.finish()
        self.cannonBase.removeNode()
        self.myExplosionManager.destroy()
        if self.readySequence != None and not self.readySequence.isStopped():
            self.readySequence.finish()
        if self.tutorialSequence != None and not self.tutorialSequence.isStopped():
            self.tutorialSequence.finish()
        if self.seaSerpentSequence != None and not self.seaSerpentSequence.isStopped():
            self.seaSerpentSequence.finish()
        if self.seaSerpentWiggle != None and not self.seaSerpentWiggle.isStopped():
            self.seaSerpentWiggle.finish()
        PinballErrand.destroy(self)
        return

    def invertMouseControl(self):
        self.inverted = not self.inverted
        self.board.display.invertCheckButton['text'] = Localizer.ppCannonAreaInvert[self.inverted]

    def changeToZone(self, zoneNumber):
        if zoneNumber == self.myZone:
            self.board.display.hideMap()
        elif not self.board.gameOver:
            self.board.display.showMap()

    def reset(self, time=1):
        self.inCannonArea = False
        self.shipsApproaching = False
        self.underAttack = False
        self.serpentCanGetHit = True
        self.islandHitCount = -1
        self.board.beacons['CannonArrowBeacon'].setState(Beacon.OFF)
        self.cannonIncrement = 1
        self.board.boardObjects['CannonBlockDrop'].drop()
        self.board.display.compass.setHpr(0, 0, 45)
        self.board.display.skullIsland.setColor(1, 1, 1, 0)
        self.openCannon()

    def refresh(self, time=1):
        if self.inCannonArea:
            self.board.boardObjects['CannonBlockDrop'].restore()
        else:
            self.board.boardObjects['CannonBlockDrop'].drop()
        if self.shipsApproaching:
            self.board.beacons['CannonArrowBeacon'].setState(Beacon.BLINK)
        else:
            self.board.beacons['CannonArrowBeacon'].setState(Beacon.OFF)
        self.board.display.compass.setHpr(0, 0, 45)
        self.board.display.skullIsland.setColor(1, 1, 1, 0)
        self.board.pbTaskMgr.doMethodLater(random.randint(self.ast, self.aet), self.startShipApproach, 'startshipapproach')

    def showTutorialHud(self):
        self.board.display.minigameInstructionBackground.reparentTo(aspect2d)
        self.board.display.minigameInstruction1.reparentTo(aspect2d)
        self.board.display.minigameInstruction2.reparentTo(aspect2d)
        self.board.display.invertCheckButton.reparentTo(aspect2d)
        self.board.display.mouseGraphic.reparentTo(aspect2d)
        for i in range(4):
            self.board.display.mouseArrows[i].reparentTo(aspect2d)

    def hideTutorialHud(self):
        self.board.display.minigameInstructionBackground.reparentTo(hidden)
        self.board.display.minigameInstruction1.reparentTo(hidden)
        self.board.display.minigameInstruction2.reparentTo(hidden)
        self.board.display.invertCheckButton.reparentTo(hidden)
        self.board.display.mouseGraphic.reparentTo(hidden)
        for i in range(4):
            self.board.display.mouseArrows[i].reparentTo(hidden)

    def launchTargetShip(self):
        self.board.display.minigameInstruction1['text'] = Localizer.ppDisplayMiniGameInstructions3
        self.board.display.minigameInstruction2['text'] = Localizer.ppDisplayMiniGameInstructions4
        self.evilShipFSMs[0].myRoute = 4
        self.evilShipFSMs[0].request('Docked')
        self.evilShipFSMs[0].request('Sailing')

    def setIslandHit(self, val):
        self.islandHitCount = val

    def tutorial(self, interactiveMode=True):
        self.board.display.setHudState(0)
        self.board.setInTutorialMode(True)
        self.tutorialSequence = Sequence(name='cannonAreaTutorialSequence')
        self.tutorialSequence.append(Wait(3))
        self.tutorialSequence.append(Func(self.showTutorialHud))
        self.tutorialSequence.append(Func(self.board.dialogueMgr.playDialogue, 'UseMouseAim'))
        self.tutorialSequence.append(Func(self.setIslandHit, 0))
        self.tutorialSequence.append(Func(self.board.display.tutorialElements['skipIt'].reparentTo, hidden))
        if interactiveMode:
            self.tutorialSequence.append(Func(self.pauseTutorial))
            self.tutorialSequence.append(Wait(0.2))
        else:
            self.tutorialSequence.append(Wait(2))
        self.tutorialSequence.append(Func(self.launchTargetShip))
        self.tutorialSequence.append(Func(self.playMouseFireDialogue))
        self.tutorialSequence.append(Func(self.setIslandHit, -1))
        self.tutorialSequence.append(Wait(0.1))
        self.tutorialSequence.append(Func(self.board.dialogueMgr.playDialogue, 'HitShip'))
        if interactiveMode:
            self.tutorialSequence.append(Func(self.pauseTutorial, False))
            self.tutorialSequence.append(Wait(0.2))
        else:
            self.tutorialSequence.append(Wait(2))
        self.tutorialSequence.append(Func(self.hideTutorialHud))
        self.tutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppCannonAreaInstructions1, 0))
        self.tutorialSequence.append(Func(self.board.display.tutorialElements['continueOn'].reparentTo, hidden))
        self.tutorialSequence.append(Func(self.board.display.tutorialElements['skipIt'].reparentTo, hidden))
        self.tutorialSequence.append(Wait(4))
        self.tutorialSequence.append(Func(self.board.display.setHudState, 0))
        self.tutorialSequence.append(Func(self.board.setInTutorialMode, False))
        self.tutorialSequence.append(Func(self.launchShips, 0))
        self.tutorialSequence.append(Func(self.board.musicMgr.playMusic, 'CannonAttack'))
        self.tutorialSequence.start()

    def playMouseFireDialogue(self):
        if self.islandHitCount < 1:
            self.board.dialogueMgr.playDialogue('UseMouseFire')

    def pauseTutorial(self, showContinue=True):
        if self.tutorialSequence != None and self.tutorialSequence.isPlaying():
            self.tutorialSequence.pause()
            if showContinue:
                self.board.display.showContinue(True)
                if Localizer.myLanguage == 'english' and self.underAttack:
                    self.board.display.tutorialElements['continueOn']['text'] = Localizer.ppRightClickContinue
                self.board.display.tutorialElements['skipIt'].reparentTo(hidden)
            else:
                self.dontHonorEnter = True
        return

    def continueOn(self):
        if self.dontHonorEnter:
            return
        if self.tutorialSequence != None and not self.tutorialSequence.isStopped():
            self.tutorialSequence.resume()
            self.board.display.showContinue(False)
            self.board.display.tutorialElements['continueOn']['text'] = Localizer.pDisplayContinue
        return

    def skip(self):
        if self.tutorialSequence != None and not self.tutorialSequence.isStopped():
            self.tutorialSequence.finish()
            self.board.display.tutorialElements['continueOn']['text'] = Localizer.pDisplayContinue
        return

    def start(self):
        self.numberOfVictories = 0
        self.board.pbTaskMgr.doMethodLater(random.randint(self.ast, self.aet), self.startShipApproach, 'startshipapproach')
        self.openCannon()

    def pause(self):
        self.pauseFlight = True
        if self.underAttack:
            props = base.win.getProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
            self.seaSerpentSequence.pause()
            for e in self.evilShipFSMs:
                if e.state == 'Sailing':
                    e.sailingSequence.pause()

    def resume(self):
        self.pauseFlight = False
        if self.underAttack:
            props = base.win.getProperties()
            props.setCursorHidden(True)
            base.win.requestProperties(props)
            self.seaSerpentSequence.resume()
            if not self.stopBattle:
                for e in self.evilShipFSMs:
                    if e.state == 'Sailing':
                        e.sailingSequence.resume()

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        status = ''
        if self.inCannonArea:
            status = status + Localizer.ppCannonAreaInIt
        if self.shipsApproaching:
            status = status + ' ' + Localizer.ppCannonAreaReady
        else:
            status = status + ' ' + Localizer.ppCannonAreaGetReady
        return status

    def getName(self):
        return 'CannonArea'

    def getBonus(self):
        bonus = self.totalSeaSerpentsHit
        self.totalSeaSerpentsHit = 0
        return (Localizer.ppCannonAreaSeaSerpents, bonus, self.bonusGift * self.numberOfVictories)

    def makeSerpent(self):
        self.seaSerpent = NodePath('SeaSerpent')
        self.seaSerpent.reparentTo(render)
        self.seaSerpent.setPos(-155, -75, -1.5)
        self.seaSerpent.setHpr(90, 0, 0)
        self.seaSerpent.setScale(1.0)
        self.seaSerpentPieces = {}
        cm1 = CardMaker('seaserpenthead')
        lowerLeftTextureEdge = Point2(0.04, 0.04)
        upperRightTextureEdge = Point2(0.96, 0.96)
        cm1.setUvRange(lowerLeftTextureEdge, upperRightTextureEdge)
        cm1.setFrame(-2, 2, -2, 2)
        self.seaSerpentPieces['head'] = NodePath(cm1.generate())
        self.seaSerpentPieces['head'].setTexture(loader.loadTexture('piratepinball/art/skull_island/textures/seaserpenthead.png'))
        self.seaSerpentPieces['head'].setPos(9, 0, -0.5)
        for i in range(3):
            cm1 = CardMaker('seaserpentmiddle%d' % i)
            cm1.setUvRange(lowerLeftTextureEdge, upperRightTextureEdge)
            cm1.setFrame(-2, 2, -2, 2)
            self.seaSerpentPieces['middle%d' % i] = NodePath(cm1.generate())
            self.seaSerpentPieces[('middle%d' % i)].setTexture(loader.loadTexture('piratepinball/art/skull_island/textures/seaserpentmiddle.png'))
            self.seaSerpentPieces[('middle%d' % i)].setPos((1 - i) * 4.5, 0, 0)

        self.seaSerpentPieces['middle1'].setPos(0, 0, -1.5)
        cm1 = CardMaker('seaserpenttail')
        cm1.setUvRange(lowerLeftTextureEdge, upperRightTextureEdge)
        cm1.setFrame(-2, 2, -2, 2)
        self.seaSerpentPieces['tail'] = NodePath(cm1.generate())
        self.seaSerpentPieces['tail'].setTexture(loader.loadTexture('piratepinball/art/skull_island/textures/seaserpenttail.png'))
        self.seaSerpentPieces['tail'].setPos(-9, 0, -0.4)
        for ssp in self.seaSerpentPieces.values():
            ssp.reparentTo(self.seaSerpent)
            ssp.setHpr(0, 0, 0)
            ssp.node().setAttrib(LightAttrib.makeAllOff())
            ssp.setTransparency(1)
            ssp.setBin('flat', 5)

        self.seaSerpentWiggle = Sequence(name='seaserpentwiggle')
        updown = []
        updown.append(self.seaSerpentPieces['middle0'].posInterval(self.wSpeed, VBase3(4.5, 0, -1.5), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['middle1'].posInterval(self.wSpeed, VBase3(0, 0, 0), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['middle2'].posInterval(self.wSpeed, VBase3(-4.5, 0, -1.5), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['head'].hprInterval(self.wSpeed, VBase3(0, 0, 15), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['tail'].hprInterval(self.wSpeed, VBase3(0, 0, 17), blendType='easeInOut'))
        self.seaSerpentWiggle.append(Parallel(*updown))
        updown = []
        updown.append(self.seaSerpentPieces['middle0'].posInterval(self.wSpeed, VBase3(4.5, 0, 0), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['middle1'].posInterval(self.wSpeed, VBase3(0, 0, -1.5), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['middle2'].posInterval(self.wSpeed, VBase3(-4.5, 0, 0), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['head'].hprInterval(self.wSpeed, VBase3(0, 0, 0), blendType='easeInOut'))
        updown.append(self.seaSerpentPieces['tail'].hprInterval(self.wSpeed, VBase3(0, 0, 0), blendType='easeInOut'))
        self.seaSerpentWiggle.append(Parallel(*updown))
        self.seaSerpentSequence = Sequence(name='cannonAreaSeaSerpentSequence')
        self.seaSerpentSequence.append(Wait(3))
        self.seaSerpentSequence.append(Func(self.seaSerpent.reparentTo, render))
        self.seaSerpentSequence.append(Func(self.seaSerpent.setPos, -155, -75, -1.5))
        self.seaSerpentSequence.append(Func(self.seaSerpentWiggle.loop))
        self.seaSerpentSequence.append(self.seaSerpent.posInterval(self.seaSerpentCrossTime, VBase3(-155, 75, -1.5)))
        self.seaSerpentSequence.append(Func(self.seaSerpentWiggle.finish))
        self.seaSerpentSequence.append(Func(self.seaSerpent.reparentTo, hidden))
        for ssp in self.seaSerpentPieces.values():
            self.board.proxPoints['SeaSerpent%s' % ssp.getName()] = ProxPoint(self.board.odeWorld, self.board.odeSpace, 0, 0, 0, 2.7, 3.0, 'SeaSerpent%s' % ssp.getName(), 'CannonArea', callMethodIn=self.serpentHit, args=[], zone=2, writeOut=False)
            self.board.proxPoints[('SeaSerpent%s' % ssp.getName())].reparentTo(ssp)

    def serpentHit(self, ballIndex, args):
        if not self.serpentCanGetHit:
            return
        self.serpentCanGetHit = False
        self.totalSeaSerpentsHit += 1
        self.board.pbTaskMgr.doMethodLater(2, self.board.dialogueMgr.playDialogue, 'serpenthitdialogue', ['SerpentHit'])
        self.notify.debug('serpentHit: Serpent got hit by ball number %d ' % ballIndex)
        self.board.pirateSounds['CannonArea_SerpentHit'].play()
        self.board.updateScore(self.board.pointValues['SerpentHit'], 'SerpentHit')
        self.seaSerpent.setColorScale(1, 0, 0, 1)
        self.seaSerpentSequence.pause()
        seaSerpentSinkSequence = Sequence(name='cannonAreaSeaSerpentSinkSequence')
        seaSerpentSinkSequence.append(self.seaSerpent.posInterval(2, VBase3(self.seaSerpent.getPos()[0], self.seaSerpent.getPos()[1], -4.5)))
        seaSerpentSinkSequence.append(Func(self.seaSerpentWiggle.finish))
        seaSerpentSinkSequence.start()
        self.board.pbTaskMgr.doMethodLater(0.1, self.seaSerpent.setColorScale, 'seaserpentcolor', [VBase4(1, 1, 1, 1)])
        self.board.pbTaskMgr.doMethodLater(2.0, self.seaSerpentSequenceReset, 'seaserpentrestart')

    def seaSerpentSequenceReset(self, taskInstance=None):
        self.serpentCanGetHit = True
        self.seaSerpentSequence.finish()
        if not self.stopBattle:
            self.seaSerpentSequence.loop()

    def cannonArea(self, ballIndex, args):
        self.inCannonArea = True
        if self.shipsApproaching:
            if self.board.ballsOnTable <= 1:
                self.board.display.show(Localizer.ppCannonAreaPrepare)
                self.board.dialogueMgr.playDialogue('UnderAttack')
        else:
            self.board.display.show(Localizer.ppCannonAreaCongrats)
            self.board.dialogueMgr.playDialogue('NoEnemies')
            self.saidEnemies = True
        self.board.updateScore(self.board.pointValues['CannonAreaNotLit'], 'CannonAreaNotLit')
        self.board.pirateSounds['CannonArea_BallLocked'].play()
        self.board.boardObjects['CannonBlockDrop'].restore()
        self.board.balls[ballIndex].setODEPos(-9.5, -0.2, 0.5)
        sgode.pyode.dBodySetLinearVel(self.board.balls[ballIndex].body, 0, 0, 0)
        self.board.balls[ballIndex].update()

    def cannonAreaRelease(self, ballIndex, args):
        if self.pauseFlight:
            self.board.pbTaskMgr.doMethodLater(1, self.cannonAreaRelease, 'pausedCannonArea', [ballIndex, []])
            return
        if self.shipsApproaching and not self.saidEnemies and self.board.ballsOnTable <= 1:
            self.startBattle(ballIndex)
            self.board.errands['DeckHatches'].okToRelease = False
            return
        self.saidEnemies = False
        self.inCannonArea = False
        self.board.balls[ballIndex].setODEPos(-9.5, -0.2, 0.6)
        sgode.pyode.dBodySetLinearVel(self.board.balls[ballIndex].body, 0, 54, 0)
        self.board.boardObjects['CannonBlockDrop'].drop()
        self.board.pirateSounds['PiratePinball_BallRelease'].play()
        self.board.balls[ballIndex].update()

    def fireCannon(self):
        if self.board.gamePaused:
            return
        ball = None
        pos = self.firingCannon.getPos(render)
        ball = self.board.dropBall(False, bx=pos[0], by=pos[1], bz=pos[2], camReset=False, ballMode=self.ballMode, resetGravity=False)
        if ball == None:
            self.notify.debug('fireCannon: Out of Cannon Balls')
            self.board.pirateSounds['CannonArea_Empty'].play()
            self.board.display.show(Localizer.ppCannonAreaEmpty)
            return
        ball.setUnderAttack(True)
        self.board.pirateSounds['PiratePinball_Explode'].setVolume(0.8)
        self.board.pirateSounds['PiratePinball_Explode'].play()
        sgode.pyode.dGeomDisable(ball.geom)
        sgode.pyode.dGeomSetCollideBits(ball.geom, 4294967295 ^ WALL_CATEGORY ^ GROUND_CATEGORY ^ RUBBER_CATEGORY)
        sgode.pyode.dWorldSetGravity(self.board.odeWorld, 0, 0, -64)
        vec = render.getRelativeVector(self.firingCannon, Vec3(0, -1, 0))
        vec *= self.cannonPower
        sgode.pyode.dBodySetLinearVel(ball.body, vec[0], vec[1], vec[2])
        ball.setZone(self.myZone)
        ball.update()
        return

    def changeGravity(self, taskInstance=None):
        sgode.pyode.dWorldSetGravity(self.board.odeWorld, 0, 0, self.board.gravZ - 30)
        self.board.proxPoints['CrowCannon'].setActive(True)
        self.board.proxPoints['Cannon Switch'].setActive(True)
        self.board.boardObjects['UberRoof'].restore()

    def stepCannonMovement(self, dt):
        if self.myMouseWatcher.hasMouse() and not self.board.gamePaused:
            midX = base.win.getXSize() / 2
            midY = base.win.getYSize() / 2
            mouseData = MouseData()
            mouseData = base.win.getPointer(0)
            dx = mouseData.getX() - midX
            dy = mouseData.getY() - midY
            kx = float(self.maxHeading - self.minHeading) / float(base.win.getXSize()) * 3.0
            ky = float(self.maxPitch - self.minPitch) / float(base.win.getYSize()) * 1.5
            newHeading = self.cannonBase.getH() - dx * kx
            if self.inverted:
                newPitch = self.firingCannon.getP() - dy * ky
            else:
                newPitch = self.firingCannon.getP() + dy * ky
            newHeading = max(min(newHeading, self.maxHeading), self.minHeading)
            newPitch = max(min(newPitch, self.maxPitch), self.minPitch)
            self.cannonBase.setH(newHeading)
            self.firingCannon.setP(newPitch)
            base.win.movePointer(0, midX, midY)

    def islandHit(self, ballIndex, args):
        self.skullIsland.setColorScale(1, 0, 0, 1)
        self.myExplosionManager.startHere(self.board.balls[ballIndex].getPos())
        self.board.pbTaskMgr.doMethodLater(0.1, self.skullIsland.setColorScale, 'islandcolor', [VBase4(1, 1, 1, 1)])
        self.board.pirateSounds['CannonArea_IslandHit'].play()
        if not self.board.inTutorialMode:
            self.board.updateScore(self.board.pointValues['IslandHit'], 'IslandHit')
        elif self.islandHitCount >= 0:
            self.islandHitCount += 1
            if self.islandHitCount > 1:
                self.continueOn()
        self.board.deactivateBall(ballIndex)

    def gameOver(self):
        ivalMgr.finishIntervalsMatching('cannonareareadysequence')
        self.board.display.compass.setHpr(0, 0, 45)
        self.board.display.skullIsland.setColor(1, 1, 1, 0)
        self.board.display.hideMap()
        self.board.pbTaskMgr.removeDelayedMethod('startshipapproach')

    def startShipApproach(self, taskInstance=None):
        if self.board.currentZone != 0 or self.board.ballsOnTable > 1:
            self.board.pbTaskMgr.doMethodLater(random.randint(10, 20), self.startShipApproach, 'startshipapproach')
            return
        self.shipsApproaching = True
        self.board.dialogueMgr.playDialogue('EnemyShips')
        self.board.display.skullIsland.setPos(-0.689, 0.0, 0.782)
        self.board.display.skullIsland.setScale(0.01777, 1.0, 0.0089)
        self.board.display.skullIsland.reparentTo(aspect2d, 54)
        self.notify.debug('startShipApproach: cannonareareadysequence about to start')
        self.readySequence = Sequence(name='cannonareareadysequence')
        self.readySequence.append(self.board.display.compass.hprInterval(3, VBase3(0, 0, 25), blendType='easeIn'))
        self.readySequence.append(Func(self.board.beacons['CannonArrowBeacon'].setState, Beacon.BLINK))
        self.readySequence.append(Func(self.board.display.show, Localizer.ppCannonAreaGetReady))
        islandMoveFadeScale = []
        islandMoveFadeScale.append(LerpColorInterval(self.board.display.skullIsland, 10, Vec4(1, 1, 1, 1)))
        islandMoveFadeScale.append(self.board.display.skullIsland.posInterval(10, VBase3(-1.024667, 0.0, 0.77386), blendType='easeOut'))
        islandMoveFadeScale.append(self.board.display.skullIsland.scaleInterval(10, VBase3(0.16, 1.0, 0.08), blendType='easeOut'))
        islandMoveFadeScale.append(self.board.display.compass.hprInterval(10, VBase3(0, 0, -60), blendType='easeOut'))
        self.readySequence.append(Parallel(*islandMoveFadeScale))
        self.readySequence.append(Func(self.playCannonAreaDialogue))
        self.readySequence.start()

    def playCannonAreaDialogue(self):
        if self.board.currentZone != 0 or self.board.ballsOnTable > 1:
            return
        self.board.dialogueMgr.playDialogue('CannonArea')

    def startBattle(self, ballIndex):
        if self.readySequence != None:
            self.readySequence.finish()
        self.ballMode = self.board.balls[ballIndex].getBallMode()
        self.ballIndex = ballIndex
        props = base.win.getProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        self.notify.debug('startBattle: starting battle!!!!!')
        self.board.setCameraPosition('fireCannon', time=3)
        self.readySequence = Sequence(name='cannonareareadysequence')
        self.readySequence.append(self.otherCannon.hprInterval(1.5, VBase3(0, 0, 0), blendType='easeInOut'))
        self.readySequence.append(self.firingCannon.scaleInterval(1.5, 1.5))
        self.readySequence.start()
        self.shipReports = []
        self.underAttack = True
        self.stopBattle = False
        self.board.waterEffects.stopMoving()
        self.board.pauseBalls()
        self.board.changeToZone(2)
        self.board.beacons['CannonArrowBeacon'].setState(Beacon.OFF)
        self.board.display.setHudState(0)
        self.board.display.invertCheckButton.reparentTo(aspect2d)
        self.board.musicMgr.playMusic('CannonPractice')
        if self.seenTutorial:
            self.board.setInTutorialMode(True)
            if Localizer.myLanguage == 'english':
                self.board.display.tutorialElements['continueOn']['text'] = Localizer.pDisplayContinue
            self.tutorialSequence = Sequence(name='cannonAreaTutorialSequence')
            self.tutorialSequence.append(Wait(3))
            self.tutorialSequence.append(Func(self.board.display.mouseGraphic.reparentTo, aspect2d))
            self.tutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppCannonAreaRefresherMouse, 0, 0))
            self.tutorialSequence.append(Func(self.board.dialogueMgr.playDialogue, 'SinkShips'))
            self.tutorialSequence.append(Func(self.pauseTutorial))
            self.tutorialSequence.append(Wait(0.2))
            self.tutorialSequence.append(Func(self.board.display.showInstructions, '', 0.01, 0))
            self.tutorialSequence.append(Func(self.board.setInTutorialMode, False))
            self.tutorialSequence.append(Func(self.board.display.mouseGraphic.reparentTo, hidden))
            self.tutorialSequence.append(Func(self.launchShips, 0))
            self.tutorialSequence.append(Func(self.board.musicMgr.playMusic, 'CannonAttack'))
            if Localizer.myLanguage == 'english':
                self.tutorialSequence.append(Func(self.resetEnterText))
            self.tutorialSequence.start()
        else:
            self.tutorial()
            self.seenTutorial = True
        return

    def resetEnterText(self):
        self.board.display.tutorialElements['continueOn']['text'] = Localizer.pDisplayContinue

    def endBattle(self, youWon=True):
        self.board.display.invertCheckButton.reparentTo(hidden)
        self.seaSerpentSequence.finish()
        self.board.setCameraPosition('main', time=3)
        self.firingCannon.setScale(1)
        self.board.changeToZone(0)
        self.board.waterEffects.startMoving()
        self.inCannonArea = False
        self.board.pbTaskMgr.doMethodLater(3, self.showKeyboardReminder, 'showkeyboardreminder')
        if youWon:
            self.numberOfVictories += 1
            if self.numberOfVictories > 3:
                self.numberOfVictories = 3
            self.board.dialogueMgr.playDialogue('Congratulations')
            self.board.updateScore(self.board.pointValues['WonBattle'], 'WonBattle')
            self.board.display.show(Localizer.ppCannonAreaYouWin)
        else:
            self.board.dialogueMgr.playDialogue('Boarded')
            self.board.display.show(Localizer.ppCannonAreaYouLose)

    def showKeyboardReminder(self, taskInstance=None):
        self.underAttack = False
        self.dockTheShips()
        self.shipsApproaching = False
        self.dontHonorEnter = False
        self.board.myTransition.noFade()
        self.board.setInTutorialMode(True)
        self.tutorialSequence = Sequence(name='cannonAreaTutorialSequence')
        self.tutorialSequence.append(Func(self.board.display.keyboardGraphic.reparentTo, aspect2d))
        self.tutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppCannonAreaRefresherKeyboard, 0, 0))
        self.tutorialSequence.append(Func(self.pauseTutorial))
        self.tutorialSequence.append(Wait(0.2))
        self.tutorialSequence.append(Func(self.board.display.showInstructions, '', 0.01, 1))
        self.tutorialSequence.append(Func(self.board.setInTutorialMode, False))
        self.tutorialSequence.append(Func(self.board.display.keyboardGraphic.reparentTo, hidden))
        self.tutorialSequence.append(Func(self.startBallsAgain))
        self.tutorialSequence.start()

    def startBallsAgain(self, taskInstance=None):
        if not self.board.hideCursor:
            props = base.win.getProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
        self.board.errands['DeckHatches'].okToRelease = True
        sgode.pyode.dWorldSetGravity(self.board.odeWorld, self.board.gravX, self.board.gravY, self.board.gravZ)
        self.board.boardObjects['CannonBlockDrop'].drop()
        self.board.pauseBalls(False)
        self.cannonAreaRelease(self.ballIndex, [])
        self.board.display.setHudState(1)
        self.board.display.showMap(3)
        self.board.display.invertCheckButton.reparentTo(hidden)
        self.board.display.compass.setHpr(0, 0, 45)
        self.board.display.skullIsland.setColor(1, 1, 1, 0)
        self.board.pbTaskMgr.doMethodLater(random.randint(self.ast, self.aet), self.startShipApproach, 'startshipapproach')

    def dockTheShips(self):
        lownumber = 0
        self.courseStatus = [0, 0, 0, 0]
        for i in range(self.numberOfEvilShips):
            whichCourse = random.randint(0, 3)
            while self.courseStatus[whichCourse] > lownumber:
                whichCourse = random.randint(0, 3)

            good = False
            for j in self.courseStatus:
                if j == lownumber:
                    good = True

            if not good:
                lownumber += 1
            self.courseStatus[whichCourse] += 1
            self.evilShipFSMs[i].myRoute = whichCourse
            self.evilShipFSMs[i].request('Docked')

    def launchShips(self, shipNumber):
        if self.pauseFlight:
            self.board.pbTaskMgr.doMethodLater(self.timeBetweenShipLaunches, self.launchShips, 'launchships', [shipNumber])
            return
        self.notify.debug('launchShips:  ----------  Calling launchShips, shipNumber = %d ' % shipNumber)
        if self.board.fromPalace == True:
            self.board.display.playTimer.playing()
        if shipNumber == 0:
            self.notify.debug('launchShips: Docking the ships')
            self.board.display.invertCheckButton.reparentTo(aspect2d)
            self.dockTheShips()
            self.seaSerpentSequence.loop()
        if shipNumber == self.numberOfShipsToEnd + 2 * self.numberOfVictories or self.stopBattle:
            return
        good = False
        for e in self.evilShipFSMs:
            if e.state == 'Docked':
                e.totalTimeToAttack -= 4 * self.numberOfVictories
                if shipNumber > (self.numberOfShipsToEnd + 2 * self.numberOfVictories) / 2:
                    self.notify.debug('launchShips: Speeding up ship')
                    e.totalTimeToAttack = float(e.totalTimeToAttack) * 0.8
                e.request('Sailing')
                good = True
                break

        if not good:
            self.notify.debug('launchShips: We ran out of ships to launch!!')
            self.board.pbTaskMgr.doMethodLater(self.timeBetweenShipLaunches, self.launchShips, 'launchships', [shipNumber])
        else:
            self.notify.debug('launchShips: Launching new ship!')
            self.board.pbTaskMgr.doMethodLater(self.timeBetweenShipLaunches, self.launchShips, 'launchships', [shipNumber + 1])

    def getNewDock(self, shipRequestingIt):
        self.notify.debug('getNewDock: Course status = %s ' % self.courseStatus)
        low = 10000
        leastCrowdedCourse = 1
        for i in range(len(self.courseStatus)):
            if self.courseStatus[i] < low:
                low = self.courseStatus[i]
                leastCrowdedCourse = i

        self.notify.debug('getNewDock: --Ship number %d requesting a new dock, giving it %d ' % (shipRequestingIt, leastCrowdedCourse))
        self.courseStatus[leastCrowdedCourse] += 1
        return leastCrowdedCourse

    def shipReportIn(self, shipNumber, howManyTimesHit, status):
        if self.stopBattle:
            self.notify.debug('----------------- You checked in late buddy.... ------------------ ')
            return
        if self.board.inTutorialMode:
            self.dontHonorEnter = False
            self.continueOn()
            return
        self.shipReports.append(ShipReport(shipNumber, howManyTimesHit, status))
        self.notify.debug('Ship number %d reporting in sir, we got hit %d times and our status is %s' % (shipNumber, howManyTimesHit, status))
        if status == 'boarded':
            self.stopBattle = True
            self.board.pirateSounds['CannonArea_PirateCharge'].play()
            self.board.musicMgr.playJingle('DefeatJingle', musicContinue=True)
            self.board.pbTaskMgr.doMethodLater(3, self.endBattle, 'endbattleboarded', [False])
            for e in self.evilShipFSMs:
                e.sailingSequence.pause()

            self.board.myTransition.fadeScreenColor(VBase4(1, 0, 0, 0.5))
            self.board.bumpManager.disable()
            self.board.display.showInstructions(Localizer.ppCannonAreaYouLose, 3, 0)
            self.board.display.tutorialElements['skipIt'].reparentTo(hidden)
            self.board.display.tutorialElements['continueOn'].reparentTo(hidden)
            self.board.display.tutorialElements['tutorialLabel'].reparentTo(hidden)
            return
        self.board.updateScore(self.board.pointValues['SunkShip'], 'SunkShip')
        if len(self.shipReports) == self.numberOfShipsToEnd + 2 * self.numberOfVictories:
            self.notify.debug("It's over! You survived!")
            self.board.musicMgr.playJingle('VictoryJingle', musicContinue=True)
            self.stopBattle = True
            self.board.pbTaskMgr.doMethodLater(3, self.endBattle, 'endbattlevictory', [True])
            for e in self.evilShipFSMs:
                e.sailingSequence.pause()

            self.board.display.showInstructions(Localizer.ppCannonAreaYouWin, 3, 0)
            self.board.display.tutorialElements['skipIt'].reparentTo(hidden)
            self.board.display.tutorialElements['continueOn'].reparentTo(hidden)
            self.board.display.tutorialElements['tutorialLabel'].reparentTo(hidden)

    def closeCannon(self):
        self.cannonOpen = False
        self.board.boardObjects['CannonBlockDrop'].restore()
        self.cannonBlockerFlat.setColor(1, 1, 1, 0)
        self.cannonBlockerFlat.setColor(1, 1, 1, 0)
        self.cannonBlockerFlat.unstash()
        if self.cannonBlockerFade is not None:
            self.cannonBlockerFade.finish()
        self.cannonBlockerFade = LerpColorInterval(self.cannonBlockerFlat, 1, Vec4(1, 1, 1, 1))
        self.cannonBlockerFade.start()
        return

    def openCannon(self):
        self.cannonOpen = True
        self.board.boardObjects['CannonBlockDrop'].drop()
        if self.cannonBlockerFade is not None:
            self.cannonBlockerFade.finish()
        self.cannonBlockerFade = Sequence(name='cannonBlockerFade')
        self.cannonBlockerFade.append(LerpColorInterval(self.cannonBlockerFlat, 1, Vec4(1, 1, 1, 0)))
        self.cannonBlockerFade.append(Func(self.cannonBlockerFlat.stash))
        self.cannonBlockerFade.start()
        return


class ShipReport:
    __module__ = __name__

    def __init__(self, shipNumber, howManyTimesHit, status):
        self.shipNumber = shipNumber
        self.howManyTimesHit = howManyTimesHit
        self.status = status