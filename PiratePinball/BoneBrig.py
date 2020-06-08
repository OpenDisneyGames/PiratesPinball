from pinballbase.PinballErrand import PinballErrand
from .PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
import Localizer

class BoneBrig(PinballErrand):
    __module__ = __name__

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.bonusGift = self.board.pointValues['BoneBrigBonus']
        self.myZone = 1
        self.leftFlipper = None
        self.rightFlipper = None
        self.skeletonStatus = [
         0, 0, 0]
        self.skeletonsFreed = 0
        self.totalSkeletonsFreed = 0
        self.seenTutorial = False
        self.tutorialSequence = None
        self.board.beacons['BBBarrel1'] = Beacon(board.brigModel.find('**/BoneRedLight_2'), 'piratepinball/art/bonebrig/beacons/BoneRedLight.png', onTextureName=['piratepinball/art/bonebrig/beacons/BoneYellowLightLit.png', 'piratepinball/art/bonebrig/beacons/BoneGreenLightLit.png'])
        self.board.beacons['BBBarrel2'] = Beacon(board.brigModel.find('**/BoneRedLight_1'), 'piratepinball/art/bonebrig/beacons/BoneRedLight.png', onTextureName=['piratepinball/art/bonebrig/beacons/BoneYellowLightLit.png', 'piratepinball/art/bonebrig/beacons/BoneGreenLightLit.png'])
        self.board.beacons['BBBarrel3'] = Beacon(board.brigModel.find('**/BoneRedLight_3'), 'piratepinball/art/bonebrig/beacons/BoneRedLight.png', onTextureName=['piratepinball/art/bonebrig/beacons/BoneYellowLightLit.png', 'piratepinball/art/bonebrig/beacons/BoneGreenLightLit.png'])
        self.board.beacons['BBSkull'] = Beacon(board.brigModel.find('**/Skullflat'), 'piratepinball/art/main_ship/beacons/Skullflat.png')
        self.gate = board.brigModel.find('**/Gate')
        self.leftSkullBall = self.makeSkullBall()
        self.rightSkullBall = self.makeSkullBall()
        self.leftCage = board.brigModel.find('**/LeftCageBars')
        self.rightCage = board.brigModel.find('**/RightCageBars')
        self.lcPos = self.leftCage.getPos()
        self.rcPos = self.rightCage.getPos()
        self.leftCage.setTransparency(1)
        self.rightCage.setTransparency(1)
        self.resetCages()
        self.myExplosionManager = BillboardManager(name='skeletonbarrels', howManyAtOnce=1, textureName='piratepinball/art/explosions/HitShip', numberOfTextures=6, seconds=0.3, scale=3.5)
        return

    def finishSetup(self):
        self.skeletonModels = []
        for i in range(0, 3):
            skelActor = Actor('piratepinball/art/bonebrig/skeleton_base', {'hit1': 'piratepinball/art/bonebrig/skeleton_hit1', 'hit2': 'piratepinball/art/bonebrig/skeleton_hit2', 'hit3': 'piratepinball/art/bonebrig/skeleton_hit3', 'shakefist3': 'piratepinball/art/bonebrig/skeleton_shakefist3', 'shakefist4': 'piratepinball/art/bonebrig/skeleton_shakefist4'})
            myBarrel = self.board.boardObjects[('BBBumper%d' % int(i + 1))]
            myBarrel.setTransparency(1)
            x = myBarrel.getPos()[0]
            y = myBarrel.getPos()[1] + -0.3
            z = myBarrel.getPos()[2] + 2.4
            skelActor.setPos(VBase3(x, y, z))
            if i == 2:
                skelActor.setHpr(355, 0, 0)
            elif i == 0:
                skelActor.setHpr(10, 0, 0)
            skelActor.setScale(0.02)
            skelActor.setTransparency(1)
            skelActor.reparentTo(hidden)
            skelActor.setColor(1, 1, 1, 0)
            self.skeletonModels.append(skelActor)

    def changeToZone(self, zoneNumber):
        if zoneNumber == self.myZone:
            self.board.display.setHudState(0)
            for s in self.skeletonModels:
                s.reparentTo(render)

        for s in self.skeletonModels:
            s.reparentTo(hidden)

        if zoneNumber == 0 and not self.board.gameOver:
            self.board.display.setHudState(1)

    def reset(self, time=1):
        self.skeletonStatus = [
         0, 0, 0]
        self.skeletonsFreed = 0
        for i in range(1, 4):
            self.board.beacons[('BBBarrel%d' % i)].setState(Beacon.OFF)

        self.board.beacons['BBSkull'].setState(Beacon.OFF)
        self.hideFlippers()
        gateMovement = Sequence(name='gateMovement')
        gateMovement.append(self.gate.hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeInOut'))
        gateMovement.start()
        self.board.boardObjects['GateDrop'].drop()

    def refresh(self, time=1):
        self.reset(time)

    def intro(self, ballIndex):
        self.tutorial(ballIndex=ballIndex)

    def tutorial(self, interactiveMode=True, ballIndex=0):
        self.board.setInTutorialMode(True)
        self.board.setCameraPosition('boneBrigTeach1', time=2)
        self.tutorialSequence = Sequence(name='tutorialSequence')
        self.tutorialSequence.append(Wait(2))
        self.tutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppBoneBrigInstructions1, 0))
        if interactiveMode:
            self.tutorialSequence.append(Func(self.pauseTutorial))
            self.tutorialSequence.append(Wait(0.2))
        else:
            self.tutorialSequence.append(Wait(2))
        self.tutorialSequence.append(Func(self.board.setCameraPosition, 'boneBrigTeach2', time=1))
        self.tutorialSequence.append(Wait(1))
        self.tutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppBoneBrigInstructions2, 0))
        self.tutorialSequence.append(Func(self.skeletonModels[2].setColor, 1, 1, 1, 1))
        self.tutorialSequence.append(Func(self.skeletonModels[2].play, 'hit1'))
        self.tutorialSequence.append(Func(self.board.pirateSounds['BoneBrig_SkeletonEmerge3'].play))
        self.tutorialSequence.append(Func(self.board.beacons['BBBarrel3'].setCurrentOnState, 0))
        self.tutorialSequence.append(Func(self.board.beacons['BBBarrel3'].setState, Beacon.ON))
        if interactiveMode:
            self.tutorialSequence.append(Func(self.pauseTutorial))
            self.tutorialSequence.append(Wait(0.2))
        else:
            self.tutorialSequence.append(Wait(2))
        self.tutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppBoneBrigInstructions3, 0))
        self.tutorialSequence.append(Func(self.skeletonModels[2].play, 'hit2'))
        self.tutorialSequence.append(Func(self.board.dialogueMgr.playDialogue, 'SkeletonsAngry'))
        self.tutorialSequence.append(Func(self.board.pirateSounds['BoneBrig_IrateSkeleton3'].play))
        self.tutorialSequence.append(Func(self.board.beacons['BBBarrel3'].setCurrentOnState, 1))
        self.tutorialSequence.append(Func(self.board.beacons['BBBarrel3'].setState, Beacon.ON))
        self.tutorialSequence.append(Func(self.loopIt, [2]))
        if interactiveMode:
            self.tutorialSequence.append(Func(self.pauseTutorial))
            self.tutorialSequence.append(Wait(0.2))
        else:
            self.tutorialSequence.append(Wait(2))
        self.tutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppBoneBrigInstructions4, 0))
        self.tutorialSequence.append(Func(self.skeletonModels[2].stop))
        self.tutorialSequence.append(self.skeletonModels[2].actorInterval('hit2', playRate=-1.0, startFrame=20, endFrame=8))
        self.tutorialSequence.append(self.skeletonModels[2].actorInterval('hit1', playRate=-1.0, startFrame=7, endFrame=0))
        self.tutorialSequence.append(Func(self.skeletonModels[2].setColor, VBase4(1, 1, 1, 0)))
        self.tutorialSequence.append(Func(self.board.beacons['BBBarrel3'].setState, Beacon.OFF))
        if interactiveMode:
            self.tutorialSequence.append(Func(self.pauseTutorial))
            self.tutorialSequence.append(Wait(0.2))
        else:
            self.tutorialSequence.append(Wait(2))
        self.tutorialSequence.append(Func(self.board.display.setHudState, 0))
        self.tutorialSequence.append(Func(self.board.setCameraPosition, 'boneBrig', 1.5))
        self.tutorialSequence.append(Wait(1.5))
        self.tutorialSequence.append(Func(self.board.balls[ballIndex].setChilled, False))
        self.tutorialSequence.append(Func(sgode.pyode.dBodyEnable, self.board.balls[ballIndex].body))
        self.tutorialSequence.append(Func(sgode.pyode.dGeomEnable, self.board.balls[ballIndex].geom))
        self.tutorialSequence.append(Func(self.skeletonModels[2].stop))
        self.tutorialSequence.append(Func(self.board.setInTutorialMode, False))
        self.tutorialSequence.append(Func(self.putDownGateInASecond))
        if self.board.fromPalace == True:
            self.tutorialSequence.append(Func(self.board.display.playTimer.playing))
        self.tutorialSequence.start()

    def pauseTutorial(self):
        if self.tutorialSequence != None and self.tutorialSequence.isPlaying():
            self.tutorialSequence.pause()
            self.board.display.showContinue(True)
        return

    def continueOn(self):
        if self.tutorialSequence != None and not self.tutorialSequence.isStopped():
            self.tutorialSequence.resume()
            self.board.display.showContinue(False)
        return

    def skip(self):
        if self.tutorialSequence != None and not self.tutorialSequence.isStopped():
            self.tutorialSequence.finish()
        return

    def putDownGateInASecond(self):
        self.board.pbTaskMgr.doMethodLater(1, self.putDownGate, 'putDownGate')

    def start(self):
        if self.board.currentZone != 1:
            return
        self.showFlippers()
        self.skeletonStatus = [0, 0, 0]
        self.skeletonsFreed = 0
        for i in range(1, 4):
            self.board.beacons[('BBBarrel%d' % i)].setState(Beacon.OFF)

        self.board.beacons['BBSkull'].setState(Beacon.OFF)
        gateMovement = Sequence(name='gateMovement')
        gateMovement.append(self.gate.hprInterval(1.2, Point3(0.0, -90.0, 0.0), blendType='easeInOut'))
        gateMovement.start()
        self.board.boardObjects['GateDrop'].drop()
        self.resetCages()
        for i in range(1, 4):
            self.board.boardObjects[('BBBumper%d' % i)].setColor(1, 1, 1, 1)
            self.board.boardObjects[('BBBumper%d' % i)].restore()
            self.skeletonModels[(i - 1)].stop()
            backdown = Sequence(name='backdown')
            backdown.append(self.skeletonModels[(i - 1)].actorInterval('hit1', playRate=-1.0, startFrame=7, endFrame=0))
            backdown.append(Func(self.skeletonModels[(i - 1)].setColor, VBase4(1, 1, 1, 0)))
            backdown.start()

    def pause(self):
        pass

    def resume(self):
        pass

    def wake(self):
        self.myExplosionManager.wake()

    def sleep(self):
        self.myExplosionManager.sleep()

    def destroy(self):
        self.myExplosionManager.destroy()
        del self.myExplosionManager
        PinballErrand.destroy(self)

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        if self.skeletonsFreed == 0:
            return Localizer.ppBoneBrigGetGoing
        else:
            return Localizer.ppBoneBrigStatus % self.skeletonsFreed
        return

    def getName(self):
        return 'BoneBrig'

    def getBonus(self):
        bonus = self.totalSkeletonsFreed
        self.totalSkeletonsFreed = 0
        return (Localizer.ppBoneBrigSkeletons, bonus, self.bonusGift)

    def hideFlippers(self):
        self.leftFlipper.reparentTo(hidden)
        self.rightFlipper.reparentTo(hidden)

    def showFlippers(self):
        self.leftFlipper.reparentTo(render)
        self.rightFlipper.reparentTo(render)

    def escapeBoneBrigIn(self, ballIndex, args):
        if self.skeletonsFreed == 3:
            self.board.pauseBalls()
            self.board.beacons['BBSkull'].setState(Beacon.OFF)
            if self.board.balls[ballIndex].getBallMode() == 1:
                self.skeletonsFreed = 5
            else:
                self.skeletonsFreed = 4
            self.board.display.show(Localizer.ppBoneBrigSuccess)
            self.cagesFall(ballIndex, args)
            for i in range(0, len(self.board.balls)):
                self.board.deactivateBall(i)

    def cagesFall(self, ballIndex, args):
        cageMovement = Sequence(name='cageMovement')
        m = []
        m.append(self.leftCage.posInterval(0.8, Point3(0.0, 0.0, -0.7)))
        m.append(self.rightCage.posInterval(0.8, Point3(-0.25, -0.1, -1.6)))
        m.append(self.leftSkullBall.posInterval(1, Point3(0.2, 0.85, 1.6), blendType='easeIn'))
        m.append(self.rightSkullBall.posInterval(1, Point3(-0.2, 0.85, 1.6), blendType='easeIn'))
        m.append(LerpColorInterval(self.leftCage, 0.7, Vec4(1, 1, 1, 0)))
        m.append(LerpColorInterval(self.rightCage, 0.7, Vec4(1, 1, 1, 0)))
        cageMovement.append(Parallel(*m))
        cageMovement.start()
        self.board.pbTaskMgr.doMethodLater(0.6, self.board.pirateSounds['BoneBrig_CageFall'].play, 'playcagefallsound')
        self.board.pbTaskMgr.doMethodLater(1, self.boneBrigExitIn, 'bonebrigexitin', [ballIndex, args])
        self.board.pbTaskMgr.doMethodLater(4, self.boneBrigExitTimer, 'boneBrigExitTimer', [ballIndex, args])

    def boneBrigEnterIn(self, ballIndex, args):
        self.board.balls[ballIndex].setChilled(True)
        self.board.waterEffects.turnOff()
        self.board.balls[ballIndex].setZone(1)
        self.board.display.show(Localizer.ppBoneBrigWelcome)
        self.start()

    def boneBrigEnterTimer(self, ballIndex, args):
        self.board.dialogueMgr.playDialogue('WelcomeBrig')
        if not self.seenTutorial:
            self.ballIndex = ballIndex
            self.intro(ballIndex)
            self.seenTutorial = True
            return
        if self.board.fromPalace == True:
            self.board.display.playTimer.playing()
        self.board.bumpManager.enable()
        self.board.balls[ballIndex].setChilled(False)
        sgode.pyode.dBodyEnable(self.board.balls[ballIndex].body)
        sgode.pyode.dGeomEnable(self.board.balls[ballIndex].geom)
        self.board.pirateSounds['PiratePinball_BallSink'].play()
        self.board.pbTaskMgr.doMethodLater(1, self.putDownGate, 'putDownGate')

    def putDownGate(self, taskInstance=None):
        gateMovement = Sequence(name='gateMovement')
        gateMovement.append(self.gate.hprInterval(0.5, Point3(0.0, 0.0, 0.0), blendType='easeInOut'))
        gateMovement.start()
        self.board.boardObjects['GateDrop'].restore()

    def boneBrigExitIn(self, ballIndex, args):
        self.board.myTransition.fadeOut(1.5)
        self.board.pbTaskMgr.doMethodLater(1.5, self.resetFromBoneBrig, 'resetFromBoneBrig', [ballIndex])

    def resetFromBoneBrig(self, ballIndex):
        self.board.boatModel.reparentTo(render)
        self.board.brigModel.reparentTo(hidden)
        self.board.deactivateBall(ballIndex)
        self.board.changeToZone(0)
        self.board.balls[ballIndex].setZone(0)
        self.board.myTransition.fadeIn(1.5)
        self.board.setCameraPosition('main')
        self.hideFlippers()
        base.setBackgroundColor(0.3, 0.3, 0.7)
        self.board.waterEffects.turnOn()

    def boneBrigExitTimer(self, ballIndex, args):
        self.board.boardObjects['UberRoof'].restore()
        self.board.pauseBalls(False)
        if self.skeletonsFreed == 4:
            self.board.errands['MultiBall'].start(permission=1)
        elif self.skeletonsFreed == 5:
            self.board.errands['MultiBall'].start(permission=2)
        else:
            self.board.errands['CrowCannon'].start()
            self.board.errands['TopDeck'].openUpRamp()
            self.board.errands['CannonArea'].openCannon()

    def loopIt(self, number):
        self.skeletonModels[number[0]].loop('shakefist3')

    def bumperHit(self, ballIndex, args):
        self.skeletonStatus[args[0] - 1] = self.skeletonStatus[(args[0] - 1)] + 1
        if self.skeletonStatus[(args[0] - 1)] > 2:
            self.skeletonStatus[args[0] - 1] = 0
        notAllGreen = False
        for i in range(0, 3):
            if self.skeletonStatus[i] < 2:
                notAllGreen = True

        if self.skeletonStatus[(args[0] - 1)] == 0:
            self.board.beacons[('BBBarrel%d' % args[0])].setState(Beacon.OFF)
            self.skeletonModels[(args[0] - 1)].stop()
            backdown = Sequence(name='backdown0%d' % args[0])
            backdown.append(self.skeletonModels[(args[0] - 1)].actorInterval('hit2', playRate=-1.0, startFrame=20, endFrame=8))
            backdown.append(self.skeletonModels[(args[0] - 1)].actorInterval('hit1', playRate=-1.0, startFrame=7, endFrame=0))
            backdown.append(Func(self.skeletonModels[(args[0] - 1)].setColor, VBase4(1, 1, 1, 0)))
            backdown.start()
        elif self.skeletonStatus[(args[0] - 1)] == 1:
            self.board.pirateSounds[('BoneBrig_SkeletonEmerge%d' % args[0])].play()
            self.board.beacons[('BBBarrel%d' % args[0])].setCurrentOnState(0)
            self.board.beacons[('BBBarrel%d' % args[0])].setState(Beacon.ON)
            self.skeletonModels[(args[0] - 1)].stop()
            self.skeletonModels[(args[0] - 1)].setColor(1, 1, 1, 1)
            backup = Sequence(name='backup1%d' % args[0])
            backup.append(self.skeletonModels[(args[0] - 1)].actorInterval('hit1'))
            backup.append(Func(self.makeSkeletonSolid, args[0] - 1))
            backup.start()
        elif self.skeletonStatus[(args[0] - 1)] == 2:
            self.board.pirateSounds[('BoneBrig_IrateSkeleton%d' % args[0])].play()
            self.board.beacons[('BBBarrel%d' % args[0])].setCurrentOnState(1)
            self.board.beacons[('BBBarrel%d' % args[0])].setState(Beacon.ON)
            self.skeletonModels[(args[0] - 1)].stop()
            self.makeSkeletonSolid(args[0] - 1)
            if notAllGreen:
                shakeFist = Sequence(name='shakeFist2%d' % args[0])
                shakeFist.append(self.skeletonModels[(args[0] - 1)].actorInterval('hit2'))
                shakeFist.append(Func(self.loopIt, [args[0] - 1]))
                shakeFist.start()
        if notAllGreen:
            return
        self.skeletonStatus[args[0] - 1] = 3
        self.skeletonModels[(args[0] - 1)].stop()
        self.skeletonModels[(args[0] - 1)].play('hit3')
        for i in range(1, 4):
            if self.skeletonStatus[(i - 1)] != 3:
                self.board.beacons[('BBBarrel%d' % i)].setState(Beacon.OFF)
                self.skeletonModels[(i - 1)].stop()
                backdown = Sequence(name='backdownQ%d' % i)
                backdown.append(self.skeletonModels[(i - 1)].actorInterval('hit2', playRate=-1.0, startFrame=20, endFrame=8))
                backdown.append(self.skeletonModels[(i - 1)].actorInterval('hit1', playRate=-1.0, startFrame=7, endFrame=0))
                backdown.append(Func(self.skeletonModels[(i - 1)].setColor, VBase4(1, 1, 1, 0)))
                backdown.start()
                self.skeletonStatus[i - 1] = 0

        self.totalSkeletonsFreed = self.totalSkeletonsFreed + 1
        self.skeletonsFreed = self.skeletonsFreed + 1
        self.board.boardObjects[('BBBumper%d' % args[0])].drop()
        barrelFade = Sequence(name='barrelFade%d' % args[0])
        barrelPos = self.board.boardObjects[('BBBumper%d' % args[0])].getPos()
        explodePos = VBase3(barrelPos[0], barrelPos[1] - 1, barrelPos[2] + 0.8)
        self.myExplosionManager.startHere(explodePos)
        self.board.pirateSounds['PiratePinball_Explode'].play()
        bothFade = []
        bothFade.append(LerpColorInterval(self.board.boardObjects[('BBBumper%d' % args[0])], 0.25, Vec4(1, 1, 1, 0), blendType='easeOut'))
        bothFade.append(LerpColorInterval(self.skeletonModels[(args[0] - 1)], 0.25, Vec4(1, 1, 1, 0), blendType='easeOut'))
        barrelFade.append(Parallel(*bothFade))
        barrelFade.start()
        if self.skeletonsFreed == 1:
            self.board.display.show(Localizer.ppBoneBrigOneSkeleton)
            self.board.pbTaskMgr.doMethodLater(0.5, self.board.dialogueMgr.playDialogue, 'playOnlyTwo', ['OnlyTwo'])
        elif self.skeletonsFreed == 2:
            self.board.display.show(Localizer.ppBoneBrigTwoSkeleton)
            self.board.pbTaskMgr.doMethodLater(0.5, self.board.dialogueMgr.playDialogue, 'playOneMore', ['OneMore'])
        elif self.skeletonsFreed == 3:
            self.board.display.show(Localizer.ppBoneBrigThreeSkeleton)
            gateMovement = Sequence(name='gateMovement')
            gateMovement.append(self.gate.hprInterval(0.5, Point3(0.0, -90.0, 0.0), blendType='easeInOut'))
            gateMovement.start()
            self.board.dialogueMgr.playDialogue('Escape')
            self.board.beacons['BBSkull'].setState(Beacon.BLINK)
            self.board.boardObjects['GateDrop'].drop()

    def makeSkeletonSolid(self, skelNumber):
        if self.skeletonStatus[skelNumber] != 3:
            self.skeletonModels[skelNumber].setColor(VBase4(1, 1, 1, 1))

    def makeSkullBall(self):
        ballModel = loader.loadModelCopy('piratepinball/art/bonebrig/SkullBall')
        ballModel.reparentTo(render)
        ballMaterial = Material()
        ballMaterial.setSpecular(VBase4(1, 1, 1, 1))
        ballMaterial.setShininess(30.0)
        ballModel.setMaterial(ballMaterial)
        ballModel.setTransparency(1)
        skull = ballModel.find('**/skull')
        skull.setBin('flat', 100)
        ballModel.setColor(0.2, 0.7, 0.2, 0.3)
        skull.setColor(1, 1, 1, 1)
        return ballModel

    def resetCages(self, ignore=None):
        self.leftCage.setPos(self.lcPos)
        self.rightCage.setPos(self.rcPos)
        self.leftSkullBall.reparentTo(self.leftCage)
        self.leftSkullBall.setPos(-0.23, 0.1, 0.5)
        self.rightSkullBall.reparentTo(self.rightCage)
        self.rightSkullBall.setPos(0.25, 0.1, 0.5)
        self.leftCage.setColor(1, 1, 1, 1)
        self.rightCage.setColor(1, 1, 1, 1)