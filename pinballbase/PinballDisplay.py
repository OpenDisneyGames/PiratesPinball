# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: PinballDisplay.py
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
import random, string
from direct.gui import DirectGuiGlobals
from direct.directnotify import DirectNotifyGlobal
import Localizer, re
from pinballbase.DirectMaxScaleLabel import DirectMaxScaleLabel
from pinballbase.DirectMaxScaleButton import DirectMaxScaleButton
from pinballbase.PinballElements import PlayTimer

class PinballDisplay:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballDisplay.PinballDisplay')

    def __init__(self, world, fontName, idleMessages, attractMessages):
        self.hudElements = {}
        self.tutorialElements = {}
        self.world = world
        self.extraBallLimit = 5
        self.numberOfLines = 3
        self.controlsOver = False
        self.grayScreen = None
        self.controlLabels = None
        self.alertMessageSequence = None
        if self.world.fromPalace == True:
            self.playTimer = PlayTimer()
        self.scoreLineLabel = None
        self.scoreLine = None
        self.lines = []
        self.hudElements['mainBackground'] = None
        self.instructions = None
        self.tutorialElements['tutorialLabel'] = None
        self.hudElements['ballHolder'] = None
        self.exitButton = None
        self.resumeButton = None
        self.tutorialElements['continueOn'] = None
        self.tutorialElements['skipIt'] = None
        self.tutorialElements['instructionsBackground'] = None
        self.ballIcons = []
        self.extraBallsReleased = 0
        self.extraBallScoreBase = 250000
        self.extraBallMultiplier = 4
        self.extraBallSound = base.loadSfx('pinballbase/extraBall')
        self.levelupSound = base.loadSfx('pinballbase/levelup')
        self.myScore = 0
        self.idleState = 0
        self.shouldIdle = False
        self.alertMode = True
        self.displayLocked = False
        self.numBallsLeft = 3
        taskMgr.doMethodLater(30, self.idle, 'idletimer')
        if fontName != None:
            font = loader.loadFont(fontName)
            DirectGuiGlobals.setDefaultFont(font)
        self.numberFont = loader.loadFont('DomCasualBT.ttf')
        self.hudState = 3
        self.exitButton = DirectMaxScaleButton(relief=None, command=self.world.exit, image=('pinballbase/exitButton.png',
                                                                                            'pinballbase/exitButtonOver.png',
                                                                                            'pinballbase/exitButtonOver.png'), scale=(0.2,
                                                                                                                                      1.0,
                                                                                                                                      0.2), image_scale=(1.7,
                                                                                                                                                         1.0,
                                                                                                                                                         0.85), pos=(0.4, 0, -0.65), text_pos=(-0.03,
                                                                                                                                                                                               -0.08), text=Localizer.pDisplayExitButton, text_fg=(1,
                                                                                                                                                                                                                                                   1,
                                                                                                                                                                                                                                                   1,
                                                                                                                                                                                                                                                   1), text_shadow=(1,
                                                                                                                                                                                                                                                                    1,
                                                                                                                                                                                                                                                                    1,
                                                                                                                                                                                                                                                                    1), text_shadowOffset=(0.02,
                                                                                                                                                                                                                                                                                           0.02), maxHeight=0.37, maxWidth=2.2)
        self.exitButton.reparentTo(hidden)
        self.exitButton.setTransparency(1)
        self.resumeButton = DirectMaxScaleButton(relief=None, command=self.world.pauseGame, image=('pinballbase/resumeButton.png',
                                                                                                   'pinballbase/resumeButtonOver.png',
                                                                                                   'pinballbase/resumeButtonOver.png'), scale=(0.2,
                                                                                                                                               1.0,
                                                                                                                                               0.2), image_scale=(1.7,
                                                                                                                                                                  1.0,
                                                                                                                                                                  0.85), pos=(-0.4, 0, -0.65), text_pos=(-0.02,
                                                                                                                                                                                                         -0.06), text=Localizer.pDisplayResumeButton, text_fg=(1,
                                                                                                                                                                                                                                                               1,
                                                                                                                                                                                                                                                               1,
                                                                                                                                                                                                                                                               1), text_shadow=(1,
                                                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                                                1), text_shadowOffset=(0.02,
                                                                                                                                                                                                                                                                                                       0.02), maxHeight=0.37, maxWidth=2.2)
        self.resumeButton.reparentTo(hidden)
        self.resumeButton.setTransparency(1)
        self.alertMessageLabel = DirectMaxScaleLabel(relief=None, pos=(0, 0, 0), text=' ', text_fg=(1,
                                                                                                    1,
                                                                                                    1,
                                                                                                    1), text_shadow=(0,
                                                                                                                     0,
                                                                                                                     0,
                                                                                                                     1), text_shadowOffset=(0.02,
                                                                                                                                            0.02), maxWidth=1.8, maxHeight=0.3)
        self.alertMessageLabel.reparentTo(hidden)
        self.alertMessageLabel.setTransparency(1)
        self.idleMessages = idleMessages
        self.attractMessages = attractMessages
        return

    def increaseScore(self):
        self.world.updateScore(49900, 'increase')

    def finishInit(self):
        self.instructionFont = loader.loadFont(Localizer.instructionFont)
        self.hudElements['leftInstructions1'].component('text0').setFont(self.instructionFont)
        self.hudElements['leftInstructions2'].component('text0').setFont(self.instructionFont)
        self.hudElements['rightInstructions1'].component('text0').setFont(self.instructionFont)
        self.hudElements['rightInstructions2'].component('text0').setFont(self.instructionFont)
        self.tutorialElements['continueOn'].component('text0').setFont(self.instructionFont)
        self.tutorialElements['skipIt'].component('text0').setFont(self.instructionFont)
        self.scoreFont = loader.loadFont(Localizer.scoreFont)
        self.scoreLineLabel.component('text0').setFont(self.scoreFont)
        self.scoreLine.component('text0').setFont(self.scoreFont)
        if Localizer.myLanguage != 'japanese':
            for l in self.lines:
                l['squish'] = True

        self.threeLinesZValues = []
        self.twoLinesZValues = []
        self.statusLineInitialZ = self.lines[0].getZ()
        self.statusLineZIncrement = self.lines[0].getZ() - self.lines[1].getZ()
        for line in self.lines:
            self.threeLinesZValues.append(line.getZ())

        self.twoLinesZValues.append(self.threeLinesZValues[0] + (self.threeLinesZValues[1] - self.threeLinesZValues[0]) / 2.0)
        self.twoLinesZValues.append(self.threeLinesZValues[1] + (self.threeLinesZValues[2] - self.threeLinesZValues[1]) / 2.0)

    def gameRunning(self):
        cm = CardMaker('animatedBillboardNode')
        cm.setFrame(-1, 1, -1, 1)
        self.grayScreen = NodePath(cm.generate())
        self.grayScreen.reparentTo(aspect2d, 90)
        self.grayScreen.setTransparency(1)
        self.grayScreen.setColorScale(0, 0, 0, 0.6)
        self.grayScreen.setPos(0, 0, 0)
        self.grayScreen.setScale(10)
        self.controlText = [
         (
          Localizer.pEsc, Localizer.pPauseResume), (Localizer.pDownArrow, Localizer.pLaunchBall), (Localizer.pLeftControl, Localizer.pLeftFlipper), (Localizer.pRightControl, Localizer.pRightFlipper), (Localizer.pTiltControls, Localizer.pTiltInstructions), (Localizer.pEnter, Localizer.pStartGame)]
        if Localizer.myLanguage == 'japanese':
            self.controlLabels = []
            self.controlLabels.append(DirectLabel(relief=None, scale=(1, 1, 0.8), image='pinballbase/help_screen_background_top.png'))
            self.controlLabels[0].setTransparency(1)
            self.controlLabels[0].reparentTo(aspect2d, 100)
            self.controlLabels.append(DirectLabel(relief=None, pos=(0, 0, -0.6), scale=(1,
                                                                                        1,
                                                                                        0.2), image='pinballbase/help_screen_background_bottom.png'))
            self.controlLabels[1].setTransparency(1)
            self.controlLabels[1].reparentTo(aspect2d, 100)
            self.grayScreen.setColorScale(0, 0, 0, 0.75)
        if Localizer.myLanguage != 'japanese':
            self.controlLabels = []
            cl = DirectMaxScaleLabel(relief=None, text=Localizer.pControls, pos=(0.05,
                                                                                 0.0,
                                                                                 0.67), text_fg=(1,
                                                                                                 1,
                                                                                                 1,
                                                                                                 1), text_shadow=(0,
                                                                                                                  0,
                                                                                                                  0,
                                                                                                                  1), text_shadowOffset=(0.02,
                                                                                                                                         0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=1, maxHeight=0.2)
            self.controlLabels.append(cl)
            i = 0
            for ct in self.controlText:
                i += 1
                if i == len(self.controlText):
                    i += 1
                    textfg = (0.4, 1, 0.4, 1)
                else:
                    textfg = (1, 1, 1, 1)
                cl = DirectMaxScaleLabel(relief=None, text=ct[0], pos=(-0.02, 0.0, 0.57 - i * 0.18), text_fg=textfg, text_shadow=(0,
                                                                                                                                  0,
                                                                                                                                  0,
                                                                                                                                  1), text_shadowOffset=(0.02,
                                                                                                                                                         0.02), text_align=TextNode.ARight, text_mayChange=1, maxWidth=1.0, maxHeight=0.17)
                self.controlLabels.append(cl)
                cl = DirectMaxScaleLabel(relief=None, text='-', pos=(0.06, 0.0, 0.57 - i * 0.18), text_fg=textfg, text_shadow=(0,
                                                                                                                               0,
                                                                                                                               0,
                                                                                                                               1), text_shadowOffset=(0.02,
                                                                                                                                                      0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=1.1, maxHeight=0.17)
                self.controlLabels.append(cl)
                cl = DirectMaxScaleLabel(relief=None, text=ct[1], pos=(0.14, 0.0, 0.57 - i * 0.18), text_fg=textfg, text_shadow=(0,
                                                                                                                                 0,
                                                                                                                                 0,
                                                                                                                                 1), text_shadowOffset=(0.02,
                                                                                                                                                        0.02), text_align=TextNode.ALeft, text_mayChange=1, maxWidth=1.0, maxHeight=0.17)
                self.controlLabels.append(cl)

            for cl in self.controlLabels:
                cl.reparentTo(aspect2d, 100)
                cl.component('text0').setFont(self.instructionFont)

            self.setSmallestScale(self.controlLabels)
        self.controlsOver = False
        messenger.send('boardRunning')
        if not self.world.gameOver:
            self.start()
        return

    def setSmallestScale(self, labels):
        smallestScaleX = 100
        smallestScaleY = 100
        for lineIndex in range(len(labels)):
            if labels[lineIndex]['text'] == '':
                continue
            lscale = labels[lineIndex]['text_scale']
            if isinstance(lscale, tuple) or isinstance(lscale, list):
                if lscale[0] < smallestScaleX:
                    smallestScaleX = lscale[0]
                    smallestScaleY = lscale[1]
            elif lscale < smallestScaleX and lscale < smallestScaleX:
                smallestScaleX = lscale

        for lineIndex in range(len(labels)):
            labels[lineIndex]['text_scale'] = (
             smallestScaleX, smallestScaleY)

        return smallestScaleY

    def resetExtraBallNumber(self):
        self.extraBallsReleased = 0

    def start(self):
        self.idleState = 0
        if self.world.fromPalace:
            self.playTimer.reset()
            self.playTimer.playing()
        self.world.pbTaskMgr.doMethodLater(1, self.resetExtraBallNumber, 'resetextraballnumber')
        self.setHudState(1)
        self.controlsOver = True
        if self.grayScreen:
            self.grayScreen.reparentTo(hidden)
        if self.controlLabels != None:
            for cl in self.controlLabels:
                cl.reparentTo(hidden)

        return

    def wake(self):
        taskMgr.doMethodLater(30, self.idle, 'idletimer')
        self.extraBallSound = base.loadSfx('pinballbase/extraBall')
        self.levelupSound = base.loadSfx('pinballbase/levelup')

    def sleep(self):
        taskMgr.remove('idletimer')
        if self.grayScreen:
            self.grayScreen.reparentTo(hidden)
        del self.extraBallSound
        del self.levelupSound
        if self.controlLabels != None:
            for cl in self.controlLabels:
                cl.reparentTo(hidden)
                cl.removeNode()

            self.controlLabels = None
        return

    def destroy(self):
        self.sleep()
        if self.grayScreen:
            self.grayScreen.removeNode()
        taskMgr.remove('idletimer')
        for (key, p) in self.hudElements.items():
            self.notify.debug('deleteing hud element: %s' % key)
            p.destroy()
            p.removeNode()
            del self.hudElements[key]

        for (key, p) in self.tutorialElements.items():
            self.notify.debug('deleteing tutorial element: %s' % key)
            p.destroy()
            p.removeNode()
            del self.tutorialElements[key]

        del self.hudElements
        del self.tutorialElements
        del self.world
        self.exitButton.destroy()
        self.exitButton.removeNode()
        del self.exitButton
        if self.alertMessageSequence is not None:
            self.alertMessageSequence.finish()
        self.alertMessageLabel.destroy()
        self.resumeButton.destroy()
        self.resumeButton.removeNode()
        del self.resumeButton
        self.scoreLineLabel.removeNode()
        self.scoreLine.removeNode()
        self.instructions.removeNode()
        while self.lines != []:
            l = self.lines.pop()
            l.removeNode()

        while self.ballIcons != []:
            b = self.ballIcons.pop()
            b.destroy()
            del b

        return

    def displayCommonText(self, text):
        for i in range(self.numberOfLines):
            self.lines[i]['text'] = ''

        barSubtract = string.count(text, '|') * 2
        self.notify.debug('displayCommonText: amount of characters lost to |s is %d ' % barSubtract)
        characterLengthOfText = len(text) - barSubtract
        averageCharacterLineLength = characterLengthOfText / self.numberOfLines
        if Localizer.myLanguage == 'japanese':
            newLines = text.split(Localizer.japanSep)
        else:
            splitText = text.split()
            self.notify.debug('displayCommonText: characterLengthOfText = %d and average is %d ' % (characterLengthOfText, averageCharacterLineLength))
            newLines = ['']
            lineCount = 0
            wordIndex = -1
            for i in range(len(splitText)):
                wordIndex += 1
                if wordIndex >= len(splitText):
                    break
                enforcedBreakAtEnd = False
                while splitText[wordIndex] == '|':
                    if newLines[lineCount] != '':
                        lineCount += 1
                    wordIndex += 1
                    if wordIndex >= len(splitText):
                        enforcedBreakAtEnd = True
                        self.notify.warning(' displayCommonText: Text with a | as last character entered')
                    if lineCount >= self.numberOfLines:
                        lineCount -= 1
                        break
                    else:
                        newLines.append('')

                if enforcedBreakAtEnd:
                    break
                if newLines[lineCount] == '':
                    newLines[lineCount] += splitText[wordIndex]
                elif Localizer.myLanguage == 'japanese':
                    newLines[lineCount] += splitText[wordIndex]
                else:
                    newLines[lineCount] += ' ' + splitText[wordIndex]
                if len(newLines[lineCount]) >= averageCharacterLineLength:
                    if lineCount + 1 < self.numberOfLines:
                        lineCount += 1
                        newLines.append('')

        while newLines[(len(newLines) - 1)] == '':
            newLines.pop()

        self.notify.debug('displayCommonText: newlines')
        self.notify.debug(newLines)
        success = True
        while len(newLines) > self.numberOfLines and success:
            success = False
            for i in range(len(newLines)):
                if newLines[i] == '':
                    newLines.pop(i)
                    success = True
                    break

        while len(newLines) > self.numberOfLines:
            self.notify.warning('----------------------------------------------------------------------------')
            self.notify.warning('displayCommonText: Number of lines to displayed greater then lines available')
            print newLines
            self.notify.warning('----------------------------------------------------------------------------')
            newLines.pop()

        if len(newLines) == 2:
            for i in range(2):
                self.lines[i].setZ(self.twoLinesZValues[i])

        for i in range(3):
            self.lines[i].setZ(self.threeLinesZValues[i])

        if len(newLines) == 1:
            newLines.insert(0, '')
        for lineIndex in range(len(newLines)):
            self.lines[lineIndex]['text'] = newLines[lineIndex]

        if Localizer.myLanguage == 'japanese':
            maxHeight = self.setSmallestScale(self.lines)
            new0Z = self.lines[0].getZ() - self.statusLineZIncrement * (1 - maxHeight / 0.08)
            self.lines[0].setZ(new0Z)
            new1Z = self.lines[2].getZ() + self.statusLineZIncrement * (1 - maxHeight / 0.08)
            self.lines[2].setZ(new1Z)

    def getCurrentScreenWidth(self, dLabel):
        if dLabel.hascomponent('text0'):
            return dLabel.component('text0').textNode.getWidth() * dLabel.component('text0')['scale'][0]
        else:
            return 0

    def setBallNumber(self, num):
        if num > self.extraBallLimit:
            return False
        self.numBallsLeft = num
        if self.hudState == 0 or self.hudState == 2:
            return False
        self.hudElements['ballHolder'].reparentTo(aspect2d, 50)
        for i in range(len(self.ballIcons)):
            if num > i:
                self.ballIcons[i].reparentTo(aspect2d, 60)
            else:
                self.ballIcons[i].reparentTo(hidden)

        if self.world.gameOver:
            self.show(Localizer.pDisplayStartMessage)
        else:
            self.show('%d %s' % (num, Localizer.pBallsLeft))
        return True

    def idle(self, taskInstance):
        if not self.shouldIdle:
            self.shouldIdle = True
            taskMgr.doMethodLater(6, self.idle, 'idletimer')
            return
        if self.world.gameOver and self.idleState < 3:
            self.idleState = 3
        if self.idleState == 0:
            self.show(self.idleMessages[self.idleState])
            self.idleState = 1
        elif self.idleState == 1:
            self.show(self.idleMessages[self.idleState])
            self.idleState = 2
        elif self.idleState == 2:
            self.show(self.idleMessages[self.idleState])
            self.idleState = 0
        elif self.idleState >= 3:
            self.show(self.attractMessages[(self.idleState - 3)])
            self.idleState = self.idleState + 1
            if self.idleState - 3 == len(self.attractMessages):
                self.idleState = 3
        taskMgr.doMethodLater(4, self.idle, 'idletimer')

    def pause(self):
        if self.world.fromPalace:
            self.playTimer.stop()
        if self.grayScreen and not base.direct:
            self.grayScreen.reparentTo(aspect2d, 90)
        self.show(Localizer.pDisplayPauseMessage)
        self.hudElements['leftInstructions1']['text'] = Localizer.pDisplayResumeInstructions
        if self.controlLabels != None:
            if len(self.controlLabels) == 2:
                self.controlLabels[0].reparentTo(aspect2d, 100)
            else:
                for i in range(len(self.controlLabels) - 3):
                    self.controlLabels[i].reparentTo(aspect2d, 90)

        if self.controlsOver:
            self.exitButton.reparentTo(aspect2d, 100)
            self.resumeButton.reparentTo(aspect2d, 100)
        return

    def unPause(self):
        if self.world.fromPalace:
            self.playTimer.playing()
        if self.controlsOver:
            if self.grayScreen:
                self.grayScreen.reparentTo(hidden)
            if self.controlLabels != None:
                for cl in self.controlLabels:
                    cl.reparentTo(hidden)

        self.hudElements['leftInstructions1']['text'] = Localizer.pDisplayExitInstructions
        self.exitButton.reparentTo(hidden)
        self.resumeButton.reparentTo(hidden)
        return

    def showContinue(self, showIt):
        if showIt:
            self.tutorialElements['continueOn'].reparentTo(aspect2d, 50)
        else:
            self.tutorialElements['continueOn'].reparentTo(hidden)

    def unlockDisplay(self):
        self.displayLocked = False

    def show(self, text, alert=False, priority=False):
        if self.hudState == 0 or self.hudState == 2:
            return
        if self.displayLocked:
            return
        if priority:
            self.displayLocked = True
        if isinstance(text, list):
            text = text[0]
        if not isinstance(text, str):
            text = str(text)
        if Localizer.myLanguage != 'japanese':
            text = self.myUpper(text)
        if self.alertMode and alert:
            if Localizer.myLanguage == 'japanese':
                self.alertMessageLabel['text'] = text.replace(Localizer.japanSep, '')
            else:
                self.alertMessageLabel['text'] = self.myUpper(text).replace('| ', '')
            if self.alertMessageSequence is not None:
                self.alertMessageSequence.finish()
            self.alertMessageLabel.reparentTo(aspect2d)
            self.alertMessageLabel.setColorScale(1, 1, 1, 1)
            self.alertMessageSequence = Sequence(name='alertMessageSequence')
            self.alertMessageSequence.append(LerpColorScaleInterval(self.alertMessageLabel, 5, Vec4(1, 1, 1, 0), blendType='easeOut'))
            self.alertMessageSequence.append(Func(self.alertMessageLabel.reparentTo, hidden))
            self.alertMessageSequence.start()
        self.displayCommonText(text)
        self.shouldIdle = False
        return

    def showInstructions(self, text, time=0, hudState=1):
        if isinstance(text, list):
            text = join(text)
        if not isinstance(text, str):
            text = str(text)
        text = self.myUpper(text)
        oldHudState = hudState
        self.setHudState(2)
        self.instructions['text'] = text
        if time > 0:
            self.world.pbTaskMgr.doMethodLater(time, self.setHudState, 'hideinstructions', [oldHudState])

    def setHudState(self, newState):
        self.hudState = newState
        if self.world.fromPalace:
            if newState == 1:
                self.playTimer.playing()
            else:
                self.playTimer.stop()
        if newState == 3:
            self.show(Localizer.pDisplayStartMessage)
        if newState == 2:
            for i in self.tutorialElements.values():
                i.reparentTo(aspect2d, 50)

            self.tutorialElements['tutorialLabel'].reparentTo(aspect2d, 60)
            self.tutorialElements['continueOn'].reparentTo(aspect2d, 60)
            self.tutorialElements['skipIt'].reparentTo(aspect2d, 60)
        if newState == 1 or newState == 0 or newState == 3:
            for i in self.tutorialElements.values():
                i.reparentTo(hidden)
                self.instructions['text'] = ''

        if newState == 2 or newState == 0:
            self.scoreLine['text'] = ''
            self.scoreLineLabel['text'] = ''
            for i in range(3):
                self.lines[i]['text'] = ''

            for he in self.hudElements.values():
                he.reparentTo(hidden)

            for bi in self.ballIcons:
                bi.reparentTo(hidden)

        if newState == 1 or newState == 3:
            for he in self.hudElements.values():
                he.reparentTo(aspect2d, 50)

            self.updateScore(self.myScore)
            self.scoreLineLabel['text'] = Localizer.pScore
        if newState == 1:
            self.setBallNumber(self.numBallsLeft)

    def updateScore(self, score):
        while True:
            breakNow = True
            if score > self.extraBallScoreBase * pow(self.extraBallMultiplier, self.extraBallsReleased) and not self.world.gameOver:
                self.extraBallsReleased += 1
                if self.world.BOARDNAME == 'Mermaid':
                    self.world.ballMgr.addReserveBall()
                    self.setBallNumber(self.world.ballMgr.getNumReserveBalls())
                else:
                    self.world.ballReserve += 1
                    self.setBallNumber(self.world.ballReserve)
                self.extraBallSound.play()
                self.show(Localizer.pExtraBall)
                breakNow = False
            if breakNow:
                break

        if self.hudState == 1:
            self.shouldIdle = False
            self.myScore = int(score)
            self.scoreLine['text'] = self.addCommas(str(self.myScore))

    def gameOver(self):
        pass

    def myUpper(self, newstring):
        if Localizer.myLanguage == 'english':
            return newstring.upper()
        newstring = unicode(newstring, 'utf8')
        upperNewString = newstring.upper()
        return upperNewString.encode('utf8')

    def addCommas(self, amount):
        orig = amount
        if Localizer.myLanguage != 'brazilian':
            new = re.sub('^(-?\\d+)(\\d{3})', '\\g<1>,\\g<2>', amount)
        else:
            new = re.sub('^(-?\\d+)(\\d{3})', '\\g<1>.\\g<2>', amount)
        if orig == new:
            return new
        else:
            return self.addCommas(new)