# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: RunPiratePinball.py
import string, re, codecs
from random import randint
from winreg import *
import base64, direct.directbase.DirectStart
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectDialog import DirectDialog
from direct.gui import DirectGuiGlobals
from direct.directnotify import DirectNotifyGlobal
from piratepinball.PiratePinball import PiratePinball
from pinballbase.odeConstructs import ODENodePath
from pinballbase.DirectMaxWidthLabel import DirectMaxWidthLabel
from pinballbase.DirectMaxScaleLabel import DirectMaxScaleLabel
from dgdCode.MainMenu import MainMenu
from dgdCode.HelpMenu import HelpMenu
from dgdCode.HighScore import HighScore
from dgdCode.PauseMenu import PauseMenu
import Localizer

class RunPiratePinball(direct.showbase.DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('RunPiratePinball')
    boardName = 'Pirate'
    defaultKeyValue = 'P---DEP=1000000&ARG=500000&YAR=250000&SME=125000&CAP=50000&---=0&---=0&---=0&---=0&---=0'

    def __init__(self):
        self.mDialog = None
        self.rolloverSound = base.loadSfx('pinballbase/mouseover')
        self.clickSound = base.loadSfx('pinballbase/mouseclick')
        DirectGuiGlobals.setDefaultRolloverSound(self.rolloverSound)
        DirectGuiGlobals.setDefaultClickSound(self.clickSound)
        self.palaceFont = loader.loadFont(Localizer.palaceFont)
        DirectGuiGlobals.setDefaultFont(self.palaceFont)
        self.accept('killPinballWorld', self.exitBoard)
        self.accept('reportPinballScore', self.reportPinballScore)
        self.accept('boardRunning', self.boardRunning)
        self.pinballPalaceElements = []
        self.buttons = {}
        self.hintLabel = DirectMaxScaleLabel(relief=None, text=Localizer.pHint, pos=(-1.215, 0.0, -0.72), text_scale=0.15, text_fg=(1,
                                                                                                                                    1,
                                                                                                                                    1,
                                                                                                                                    1), text_shadow=(0,
                                                                                                                                                     0,
                                                                                                                                                     0,
                                                                                                                                                     1), text_shadowOffset=(0.02,
                                                                                                                                                                            0.02), text_align=TextNode.ALeft, text_mayChange=1, maxWidth=0.3, maxHeight=0.15)
        self.hintLabel.reparentTo(hidden)
        self.tipLabel = DirectMaxWidthLabel(relief=None, text=Localizer.pTip1, pos=(-0.04, 0.0, -0.85), text_scale=0.15, text_fg=(1,
                                                                                                                                  1,
                                                                                                                                  1,
                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                   0,
                                                                                                                                                   0,
                                                                                                                                                   1), text_shadowOffset=(0.02,
                                                                                                                                                                          0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=2.35, maxXScale=0.15, maxYScale=0.15)
        self.tipLabel.reparentTo(hidden)
        pirateName = Localizer.ppDisplayGameName
        self.loadLabel = DirectMaxWidthLabel(relief=None, text=Localizer.pLoading, pos=(0,
                                                                                        0,
                                                                                        0), text_scale=0.21, text_fg=(1,
                                                                                                                      1,
                                                                                                                      1,
                                                                                                                      1), text_shadow=(0,
                                                                                                                                       0,
                                                                                                                                       0,
                                                                                                                                       1), text_shadowOffset=(0.02,
                                                                                                                                                              0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=0.75, maxXScale=0.21, maxYScale=0.21)
        self.loadingScreens = DirectLabel(scale=(1.33, 1.0, 1.0), image='dgdPirateArt/textures/loading.jpg', relief=None)
        self.loadingScreens.setPos(0, 0, 0)
        self.hideLoadingScreens()
        base.exitFunc = self.exit
        self.piratePinball = None
        self.piratesODEDicts = None
        self.nameList = [
         '', '', '', '', '', '', '', '', '', '']
        self.scoreList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.loadPinballScores()
        print('DEBUG: calling main menu')
        self.mainMenu = MainMenu(self)
        return

    def exitHighScoreGame(self):
        self.highScore.destroy()
        self.accept('escape', self.pauseGame)
        self.accept('p', self.pauseGame)
        self.accept('window-event', self.processWindowEvent)
        self.scoreString = ''
        x = 0
        while x < 10:
            self.scoreString += self.nameList[x] + '=' + str(self.scoreList[x]) + '&'
            x += 1

        self.writeHighScoreFile(string.rstrip(self.scoreString, '&'))
        self.piratePinball.display.setHudState(1)
        self.piratePinball.setupHooks()
        self.piratePinball.ignore('escape')
        self.piratePinball.ignore('p')
        self.piratePinball.ignore('window-event')
        props = base.win.getProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

    def writeHighScoreFile(self, string):
        scoreString = 'P---%s' % string
        scoreString = base64.encodestring(scoreString)
        try:
            scoreFile = open('pinball.dat', 'wb')
            scoreFile.write(scoreString)
            scoreFile.close()
        except:
            print('Problems writing Score file')

    def readHighScoreFile(self):
        score = None
        try:
            scoreFile = open('pinball.dat', 'rb')
            score = ('').join(scoreFile.readlines())
            score = base64.decodestring(score)
            scoreFile.close()
        except:
            print('Problems reading Score file')
            score = 'aaaaaa'

        if score[:4] != 'P---':
            s = self.defaultKeyValue
            e = base64.encodestring(s)
            try:
                scoreFile = open('pinball.dat', 'wb')
                scoreFile.write(e)
                scoreFile.close()
            except:
                print('Problems reading Score file')
            else:
                score = s
        return score[4:]

    def exitHighScore(self):
        self.highScore.destroy()
        self.accept('escape', self.pauseGame)
        self.accept('p', self.pauseGame)
        if not self.fromGame:
            self.mainMenu.show()
        else:
            if self.piratePinball.errands['CannonArea'].board.currentZone != 2:
                self.piratePinball.display.setHudState(1)
                self.piratePinball.display.showMap()
            self.accept('window-event', self.processWindowEvent)
        self.fromGame = False

    def exitHelpMenu(self):
        self.helpMenu.destroy()
        self.accept('escape', self.pauseGame)
        self.accept('p', self.pauseGame)
        if not self.fromGame:
            self.mainMenu.show()
        else:
            if self.piratePinball.errands['CannonArea'].board.currentZone != 2:
                self.piratePinball.display.setHudState(1)
                self.piratePinball.display.showMap()
            self.accept('window-event', self.processWindowEvent)
        self.fromGame = False

    def quitGame(self):
        if self.mDialog is not None:
            self.mDialog.destroy()
            self.mDialog = None
        self.pauseMenu.destroy()
        self.piratePinball.exit()
        self.ignore('escape')
        self.ignore('p')
        return

    def createHighScore(self, bool=False):
        self.fromGame = bool
        if self.fromGame:
            self.piratePinball.display.setHudState(0)
            self.piratePinball.display.hideMap()
            self.ignore('window-event')
        self.mainMenu.hide()
        self.highScore = HighScore(self, self.nameList, self.scoreList, 10, self.defaultInitials)

    def createHelpMenu(self, bool=False):
        self.fromGame = bool
        if self.fromGame:
            self.piratePinball.display.setHudState(0)
            self.piratePinball.display.hideMap()
            self.ignore('window-event')
        self.mainMenu.hide()
        self.helpMenu = HelpMenu(self)

    def killMe(self):
        self.piratePinball.ballReserve = 0
        self.piratePinball.myBallSaveManager.ballSaveState = 0

    def exit(self):
        self.notify.info('exit: Leaving PinballPalace')
        self.mainMenu.destroy()
        if self.piratesODEDicts != None:
            ODENodePath.geomsToNodePaths = self.piratesODEDicts[0]
            ODENodePath.namesToGeoms = self.piratesODEDicts[1]
        if self.piratePinball != None:
            self.piratePinball.destroy()
            del self.piratePinball
        del self.rolloverSound
        del self.clickSound
        sys.exit()
        return

    def uploadScore(self):
        self.scoreString = ''
        x = 0
        while x < 10:
            self.scoreString += self.nameList[x] + '=' + str(self.scoreList[x]) + '&'
            x += 1

        try:
            self.key = CreateKey(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Disney\\Disney Online\\DGD_Pirate\\Results')
            SetValueEx(self.key, 'score', 0, REG_SZ, string.rstrip(self.scoreString, '&'))
        except:
            self.mDialog = DirectDialog(relief=None, scale=(0.05, 0.1, 0.1), image='dgd%sArt/textures/pirate_button_back.png' % self.boardName, pos=(0,
                                                                                                                                                     0,
                                                                                                                                                     0.3), fadeScreen=None, button_relief=None, text="Your computer settings prevent Pirate Pinball\nfrom uploading high scores.  If you would like to upload\nyour high scores, please have the computer's administrator\nlog in before starting the game.", text_scale=(1.4,
                                                                                                                                                                                                                                                                                                                                                                                                                          1,
                                                                                                                                                                                                                                                                                                                                                                                                                          1), buttonImageList=['dgd%sArt/textures/pirate_button.png' % self.boardName], sidePad=0, command=self.clearMDialog)
            self.mDialog['image_scale'] = Vec3(18, 7, 7)
            for i in range(self.mDialog.numButtons):
                self.mDialog.buttonList[i]['image_scale'] = Vec3(3, 1, 1)

            self.mDialog.setTransparency(1)

        return

    def clearMDialog(self, res=None):
        if self.mDialog is not None:
            self.mDialog.destroy()
            self.mDialog = None
        return

    def runBoard(self):
        self.mainMenu.hide()
        for b in list(self.buttons.values()):
            b.reparentTo(hidden)

        for element in self.pinballPalaceElements:
            element.reparentTo(hidden)

        self.loadingScreens.reparentTo(aspect2d, 54)
        self.loadLabel.reparentTo(aspect2d, 55)
        self.ran = randint(1, 6)
        self.tipLabel['text'] = getattr(Localizer, 'pTip%d' % self.ran)
        self.tipLabel.reparentTo(aspect2d, 55)
        self.hintLabel.reparentTo(aspect2d, 55)
        taskMgr.doMethodLater(0.1, self.startBoard, 'startBoard', [])

    def startBoard(self):
        if self.piratesODEDicts != None:
            ODENodePath.geomsToNodePaths = self.piratesODEDicts[0]
            ODENodePath.namesToGeoms = self.piratesODEDicts[1]
        if self.piratePinball == None:
            self.piratePinball = PiratePinball()
        else:
            self.piratePinball.wake()
        self.piratePinball.ignore('escape')
        self.piratePinball.ignore('p')
        self.piratePinball.ignore('window-event')
        self.accept('escape', self.pauseGame)
        self.accept('p', self.pauseGame)
        self.mainWinForeground = 1
        self.ignore('window-event')
        self.accept('window-event', self.processWindowEvent)
        menuFade = Sequence(name='menuFade')
        menuFade.append(Wait(0.01))
        menuFade.append(Func(self.hideLoadingScreens))
        for element in self.pinballPalaceElements:
            menuFade.append(Func(element.reparentTo, hidden))

        menuFade.start()
        return

    def boardRunning(self):
        self.piratePinball.display.controlsOver = True
        self.piratePinball.display.unPause()
        self.piratePinball.display.setHudState(1)

    def processWindowEvent(self, win):
        properties = win.getProperties()
        if properties.getForeground() and not self.mainWinForeground:
            self.mainWinForeground = 1
        elif not properties.getForeground() and self.mainWinForeground:
            self.mainWinForeground = 0
            if not self.piratePinball.gamePaused and not self.piratePinball.inTutorialMode:
                self.pauseGame()

    def pauseGame(self):
        if not self.piratePinball.bumpManager.bumpEnabled:
            return
        if self.piratePinball.inTutorialMode:
            self.piratePinball.pauseGame()
            return
        else:
            self.piratePinball.pauseGame()
        if self.piratePinball.gamePaused:
            self.piratePinball.display.unPause()
            if self.piratePinball.display.grayScreen and not base.direct:
                self.piratePinball.display.grayScreen.reparentTo(aspect2d, 90)
            self.pauseMenu = PauseMenu(self)
            self.piratePinball.ignore('enter')
        else:
            try:
                self.pauseMenu.destroy()
                self.piratePinball.accept('enter', self.piratePinball.pressStart)
            except:
                print('ERROR -- Problems destroying pauseMenu')

    def hideLoadingScreens(self):
        self.loadLabel.reparentTo(hidden)
        self.tipLabel.reparentTo(hidden)
        self.hintLabel.reparentTo(hidden)
        self.loadingScreens.reparentTo(hidden)

    def addCommas(self, amount):
        orig = amount
        new = re.sub('^(-?\\d+)(\\d{3})', '\\g<1>,\\g<2>', amount)
        if orig == new:
            return new
        else:
            return self.addCommas(new)

    def loadPinballScores(self):
        self.val = self.readHighScoreFile()
        try:
            self.list = string.split(self.val, '&')
            self.defaultInitials = ''
            self.count = 0
            for x in self.list:
                self.temp = string.split(x, '=')
                self.nameList[self.count] = self.temp[0]
                self.scoreList[self.count] = string.atoi(self.temp[1])
                self.count += 1

        except:
            self.val = self.defaultKeyValue[4:]
            self.list = string.split(self.val, '&')
            self.defaultInitials = ''
            self.count = 0
            for x in self.list:
                self.temp = string.split(x, '=')
                self.nameList[self.count] = self.temp[0]
                self.scoreList[self.count] = string.atoi(self.temp[1])
                self.count += 1

    def reportPinballScore(self, boardID, score):
        if score < self.scoreList[9]:
            return
        self.piratePinball.ignoreAll()
        self.ignore('p')
        self.ignore('escape')
        self.ignore('window-event')
        props = base.win.getProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        x = 9
        while score > self.scoreList[(x - 1)]:
            if x == 0:
                break
            self.scoreList[x] = self.scoreList[(x - 1)]
            self.nameList[x] = self.nameList[(x - 1)]
            x -= 1

        self.scoreList[x] = int(score)
        self.nameList[x] = 'AAA'
        self.myTopScoreIndex = x
        self.accept('bonusDoneShowing', self.finishReport)
        self.accept('enter', self.finishReport)

    def finishReport(self):
        self.ignore('bonusDoneShowing')
        self.ignore('enter')
        self.piratePinball.display.setHudState(0)
        self.highScore = HighScore(self, self.nameList, self.scoreList, self.myTopScoreIndex, self.defaultInitials)

    def exitBoard(self, boardID, score):
        self.notify.debug('Put Pirates to sleep')
        self.piratePinball.sleep()
        self.piratesODEDicts = (ODENodePath.geomsToNodePaths, ODENodePath.namesToGeoms)
        ODENodePath.namesToGeoms = {}
        ODENodePath.geomsToNodePaths = {}
        self.mainMenu.show(True)

    def checkCleanup(self, task=None):
        allowedTasks = ('dataLoop', 'doLaterProcessor', 'eventManager', 'igLoop', 'collisionLoop',
                        'shadowCollisionLoop', 'ivalLoop', 'tkLoop', 'DIRECTContextTask',
                        'resetPrevTransform', 'checkcleanup')
        problems = []
        for taskPriList in taskMgr.taskList:
            for task in taskPriList:
                if task is None:
                    continue
                elif task.isRemoved():
                    continue
                elif task.name in allowedTasks:
                    continue
                else:
                    problems.append(task.name)

        if problems:
            print(taskMgr)
            msg = "You can't leave the Pinball Board until you clean up your tasks:"
            for task in problems:
                msg += '\n  ' + task

            self.notify.error(msg)
        if ivalMgr.getNumIntervals() > 0:
            print(ivalMgr)
            self.notify.error("You can't leave the Pinball Board until you clean up your intervals.")
        allowedHooks = [
         'resetClock', 'window-event', 'killPinballWorld', 'reportPinballScore', 'click-mouse1-apButton', 'click-mouse1-mpButton', 'click-mouse1-ppButton', 'click-mouse1-exitButton', 'enter-mpButton', 'exit-mpButton', 'enter-apButton', 'exit-apButton', 'enter-ppButton', 'exit-ppButton']
        problems = []
        for hook in list(messenger.dict.keys()):
            if hook in allowedHooks:
                pass
            else:
                problems.append(hook)

        if problems:
            print(messenger)
            msg = "You can't leave the PinballBoard until you clean up your hooks:"
            for hook in problems:
                msg += '\n  ' + hook

            self.notify.error(msg)
        if ODENodePath.geomsToNodePaths != {}:
            self.notify.warning('All ODE geoms to NodePaths not cleaned up')
            self.notify.warning(ODENodePath.geomsToNodePaths)
        if ODENodePath.namesToGeoms != {}:
            self.notify.warning('All ODE names to Geoms not cleaned up')
            self.notify.warning(ODENodePath.namesToGeoms)
        self.mainMenu.show(True)
        return


def main():
    taskMgr.doMethodLater(0.3, startGame, 'startMainGame')
    base.graphicsEngine.renderFrame()
    run()


def startGame(task=None):
    pinballPalace = RunPiratePinball()


if __name__ == '__main__':
    main()