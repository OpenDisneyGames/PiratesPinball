# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: PiratePinball.py
import direct.directbase.DirectStart
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
import random, sys, time
from pandac.PandaModules import *
from pinballbase.odeConstructs import *
from pinballbase.PinballElements import *
from pinballbase.fpsmeter import *
from .PirateDisplay import PirateDisplay
from direct.showbase.Transitions import *
import sgode.pyode, Localizer
from pinballbase.ContactParams import *
import pinballbase.PinballErrand, PirateBoard
from pinballbase.Cheater import Cheater
from .PirateWaterEffects import PirateWaterEffects
from pinballbase.LocalizerHelper import LocalizerHelper
from .TreasureChests import TreasureChests
from .SkullAlleys import SkullAlleys
from .DeckHatches import DeckHatches
from .StairCase import StairCase
from .CannonArea import CannonArea
from .CrowCannon import CrowCannon
from .BoneBrig import BoneBrig
from .MultiBall import MultiBall
from .TopDeck import TopDeck
import importlib
EDITMODE = False
DEFAULT_BALL_START_POS = Point3(9.3, 0.9, 0.6)

class PiratePinball(direct.showbase.DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratePinball')
    cheatCodes = False
    BOARDNAME = 'Pirates'

    def __init__(self, fromPalace=False):
        self.fromPalace = fromPalace
        cbm = CullBinManager.getGlobalPtr()
        cbm.addBin('flat', CullBinManager.BTFixed, 25)
        base.mouseInterfaceNode.setPos(-8, 40, -10)
        base.disableMouse()
        base.camLens.setFov(40)
        base.camLens.setFar(400)
        self.boatColor = Vec4(0.36, 0.19, 0, 1)
        self.crowColor = Vec4(0.46, 0.29, 0, 1)
        base.setBackgroundColor(0.3, 0.3, 0.7)
        self.lightAttrib = LightAttrib.makeAllOff()
        self.ambientLight = AmbientLight('ambientLight')
        self.ambientLight.setColor(Vec4(0.1, 0.1, 0.2, 1))
        self.lightAttrib = self.lightAttrib.addLight(self.ambientLight)
        render.attachNewNode(self.ambientLight.upcastToPandaNode())
        self.directionalLight = DirectionalLight('directionalLight')
        self.directionalLight.setColor(Vec4(1.3, 1.3, 1.3, 1))
        self.directionalLight.setDirection(Vec3(2, 3, -4))
        self.lightAttrib = self.lightAttrib.addLight(self.directionalLight)
        render.attachNewNode(self.directionalLight.upcastToPandaNode())
        render.node().setAttrib(self.lightAttrib)
        self.gravX = 0
        self.gravY = -20
        self.gravZ = -32
        self.odeWorld = sgode.pyode.dWorldCreate()
        self.odeSpace = sgode.pyode.dHashSpaceCreate(None)
        self.odeContactGroup = sgode.pyode.dJointGroupCreate(0)
        sgode.pyode.dWorldSetGravity(self.odeWorld, self.gravX, self.gravY, self.gravZ)
        sgode.pyode.dWorldSetCFM(self.odeWorld, 5e-05)
        sgode.pyode.dWorldSetERP(self.odeWorld, 0.5)
        sgode.pyode.dWorldSetContactMaxCorrectingVel(self.odeWorld, 10.0)
        planeGeom = sgode.pyode.dCreatePlane(self.odeSpace, 0, 0, 1, 0)
        sgode.pyode.dGeomSetCategoryBits(planeGeom, GROUND_CATEGORY)
        sgode.pyode.dGeomSetCollideBits(planeGeom, 0)
        self.odeStepLength = 0.008
        self.worldInfo = sgode.pyode.WorldInfo()
        self.worldInfo.world = self.odeWorld
        self.worldInfo.contactGroup = self.odeContactGroup
        setupContactParams(self.worldInfo)
        self.proxPoints = {}
        self.beacons = {}
        self.triggers = {}
        self.pointValues = {}
        self.boardObjects = {}
        self.errands = {}
        self.cameraPositions = {}
        self.refPoints = {}
        self.pirateSounds = {}
        self.pirateDialogue = {}
        self.pirateMusic = {}
        self.movables = []
        self.balls = []
        self.leftFlippers = []
        self.rightFlippers = []
        self.gamePaused = False
        self.currentCameraPosition = ''
        self.geomsEnabled = True
        self.currentZone = 0
        self.myScore = 0
        self.highestScoreEver = 0
        self.flipperTimeUp = -1
        self.showAllStatus = -1
        self.inTutorialMode = False
        self.nowletgoShowing = False
        self.texturesOn = True
        self.flipperNoise = True
        self.renderOn = True
        self.sentScoreAlready = True
        self.difficultlyLevelAdvanced = False
        self.ballsOnTable = 0
        self.launchHatchMovement = None
        self.cameraMovement = None
        self.myTransition = Transitions(base.loader)
        self.dialogueMgr = None
        self.musicMgr = None
        self.scoreFile = None
        self.scoreWrite = False
        self.gameStartTime = 0
        self.flipperFlashSequence = None
        if base.direct:
            self.hideCursor = False
        else:
            self.hideCursor = True
        self.mainWinForeground = 1
        self.leftSlingshotOn = False
        self.rightSlingshotOn = False
        self.plungerPower = 0
        self.plungerDepressed = False
        self.ballDensity = 100.0
        self.loadCameraAngles()
        self.loadSounds()
        self.loadPoints()
        self.createPlunger()
        self.createBoat()
        self.waterEffects = PirateWaterEffects(self)
        self.loadErrands()
        self.createGate()
        self.createCrows()
        self.createFlippers()
        self.createSlingshots()
        self.display = PirateDisplay(self)
        self.display.setHudState(0)
        self.lostBallMgr = LostBallManager(self)
        self.pbTaskMgr = PinballDelayedCallManager()
        self.createBoardFromEditorFile()
        self.credsCheater = Cheater('creds', self.credsCallBack)
        self.musicCheater = Cheater('music', self.musicCallBack)
        self.myBallSaveManager = BallSaveManager(self.beacons['laneBeacon2'])
        for e in list(self.errands.values()):
            e.finishSetup()

        self.bonusManager = BonusManager(self)
        slingshotPeriod = 0.2
        self.slingshotIntervals = {}
        self.leftSlingshotInterval = Sequence(Func(setattr, self, 'leftSlingshotOn', True), Wait(slingshotPeriod), Func(setattr, self, 'leftSlingshotOn', False))
        self.rightSlingshotInterval = Sequence(Func(setattr, self, 'rightSlingshotOn', True), Wait(slingshotPeriod), Func(setattr, self, 'rightSlingshotOn', False))
        if EDITMODE:
            from pinballbase.PinballEditor import PinballEditor
            pe = PinballEditor(self, 'piratepinball/PirateBoard.py')
            self.waterEffects.skyDome.reparentTo(hidden)
        self.setCameraPosition('fireCannon')
        self.myTransition.fadeOut(0)
        self.prepareBoard = Sequence(name='prepareBoard')
        self.prepareBoard.append(Wait(0.8))
        self.prepareBoard.append(Func(self.setCameraPosition, 'main'))
        self.prepareBoard.append(Func(self.myTransition.fadeIn, 1.5))
        self.prepareBoard.append(Func(self.musicMgr.playMusic, 'Ocean'))
        self.prepareBoard.append(Func(self.display.gameRunning))
        self.prepareBoard.start()
        self.bumpManager = BumpManager(self)
        self.resetGameState()
        mods = ModifierButtons()
        if base.direct:
            mods.addButton(KeyboardButton.shift())
        mods.addButton(KeyboardButton.alt())
        try:
            base.buttonThrower.node().setModifierButtons(mods)
        except:
            base.buttonThrowers[0].node().setModifierButtons(mods)

        self.setupHooks()
        self.currentLocalPoint = 4
        if base.direct:
            self.ballPlacer = base.direct.cameraControl.coaMarker
        else:
            self.ballPlacer = None
        taskMgr.add(self.odeSimulationTask, 'piratesOdeSimulationTask')
        if self.hideCursor:
            props = base.win.getProperties()
            props.setCursorHidden(True)
            base.win.requestProperties(props)
        if not self.fromPalace:
            base.exitFunc = self.exit
        return

    def setupHooks(self):
        self.accept('lcontrol', self.leftFlipperUp)
        self.accept('lcontrol-up', self.leftFlipperDown)
        self.accept('rcontrol', self.rightFlipperUp)
        self.accept('rcontrol-up', self.rightFlipperDown)
        self.accept('arrow_left', self.leftFlipperUp)
        self.accept('arrow_left-up', self.leftFlipperDown)
        self.accept('arrow_right', self.rightFlipperUp)
        self.accept('arrow_right-up', self.rightFlipperDown)
        self.accept('z', self.leftFlipperUp)
        self.accept('z-up', self.leftFlipperDown)
        self.accept('/', self.rightFlipperUp)
        self.accept('/-up', self.rightFlipperDown)
        self.accept('1', self.leftFlipperUp)
        self.accept('1-up', self.leftFlipperDown)
        self.accept('2', self.rightFlipperUp)
        self.accept('2-up', self.rightFlipperDown)
        self.accept('6', self.superPullPlunger)
        self.accept('i', self.invertMouseControl)
        self.accept('enter', self.pressStart)
        self.accept('lshift', self.bumpManager.bump, [BumpManager.BUMPLEFT])
        self.accept('rshift', self.bumpManager.bump, [BumpManager.BUMPRIGHT])
        self.accept('space', self.bumpManager.bump, [BumpManager.BUMPUP])
        self.accept('p', self.pauseGame)
        self.accept('escape', self.pauseGame)
        self.accept('arrow_down', self.pullPlunger)
        self.accept('arrow_down-up', self.releasePlunger)
        self.accept('mouse1', self.cannonFire)
        self.accept('mouse3', self.pressStart)
        self.accept('window-event', self.processWindowEvent)
        if self.cheatCodes:
            self.accept('f9', base.screenshot)
            self.accept('alt-l', self.cheatCannon2)
            self.accept('alt-t', self.topArea)
            self.accept('alt-g', self.toggleGeoms)
            self.accept('alt-n', self.getNewBall)
            self.accept('alt-m', self.moveBall)
            self.accept('alt-f', self.freeSkullBalls)
            self.accept('alt-o', self.showStatus)
            self.accept('alt-q', self.cannonAreaCheat)
            self.accept('alt-i', self.startFakeBattle)
            self.accept('alt-u', self.endFakeBattle)
            self.accept('alt-e', self.explorePolys)
            self.accept('alt-0', self.debugZone, [0])
            self.accept('alt-1', self.debugZone, [1])
            self.accept('alt-2', self.debugZone, [2])
            self.accept('alt-3', self.debugZone, [3])
            self.accept('alt-r', self.reloadSoundsAndText)
            self.accept('alt-t', self.toggleTextures)
            self.accept('alt-r', self.toggleRender)
            self.accept('alt-f', self.toggleFlipperNoise)
            self.accept('alt-i', self.display.increaseScore)
            self.accept('wheel_down', self.loadStringToDisplay, [-1])
            self.accept('wheel_up', self.loadStringToDisplay, [1])
            self.accept('f6', self.reloadLocalizer)
            self.localizerListIndex = 0
            self.localizerMyList = []
            for lElement in dir(Localizer):
                if lElement[:2] == 'pp':
                    j = getattr(Localizer, lElement)
                    if not isinstance(j, list):
                        if j.find('/') < 0:
                            self.localizerMyList.append(lElement)

    def loadStringToDisplay(self, direction):
        taskMgr.remove('idletimer')
        self.localizerListIndex += direction
        self.display.grayScreen.reparentTo(hidden)
        self.display.controlLabels[0].reparentTo(hidden)
        self.localizerListIndex = min(max(self.localizerListIndex, 0), len(self.localizerMyList) - 1)
        print('Showing string named %s ' % self.localizerMyList[self.localizerListIndex])
        self.display.unlockDisplay()
        self.display.show(getattr(Localizer, self.localizerMyList[self.localizerListIndex]))

    def reloadLocalizer(self, extra=None):
        importlib.reload(Localizer)
        self.loadStringToDisplay(0)

    def toggleFlipperNoise(self):
        if self.flipperNoise:
            self.flipperNoise = False
        else:
            self.flipperNoise = True

    def toggleRender(self):
        if self.renderOn:
            self.boatModel.reparentTo(hidden)
        else:
            self.boatModel.reparentTo(render)
        self.renderOn = not self.renderOn

    def toggleTextures(self):
        if self.texturesOn:
            render.setTextureOff(1)
            self.texturesOn = False
        else:
            render.clearTexture()
            self.texturesOn = True

    def processWindowEvent(self, win):
        properties = win.getProperties()
        if properties.getForeground() and not self.mainWinForeground:
            self.mainWinForeground = 1
        elif not properties.getForeground() and self.mainWinForeground:
            self.mainWinForeground = 0
            if not self.gamePaused and not self.inTutorialMode:
                self.pauseGame()

    def debugZone(self, zoneNumber):
        for b in self.balls:
            self.deactivateBall(-1, b)

        if zoneNumber == 0:
            self.boatModel.reparentTo(render)
            self.brigModel.reparentTo(hidden)
            self.setCameraPosition('main')
            self.errands['BoneBrig'].hideFlippers()
            base.setBackgroundColor(0.3, 0.3, 0.7)
            self.waterEffects.turnOn()
            self.gateIn(0, [])
            self.dropBall(False)
            self.changeToZone(zoneNumber)
        elif zoneNumber == 1:
            self.boatModel.reparentTo(hidden)
            self.brigModel.reparentTo(render)
            base.setBackgroundColor(0, 0, 0)
            self.setCameraPosition('boneBrig')
            ppos = self.proxPoints['BoneBrigEnter'].getPos()
            ball = self.dropBall(False, bx=ppos[0], by=ppos[1], bz=ppos[2], camReset=False)
            sgode.pyode.dBodySetLinearVel(ball.body, 0, 0, 0)
            sgode.pyode.dBodyDisable(ball.body)
            ball.update()
            self.changeToZone(zoneNumber)
        elif zoneNumber == 2:
            self.errands['CannonArea'].shipsApproaching = True
            self.cannonAreaCheat()
        elif zoneNumber == 3:
            self.topArea()

    def callCreateBoard(self):
        importlib.reload(PirateBoard)
        self.createBoardFromEditorFile()

    def createBoardFromEditorFile(self):
        PirateBoard.createBoard(self)
        for p in list(self.proxPoints.values()):
            p.setPBTaskMgr(self.pbTaskMgr)

    def explorePolys(self):
        polyExplore = PolyExplore(render)
        lh = LocalizerHelper()

    def freeSkullBalls(self):
        if self.currentZone == 1:
            self.errands['BoneBrig'].skeletonsFreed = 5
            self.errands['BoneBrig'].resetFromBoneBrig(0)
            self.errands['BoneBrig'].boneBrigExitTimer(0, [])

    def reloadSoundsAndText(self):
        self.notify.debug('About to reload sounds')
        print('Reloading sounds')
        for (key, p) in list(self.pirateSounds.items()):
            del p
            del self.pirateSounds[key]

        for (key, p) in list(self.pirateDialogue.items()):
            del p
            del self.pirateDialogue[key]

        for (key, p) in list(self.pirateMusic.items()):
            del p
            del self.pirateMusic[key]

        self.loadSounds()

    def wake(self):
        if self.hideCursor:
            props = base.win.getProperties()
            props.setCursorHidden(True)
            base.win.requestProperties(props)
        render.node().setAttrib(self.lightAttrib)
        self.sentScoreAlready = True
        base.enableParticles()
        self.waterEffects.wake()
        self.lostBallMgr.wake()
        PirateBall.splashSounds = [
         base.loadSfx(Localizer.PirateBall_Splash1), base.loadSfx(Localizer.PirateBall_Splash2)]
        base.camLens.setFov(40)
        self.credsCheater.wake()
        self.musicCheater.wake()
        for (key, p) in list(self.proxPoints.items()):
            p.wake()

        for (key, p) in list(self.beacons.items()):
            p.wake()

        for (key, p) in list(self.triggers.items()):
            p.wake()

        for (key, p) in list(self.boardObjects.items()):
            sgode.pyode.dGeomEnable(p.geom)
            p.show()

        for (key, e) in list(self.errands.items()):
            self.notify.debug('About to wake %s' % e.getName())
            e.wake()

        self.notify.debug('About to wake movables')
        for item in self.movables:
            item.wake()

        for object in (self.leftSlingshot, self.rightSlingshot):
            object.reparentTo(render)

        self.notify.debug('About to wake bonus manager')
        self.bonusManager.wake()
        self.notify.debug('About to wake ballsavemanager')
        self.myBallSaveManager.wake()
        self.notify.debug('About to wake pbtaskmgr')
        self.pbTaskMgr.wake()
        self.notify.debug('About to wake bumpmanager')
        self.bumpManager.wake()
        self.notify.debug('About to reload sounds')
        self.loadSounds()
        self.musicMgr.playMusic('Ocean')
        self.notify.debug('About to wake piratesOdeSimulationTask')
        taskMgr.remove('piratesOdeSimulationTask')
        taskMgr.add(self.odeSimulationTask, 'piratesOdeSimulationTask')
        self.notify.debug('About to recreate display')
        self.display = PirateDisplay(self)
        self.display.setHudState(3)
        self.display.gameRunning()
        self.notify.debug('About to reaccept things')
        self.setupHooks()
        self.notify.debug('About to show models')
        self.boatSides.reparentTo(render)
        self.boatModel.reparentTo(render)
        self.funnel.reparentTo(self.plunger.box)
        self.plunger.reparentTo(render)
        self.plunger.box.model.reparentTo(hidden)
        self.brigModel.reparentTo(hidden)
        self.resetGameState()
        self.pauseGame()
        self.setCameraPosition('main')

    def sleep(self):
        if self.display is None:
            return
        if self.hideCursor:
            props = base.win.getProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
        base.disableParticles()
        self.waterEffects.sleep()
        ivalMgr.finishIntervalsMatching('cameraMovement')
        self.lostBallMgr.sleep()
        self.credsCheater.sleep()
        self.musicCheater.sleep()
        for (key, p) in list(self.proxPoints.items()):
            p.sleep()

        for (key, p) in list(self.beacons.items()):
            p.sleep()

        for (key, p) in list(self.triggers.items()):
            p.sleep()

        for (key, p) in list(self.boardObjects.items()):
            sgode.pyode.dGeomDisable(p.geom)
            p.hide()

        for (key, e) in list(self.errands.items()):
            self.notify.debug('About to sleep %s' % e.getName())
            e.sleep()

        self.notify.debug('About to sleep movables')
        for item in self.movables:
            item.sleep()

        for object in (self.leftSlingshot, self.rightSlingshot):
            object.reparentTo(hidden)

        self.notify.debug('About to delete balls')
        while self.balls != []:
            item = self.balls.pop()
            item.destroy()
            del item

        self.notify.debug('About to sleep ballsavemanager')
        self.myBallSaveManager.sleep()
        self.notify.debug('About to sleep pbtaskmgr')
        self.pbTaskMgr.sleep()
        self.notify.debug('About to sleep bumpmanager')
        self.bumpManager.sleep()
        self.notify.debug('About to sleep bonus manager')
        self.bonusManager.sleep()
        self.notify.debug('About to sleep prepareboard')
        if self.prepareBoard.isPlaying():
            self.prepareBoard.finish()
        if self.launchHatchMovement != None and self.launchHatchMovement.isPlaying():
            self.launchHatchMovement.finish()
        self.notify.debug('About to ignore all (gets rid of self.accepts)')
        self.ignoreAll()
        if self.musicMgr != None:
            self.musicMgr.destroy()
            self.musicMgr = None
        if self.dialogueMgr != None:
            self.dialogueMgr.destroy()
            self.dialogueMgr = None
        self.notify.debug('About to delete sounds')
        for (key, p) in list(self.pirateSounds.items()):
            del p
            del self.pirateSounds[key]

        for (key, p) in list(self.pirateDialogue.items()):
            del p
            del self.pirateDialogue[key]

        for (key, p) in list(self.pirateMusic.items()):
            del p
            del self.pirateMusic[key]

        self.notify.debug('About to sleep piratesOdeSimulationTask')
        taskMgr.remove('piratesOdeSimulationTask')
        self.notify.debug('About to destroy display')
        self.display.destroy()
        del self.display
        self.display = None
        self.notify.debug('About to hide models')
        self.boatSides.reparentTo(hidden)
        self.boatModel.reparentTo(hidden)
        self.funnel.reparentTo(hidden)
        self.plunger.reparentTo(hidden)
        self.plunger.box.model.reparentTo(hidden)
        self.brigModel.reparentTo(hidden)
        self.notify.debug('About to stop all sounds')
        base.sfxManagerList[0].stopAllSounds()
        base.sfxManagerList[0].clearCache()
        self.myTransition.noTransitions()
        return

    def destroy(self):
        self.notify.debug('destroy: Destroying everything')
        ivalMgr.finishIntervalsMatching('cameraMovement')
        if self.flipperFlashSequence is not None:
            self.flipperFlashSequence.finish()
        del self.directionalLight
        del self.odeWorld
        del self.odeSpace
        del self.odeContactGroup
        del self.worldInfo
        for (key, p) in list(self.proxPoints.items()):
            p.destroy()
            del self.proxPoints[key]

        del self.proxPoints
        for (key, p) in list(self.beacons.items()):
            p.destroy()
            del self.beacons[key]

        del self.beacons
        for (key, p) in list(self.triggers.items()):
            p.destroy()
            del self.triggers[key]

        del self.triggers
        for (key, p) in list(self.boardObjects.items()):
            p.destroy()
            del self.boardObjects[key]

        del self.boardObjects
        del self.pointValues
        if self.musicMgr != None:
            self.musicMgr.destroy()
        if self.dialogueMgr != None:
            self.dialogueMgr.destroy()
        self.notify.debug('About to delete sounds')
        for (key, p) in list(self.pirateSounds.items()):
            del p
            del self.pirateSounds[key]

        for (key, p) in list(self.pirateDialogue.items()):
            del p
            del self.pirateDialogue[key]

        for (key, p) in list(self.pirateMusic.items()):
            del p
            del self.pirateMusic[key]

        for (key, e) in list(self.errands.items()):
            self.notify.debug('About to destroy %s' % e.getName())
            e.destroy()
            del self.errands[key]

        del self.errands
        self.notify.debug('About to delete camera positions')
        del self.cameraPositions
        self.notify.debug('About to delete ref points')
        for (key, p) in list(self.refPoints.items()):
            p.destroy()
            del self.refPoints[key]

        del self.refPoints
        self.notify.debug('About to delete movables')
        while self.movables != []:
            item = self.movables.pop()
            item.destroy()
            del item

        self.notify.debug('About to destroy bonus manager')
        self.bonusManager.destroy()
        del self.bonusManager
        self.notify.debug('About to delete balls')
        while self.balls != []:
            item = self.balls.pop()
            item.destroy()
            del item

        self.notify.debug('About to delete flippers')
        del self.leftFlippers
        del self.rightFlippers
        self.myTransition.noTransitions()
        self.notify.debug('About to delete my transition')
        del self.myTransition
        self.notify.debug('About to delete ballsavemanager')
        self.myBallSaveManager.destroy()
        del self.myBallSaveManager
        self.notify.debug('About to delete pbtaskmgr')
        self.pbTaskMgr.destroy()
        del self.pbTaskMgr
        self.notify.debug('About to delete bumpmanager')
        self.bumpManager.destroy()
        del self.bumpManager
        self.notify.debug('About to delete prepareboard')
        if self.prepareBoard != None and self.prepareBoard.isPlaying():
            self.prepareBoard.finish()
        del self.prepareBoard
        if self.launchHatchMovement != None and self.launchHatchMovement.isPlaying():
            self.launchHatchMovement.finish()
        del self.launchHatchMovement
        self.notify.debug('About to ignore all (gets rid of self.accepts)')
        self.ignoreAll()
        self.notify.debug('About to delete piratesOdesimulationtask')
        taskMgr.remove('piratesOdeSimulationTask')
        self.notify.debug('About to delete gatehinge')
        del self.gateHinge
        self.notify.debug('About to delete models')
        self.boatSides.removeNode()
        self.boatModel.removeNode()
        self.funnel.removeNode()
        self.plunger.removeNode()
        self.plunger.box.model.removeNode()
        self.brigModel.removeNode()
        self.notify.debug('About to stop all sounds')
        base.sfxManagerList[0].stopAllSounds()
        base.sfxManagerList[0].clearCache()
        return

    def getNewBall(self):
        if self.ballPlacer == None:
            return
        pos = self.ballPlacer.getPos()
        ball = self.dropBall(False, tryNumber=0, bx=pos[0], by=pos[1], bz=pos[2] + 0.6, camReset=False)
        if ball != None:
            ball.setZone(self.currentZone)
        return

    def moveBall(self):
        if self.ballPlacer == None:
            return
        pos = self.ballPlacer.getPos()
        for i in range(len(self.balls)):
            if self.balls[i].active:
                self.deactivateBall(i)

        ball = self.dropBall(False, tryNumber=0, bx=pos[0], by=pos[1], bz=pos[2] + 0.6, camReset=False)
        if ball != None:
            ball.setZone(self.currentZone)
        return

    def startFakeBattle(self):
        self.errands['CannonArea'].shipsApproaching = True
        self.errands['CannonArea'].underAttack = False
        self.errands['CannonArea'].startBattle(0)

    def endFakeBattle(self):
        self.errands['CannonArea'].endBattle()

    def cheatCannon2(self):
        self.errands['CrowCannon'].cannonState = 2
        self.errands['CrowCannon'].torchIn(0, [])
        self.pbTaskMgr.doMethodLater(3, self.errands['CrowCannon'].torchTimer, 'cheatcannon', [0, []])

    def cannonAreaCheat(self):
        pos = self.proxPoints['Cannon Area'].getPos()
        for i in range(len(self.balls)):
            if self.balls[i].active:
                self.deactivateBall(i)

        self.dropBall(False, tryNumber=0, bx=pos[0], by=pos[1], bz=pos[2] + 0.6, camReset=False)

    def topArea(self):
        self.gameOver = False
        for b in self.balls:
            self.deactivateBall(-1, b)

        self.dropBall(False, bx=0, by=23, bz=3)
        self.errands['TopDeck'].start()
        self.errands['TopDeck'].rampLogic(0, ['top', False])

    def adjustVariable(self, amount):
        self.currentLocalPoint = self.currentLocalPoint + amount
        if self.currentLocalPoint < 4:
            self.currentLocalPoint = 4

    def toggleGeoms(self):
        if self.geomsEnabled:
            self.geomsEnabled = False
            print('all boardobjects disabled')
            for g in list(self.boardObjects.values()):
                sgode.pyode.dGeomDisable(g.geom)

        self.geomsEnabled = True
        print('all boardobjects enabled')
        for g in list(self.boardObjects.values()):
            sgode.pyode.dGeomEnable(g.geom)

    def setInTutorialMode(self, bool):
        if bool:
            self.inTutorialMode = True
            self.musicMgr.startTutorial()
            self.lostBallMgr.startTutorial()
            self.myBallSaveManager.pause()
        else:
            self.inTutorialMode = False
            self.lostBallMgr.stopTutorial()
            self.musicMgr.stopTutorial()
            self.myBallSaveManager.resume()

    def __del__(self):
        self.notify.info('__del__: Delete being called, call exit()')
        self.exit()

    def exit(self):
        if self.scoreWrite and self.scoreFile != None:
            self.scoreFile.close()
            self.scoreFile = None
        self.notify.info('exit: exiting pirate board')
        if not self.fromPalace:
            self.destroy()
            sys.exit()
        if self.sentScoreAlready:
            messenger.send('killPinballWorld', ['Pirates', 0, 0])
        else:
            messenger.send('killPinballWorld', ['Pirates', self.myScore, self.display.playTimer.getTime()])
        return

    def pauseGame(self):
        if self.inTutorialMode:
            for e in list(self.errands.values()):
                e.skip()

            return
        if not self.gamePaused:
            if self.cameraMovement != None and self.cameraMovement.isPlaying():
                self.cameraMovement.pause()
            self.pbTaskMgr.removeDelayedMethod('resumeBallsAfterPause')
            self.pbTaskMgr.pause()
            for e in list(self.errands.values()):
                e.pause()

            self.myBallSaveManager.pause()
            self.display.pause()
            self.pauseBalls()
            self.dialogueMgr.pause()
            self.musicMgr.pause()
            self.flippersEnabled = False
            if self.hideCursor:
                props = base.win.getProperties()
                props.setCursorHidden(False)
                base.win.requestProperties(props)
        else:
            if self.cameraMovement != None and self.cameraMovement.getState() == CInterval.SPaused:
                self.cameraMovement.resume()
            self.pbTaskMgr.resume()
            for e in list(self.errands.values()):
                e.resume()

            self.myBallSaveManager.resume()
            if not self.bumpManager.tiltActive:
                self.flippersEnabled = True
            self.display.unPause()
            self.dialogueMgr.resume()
            self.musicMgr.resume()
            self.pbTaskMgr.removeDelayedMethod('resumeBallsAfterPause')
            self.pbTaskMgr.doMethodLater(0.75, self.pauseBalls, 'resumeBallsAfterPause', [False])
            if self.hideCursor:
                props = base.win.getProperties()
                props.setCursorHidden(True)
                base.win.requestProperties(props)
        self.gamePaused = not self.gamePaused
        return

    def pauseBalls(self, doIt=True):
        if doIt:
            for b in self.balls:
                if b.active and self.currentZone == b.getZone() and not b.chilled:
                    sgode.pyode.dBodyDisable(b.body)
                    sgode.pyode.dGeomDisable(b.geom)

        for b in self.balls:
            if b.active and self.currentZone == b.getZone() and not b.chilled:
                sgode.pyode.dBodyEnable(b.body)
                sgode.pyode.dGeomEnable(b.geom)

    def plungerUpdate(self, dt):
        self.launchCannon.setColor(Vec4(1, 1 - self.plungerPower, 1 - self.plungerPower, 1))
        self.plungerPower = self.plungerPower + dt / self.plunger.timeToFullDepress
        if self.plungerPower > 1:
            self.plungerPower = 1
        self.plunger.pullPlunger()

    def superPullPlunger(self):
        if self.inTutorialMode or self.gameOver:
            self.pressStart()
        else:
            self.plungerDepressed = True
            self.pbTaskMgr.removeDelayedMethod('setPlungerBoxInactive')
            self.pbTaskMgr.doMethodLater(3, self.releasePlunger, 'superPullPlunger')

    def pullPlunger(self):
        self.plungerDepressed = True
        self.pbTaskMgr.removeDelayedMethod('setPlungerBoxInactive')

    def releasePlunger(self):
        if self.gamePaused:
            return
        self.plungerDepressed = False
        self.pbTaskMgr.doMethodLater(0.5, self.plunger.box.setActive, 'setPlungerBoxInactive', [False])
        self.plungerPower = 0
        self.launchCannon.setColor(Vec4(1, 1, 1, 1))
        self.pirateSounds['PiratePinball_Explode'].setVolume(1)
        self.pirateSounds['PiratePinball_Explode'].play()
        self.plunger.releasePlunger()

    def credsCallBack(self):
        self.display.show(Localizer.Creds)
        self.pbTaskMgr.doMethodLater(5, self.display.show, 'displayGameNameCreds', [Localizer.ppDisplayGameName])

    def musicCallBack(self):
        if self.musicMgr.enabled():
            self.musicMgr.disable()
        else:
            self.musicMgr.enable()

    def cannonFire(self):
        if self.errands['CannonArea'].underAttack:
            self.errands['CannonArea'].fireCannon()

    def invertMouseControl(self):
        if self.errands['CannonArea'].underAttack:
            self.errands['CannonArea'].invertMouseControl()

    def leftFlipperUp(self):
        if self.pbTaskMgr.removeDelayedMethod('resumeBallsAfterPause'):
            self.pauseBalls(False)
        if self.flippersEnabled:
            if self.flipperCycleLimit == 0:
                self.errands['SkullAlleys'].cycleLeft()
                self.flipperCycleLimit = 1
                if self.flipperTimeUp == -1:
                    self.flipperTimeUp = time.mktime(time.localtime())
            self.checkForStatus()
            for f in self.leftFlippers:
                if f.getZone() != self.currentZone:
                    continue
                if not f.flipperOn and self.flipperNoise:
                    if self.currentZone == 1:
                        self.pirateSounds['BoneBrig_FlippersUp'].play()
                    else:
                        self.pirateSounds['PiratePinball_LeftFlipper'].play()
                f.flipperOn = True

    def leftFlipperDown(self):
        if self.pbTaskMgr.removeDelayedMethod('resumeBallsAfterPause'):
            self.pauseBalls(False)
        if self.flippersEnabled:
            self.flipperCycleLimit = 0
            for f in self.leftFlippers:
                if f.getZone() != self.currentZone:
                    continue
                if f.flipperOn and self.flipperNoise:
                    if self.currentZone == 1:
                        self.pirateSounds['BoneBrig_FlippersBack'].play()
                    else:
                        self.pirateSounds['PiratePinball_LeftFlipperBack'].play()
                f.flipperOn = False

            self.flipperTimeUp = -1
            self.showAllStatus = -1

    def rightFlipperUp(self):
        if self.pbTaskMgr.removeDelayedMethod('resumeBallsAfterPause'):
            self.pauseBalls(False)
        if self.flippersEnabled:
            if self.flipperCycleLimit == 0:
                self.errands['SkullAlleys'].cycleRight()
                self.flipperCycleLimit = 1
                if self.flipperTimeUp == -1:
                    self.flipperTimeUp = time.mktime(time.localtime())
            self.checkForStatus()
            for f in self.rightFlippers:
                if f.getZone() != self.currentZone:
                    continue
                if not f.flipperOn and self.flipperNoise:
                    if self.currentZone == 1:
                        self.pirateSounds['BoneBrig_FlippersUp'].play()
                    else:
                        self.pirateSounds['PiratePinball_RightFlipper'].play()
                f.flipperOn = True

    def rightFlipperDown(self):
        if self.pbTaskMgr.removeDelayedMethod('resumeBallsAfterPause'):
            self.pauseBalls(False)
        if self.flippersEnabled:
            self.flipperCycleLimit = 0
            for f in self.rightFlippers:
                if f.getZone() != self.currentZone:
                    continue
                if f.flipperOn and self.flipperNoise:
                    if self.currentZone == 1:
                        self.pirateSounds['BoneBrig_FlippersBack'].play()
                    else:
                        self.pirateSounds['PiratePinball_RightFlipperBack'].play()
                f.flipperOn = False

            self.flipperTimeUp = -1
            self.showAllStatus = -1

    def checkForStatus(self):
        currentTime = time.mktime(time.localtime())
        if currentTime - self.flipperTimeUp > 5 and self.showAllStatus == -1:
            self.showAllStatus = 0
            self.display.show(Localizer.pDisplayStatusStart)
            self.pbTaskMgr.doMethodLater(2, self.showStatus, 'statusShower')

    def showStatus(self, taskInstance=None):
        if self.showAllStatus == -1:
            self.display.show(Localizer.ppDisplayGameName)
            return
        if self.showAllStatus == len(list(self.errands.values())):
            self.showAllStatus = 0
            if self.myScore > self.highestScoreEver:
                self.highestScoreEver = self.myScore
            self.display.show(Localizer.pHighestScore % self.highestScoreEver)
            self.pbTaskMgr.doMethodLater(2, self.showStatus, 'statusShower')
            return
        delayTime = 2.0
        if list(self.errands.values())[self.showAllStatus].getStatus() == None:
            delayTime = 0
        else:
            self.display.show(list(self.errands.values())[self.showAllStatus].getStatus())
        self.showAllStatus = self.showAllStatus + 1
        self.pbTaskMgr.doMethodLater(delayTime, self.showStatus, 'statusShower')
        return

    def changeToZone(self, zoneNumber):
        ivalMgr.finishIntervalsMatching('tiltCameraMovement')
        oldZone = self.currentZone
        if self.dialogueMgr != None:
            self.dialogueMgr.changeZone()
        if self.musicMgr != None:
            self.musicMgr.changeZone()
        self.flipperCycleLimit = 0
        for object in self.leftFlippers + self.rightFlippers:
            object.changeToZone(zoneNumber, oldZone)
            object.flipperOn = False

        self.flipperTimeUp = -1
        self.showAllStatus = -1
        self.currentZone = zoneNumber
        if self.currentZone == 2:
            self.lostBallMgr.dontWorry()
        else:
            self.lostBallMgr.worry()
        if oldZone != self.currentZone:
            if self.currentZone == 0:
                if self.errands['MultiBall'].multiBallMode > 0:
                    self.musicMgr.playMusic('SkullBall')
                else:
                    self.musicMgr.playMusic('MainDeck')
            elif self.currentZone == 1:
                self.musicMgr.playMusic('BoneBrig')
        for e in list(self.errands.values()):
            e.changeToZone(self.currentZone)

        for b in list(self.boardObjects.values()):
            if b.getZone() == zoneNumber:
                sgode.pyode.dGeomEnable(b.geom)
                if b.normallySeen:
                    b.reparentTo(render)
            else:
                sgode.pyode.dGeomDisable(b.geom)
                b.reparentTo(hidden)

        return

    def resetGameState(self):
        self.myScore = 0
        self.destroyFlippers()
        self.createFlippers()
        self.gameOver = True
        self.flippersEnabled = True
        self.currentZone = 0
        self.changeToZone(0)
        self.flipperCycleLimit = 0
        self.multiplier = 1
        self.beacons['Multiplier'].setCurrentOnState(0)
        self.ballNumber = 0
        self.ballReserve = 3
        self.ballsOnTable = 0
        self.launchLaneEmpty = True
        self.displayFree = False
        self.myBallSaveManager.reset()
        for b in range(0, len(self.balls)):
            self.deactivateBall(b)

        for e in list(self.errands.values()):
            e.reset()

        for (key, beacon) in list(self.beacons.items()):
            beacon.setState(Beacon.ONCE)

        self.waterEffects.turnOn()
        self.rollSoundPlaying = False
        base.setBackgroundColor(0.3, 0.3, 0.7)
        self.errands['BoneBrig'].hideFlippers()

    def loadCameraAngles(self):
        self.cameraPositions['main'] = [
         0, -43, 32.5, 0, 321, 0]
        self.cameraPositions['midCrow'] = [-22.7, -25, 37.7, -40, 320, 0]
        self.cameraPositions['crow'] = [0, -8, 43, 0, 282, 0]
        self.cameraPositions['topDeck'] = [0, -5.13, 27.6, 0, 315.8, 0]
        self.cameraPositions['crowCannon'] = [2.5, -6.4, 11.2, 0, 333, 0]
        self.cameraPositions['boneBrig'] = [
         0, 48, 24.5, 0, 325, 0]
        self.cameraPositions['skullLanes'] = [-2.5, 1.15, 12, 0, 321, 0]
        self.cameraPositions['pirates'] = [0, -20, 12, 0, 318, 0]
        self.cameraPositions['boneBrigTeach1'] = [4, 72, 11, -10, 328, 0]
        self.cameraPositions['boneBrigTeach2'] = [2.3, 72, 8.5, -10, 328, 0]
        self.cameraPositions['crowCannonTeach'] = [3.91, -3.06, 9.19, 0, 326.74, 0]
        self.cameraPositions['fireCannon'] = [
         0, -0.1, 3.5, 90, 360, 0]

    def setCameraPosition(self, posName, time=0, blend='easeInOut'):
        ivalMgr.finishIntervalsMatching('tiltCameraMovement')
        ivalMgr.finishIntervalsMatching('cameraMovement')
        self.currentCameraPosition = posName
        poshpr = self.cameraPositions[posName]
        if time == 0:
            camera.setPos(poshpr[0], poshpr[1], poshpr[2])
            camera.setHpr(poshpr[3], poshpr[4], poshpr[5])
        else:
            if self.cameraMovement != None and self.cameraMovement.isPlaying():
                self.cameraMovement.finish()
            self.cameraMovement = Sequence(name='cameraMovement')
            camera1stMove = []
            camera1stMove.append(camera.posInterval(time, self.getCameraPos(posName), blendType=blend))
            camera1stMove.append(camera.hprInterval(time, self.getCameraHpr(posName), blendType=blend))
            self.cameraMovement.append(Func(self.bumpManager.disable))
            self.cameraMovement.append(Parallel(*camera1stMove))
            self.cameraMovement.append(Func(self.bumpManager.enable))
            self.cameraMovement.start()
        return

    def getCameraPos(self, posName):
        self.currentCameraPosition = posName
        poshpr = self.cameraPositions[posName]
        return Point3(poshpr[0], poshpr[1], poshpr[2])

    def getCameraHpr(self, posName):
        self.currentCameraPosition = posName
        poshpr = self.cameraPositions[posName]
        return Point3(poshpr[3], poshpr[4], poshpr[5])

    def loadErrands(self):
        self.errands['TreasureChests'] = TreasureChests(self)
        self.errands['SkullAlleys'] = SkullAlleys(self)
        self.errands['DeckHatches'] = DeckHatches(self)
        self.errands['StairCase'] = StairCase(self)
        self.errands['CannonArea'] = CannonArea(self)
        self.errands['CrowCannon'] = CrowCannon(self)
        self.errands['BoneBrig'] = BoneBrig(self)
        self.errands['MultiBall'] = MultiBall(self)
        self.errands['TopDeck'] = TopDeck(self)

    def loadSounds(self):
        base.sfxManagerList[0].stopAllSounds()
        base.sfxManagerList[0].clearCache()
        self.tiltSound = base.loadSfx('pinballbase/tilt')
        base.sfxManagerList[0].setPreferSpeedOverMemory(True)
        self.pirateSounds['PiratePinball_LeftFlipper'] = base.loadSfx(Localizer.PiratePinball_LeftFlipper)
        self.pirateSounds['PiratePinball_RightFlipper'] = base.loadSfx(Localizer.PiratePinball_RightFlipper)
        self.pirateSounds['BoneBrig_FlippersUp'] = base.loadSfx(Localizer.BoneBrig_FlippersUp)
        self.pirateSounds['BoneBrig_FlippersBack'] = base.loadSfx(Localizer.BoneBrig_FlippersBack)
        self.pirateSounds['PiratePinball_LeftFlipperBack'] = base.loadSfx(Localizer.PiratePinball_LeftFlipperBack)
        self.pirateSounds['PiratePinball_RightFlipperBack'] = base.loadSfx(Localizer.PiratePinball_RightFlipperBack)
        self.pirateSounds['StairCase_Found'] = base.loadSfx(Localizer.StairCase_Found)
        self.pirateSounds['StairCase_Wind'] = base.loadSfx(Localizer.StairCase_Wind)
        self.pirateSounds['CrowCannon_Success'] = base.loadSfx(Localizer.CrowCannon_Success)
        self.pirateSounds['TopDeck_SeagullStartle'] = base.loadSfx(Localizer.TopDeck_SeagullStartle)
        self.pirateSounds['TopDeck_SeagullFlap'] = base.loadSfx(Localizer.TopDeck_SeagullFlap)
        self.pirateSounds['TopDeck_HelmThread'] = base.loadSfx(Localizer.TopDeck_HelmThread)
        self.pirateSounds['TopDeck_Bird'] = base.loadSfx(Localizer.TopDeck_Bird)
        self.pirateSounds['TopDeck_Barrel'] = base.loadSfx(Localizer.TopDeck_Barrel)
        self.pirateSounds['CannonArea_BallLocked'] = base.loadSfx(Localizer.CannonArea_BallLocked)
        self.pirateSounds['CannonArea_SerpentHit'] = base.loadSfx(Localizer.CannonArea_SerpentHit)
        self.pirateSounds['CannonArea_ShipHit'] = base.loadSfx(Localizer.CannonArea_ShipHit)
        self.pirateSounds['CannonArea_SailHit'] = base.loadSfx(Localizer.CannonArea_SailHit)
        self.pirateSounds['CannonArea_IslandHit'] = base.loadSfx(Localizer.CannonArea_IslandHit)
        self.pirateSounds['CannonArea_Empty'] = base.loadSfx(Localizer.CannonArea_Empty)
        self.pirateSounds['TreasureChests_CaptainsTreasure'] = base.loadSfx(Localizer.TreasureChests_CaptainsTreasure)
        self.pirateSounds['TreasureChests_AllChests'] = base.loadSfx(Localizer.TreasureChests_AllChests)
        self.pirateSounds['TreasureChests_HitTreasureChest'] = base.loadSfx(Localizer.TreasureChests_HitTreasureChest)
        self.pirateSounds['SkullAlleys_LightAlley'] = base.loadSfx(Localizer.SkullAlleys_LightAlley)
        self.pirateSounds['SkullAlleys_SavesActivated'] = base.loadSfx(Localizer.SkullAlleys_SavesActivated)
        self.pirateSounds['DeckHatches_MultiplierAdvances'] = base.loadSfx(Localizer.DeckHatches_MultiplierAdvances)
        self.pirateSounds['DeckHatches_LetterLit'] = base.loadSfx(Localizer.DeckHatches_LetterLit)
        self.pirateSounds['DeckHatches_HatchClose'] = base.loadSfx(Localizer.DeckHatches_HatchClose)
        self.pirateSounds['DeckHatches_HatchSqueak'] = base.loadSfx(Localizer.DeckHatches_HatchSqueak)
        self.pirateSounds['PiratePinball_BallRelease'] = base.loadSfx(Localizer.PiratePinball_BallRelease)
        self.pirateSounds['PiratePinball_BallSink'] = base.loadSfx(Localizer.PiratePinball_BallSink)
        self.pirateSounds['PiratePinball_Wood0'] = base.loadSfx(Localizer.PiratePinball_Wood0)
        self.pirateSounds['PiratePinball_Wood1'] = base.loadSfx(Localizer.PiratePinball_Wood1)
        self.pirateSounds['PiratePinball_Wood2'] = base.loadSfx(Localizer.PiratePinball_Wood2)
        self.pirateSounds['MultiBall_SkeletonHit'] = base.loadSfx(Localizer.MultiBall_SkeletonHit)
        self.pirateSounds['BoneBrig_CageFall'] = base.loadSfx(Localizer.BoneBrig_CageFall)
        self.pirateSounds['BoneBrig_IrateSkeleton1'] = base.loadSfx(Localizer.BoneBrig_IrateSkeleton1)
        self.pirateSounds['BoneBrig_SkeletonEmerge1'] = base.loadSfx(Localizer.BoneBrig_SkeletonEmerge1)
        self.pirateSounds['BoneBrig_IrateSkeleton2'] = base.loadSfx(Localizer.BoneBrig_IrateSkeleton2)
        self.pirateSounds['BoneBrig_SkeletonEmerge2'] = base.loadSfx(Localizer.BoneBrig_SkeletonEmerge2)
        self.pirateSounds['BoneBrig_IrateSkeleton3'] = base.loadSfx(Localizer.BoneBrig_IrateSkeleton3)
        self.pirateSounds['BoneBrig_SkeletonEmerge3'] = base.loadSfx(Localizer.BoneBrig_SkeletonEmerge3)
        self.pirateSounds['CannonArea_ShipSink'] = base.loadSfx(Localizer.CannonArea_ShipSink)
        self.pirateSounds['CannonArea_PirateCharge'] = base.loadSfx(Localizer.CannonArea_PirateCharge)
        self.pirateSounds['PiratePinball_Bell1'] = base.loadSfx(Localizer.PiratePinball_Bell1)
        self.pirateSounds['PiratePinball_Bell2'] = base.loadSfx(Localizer.PiratePinball_Bell2)
        base.sfxManagerList[0].setPreferSpeedOverMemory(False)
        self.pirateSounds['StairCase_Roll'] = base.loadSfx(Localizer.StairCase_Roll)
        self.pirateSounds['PiratePinball_Explode'] = base.loadSfx(Localizer.PiratePinball_Explode)
        self.pirateDialogue['ShootToLoad'] = base.loadSfx(Localizer.ppShootToLoad)
        self.pirateDialogue['ShootToAim'] = base.loadSfx(Localizer.ppShootToAim)
        self.pirateDialogue['ShootToFire'] = base.loadSfx(Localizer.ppShootToFire)
        self.pirateDialogue['AimRamp'] = base.loadSfx(Localizer.ppAimRamp)
        self.pirateDialogue['Arr1'] = base.loadSfx(Localizer.ppArr1)
        self.pirateDialogue['Arr2'] = base.loadSfx(Localizer.ppArr2)
        self.pirateDialogue['Arr3'] = base.loadSfx(Localizer.ppArr3)
        self.pirateDialogue['Boarded'] = base.loadSfx(Localizer.ppBoarded)
        self.pirateDialogue['CannonArea'] = base.loadSfx(Localizer.ppCannonArea)
        self.pirateDialogue['CannonLock'] = base.loadSfx(Localizer.ppCannonLock)
        self.pirateDialogue['Congratulations'] = base.loadSfx(Localizer.ppCongratulations)
        self.pirateDialogue['EnemyShips'] = base.loadSfx(Localizer.ppEnemyShips)
        self.pirateDialogue['Escape'] = base.loadSfx(Localizer.ppEscape)
        self.pirateDialogue['Fire'] = base.loadSfx(Localizer.ppFire)
        self.pirateDialogue['FreeBall'] = base.loadSfx(Localizer.ppFreeBall)
        self.pirateDialogue['GameOver'] = base.loadSfx(Localizer.ppGameOver)
        self.pirateDialogue['GoldTaunt'] = base.loadSfx(Localizer.ppGoldTaunt)
        self.pirateDialogue['Hatch'] = base.loadSfx(Localizer.ppHatch)
        self.pirateDialogue['HitShip'] = base.loadSfx(Localizer.ppHitShip)
        self.pirateDialogue['LaneSaves'] = base.loadSfx(Localizer.ppLaneSaves)
        self.pirateDialogue['NiceShot'] = base.loadSfx(Localizer.ppNiceShot)
        self.pirateDialogue['Plank'] = base.loadSfx(Localizer.ppPlank)
        self.pirateDialogue['Plunger'] = base.loadSfx(Localizer.ppPlunger)
        self.pirateDialogue['SailAgain'] = base.loadSfx(Localizer.ppSailAgain)
        self.pirateDialogue['ScareSeagulls'] = base.loadSfx(Localizer.ppScareSeagulls)
        self.pirateDialogue['SerpentHit'] = base.loadSfx(Localizer.ppSerpentHit)
        self.pirateDialogue['SinkShips'] = base.loadSfx(Localizer.ppSinkShips)
        self.pirateDialogue['SkeletonsAngry'] = base.loadSfx(Localizer.ppSkeletonsAngry)
        self.pirateDialogue['SkullLanes'] = base.loadSfx(Localizer.ppSkullLanes)
        self.pirateDialogue['SkullMultiball'] = base.loadSfx(Localizer.ppSkullMultiball)
        self.pirateDialogue['TooBad'] = base.loadSfx(Localizer.ppTooBad)
        self.pirateDialogue['TreasureChests'] = base.loadSfx(Localizer.ppTreasureChests)
        self.pirateDialogue['UnderStairs'] = base.loadSfx(Localizer.ppUnderStairs)
        self.pirateDialogue['UseMouseAim'] = base.loadSfx(Localizer.ppUseMouseAim)
        self.pirateDialogue['UseMouseFire'] = base.loadSfx(Localizer.ppUseMouseFire)
        self.pirateDialogue['WelcomeAboard'] = base.loadSfx(Localizer.ppWelcomeAboard)
        self.pirateDialogue['WelcomeBrig'] = base.loadSfx(Localizer.ppWelcomeBrig)
        self.pirateDialogue['WelcomeLong'] = base.loadSfx(Localizer.ppWelcomeLong)
        self.pirateDialogue['WelcomeShort'] = base.loadSfx(Localizer.ppWelcomeShort)
        self.pirateDialogue['WellDone'] = base.loadSfx(Localizer.ppWellDone)
        self.pirateDialogue['GoldenBarrel'] = base.loadSfx(Localizer.ppGoldenBarrel)
        self.pirateDialogue['MultiplierAdvances'] = base.loadSfx(Localizer.ppMultiplierAdvances)
        self.pirateDialogue['BallSaved'] = base.loadSfx(Localizer.ppBallSaved)
        self.pirateDialogue['NoEnemies'] = base.loadSfx(Localizer.ppNoEnemies)
        self.pirateDialogue['UnderAttack'] = base.loadSfx(Localizer.ppUnderAttack)
        self.pirateDialogue['OnlyTwo'] = base.loadSfx(Localizer.ppOnlyTwo)
        self.pirateDialogue['SuperSkullball'] = base.loadSfx(Localizer.ppSuperSkullball)
        self.pirateDialogue['Treasure'] = base.loadSfx(Localizer.ppTreasure)
        self.pirateDialogue['OneMore'] = base.loadSfx(Localizer.ppOneMore)
        self.dialogueMgr = DialogueManager(self, self.pirateDialogue)
        self.pirateMusic['MainDeck'] = base.loadMusic(Localizer.ppMusic_MainDeck)
        self.pirateMusic['BoneBrig'] = base.loadMusic(Localizer.ppMusic_BoneBrig)
        self.pirateMusic['SkullBall'] = base.loadMusic(Localizer.ppMusic_SkullBall)
        self.pirateMusic['CannonPractice'] = base.loadMusic(Localizer.ppMusic_CannonPractice)
        self.pirateMusic['CannonAttack'] = base.loadMusic(Localizer.ppMusic_CannonAttack)
        self.pirateMusic['VictoryJingle'] = base.loadMusic(Localizer.ppMusic_VictoryJingle)
        self.pirateMusic['DefeatJingle'] = base.loadMusic(Localizer.ppMusic_DefeatJingle)
        self.pirateMusic['Music_Success1'] = base.loadMusic(Localizer.ppMusic_Success1)
        self.pirateMusic['Music_Success2'] = base.loadMusic(Localizer.ppMusic_Success2)
        self.pirateMusic['Ocean'] = base.loadMusic(Localizer.ppMusic_Ocean)
        self.musicMgr = MusicManager(self, self.pirateMusic)

    def playDialogue(self, name, priority=False, callbackFunction=None, defaultTimeToCallback=1, args=[]):
        self.dialogueMgr.playDialogue(name, priority, callbackFunction, defaultTimeToCallback, args)

    def setDialogueEnabled(self, boolarg):
        if boolarg:
            self.dialogueMgr.enable()
        else:
            self.dialogueMgr.disable()

    def loadPoints(self):
        self.pointValues['BumperHit'] = 100
        self.pointValues['PlankIn'] = 1000
        self.pointValues['MultiBallBonus'] = 50000
        self.pointValues['BoneBrigBonus'] = 10000
        self.pointValues['CrowCannonNotLit'] = 100
        self.pointValues['CrowCannonCannonBonus'] = 10000
        self.pointValues['CrowCannonBrigEnter'] = 1000
        self.pointValues['CrowCannonParrotBonus'] = 100000
        self.pointValues['SecretStaircase'] = 3000
        self.pointValues['SecretStaircaseBonus'] = 150000
        self.pointValues['HelmCenter'] = 30000
        self.pointValues['GoldenBarrel'] = 2500
        self.pointValues['GoldenBarrelBonus'] = 2500
        self.pointValues['HitSeagull'] = 500
        self.pointValues['HelmSpun'] = 10
        self.pointValues['TreasureRoomEnterNotLit'] = 700
        self.pointValues['TreasureRoomEnterLit'] = 3000
        self.pointValues['TreasureHit'] = 500
        self.pointValues['TreasureHitNotLit'] = 100
        self.pointValues['AllFourChests'] = 5000
        self.pointValues['SerpentHit'] = 10000
        self.pointValues['CannonAreaNotLit'] = 500
        self.pointValues['IslandHit'] = 500
        self.pointValues['WonBattle'] = 50000
        self.pointValues['SunkShip'] = 2000
        self.pointValues['SeaSerpentBonus'] = 50000
        self.pointValues['AllAlleysActive'] = 5000
        self.pointValues['AlleyLit'] = 100
        self.pointValues['SkullAlleyBonus'] = 10000
        self.pointValues['SpelledPirates'] = 5000
        self.pointValues['WrappedMultiplier'] = 100000
        self.pointValues['DeckHatchesBonus'] = 5000

    def createBoat(self):
        self.boatSides = loader.loadModelCopy('piratepinball/art/main_ship/boatBottom')
        self.boatSides.reparentTo(render)
        self.boatSides.setHpr(-90.0, 0.0, 0.0)
        self.boatSides.setPos(0.0, 3.5, -6.9)
        self.boatSides.setScale(12)
        self.boatSides.setColor(self.boatColor)
        boatModel = loader.loadModelCopy('piratepinball/art/main_ship/PirateShip')
        boatModel.setHpr(-90.0, 0.0, 0.0)
        boatModel.setPos(0.0, -9.44, 0.0)
        boatModel.setScale(12)
        boatModel.reparentTo(render)
        if EDITMODE:
            boatModel.setTransparency(1)
            boatModel.setAlphaScale(0.7)
        self.ropeRail1 = boatModel.find('**/RopeRail1')
        self.ropeRail1.setTransparency(1)
        self.ropeRail1.setColor(1, 1, 1, 0.7)
        self.ropeRail2 = boatModel.find('**/RopeRail2')
        self.ropeRail2.setTransparency(1)
        self.ropeRail2.setColor(1, 1, 1, 0.7)
        self.launchCannon = boatModel.find('**/launcher')
        self.funnel = loader.loadModelCopy('piratepinball/art/main_ship/Funnel')
        self.funnel.reparentTo(self.plunger.box)
        self.funnel.setPos(-0.05, 3.0, 0.4)
        self.funnel.setScale(12, 12, 25)
        self.funnel.setHpr(0, 90, 0)
        self.plunger.reparentTo(render)
        self.plunger.box.model.reparentTo(hidden)
        self.beacons['PlankBeacon'] = Beacon(boatModel.find('**/baconplates:pPlane23'), 'piratepinball/art/main_ship/beacons/RedLight.png')
        self.beacons['LaunchArrow1'] = Beacon(boatModel.find('**/baconplates:pPlane39'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png', rate=0.75)
        self.beacons['LaunchArrow2'] = Beacon(boatModel.find('**/pPlane39'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png', rate=0.75)
        self.beacons['LaunchArrow3'] = Beacon(boatModel.find('**/pPlane40'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png', rate=0.75)
        self.hatchLauncher = boatModel.find('**/hatchLauncher')
        self.hatchLauncher.setPos(-0.93, 0.84, 0)
        self.hatchLauncher.setHpr(180, 0, 0)
        boatModel.find('**/UnlitFlats').setBin('flat', 3)
        boatModel.find('**/PegFlats').setBin('flat', 60)
        self.boatModel = boatModel
        boatModel.find('**/plank').setPos(0, 0, -0.003)
        boatModel.find('**/BlackFlat5').setPos(-0.35, -0.01, 0.05)
        boatModel.find('**/BlackFlat5').setScale(0.83, 1.15, 1.0)
        boatModel.find('**/BlackFlat5').setBin('flat', 0)
        boatModel.find('**/pirateFlat1').setBin('transparent', 3)
        self.crowsNest = boatModel.find('**/CrowsNest:crowsNest')
        self.crowsNest.setPos(0.06, -0.18, -2.56)
        self.crowsNest.setHpr(347, 0, 0)
        self.crowsNest.setScale(1.2)
        self.crowsNest.setTransparency(1)
        self.rearSailTop = boatModel.find('**/rearSailTop')
        self.rearSailTop.reparentTo(hidden)
        self.frontSailTop = boatModel.find('**/frontSailTop')
        self.frontSailTop.reparentTo(hidden)
        self.rearSail = boatModel.find('**/rearSail')
        self.rearSail.setTransparency(1)
        self.frontSail = boatModel.find('**/frontSail')
        self.frontSail.setTransparency(1)
        pos = self.frontSail.getPos()
        self.frontSail.setPos(pos[0], pos[1], pos[2] + 0.3)
        self.frontMast = boatModel.find('**/frontMast')
        self.rearMast = boatModel.find('**/backMast')
        for i in range(1, 4):
            boatModel.find('**/BlackFlat%d' % i).setBin('opaque', 50)

        self.brigModel = loader.loadModelCopy('piratepinball/art/bonebrig/BoneBrig')
        self.brigModel.setPos(0.0, 80, 0.0)
        self.brigModel.setScale(12)
        self.brigModel.find('**/LeftCageChain').setPos(-0.23, 0, 0)
        self.brigModel.find('**/RightCageChain').setPos(0.5, -0.02, 0.91)
        if EDITMODE:
            self.brigModel.reparentTo(render)
        else:
            self.brigModel.reparentTo(hidden)

    def makeHole(self, odeWorld, odeSpace, hx, hy, hz, innerRadius, outerRadius, depth, density, listToAppend, wallBooleans=[
 1, 1, 1, 1, 1, 1, 1, 1], myColor=Vec4(1, 1, 1, 1), tilt=0, normSeen=False, trans=1, numberOfSides=8):
        size = outerRadius - innerRadius
        radius = innerRadius + size / 2
        offX = hx
        offY = hy
        offZ = hz
        wallLength = math.sqrt(4 * (outerRadius * outerRadius / (math.cos(math.pi / numberOfSides) * math.cos(math.pi / numberOfSides)) - outerRadius * outerRadius))
        for i in range(0, numberOfSides):
            if wallBooleans[i]:
                boxPiece = ODEBox(wallLength, size, depth, density, odeWorld, odeSpace, isStatic=True, normallySeen=normSeen)
                boxPiece.setPos(radius * math.sin(i * (2 * math.pi / numberOfSides)) + offX, radius * math.cos(i * (2 * math.pi / numberOfSides)) + offY, offZ)
                boxPiece.setHpr((numberOfSides - i) * (360 / numberOfSides), tilt, 0)
                boxPiece.setColor(myColor)
                if trans != 1:
                    boxPiece.setTransparency(1)
                    boxPiece.setAlphaScale(trans)
                listToAppend.append(boxPiece)

    def createCrows(self):
        self.crowObjects = []
        density = 5.0
        self.makeHole(self.odeWorld, self.odeSpace, 0, -1, 17, 0.8, 3, 0.5, density, self.crowObjects, tilt=20, normSeen=False, myColor=self.crowColor)
        self.makeHole(self.odeWorld, self.odeSpace, 0, -1, 17.75, 2.7, 3, 1.5, density, self.crowObjects, [1, 1, 1, 1, 1, 1, 1, 1], tilt=5, normSeen=False, myColor=self.crowColor)
        self.makeHole(self.odeWorld, self.odeSpace, 0, -1, 22, 2.7, 3, 6, density, self.crowObjects, [0, 1, 1, 1, 1, 1, 1, 1], tilt=0, normSeen=False, myColor=self.boatColor)
        self.makeHole(self.odeWorld, self.odeSpace, 0, -1, 8.75, 0.8, 0.9, 15.5, density, self.crowObjects, normSeen=False, myColor=self.boatColor, trans=0.3)
        for object in self.crowObjects:
            sgode.pyode.dGeomSetCategoryBits(object.geom, GROUND_CATEGORY)
            object.setODETransformFromNodePath()
            if object.normallySeen:
                object.reparentTo(render)
            object.update()

    def createSlingshots(self):
        length = 6.2
        slingshotVelocity = 20.0
        density = 10.0
        self.leftSlingshot = Slingshot(length, slingshotVelocity, density, self.odeWorld, self.odeSpace, name='leftSlingshot')
        self.leftSlingshot.reparentTo(render)
        self.leftSlingshot.setPos(-5, -9.5, 0.5)
        self.leftSlingshot.setH(22.0)
        self.leftSlingshot.updateAfterTransformation()
        self.rightSlingshot = Slingshot(length, slingshotVelocity, density, self.odeWorld, self.odeSpace, name='leftSlingshot')
        self.rightSlingshot.reparentTo(render)
        self.rightSlingshot.setPos(5, -9.5, 0.5)
        self.rightSlingshot.setH(163.0)
        self.rightSlingshot.updateAfterTransformation()
        for object in (self.leftSlingshot.slingActor, self.rightSlingshot.slingActor):
            object.setColorScale(self.boatColor)

    def createPlunger(self):
        self.plungerVelocity = 60.0
        self.plungerFMax = 80000.0
        density = 10.0
        self.plunger = Plunger(self.plungerVelocity, self.plungerFMax, density, self.odeWorld, self.odeSpace, name='plunger')
        self.plunger.reparentTo(render)
        self.plunger.setPos(9.5, -2.0, 0.5)
        self.plunger.setScale(1, 0.8, 1)
        self.plunger.updateAfterTransformation()
        self.plunger.reparentTo(hidden)
        self.movables.append(self.plunger.box)

    def createGate(self):
        gx = 7.2
        gy = 24.6
        gz = 1.2
        self.gate = Gate(2, self.odeWorld, self.odeSpace)
        self.gate.setPos(gx, gy, gz)
        self.gate.setHpr(45, 0, 0)
        self.gate.setODETransformFromNodePath()
        self.gate.setCategory(FLIPPER_CATEGORY, True)
        self.gateHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(self.gateHinge, None, self.gate.body)
        sgode.pyode.dJointSetHingeAnchor(self.gateHinge, gx, gy, gz + 1)
        sgode.pyode.dJointSetHingeAxis(self.gateHinge, math.sqrt(2), math.sqrt(2), 0.0)
        sgode.pyode.dJointSetHingeParam(self.gateHinge, sgode.pyode.dParamLoStop, 0)
        sgode.pyode.dJointSetHingeParam(self.gateHinge, sgode.pyode.dParamHiStop, 1.5)
        sgode.pyode.dJointSetHingeParam(self.gateHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(self.gateHinge, sgode.pyode.dParamFMax, 100.0)
        self.gate.reparentTo(render)
        self.movables.append(self.gate)
        return

    def createFlippers(self):
        baseFlipperLength = 2.7
        self.pointsToShrinkFlipper = 1000000
        self.maxShrinkAllowed = 8
        mainFlipperLength = baseFlipperLength - min(self.maxShrinkAllowed, 0.1 * int(self.myScore / self.pointsToShrinkFlipper))
        mainLengthModifier = 0.2 * min(self.maxShrinkAllowed, int(self.myScore / self.pointsToShrinkFlipper))
        mainFlipperPos = Vec3(-2.21 - 0.02 * min(self.maxShrinkAllowed, int(self.myScore / self.pointsToShrinkFlipper)), -15.9 + 0.01 * min(self.maxShrinkAllowed, int(self.myScore / self.pointsToShrinkFlipper)), 0.6)
        density = 10.0
        self.flipperVelocity = 30.0
        rightFrontOffsets = [
         0, 298, 180, 90, 0, 0.1, 0]
        leftFrontOffsets = [0, 63, 180, 90, 0, -0.1, 0]
        rightRearOffsets = [2, 299, 180, 90, 0, 0.25, 0]
        leftRearOffsets = [1.5, 61, 180, 90, 0, -0.25, 0]
        leftBoneBrigOffsets = [-1.3, 0, 180, 90, 0, -0.1, 0]
        rightBoneBrigOffsets = [-1.3, 0, 180, 90, 0, 0.1, 0]
        leftFlipper = ODEFlipper(0.6, mainFlipperLength, density, self.odeWorld, self.odeSpace, 'piratepinball/art/misc/leftFlipper', offsets=leftFrontOffsets, zone=0, lengthModifier=mainLengthModifier, name='LeftMainFlipper')
        leftFlipper.setPos(mainFlipperPos)
        leftFlipper.setHpr(-180.0, 0, -90.0)
        leftFlipper.setODETransformFromNodePath()
        sgode.pyode.dGeomSetCategoryBits(leftFlipper.geom, FLIPPER_CATEGORY)
        leftFlipper.flipperHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(leftFlipper.flipperHinge, None, leftFlipper.body)
        sgode.pyode.dJointSetHingeAnchor(leftFlipper.flipperHinge, -3.51, -15.96, 0.6)
        sgode.pyode.dJointSetHingeAxis(leftFlipper.flipperHinge, 0.0, 0.0, 1.0)
        sgode.pyode.dJointSetHingeParam(leftFlipper.flipperHinge, sgode.pyode.dParamLoStop, -math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(leftFlipper.flipperHinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(leftFlipper.flipperHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(leftFlipper.flipperHinge, sgode.pyode.dParamFMax, 250000.0)
        sgode.pyode.dJointSetHingeParam(leftFlipper.flipperHinge, sgode.pyode.dParamStopERP, 0.8)
        sgode.pyode.dJointSetHingeParam(leftFlipper.flipperHinge, sgode.pyode.dParamStopCFM, 8e-06)
        sgode.pyode.dJointSetHingeParam(leftFlipper.flipperHinge, sgode.pyode.dParamFudgeFactor, 0.1)
        self.leftFlippers.append(leftFlipper)
        rightFlipper = ODEFlipper(0.6, mainFlipperLength, density, self.odeWorld, self.odeSpace, 'piratepinball/art/misc/rightFlipper', offsets=rightFrontOffsets, zone=0, lengthModifier=mainLengthModifier, name='RightMainFlipper')
        rightFlipper.setPos(-mainFlipperPos[0], mainFlipperPos[1], mainFlipperPos[2])
        rightFlipper.setHpr(0.0, 0.0, -90.0)
        rightFlipper.setODETransformFromNodePath()
        sgode.pyode.dGeomSetCategoryBits(rightFlipper.geom, FLIPPER_CATEGORY)
        rightFlipper.flipperHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(rightFlipper.flipperHinge, None, rightFlipper.body)
        sgode.pyode.dJointSetHingeAnchor(rightFlipper.flipperHinge, 3.51, -15.96, 0.6)
        sgode.pyode.dJointSetHingeAxis(rightFlipper.flipperHinge, 0.0, 0.0, -1.0)
        sgode.pyode.dJointSetHingeParam(rightFlipper.flipperHinge, sgode.pyode.dParamLoStop, -math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightFlipper.flipperHinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightFlipper.flipperHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(rightFlipper.flipperHinge, sgode.pyode.dParamFMax, 250000.0)
        sgode.pyode.dJointSetHingeParam(rightFlipper.flipperHinge, sgode.pyode.dParamStopERP, 0.8)
        sgode.pyode.dJointSetHingeParam(rightFlipper.flipperHinge, sgode.pyode.dParamStopCFM, 8e-06)
        sgode.pyode.dJointSetHingeParam(rightFlipper.flipperHinge, sgode.pyode.dParamFudgeFactor, 0.1)
        self.rightFlippers.append(rightFlipper)
        if self.myScore > 0:
            self.flipperFlash([leftFlipper, rightFlipper], Vec4(1, 0, 0, 1))
        lrfx = -9.3
        lrfy = 14.2
        leftRearFlipper = ODEFlipper(0.5, 1.5, density, self.odeWorld, self.odeSpace, 'piratepinball/art/misc/rearLeftFlipper', offsets=leftRearOffsets, zone=0, name='LeftTopDeckFlipper')
        leftRearFlipper.setPos(lrfx, lrfy, 3.3)
        leftRearFlipper.setHpr(-180.0, 0, -90.0)
        leftRearFlipper.setODETransformFromNodePath()
        sgode.pyode.dGeomSetCategoryBits(leftRearFlipper.geom, FLIPPER_CATEGORY)
        leftRearFlipper.flipperHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(leftRearFlipper.flipperHinge, None, leftRearFlipper.body)
        sgode.pyode.dJointSetHingeAnchor(leftRearFlipper.flipperHinge, lrfx - 0.9, lrfy + 0.3, 3.3)
        sgode.pyode.dJointSetHingeAxis(leftRearFlipper.flipperHinge, 0.0, 0.0, 1.0)
        sgode.pyode.dJointSetHingeParam(leftRearFlipper.flipperHinge, sgode.pyode.dParamLoStop, -math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(leftRearFlipper.flipperHinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(leftRearFlipper.flipperHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(leftRearFlipper.flipperHinge, sgode.pyode.dParamFMax, 100000.0)
        self.leftFlippers.append(leftRearFlipper)
        rrfx = 9.15
        rrfy = 14.2
        rightRearFlipper = ODEFlipper(0.5, 1.6, density, self.odeWorld, self.odeSpace, 'piratepinball/art/misc/rearRightFlipper', offsets=rightRearOffsets, zone=0, name='RightTopDeckFlipper')
        rightRearFlipper.setPos(rrfx, rrfy, 3.3)
        rightRearFlipper.setHpr(0.0, 0.0, -90.0)
        rightRearFlipper.setODETransformFromNodePath()
        sgode.pyode.dGeomSetCategoryBits(rightRearFlipper.geom, FLIPPER_CATEGORY)
        rightRearFlipper.flipperHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(rightRearFlipper.flipperHinge, None, rightRearFlipper.body)
        sgode.pyode.dJointSetHingeAnchor(rightRearFlipper.flipperHinge, rrfx + 0.97, rrfy + 0.33, 3.3)
        sgode.pyode.dJointSetHingeAxis(rightRearFlipper.flipperHinge, 0.0, 0.0, -1.0)
        sgode.pyode.dJointSetHingeParam(rightRearFlipper.flipperHinge, sgode.pyode.dParamLoStop, -math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightRearFlipper.flipperHinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightRearFlipper.flipperHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(rightRearFlipper.flipperHinge, sgode.pyode.dParamFMax, 100000.0)
        self.rightFlippers.append(rightRearFlipper)
        mfx = 7.45
        mfy = 4.1
        rightMidFlipper = ODEFlipper(0.5, 1.6, density, self.odeWorld, self.odeSpace, 'piratepinball/art/misc/rearRightFlipper', offsets=rightRearOffsets, zone=0, name='RightMidFlipper')
        rightMidFlipper.setPos(mfx, mfy, 0.5)
        rightMidFlipper.setHpr(0.0, 0.0, -90.0)
        rightMidFlipper.setODETransformFromNodePath()
        sgode.pyode.dGeomSetCategoryBits(rightMidFlipper.geom, FLIPPER_CATEGORY)
        rightMidFlipper.flipperHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(rightMidFlipper.flipperHinge, None, rightMidFlipper.body)
        sgode.pyode.dJointSetHingeAnchor(rightMidFlipper.flipperHinge, mfx + 0.79, mfy + 0.27, 0.5)
        sgode.pyode.dJointSetHingeAxis(rightMidFlipper.flipperHinge, 0.0, 0.0, -1.0)
        sgode.pyode.dJointSetHingeParam(rightMidFlipper.flipperHinge, sgode.pyode.dParamLoStop, -math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightMidFlipper.flipperHinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightMidFlipper.flipperHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(rightMidFlipper.flipperHinge, sgode.pyode.dParamFMax, 100000.0)
        self.rightFlippers.append(rightMidFlipper)
        leftBoneBrigFlipper = ODEFlipper(0.5, 2.2, density, self.odeWorld, self.odeSpace, 'piratepinball/art/misc/LeftBoneFlipper', offsets=leftBoneBrigOffsets, zone=1)
        leftBoneBrigFlipper.setPos(-2.3, 73.2, 0.6)
        leftBoneBrigFlipper.setHpr(-180.0, 0.0, -90.0)
        leftBoneBrigFlipper.setODETransformFromNodePath()
        sgode.pyode.dGeomSetCategoryBits(leftBoneBrigFlipper.geom, FLIPPER_CATEGORY)
        leftBoneBrigFlipper.flipperHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(leftBoneBrigFlipper.flipperHinge, None, leftBoneBrigFlipper.body)
        sgode.pyode.dJointSetHingeAnchor(leftBoneBrigFlipper.flipperHinge, -3.5, 73.3, 0.6)
        sgode.pyode.dJointSetHingeAxis(leftBoneBrigFlipper.flipperHinge, 0.0, 0.0, 1.0)
        sgode.pyode.dJointSetHingeParam(leftBoneBrigFlipper.flipperHinge, sgode.pyode.dParamLoStop, -math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(leftBoneBrigFlipper.flipperHinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(leftBoneBrigFlipper.flipperHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(leftBoneBrigFlipper.flipperHinge, sgode.pyode.dParamFMax, 250000.0)
        sgode.pyode.dJointSetHingeParam(leftBoneBrigFlipper.flipperHinge, sgode.pyode.dParamStopERP, 0.8)
        sgode.pyode.dJointSetHingeParam(leftBoneBrigFlipper.flipperHinge, sgode.pyode.dParamStopCFM, 8e-06)
        sgode.pyode.dJointSetHingeParam(leftBoneBrigFlipper.flipperHinge, sgode.pyode.dParamFudgeFactor, 0.1)
        self.leftFlippers.append(leftBoneBrigFlipper)
        self.errands['BoneBrig'].leftFlipper = leftBoneBrigFlipper
        rightBoneBrigFlipper = ODEFlipper(0.5, 2.2, density, self.odeWorld, self.odeSpace, 'piratepinball/art/misc/RightBoneFlipper', offsets=rightBoneBrigOffsets, zone=1)
        rightBoneBrigFlipper.setPos(2.3, 73.2, 0.6)
        rightBoneBrigFlipper.setHpr(0.0, 0.0, -90.0)
        rightBoneBrigFlipper.setODETransformFromNodePath()
        sgode.pyode.dGeomSetCategoryBits(rightBoneBrigFlipper.geom, FLIPPER_CATEGORY)
        rightBoneBrigFlipper.flipperHinge = sgode.pyode.dJointCreateHinge(self.odeWorld, None)
        sgode.pyode.dJointAttach(rightBoneBrigFlipper.flipperHinge, None, rightBoneBrigFlipper.body)
        sgode.pyode.dJointSetHingeAnchor(rightBoneBrigFlipper.flipperHinge, 3.5, 73.3, 0.6)
        sgode.pyode.dJointSetHingeAxis(rightBoneBrigFlipper.flipperHinge, 0.0, 0.0, -1.0)
        sgode.pyode.dJointSetHingeParam(rightBoneBrigFlipper.flipperHinge, sgode.pyode.dParamLoStop, -math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightBoneBrigFlipper.flipperHinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(rightBoneBrigFlipper.flipperHinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(rightBoneBrigFlipper.flipperHinge, sgode.pyode.dParamFMax, 250000.0)
        sgode.pyode.dJointSetHingeParam(rightBoneBrigFlipper.flipperHinge, sgode.pyode.dParamStopERP, 0.8)
        sgode.pyode.dJointSetHingeParam(rightBoneBrigFlipper.flipperHinge, sgode.pyode.dParamStopCFM, 8e-06)
        sgode.pyode.dJointSetHingeParam(rightBoneBrigFlipper.flipperHinge, sgode.pyode.dParamFudgeFactor, 0.1)
        self.rightFlippers.append(rightBoneBrigFlipper)
        self.errands['BoneBrig'].rightFlipper = rightBoneBrigFlipper
        self.allFlippers = self.leftFlippers + self.rightFlippers
        for object in self.leftFlippers + self.rightFlippers:
            object.reparentTo(render)
            self.movables.append(object)

        return

    def flipperFlash(self, flippers, flipperColor=Vec4(0, 1, 0, 1)):
        if self.flipperFlashSequence is not None:
            self.flipperFlashSequence.pause()
            self.flipperFlashSequence.finish()
        self.flipperFlashSequence = Sequence(name='flipperFlashSequence')
        for i in range(6):
            par = []
            for flipper in flippers:
                par.append(LerpColorScaleInterval(flipper, 0.1, flipperColor))

            self.flipperFlashSequence.append(Parallel(*par))
            for flipper in flippers:
                self.flipperFlashSequence.append(Func(flipper.setTextureOff, 1))

            par = []
            for flipper in flippers:
                par.append(LerpColorScaleInterval(flipper, 0.1, Vec4(1, 1, 1, 1)))

            self.flipperFlashSequence.append(Parallel(*par))
            for flipper in flippers:
                self.flipperFlashSequence.append(Func(flipper.clearTexture))

        self.flipperFlashSequence.start()
        return

    def cycleBeacons(self, cycleBeaconNumber):
        cycleBeaconNumber = cycleBeaconNumber + 1
        if cycleBeaconNumber > len(self.beacons):
            return
        if cycleBeaconNumber != 0:
            list(self.beacons.values())[(cycleBeaconNumber - 1)].revert()
        if cycleBeaconNumber != len(self.beacons):
            list(self.beacons.values())[cycleBeaconNumber].setState(Beacon.ON, fake=True)
        self.pbTaskMgr.doMethodLater(0.3, self.cycleBeacons, 'cyclebeacons', [cycleBeaconNumber])

    def deactivateBall(self, ballIndex, ball=None):
        if ballIndex == -1 and ball != None:
            for i in range(len(self.balls)):
                if self.balls[i] == ball:
                    ballIndex = i

        self.notify.debug(' entered deactivateBall, ballIndex = %d, ballsOnTable = %d ' % (ballIndex, self.ballsOnTable))
        if ballIndex == -1:
            self.notify.error('deactivateBall: Not given proper ballIndex or ball not in list, returning')
            return
        if not self.balls[ballIndex].active:
            self.notify.debug('deactivateBall: trying to deactivate inactive ball %d ' % ballIndex)
            return
        self.notify.debug('deactivateBall: deactivating ball number %d' % ballIndex)
        self.balls[ballIndex].setUnderAttack(False)
        self.balls[ballIndex].setSplash(False)
        sgode.pyode.dBodyDisable(self.balls[ballIndex].body)
        sgode.pyode.dGeomDisable(self.balls[ballIndex].geom)
        self.balls[ballIndex].setODEPos(9.3, 1, -2 + ballIndex)
        self.balls[ballIndex].reparentTo(hidden)
        self.balls[ballIndex].active = False
        self.ballsOnTable -= 1
        self.notify.debug('deactivateBall: Balls on table = %d' % self.ballsOnTable)
        self.notify.debug('deactivateBall: Balls on table = %d' % self.ballsOnTable)
        sgode.pyode.dBodySetLinearVel(self.balls[ballIndex].body, 0, 0, 0)
        self.notify.debug(' exiting deactivateBall, ballIndex = %d, ballsOnTable = %d ' % (ballIndex, self.ballsOnTable))
        return self.balls[ballIndex].getBallMode()

    def checkPlungerPower(self, taskInstance=None):
        if self.plungerPower < 0.4:
            if not self.nowletgoShowing:
                return
            self.pbTaskMgr.doMethodLater(0.5, self.checkPlungerPower, 'checkPlungerPower')
            return
        self.display.unlockDisplay()
        self.display.show(Localizer.pDisplayLaunchInstructions2, priority=True)

    def pressStart(self):
        if self.gameOver:
            if self.gamePaused:
                self.pauseGame()
            self.lostBallMgr.gameStarted()
            self.nowletgoShowing = True
            self.pbTaskMgr.doMethodLater(0.5, self.checkPlungerPower, 'checkPlungerPower')
            self.dropBall(True)
            self.display.start()
            self.display.show(Localizer.pDisplayLaunchInstructions1, priority=True)
            self.musicMgr.playMusic('MainDeck')
            self.pbTaskMgr.doMethodLater(2, self.dialogueMgr.playDialogue, 'playplungerdialogue', ['Plunger'])
            self.bonusManager.newGameStarted()
            if self.myScore == 0:
                self.dialogueMgr.playDialogue('WelcomeLong')
            else:
                self.dialogueMgr.playDialogue('WelcomeAboard')
            if self.myScore > self.highestScoreEver:
                self.highestScoreEver = self.myScore
            self.myScore = 0
            self.sentScoreAlready = False
            self.updateScore(0, 'refresh')
            self.display.hudElements['rightInstructions1']['text'] = Localizer.pDisplayPlungerInstructions
            self.gameOver = False
            self.display.startMapMoving(time=3)
            for e in list(self.errands.values()):
                e.start()

            return
        if self.inTutorialMode:
            for e in list(self.errands.values()):
                e.continueOn()

    def dropBall(self, getNextBall, tryNumber=0, bx=DEFAULT_BALL_START_POS[0], by=DEFAULT_BALL_START_POS[1], bz=DEFAULT_BALL_START_POS[2], camReset=True, ballMode=0, resetGravity=True):
        self.notify.debug(' entered dropBall, getNextBall = %d, ballsOnTable = %d ' % (getNextBall, self.ballsOnTable))
        if resetGravity:
            sgode.pyode.dWorldSetGravity(self.odeWorld, self.gravX, self.gravY, self.gravZ)
        hatchPop = False
        if bx == DEFAULT_BALL_START_POS[0] and by == DEFAULT_BALL_START_POS[1] and bz == DEFAULT_BALL_START_POS[2]:
            hatchPop = True
            if self.launchLaneEmpty:
                self.launchLaneEmpty = False
                self.beacons['LaunchArrow1'].setState(Beacon.BLINK)
                self.pbTaskMgr.doMethodLater(0.75 / 3.0, self.beacons['LaunchArrow2'].setState, 'startarrow2', [Beacon.BLINK])
                self.pbTaskMgr.doMethodLater(0.75 / 3.0 * 2.0, self.beacons['LaunchArrow3'].setState, 'startarrow3', [Beacon.BLINK])
                if self.displayFree:
                    self.display.show(Localizer.pFreeBall)
                    self.dialogueMgr.playDialogue('FreeBall')
                    self.displayFree = False
                else:
                    self.display.show(Localizer.pLaunch)
            else:
                if tryNumber > 60:
                    print("I've waited a minute, I'm not waiting any longer")
                    return
                else:
                    self.pbTaskMgr.doMethodLater(2, self.dropBall, 'dropballagainlanefull', [getNextBall, tryNumber + 1, DEFAULT_BALL_START_POS[0], DEFAULT_BALL_START_POS[1], DEFAULT_BALL_START_POS[2], True, ballMode])
                    self.display.show(Localizer.pWaitingLaunch)
                return
        if camReset:
            self.setCameraPosition('main')
        if getNextBall:
            self.myBallSaveManager.startSaveState()
            self.ballNumber = self.ballNumber + 1
            self.ballReserve = self.ballReserve - 1
            self.display.setBallNumber(self.ballReserve)
        if len(self.balls) <= 4:
            ball = PirateBall(0.5, self.ballDensity, self.odeWorld, self.odeSpace, mode=0, selfDestructMethod=self.deactivateBall)
            self.balls.append(ball)
        else:
            ball = None
            for i in range(len(self.balls)):
                if not self.balls[i].active:
                    ball = self.balls[i]
                    break

            if ball == None:
                self.notify.debug('dropBall:  Unable to find in-active ball for DropBall')
                return
            ball.setBallMode(ballMode)
            sgode.pyode.dGeomSetCollideBits(ball.geom, 4294967295 ^ DROPPED_CATEGORY)
            ball.active = True
            ball.reparentTo(render)
            ball.setODEPos(bx, by, bz)
            self.ballsOnTable += 1
            ball.setZone(self.currentZone)
            self.notify.debug('dropBall: Balls on table = %d' % self.ballsOnTable)
            if self.gamePaused:
                sgode.pyode.dBodyDisable(ball.body)
                sgode.pyode.dGeomDisable(ball.geom)
            else:
                sgode.pyode.dBodyEnable(ball.body)
                sgode.pyode.dGeomEnable(ball.geom)
        ball.update()
        if resetGravity:
            self.pirateSounds['PiratePinball_BallRelease'].play()
        if hatchPop:
            self.launchHatchMovement = Sequence(name='launchHatchMovement')
            self.launchHatchMovement.append(self.hatchLauncher.hprInterval(0.1, Point3(180.0, 0.0, 90.0)))
            self.launchHatchMovement.append(self.hatchLauncher.hprInterval(0.4, Point3(180.0, 0.0, 0.0), blendType='easeOut'))
            self.launchHatchMovement.start()
            self.display.hudElements['rightInstructions1']['text'] = Localizer.pDisplayPlungerInstructions
        return ball

    def dummy(self):
        pass

    def updateScore(self, updateValue, source):
        if self.scoreWrite and self.scoreFile == None:
            datetime = time.localtime()
            self.gameStartTime = time.time()
            filename = 'PiratesScoreFile_%d-%d_%d__%d-%d-%d.txt' % (datetime[1], datetime[2], datetime[0], datetime[3], datetime[4], datetime[5])
            self.scoreFile = open(filename, 'w')
        updateValue *= max(1, self.ballsOnTable)
        oldScore = self.myScore
        self.myScore = self.myScore + updateValue
        if self.scoreWrite and self.scoreFile != None:
            self.scoreFile.write('Pirates\t%d\t%d\t%s\t%d\t%d\n' % (updateValue, max(1, self.ballsOnTable), source, self.myScore, int(time.time() - self.gameStartTime)))
        if source != 'bonus_gameover':
            if int(self.myScore / self.pointsToShrinkFlipper) != int(oldScore / self.pointsToShrinkFlipper):
                self.shrinkFlippers()
        self.display.updateScore(self.myScore)
        return

    def shrinkFlippers(self):
        if int(self.myScore / self.pointsToShrinkFlipper) > self.maxShrinkAllowed:
            return
        self.destroyFlippers()
        self.createFlippers()
        self.difficultlyLevelAdvanced = True
        self.display.levelupSound.play()
        self.pauseBalls()
        self.pbTaskMgr.doMethodLater(3, self.pauseBalls, 'resumeBallsAfterPause', [False])
        self.display.show(Localizer.pLevelup, alert=True)

    def destroyFlippers(self):
        if self.flipperFlashSequence is not None:
            self.flipperFlashSequence.pause()
            self.flipperFlashSequence.finish()
        for f in self.allFlippers:
            if f is not None:
                f.destroy()

        del self.leftFlippers
        del self.rightFlippers
        del self.allFlippers
        tempMovables = []
        for m in self.movables:
            if not isinstance(m, ODEFlipper):
                tempMovables.append(m)

        self.movables = tempMovables
        self.leftFlippers = []
        self.rightFlippers = []
        self.allFlippers = []
        return

    def drainIn(self, ballIndex, args):
        self.myBallSaveManager.drainIn()

    def drained(self, ballIndex, args):
        if self.balls[ballIndex].getODEPos()[1] < -22:
            self.display.show(Localizer.pLostBall)
            ballMode = self.deactivateBall(ballIndex)
            self.pbTaskMgr.doMethodLater(1, self.drainTimer, 'draintimer%d' % ballIndex, [ballIndex, ballMode])

    def drainTimer(self, ballIndex, ballMode):
        if self.myBallSaveManager.isSaved():
            self.myBallSaveManager.reset()
            self.displayFree = True
            nextBall = False
            dropABall = True
        else:
            if self.ballsOnTable > 0 or self.errands['SkullAlleys'].ballsInSave > 0 or self.errands['CrowCannon'].cannonState == 0.5:
                dropABall = False
            else:
                dropABall = True
            nextBall = True
        if self.ballsOnTable < 2 and self.errands['CrowCannon'].getCannonState() == 0:
            self.errands['TopDeck'].openUpRamp()
            self.errands['CannonArea'].openCannon()
            self.musicMgr.playMusic('MainDeck')
            self.errands['MultiBall'].onlyOneBall()
            self.errands['CrowCannon'].start()
        if self.ballReserve == 0 and nextBall and dropABall:
            self.gameOver = True
            self.bonusManager.showBonus(gameOver=True)
            self.musicMgr.playMusic('Ocean')
            self.musicMgr.playJingle('DefeatJingle', musicContinue=True)
            self.pbTaskMgr.doMethodLater(1, self.dialogueMgr.playDialogue, 'playgameoverdialogue', ['GameOver'])
            self.pbTaskMgr.doMethodLater(2, self.dialogueMgr.playDialogue, 'playsailagaindialogue', ['SailAgain'])
            self.errands['CannonArea'].gameOver()
            self.resetGameState()
            self.display.gameOver()
            self.lostBallMgr.gameOver()
            self.display.hudElements['rightInstructions1']['text'] = Localizer.pDisplayStartInstructions
        if dropABall and not self.gameOver:
            if nextBall:
                self.dialogueMgr.playDialogue('TooBad')
                self.bonusManager.showBonus()
            self.dropBall(nextBall, ballMode=ballMode)

    def gateIn(self, ballIndex, args):
        self.launchLaneEmpty = True
        self.beacons['LaunchArrow1'].setState(Beacon.OFF)
        self.beacons['LaunchArrow2'].setState(Beacon.OFF)
        self.beacons['LaunchArrow3'].setState(Beacon.OFF)
        self.display.hudElements['rightInstructions1']['text'] = Localizer.pDisplayStatusInstructions
        if self.nowletgoShowing:
            self.nowletgoShowing = False
            self.display.unlockDisplay()
            self.display.show(Localizer.pDisplayGreatJob)
        self.myBallSaveManager.gateIn()

    def plankIn(self, ballIndex, args):
        self.display.show(Localizer.ppPiratePinballPlankDrain)
        self.updateScore(self.pointValues['PlankIn'], 'PlankIn')
        self.balls[ballIndex].setSplash(True)
        self.dialogueMgr.playDialogue('Plank')
        self.beacons['PlankBeacon'].setState(Beacon.ONCE, onceTime=3)

    def plankTimer(self, ballIndex, args):
        ballMode = self.balls[ballIndex].getBallMode()
        self.drainTimer(ballIndex, ballMode=ballMode)

    def checkProxPoints(self, currentBallIndex):
        pointList = list(self.proxPoints.values())
        for i in pointList:
            if i.zone == self.currentZone:
                i.checkPoint(currentBallIndex, self.balls[currentBallIndex])

    def slingIn(self, ballIndex, args):
        if args[0] == 'left':
            self.leftSlingshotInterval.start()
        if args[0] == 'right':
            self.rightSlingshotInterval.start()
        self.pirateSounds[('PiratePinball_Wood%d' % random.randint(0, 2))].play()

    def odeSimulationTask(self, task=None):
        if self.flippersEnabled:
            for f in self.allFlippers:
                if f.getZone() != self.currentZone:
                    continue
                if f.flipperOn:
                    sgode.pyode.dJointSetHingeParam(f.flipperHinge, sgode.pyode.dParamVel, self.flipperVelocity)
                else:
                    sgode.pyode.dJointSetHingeParam(f.flipperHinge, sgode.pyode.dParamVel, -self.flipperVelocity)

        dt = globalClock.getDt()
        (numSteps, lastStep) = divmod(dt, self.odeStepLength)
        for i in range(int(numSteps)):
            self.stepOnce(self.odeStepLength)

        self.stepOnce(lastStep)
        if self.plungerDepressed:
            self.plungerUpdate(dt)
        if self.errands['CannonArea'].underAttack:
            self.errands['CannonArea'].stepCannonMovement(dt)
        for movable in self.movables:
            if self.difficultlyLevelAdvanced:
                self.difficultlyLevelAdvanced = False
                break
            if movable.getZone() == self.currentZone and movable.active:
                movable.update()

        if self.currentZone == 0:
            if self.leftSlingshotOn:
                self.leftSlingshot.enableSlingshotForce()
            else:
                self.leftSlingshot.disableSlingshotForce()
            if self.rightSlingshotOn:
                self.rightSlingshot.enableSlingshotForce()
            else:
                self.rightSlingshot.disableSlingshotForce()
        pointList = list(self.proxPoints.values())
        pointsToCheck = [ point for point in pointList if point.zone == self.currentZone if point.active ]
        lowBall = False
        for ballIndex in range(0, len(self.balls)):
            currentBallPos = self.balls[ballIndex].getODEPos()
            if currentBallPos[1] < -60 or currentBallPos[2] < -20:
                self.notify.debug('deactivated rogue ball number %d' % ballIndex)
                self.deactivateBall(ballIndex)
            if self.balls[ballIndex].active:
                for point in pointsToCheck:
                    point.checkPoint(ballIndex, currentBallPos, self.balls[ballIndex].geom)

                self.balls[ballIndex].update()
                if currentBallPos[1] < 6:
                    lowBall = True

        if camera.getPos()[1] > -7 and lowBall and self.currentZone == 0 and not EDITMODE and not self.errands['CannonArea'].underAttack:
            self.setCameraPosition('main', time=1)
        collisionInfoList = self.worldInfo.collisionInfoList
        while collisionInfoList != None:
            collisionInfo = sgode.pyode.getCollisionInfoFromPointer(collisionInfoList)
            self.handleCollision(collisionInfo)
            collisionInfoList = collisionInfo.__next__

        sgode.pyode.clearCollisionInfoList(self.worldInfo.collisionInfoList)
        self.worldInfo.collisionInfoList = None
        return Task.cont

    def stepOnce(self, dt):
        sgode.pyode.dSpaceCollide(self.odeSpace, self.worldInfo, sgode.pyode.nearCallback)
        sgode.pyode.dWorldStep(self.odeWorld, dt)
        sgode.pyode.dJointGroupEmpty(self.odeContactGroup)

    def handleCollision(self, collisionInfo):
        if collisionInfo.geom1 in ODENodePath.geomsToNodePaths and collisionInfo.geom2 in ODENodePath.geomsToNodePaths:
            obj1, obj2 = ODENodePath.geomsToNodePaths[collisionInfo.geom1], ODENodePath.geomsToNodePaths[collisionInfo.geom2]
            bumper = None
            ball = None
            if sgode.pyode.dGeomGetCategoryBits(obj1.geom) & BUMPER_CATEGORY > 0 or sgode.pyode.dGeomGetCategoryBits(obj1.geom) & BUMPER_TRIGGER_CATEGORY > 0:
                bumper = obj1
                ball = obj2
            elif sgode.pyode.dGeomGetCategoryBits(obj2.geom) & BUMPER_CATEGORY > 0 or sgode.pyode.dGeomGetCategoryBits(obj2.geom) & BUMPER_TRIGGER_CATEGORY > 0:
                bumper = obj2
                ball = obj1
            if bumper != None:
                if bumper.gotHit(ball):
                    self.updateScore(self.pointValues['BumperHit'], 'BumperHit')
                    self.pirateSounds[('PiratePinball_Wood%d' % random.randint(0, 2))].play()
            trigger = None
            ball = None
            if obj1.isTrigger():
                trigger = obj1
                ball = obj2
            elif obj2.isTrigger():
                trigger = obj2
                ball = obj1
            if trigger != None:
                if trigger.getName() in self.triggers:
                    self.triggers[trigger.getName()].gotHit(ball)
        return


class PirateBall(ODEBall):
    __module__ = __name__
    splashSounds = [base.loadSfx(Localizer.PirateBall_Splash1), base.loadSfx(Localizer.PirateBall_Splash2)]

    def __init__(self, radius, ballDensity, odeWorld, odeSpace, normallySeen=True, mode=0, selfDestructMethod=None):
        ODEBall.__init__(self, radius, ballDensity, odeWorld, odeSpace, normallySeen=normallySeen, eggfile='piratepinball/art/bonebrig/SkullBall')
        self.ballMode = -1
        ballMaterial = Material()
        ballMaterial.setSpecular(VBase4(1, 1, 1, 1))
        ballMaterial.setShininess(30.0)
        self.model.setMaterial(ballMaterial)
        self.model.setTransparency(1)
        self.model.setBin('flat', 50)
        self.skull = self.model.find('**/skull')
        self.skull.setBin('flat', 45)
        self.myZone = 0
        self.setBallMode(mode)
        self.underAttack = False
        self.splash = False
        self.chilled = False
        self.mySplashManager = BillboardManager(name='ball%s' % self.getName(), howManyAtOnce=1, textureName='piratepinball/art/explosions/Splash', numberOfTextures=5, seconds=0.3, scale=2.0)
        cm = CardMaker('plane maker')
        cm.setFrame(-0.8, 0.8, -0.8, 0.8)
        self.shadow = NodePath(cm.generate())
        self.shadow.reparentTo(hidden)
        self.shadow.setHpr(0, 270, 0)
        self.shadow.setTransparency(1)
        self.shadow.setTexture(loader.loadTexture('pinballbase/shadow.png'))
        self.shadow.node().setAttrib(LightAttrib.makeAllOff())
        self.shadow.setColor(1, 1, 1, 0.4)
        self.selfDestruct = None
        if selfDestructMethod != None:
            self.selfDestruct = selfDestructMethod
        return

    def setChilled(self, bool):
        self.chilled = bool

    def destroy(self):
        self.mySplashManager.destroy()
        self.shadow.removeNode()
        self.skull.removeNode()
        while PirateBall.splashSounds != []:
            i = PirateBall.splashSounds.pop()
            del i

        ODEBall.destroy(self)

    def setSplash(self, splashBool, waterLevel=-3):
        self.splash = splashBool
        self.waterLevel = waterLevel

    def setUnderAttack(self, underAttack, waterLevel=-3):
        self.underAttack = underAttack
        self.waterLevel = waterLevel
        if self.underAttack:
            self.shadow.reparentTo(render)
        else:
            self.shadow.reparentTo(hidden)

    def getZone(self):
        return self.myZone

    def setZone(self, newZone):
        self.myZone = newZone

    def update(self):
        ODEBall.update(self)
        if self.splash:
            if self.getPos()[2] < self.waterLevel + 0.3:
                df = random.randint(0, len(PirateBall.splashSounds) - 1)
                PirateBall.splashSounds[df].setVolume(1)
                PirateBall.splashSounds[df].play()
                self.mySplashManager.startHere(self.getPos())
                self.splash = False
        if self.underAttack:
            currentPos = self.getPos()
            self.shadow.setPos(currentPos[0], currentPos[1], self.waterLevel + 0.05)
            shadowScale = abs(currentPos[2] / 10.0)
            if shadowScale < 1:
                shadowScale = 1
            self.shadow.setScale(shadowScale)
            if currentPos[2] < self.waterLevel + 0.3:
                df = random.randint(0, len(PirateBall.splashSounds) - 1)
                vol = 1 + currentPos[0] / 400
                if vol <= 0.1:
                    vol = 0.1
                PirateBall.splashSounds[df].setVolume(vol)
                PirateBall.splashSounds[df].play()
                self.mySplashManager.startHere(self.getPos())
                self.splash = False
                self.shadow.reparentTo(hidden)
                if self.selfDestruct != None:
                    self.selfDestruct(-1, ball=self)
        return

    def setBallMode(self, newMode):
        if self.ballMode == newMode:
            return
        self.ballMode = newMode
        if self.ballMode == 0:
            self.setColor(0.3, 0.3, 0.3, 1)
            self.skull.reparentTo(hidden)
        elif self.ballMode == 1:
            self.setColor(0.2, 0.7, 0.2, 0.3)
            self.skull.setColor(1, 1, 1, 1)
            self.skull.reparentTo(self.model)

    def getBallMode(self):
        return self.ballMode


class ODEFlipper(ODENodePath):
    __module__ = __name__

    def __init__(self, radius, length, density, odeWorld, odeSpace, eggFile, isStatic=False, name=None, offsets=[0, 0, 0, 0, 0, 0, 0], zone=0, lengthModifier=0):
        if name == None:
            name = 'ODEFlipper'
        ODENodePath.__init__(self, sgode.pyode.dCreateCCylinder(odeSpace, radius, length), odeWorld, isStatic, name, zone=zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetCappedCylinder(mass, density, 3, radius, length)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        self.flipperHinge = None
        self.flipperOn = False
        flipper1Model = loader.loadModelCopy(eggFile)
        flipper1Model.setScale(12 + offsets[0] - lengthModifier)
        newHpr = oldToNewHpr(VBase3(offsets[1], offsets[2], offsets[3]))
        flipper1Model.setHpr(newHpr)
        flipper1Model.setPos(offsets[4], offsets[5], offsets[6])
        flipper1Model.reparentTo(self)
        if False:
            cylinderModel = loader.loadModelCopy('pinballbase/cylinder')
            cylinderModel.setScale(radius, radius, length)
            cylinderModel.reparentTo(self)
            topCapModel = loader.loadModelCopy('pinballbase/cap')
            topCapModel.setScale(radius)
            topCapModel.setZ(length / 2.0)
            topCapModel.reparentTo(self)
            bottomCapModel = loader.loadModelCopy('pinballbase/cap')
            bottomCapModel.setP(180)
            bottomCapModel.setScale(radius)
            bottomCapModel.setZ(-length / 2.0)
            bottomCapModel.reparentTo(self)
            cylinderModel.setTransparency(1)
            cylinderModel.setAlphaScale(0.7)
            topCapModel.setTransparency(1)
            topCapModel.setAlphaScale(0.7)
            bottomCapModel.setTransparency(1)
            bottomCapModel.setAlphaScale(0.6)
        return

    def changeToZone(self, newZone, oldZone):
        if newZone == self.zone:
            sgode.pyode.dBodyEnable(self.body)
            sgode.pyode.dGeomEnable(self.geom)
        else:
            sgode.pyode.dBodyDisable(self.body)
            sgode.pyode.dGeomDisable(self.geom)