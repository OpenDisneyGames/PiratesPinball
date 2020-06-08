# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: CrowCannon.py
from pinballbase.PinballErrand import PinballErrand
from .PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
import Localizer
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup

class CrowCannon(PinballErrand):
    __module__ = __name__

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.bonusGift = self.board.pointValues['CrowCannonParrotBonus']
        self.myZone = 0
        base.enableParticles()
        self.ballMode = 0
        self.parrotsHit = 0
        self.seenTutorial = False
        self.crowCannonTutorialSequence = None
        self.cameraCrowMovement = None
        self.board.beacons['CrowBeacons1'] = Beacon(board.boatModel.find('**/baconplates:pPlane40'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png')
        self.board.beacons['CrowBeacons2'] = Beacon(board.boatModel.find('**/baconplates:pPlane41'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png')
        self.board.beacons['CrowBeacons3'] = Beacon(board.boatModel.find('**/baconplates:pPlane42'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png')
        self.lever = board.boatModel.find('**/lever')
        self.torch = board.boatModel.find('**/torch')
        self.torch.setPos(0, 0, -0.03)
        self.crowCannon = loader.loadModelCopy('piratepinball/art/main_ship/rearCannon')
        self.crowCannon.setScale(11)
        self.crowCannon.setPos(3.5, 14, 2)
        self.crowCannon.setHpr(-95.0, 0.0, 0.0)
        self.crowCannon.reparentTo(render)
        self.fuseSpline = Actor('piratepinball/art/main_ship/CannonFuse', {'light': 'piratepinball/art/main_ship/CannonFuse'})
        self.fuseSpline.setScale(12)
        self.fuseSpline.setPos(4.5, 14, 2.4)
        self.fuseSpline.setHpr(-95.0, 0.0, 0.0)
        self.fuseSpline.reparentTo(render)
        self.sparkNode = render.attachNewNode('sparkNode')
        self.fuseSpline.exposeJoint(self.sparkNode, 'modelRoot', 'fuseJoint')
        self.sparkNode.reparentTo(self.fuseSpline)
        board.boatModel.find('**/rearCannonFuse').reparentTo(hidden)
        self.okToFire = False
        self.annoyingFlat = self.board.boatModel.find('**/baconplates:pPlane46')
        self.annoyingFlat.setBin('flat', 10)
        return

    def finishSetup(self):
        self.torchFire = self.board.refPoints['TorchFire']
        self.fireParticles()

    def wake(self):
        self.fireParticles()
        self.crowCannon.reparentTo(render)
        self.fuseSpline.reparentTo(render)

    def sleep(self):
        self.crowCannon.reparentTo(hidden)
        self.fuseSpline.reparentTo(hidden)
        if self.fireParts != None:
            self.fireParts.cleanup()
            self.fireParts = None
        if self.cameraCrowMovement != None and not self.cameraCrowMovement.isStopped():
            self.cameraCrowMovement.finish()
        if self.crowCannonTutorialSequence != None and not self.crowCannonTutorialSequence.isStopped():
            self.crowCannonTutorialSequence.finish()
        ivalMgr.finishIntervalsMatching('leverMovement')
        ivalMgr.finishIntervalsMatching('cannonMovement')
        return

    def destroy(self):
        self.crowCannon.removeNode()
        self.fuseSpline.removeNode()
        if self.fireParts != None:
            self.fireParts.cleanup()
            self.fireParts.removeNode()
            self.fireParts = None
        if self.cameraCrowMovement != None and not self.cameraCrowMovement.isStopped():
            self.cameraCrowMovement.finish()
        if self.crowCannonTutorialSequence != None and not self.crowCannonTutorialSequence.isStopped():
            self.crowCannonTutorialSequence.finish()
        ivalMgr.finishIntervalsMatching('leverMovement')
        ivalMgr.finishIntervalsMatching('cannonMovement')
        PinballErrand.destroy(self)
        return

    def changeToZone(self, zoneNumber):
        pass

    def reset(self, time=1):
        self.torch.setPos(0, 0, -0.03)
        self.torchFire.setPos(5.2, 12.7, 1.3)
        self.cannonState = 0
        for i in range(1, 4):
            self.board.beacons[('CrowBeacons%d' % i)].setState(Beacon.OFF)

        cannonMovement = Sequence(name='cannonMovement')
        cannonMovement.append(self.crowCannon.hprInterval(time, Point3(-95.0, 0.0, 0.0), blendType='easeInOut'))
        cannonMovement.start()
        leverMovement = Sequence(name='leverMovement')
        leverMovement.append(self.lever.hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeOut'))
        leverMovement.start()
        self.board.boardObjects['LeverTriggerDrop'].restore()

    def refresh(self, time=1):
        self.torch.setPos(0, 0, -0.03)
        self.torchFire.setPos(5.2, 12.7, 1.3)
        resetElements = True
        if self.cannonState == 0 and self.board.ballsOnTable == 1:
            self.board.beacons['CrowBeacons3'].setState(Beacon.BLINK)
            self.board.beacons['CrowBeacons1'].setState(Beacon.OFF)
            self.board.beacons['CrowBeacons2'].setState(Beacon.OFF)
        else:
            if self.cannonState == 0 and self.board.ballsOnTable > 1:
                for i in range(1, 4):
                    self.board.beacons[('CrowBeacons%d' % i)].setState(Beacon.OFF)

            elif self.cannonState == 0.5 or self.cannonState == 1:
                self.board.beacons['CrowBeacons3'].setState(Beacon.OFF)
                self.board.beacons['CrowBeacons1'].setState(Beacon.BLINK)
                self.board.beacons['CrowBeacons2'].setState(Beacon.OFF)
            elif self.cannonState == 2:
                resetElements = False
                self.board.beacons['CrowBeacons1'].setState(Beacon.OFF)
                self.board.beacons['CrowBeacons2'].setState(Beacon.BLINK)
                self.board.beacons['CrowBeacons3'].setState(Beacon.OFF)
            if resetElements:
                cannonMovement = Sequence(name='cannonMovement')
                cannonMovement.append(self.crowCannon.hprInterval(time, Point3(-95.0, 0.0, 0.0), blendType='easeInOut'))
                cannonMovement.start()
                leverMovement = Sequence(name='leverMovement')
                leverMovement.append(self.lever.hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeOut'))
                leverMovement.start()
            else:
                leverMovement = Sequence(name='leverMovement')
                leverMovement.append(self.lever.hprInterval(time, Point3(0.0, 0.0, -30.0), blendType='easeOut'))
                leverMovement.start()
                cannonMovement = Sequence(name='cannonMovement')
                cannonMovement.append(self.crowCannon.hprInterval(time, Point3(-95, 0, -80), blendType='easeInOut'))
                cannonMovement.start()

    def start(self):
        self.cannonState = 0
        self.refresh()

    def pause(self):
        self.pauseTutorial()
        if self.cameraCrowMovement != None and self.cameraCrowMovement.isPlaying():
            self.cameraCrowMovement.pause()
        return

    def resume(self):
        if self.cameraCrowMovement != None and self.cameraCrowMovement.getState() == CInterval.SPaused:
            self.cameraCrowMovement.resume()
        return

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        if self.cannonState == 0:
            return Localizer.ppCrowCannonLoad
        elif self.cannonState == 0.5 or self.cannonState == 1:
            return Localizer.ppCrowCannonAim
        else:
            return Localizer.ppCrowCannonLight
        return

    def getName(self):
        return 'CrowCannon'

    def getBonus(self):
        bonus = self.parrotsHit
        self.parrotsHit = 0
        return (Localizer.ppCrowCannonBonus, bonus, self.bonusGift)

    def crowCannonIntroIn(self, ballIndex, args):
        if self.seenTutorial:
            print('why are you here?!?!')
            return
        self.tutorial()

    def tutorial(self, interactiveMode=True):
        self.board.setInTutorialMode(True)
        self.board.proxPoints['CrowCannonIntro'].setActive(False)
        self.seenTutorial = True
        self.board.setCameraPosition('crowCannonTeach', time=1.5)
        self.board.pauseBalls()
        self.board.beacons['CrowBeacons3'].setState(Beacon.OFF)
        self.crowCannonTutorialSequence = Sequence(name='crowCannonTutorialSequence')
        self.crowCannonTutorialSequence.append(Wait(1.5))
        self.crowCannonTutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppCrowCannonInstructions1, 0))
        self.crowCannonTutorialSequence.append(Func(self.board.playDialogue, 'ShootToLoad'))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons3'].setState, Beacon.BLINK))
        if interactiveMode:
            self.crowCannonTutorialSequence.append(Func(self.pauseTutorial))
            self.crowCannonTutorialSequence.append(Wait(0.2))
        else:
            self.crowCannonTutorialSequence.append(Wait(2))
        self.crowCannonTutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppCrowCannonInstructions2, 0))
        self.crowCannonTutorialSequence.append(Func(self.board.playDialogue, 'ShootToAim'))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons3'].setState, Beacon.OFF))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons1'].setState, Beacon.BLINK))
        if interactiveMode:
            self.crowCannonTutorialSequence.append(Func(self.pauseTutorial))
            self.crowCannonTutorialSequence.append(Wait(0.2))
        else:
            self.crowCannonTutorialSequence.append(Wait(2))
        self.crowCannonTutorialSequence.append(Func(self.board.display.showInstructions, Localizer.ppCrowCannonInstructions3, 0))
        self.crowCannonTutorialSequence.append(Func(self.board.playDialogue, 'ShootToFire'))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons1'].setState, Beacon.OFF))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons2'].setState, Beacon.BLINK))
        if interactiveMode:
            self.crowCannonTutorialSequence.append(Func(self.pauseTutorial))
            self.crowCannonTutorialSequence.append(Wait(0.2))
        else:
            self.crowCannonTutorialSequence.append(Wait(2))
        self.crowCannonTutorialSequence.append(Func(self.board.display.setHudState, 1))
        self.crowCannonTutorialSequence.append(Func(self.board.setCameraPosition, 'main', 1.5))
        self.crowCannonTutorialSequence.append(Wait(1.5))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons3'].setState, Beacon.OFF))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons3'].setState, Beacon.BLINK))
        self.crowCannonTutorialSequence.append(Func(self.board.beacons['CrowBeacons2'].setState, Beacon.OFF))
        self.crowCannonTutorialSequence.append(Func(self.board.pauseBalls, False))
        self.crowCannonTutorialSequence.append(Func(self.board.setInTutorialMode, False))
        for flipper in self.board.allFlippers:
            if flipper.name == 'RightMidFlipper':
                break

        self.crowCannonTutorialSequence.append(Func(self.board.flipperFlash, [flipper]))
        self.crowCannonTutorialSequence.start()

    def pauseTutorial(self):
        if self.crowCannonTutorialSequence != None and self.crowCannonTutorialSequence.isPlaying():
            self.crowCannonTutorialSequence.pause()
            self.board.display.showContinue(True)
        return

    def continueOn(self):
        if self.crowCannonTutorialSequence != None and not self.crowCannonTutorialSequence.isStopped():
            self.crowCannonTutorialSequence.resume()
            self.board.display.showContinue(False)
        return

    def skip(self):
        if self.crowCannonTutorialSequence != None and not self.crowCannonTutorialSequence.isStopped():
            dialogueEnabled = False
            if self.board.dialogueMgr.enabled():
                dialogueEnabled = True
            self.board.setDialogueEnabled(False)
            self.crowCannonTutorialSequence.pause()
            self.crowCannonTutorialSequence.finish()
            for flipper in self.board.allFlippers:
                if flipper.name == 'RightMidFlipper':
                    break

            self.board.flipperFlash([flipper])
            self.board.setCameraPosition('main', 0)
            self.board.beacons['CrowBeacons3'].setState(Beacon.OFF)
            self.board.beacons['CrowBeacons2'].setState(Beacon.OFF)
            self.board.beacons['CrowBeacons1'].setState(Beacon.OFF)
            self.board.beacons['CrowBeacons3'].setState(Beacon.BLINK)
            self.board.pbTaskMgr.doMethodLater(0.3, self.board.setDialogueEnabled, 'resetdialogueenabled', [dialogueEnabled])
            self.board.pauseBalls(False)
            self.board.setInTutorialMode(False)
            self.board.display.showContinue(False)
            self.board.display.hudElements['leftInstructions1']['text'] = Localizer.pDisplayExitInstructions
        return

    def getCannonState(self):
        if self.cannonState == 0.5:
            return 1
        return self.cannonState

    def crowCannonIn(self, ballIndex, args):
        if self.cannonState == 1 or self.cannonState == 0.5:
            self.board.display.show(Localizer.ppCrowCannonAim)
            self.board.beacons['CrowBeacons3'].setState(Beacon.ONCE)
            self.board.updateScore(self.board.pointValues['CrowCannonNotLit'], 'CrowCannonNotLit')
            self.board.pirateSounds['CrowCannon_Success'].play()
            return
        if self.cannonState == 2:
            self.board.display.show(Localizer.ppCrowCannonLight)
            self.board.beacons['CrowBeacons3'].setState(Beacon.ONCE)
            self.board.updateScore(self.board.pointValues['CrowCannonNotLit'], 'CrowCannonNotLit')
            self.board.pirateSounds['CrowCannon_Success'].play()
            return
        ballInHatch = False
        for bino in self.board.errands['DeckHatches'].ballInNotOut:
            if len(bino) != 0:
                ballInHatch = True

        if self.board.ballsOnTable > 1 or self.board.errands['SkullAlleys'].ballsInSave != 0 or ballInHatch:
            self.board.display.show(Localizer.ppCrowCannonMessage)
            self.board.beacons['CrowBeacons3'].setState(Beacon.ONCE)
            self.board.updateScore(self.board.pointValues['CrowCannonCannonBonus'], 'CrowCannonCannonBonus')
            self.board.pirateSounds['CrowCannon_Success'].play()
            return
        self.cannonState = 0.5
        self.board.beacons['CrowBeacons3'].setState(Beacon.OFF)
        self.board.beacons['CrowBeacons1'].setState(Beacon.BLINK)
        self.board.display.show(Localizer.ppCrowCannonLoaded)
        self.board.dialogueMgr.playDialogue('CannonLock')
        self.board.pirateSounds['PiratePinball_BallSink'].play()
        self.ballMode = self.board.deactivateBall(ballIndex)
        self.board.boardObjects['LeverTriggerDrop'].drop()

    def crowCannonTimer(self, ballIndex, args):
        if self.cannonState != 0.5:
            return
        self.cannonState = 1
        self.board.display.show(Localizer.ppCrowCannonAimTheCannon)
        self.board.dropBall(False)

    def cannonSwitchIn(self, ballIndex, args):
        if self.cannonState == 0 or self.cannonState == 0.5:
            self.board.display.show(Localizer.ppCrowCannonLoad)
            self.board.beacons['CrowBeacons1'].setState(Beacon.ONCE)
            self.board.pirateSounds['CrowCannon_Success'].play()
            return
        if self.cannonState == 2:
            self.board.display.show(Localizer.ppCrowCannonLight)
            self.board.beacons['CrowBeacons1'].setState(Beacon.ONCE)
            self.board.pirateSounds['CrowCannon_Success'].play()
            return
        self.cannonState = 2
        self.board.display.show(Localizer.ppCrowCannonAimed)
        self.board.dialogueMgr.playDialogue('Fire')
        leverMovement = Sequence(name='leverMovement')
        leverMovement.append(self.lever.hprInterval(0.5, Point3(0.0, 0.0, -30.0), blendType='easeOut'))
        leverMovement.start()
        self.board.beacons['CrowBeacons1'].setState(Beacon.OFF)
        self.board.beacons['CrowBeacons2'].setState(Beacon.BLINK)
        cannonMovement = Sequence(name='cannonMovement')
        cannonMovement.append(self.crowCannon.hprInterval(3, Point3(-95, 0, -80), blendType='easeInOut'))
        cannonMovement.start()
        self.board.pirateSounds['PiratePinball_Bell1'].play()

    def cannonSwitchTimer(self, ballIndex, args):
        if self.cannonState != 2:
            return
        self.board.display.show(Localizer.ppCrowCannonLight)

    def torchIn(self, ballIndex, args):
        if self.cannonState == 0:
            self.board.display.show(Localizer.ppCrowCannonLoad)
            self.board.beacons['CrowBeacons2'].setState(Beacon.ONCE)
            return
        if self.okToFire:
            return
        self.board.errands['TopDeck'].closeRamp()
        self.board.errands['CannonArea'].closeCannon()
        self.torch.setPos(0, 0, 0.03)
        self.torchFire.setPos(5.2, 12.7, 2)
        self.okToFire = True
        self.board.display.show(Localizer.ppCrowCannonFuseLit)
        self.board.pirateSounds['PiratePinball_Bell2'].play()
        self.board.proxPoints['Cannon Switch'].setActive(False)
        self.board.beacons['CrowBeacons2'].setState(Beacon.BLINK)
        self.board.beacons['CrowBeacons1'].setState(Beacon.OFF)
        if self.cannonState == 2:
            self.board.balls[ballIndex].setChilled(True)
            self.board.pbTaskMgr.doMethodLater(10, self.board.balls[ballIndex].setChilled, 'unchillball%d' % ballIndex, [False])
            for b in self.board.balls:
                if b.active:
                    sgode.pyode.dBodyDisable(b.body)
                    sgode.pyode.dGeomDisable(b.geom)

            self.board.dialogueMgr.playDialogue('WellDone')
            self.board.musicMgr.playJingle('Music_Success1', musicContinue=True)
            self.board.bumpManager.disable()
            self.cameraCrowMovement = Sequence(name='cameraCrowMovement')
            camera1stMove = []
            camera1stMove.append(camera.posInterval(3, self.board.getCameraPos('midCrow'), blendType='easeInOut'))
            camera1stMove.append(camera.hprInterval(3, self.board.getCameraHpr('midCrow'), blendType='easeInOut'))
            camera1stMove.append(LerpColorInterval(self.board.rearSail, 3, Vec4(1, 1, 1, 0), blendType='easeInOut'))
            camera1stMove.append(LerpColorInterval(self.board.frontSail, 3, Vec4(1, 1, 1, 0.2), blendType='easeInOut'))
            self.cameraCrowMovement.append(Parallel(*camera1stMove))
            camera2ndMove = []
            camera2ndMove.append(camera.posInterval(2.5, self.board.getCameraPos('crow'), blendType='easeInOut'))
            camera2ndMove.append(camera.hprInterval(3, self.board.getCameraHpr('crow'), blendType='easeInOut'))
            camera2ndMove.append(self.crowCannon.hprInterval(3, Point3(-95.0, 0.0, 0.0), blendType='easeInOut'))
            camera2ndMove.append(self.lever.hprInterval(0.5, Point3(0.0, 0.0, 0.0), blendType='easeOut'))
            self.cameraCrowMovement.append(Parallel(*camera2ndMove))
            self.cameraCrowMovement.start()
        else:
            self.board.dialogueMgr.playDialogue('NiceShot')
            self.board.musicMgr.playJingle('Music_Success2', musicContinue=True)

    def torchTimer(self, ballIndex, args):
        if self.cannonState == 0 or self.cannonState == 0.5:
            return
        if not self.okToFire:
            return
        self.okToFire = False
        self.board.display.show(Localizer.ppCrowCannonFire)
        self.torch.setPos(0, 0, -0.03)
        self.torchFire.setPos(5.2, 12.7, 1.3)
        self.board.proxPoints['CrowCannon'].setActive(False)
        self.board.boardObjects['LeverTriggerDrop'].restore()
        self.board.beacons['CrowBeacons2'].setState(Beacon.OFF)
        ball = None
        self.board.pirateSounds['PiratePinball_Explode'].setVolume(1)
        self.board.pirateSounds['PiratePinball_Explode'].play()
        if self.cannonState == 1:
            ball = self.board.dropBall(False, tryNumber=0, bx=3.37, by=13.55, bz=0.8, ballMode=self.ballMode)
            sgode.pyode.dBodySetLinearVel(ball.body, -1.5, -25, 0)
            self.board.pbTaskMgr.doMethodLater(1, self.reactivateCannon, 'reactivatecannon')
        elif self.cannonState == 2:
            ball = self.board.dropBall(False, tryNumber=0, bx=3.37, by=13.55, bz=3, ballMode=self.ballMode)
            self.board.lostBallMgr.dontWorry()
            self.board.boardObjects['UberRoof'].drop()
            sgode.pyode.dBodySetLinearVel(ball.body, -2.4, 6, 34)
            self.board.pbTaskMgr.doMethodLater(2, self.changeGravity, 'changegravity')
        if ball == None:
            print(' --- ERROR : Bad cannon error: cannonState = %d, ballsOnTable = %d' % (self.cannonState, self.board.ballsOnTable))
            self.cannonState = 0
            return
        ball.update()
        self.cannonState = 0
        return

    def reactivateCannon(self, taskInstance=None):
        self.board.proxPoints['CrowCannon'].setActive(True)
        self.board.proxPoints['Cannon Switch'].setActive(True)

    def changeGravity(self, taskInstance=None):
        sgode.pyode.dWorldSetGravity(self.board.odeWorld, 0, 0, self.board.gravZ - 30)
        self.board.proxPoints['CrowCannon'].setActive(True)
        self.board.proxPoints['Cannon Switch'].setActive(True)
        self.board.boardObjects['UberRoof'].restore()
        self.board.lostBallMgr.worry()

    def brigBall(self, ballIndex, args):
        sgode.pyode.dWorldSetGravity(self.board.odeWorld, self.board.gravX, self.board.gravY, self.board.gravZ)
        self.board.display.show(Localizer.ppCrowCannonDown)
        self.board.updateScore(self.board.pointValues['CrowCannonBrigEnter'], 'CrowCannonBrigEnter')
        self.board.myTransition.fadeOut(1.5)

    def crowTimer(self, ballIndex, args):
        print('going to bone brig')
        self.board.changeToZone(1)
        self.board.boatModel.reparentTo(hidden)
        self.board.brigModel.reparentTo(render)
        base.setBackgroundColor(0, 0, 0)
        self.board.setCameraPosition('boneBrig')
        ppos = self.board.proxPoints['BoneBrigEnter'].getPos()
        self.board.balls[ballIndex].setODEPos(ppos[0], ppos[1], ppos[2])
        sgode.pyode.dBodySetLinearVel(self.board.balls[ballIndex].body, 0, 0, 0)
        sgode.pyode.dBodyDisable(self.board.balls[ballIndex].body)
        self.board.balls[ballIndex].update()
        self.board.myTransition.fadeIn(1.5)

    def sparkParticles(self):
        self.sparkParts = ParticleEffect.ParticleEffect(name='Sparks')
        self.sparkParts.reset()
        self.sparkParts.setPos(0.0, 0.0, 0.0)
        self.sparkParts.setHpr(0.0, 0.0, 0.0)
        self.sparkParts.setScale(1, 1, 1)
        p0 = Particles.Particles('particles-1')
        p0.setFactory('PointParticleFactory')
        p0.setRenderer('SparkleParticleRenderer')
        p0.setEmitter('SphereVolumeEmitter')
        p0.setPoolSize(128)
        p0.setBirthRate(0.02)
        p0.setLitterSize(5)
        p0.setLitterSpread(0)
        p0.setSystemLifespan(0.0)
        p0.setLocalVelocityFlag(1)
        p0.setSystemGrowsOlderFlag(0)
        p0.factory.setLifespanBase(0.5)
        p0.factory.setLifespanSpread(0.0)
        p0.factory.setMassBase(1.0)
        p0.factory.setMassSpread(0.0)
        p0.factory.setTerminalVelocityBase(400.0)
        p0.factory.setTerminalVelocitySpread(0.0)
        p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        p0.renderer.setUserAlpha(1.0)
        p0.renderer.setCenterColor(Vec4(1.0, 0.0, 0.0, 1.0))
        p0.renderer.setEdgeColor(Vec4(1.0, 1.0, 0.0, 1.0))
        p0.renderer.setBirthRadius(0.1)
        p0.renderer.setDeathRadius(0.1)
        p0.renderer.setLifeScale(SparkleParticleRenderer.SPNOSCALE)
        p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        p0.emitter.setAmplitude(1.0)
        p0.emitter.setAmplitudeSpread(0.0)
        p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        p0.emitter.setRadius(0.05)
        self.sparkParts.addParticles(p0)
        f0 = ForceGroup.ForceGroup('1')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, 6.0), 1.0, 0)
        force0.setActive(1)
        f0.addForce(force0)
        self.sparkParts.addForceGroup(f0)
        self.sparkParts.setBin('flat', 1)
        t = Sequence(Func(self.sparkParts.start, self.sparkNode, render, name='Sparks'))
        t.start()

    def fireParticles(self):
        self.fireParts = ParticleEffect.ParticleEffect(name='TorchFire')
        self.fireParts.reset()
        self.fireParts.setPos(0.0, 0.0, 0.0)
        self.fireParts.setHpr(0.0, 0.0, 0.0)
        self.fireParts.setScale(1.0, 1.0, 1.0)
        p0 = Particles.Particles('particles-1')
        p0.setFactory('PointParticleFactory')
        p0.setRenderer('SpriteParticleRenderer')
        p0.setEmitter('SphereVolumeEmitter')
        p0.setPoolSize(8)
        p0.setBirthRate(0.1)
        p0.setLitterSize(2)
        p0.setLitterSpread(1)
        p0.setSystemLifespan(0.0)
        p0.setLocalVelocityFlag(1)
        p0.setSystemGrowsOlderFlag(0)
        p0.factory.setLifespanBase(0.3)
        p0.factory.setLifespanSpread(0.0)
        p0.factory.setMassBase(1.0)
        p0.factory.setMassSpread(0.0)
        p0.factory.setTerminalVelocityBase(10.0)
        p0.factory.setTerminalVelocitySpread(0.0)
        p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        p0.renderer.setUserAlpha(1.0)
        p0.renderer.setTexture(loader.loadTexture('piratepinball/art/misc/textures/flame3.png'))
        p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        p0.renderer.setXScaleFlag(0)
        p0.renderer.setYScaleFlag(0)
        p0.renderer.setAnimAngleFlag(0)
        p0.renderer.setInitialXScale(0.02)
        p0.renderer.setFinalXScale(0.02)
        p0.renderer.setInitialYScale(0.02)
        p0.renderer.setFinalYScale(0.02)
        p0.renderer.setNonanimatedTheta(0.0)
        p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        p0.renderer.setAlphaDisable(0)
        p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        p0.emitter.setAmplitude(1.0)
        p0.emitter.setAmplitudeSpread(0.0)
        p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.8))
        p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        p0.emitter.setRadius(0.01)
        self.fireParts.addParticles(p0)
        f0 = ForceGroup.ForceGroup('jitter')
        force0 = LinearJitterForce(1.0, 0)
        force0.setActive(1)
        f0.addForce(force0)
        self.fireParts.addForceGroup(f0)
        self.fireParts.setBin('transparent', 100)
        t = Sequence(Func(self.fireParts.start, self.torchFire, render, name='TorchFire'))
        t.start()