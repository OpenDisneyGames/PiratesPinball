from pinballbase.PinballDisplay import PinballDisplay
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectCheckButton
import random, string
from direct.gui import DirectGuiGlobals
import Localizer, re
from pinballbase.DirectMaxWidthLabel import DirectMaxWidthLabel
from pinballbase.DirectMaxScaleLabel import DirectMaxScaleLabel

class PirateDisplay(PinballDisplay):
    __module__ = __name__

    def __init__(self, world):
        PinballDisplay.__init__(self, world, Localizer.pirateFont, Localizer.ppDisplayIdleMessages, Localizer.ppDisplayAttractPhrases)
        self.mapMovingSequence = None
        self.loadMapElements()
        self.showMapParallel = None
        self.scoreLineLabel = DirectMaxScaleLabel(relief=None, text=Localizer.pScore, pos=(1.0,
                                                                                           0.0,
                                                                                           0.86), text_scale=0.08, text_fg=(0.3,
                                                                                                                            0.1,
                                                                                                                            0.1,
                                                                                                                            1), text_shadow=(0,
                                                                                                                                             0,
                                                                                                                                             0,
                                                                                                                                             1), text_shadowOffset=(0.02,
                                                                                                                                                                    0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=0.25, maxHeight=0.13)
        self.scoreLine = DirectMaxWidthLabel(relief=None, text='0', text_font=self.numberFont, pos=(1.0,
                                                                                                    0.0,
                                                                                                    0.76), text_scale=0.13, text_fg=(0.3,
                                                                                                                                     0.1,
                                                                                                                                     0.1,
                                                                                                                                     1), text_shadow=(0,
                                                                                                                                                      0,
                                                                                                                                                      0,
                                                                                                                                                      1), text_shadowOffset=(0.02,
                                                                                                                                                                             0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=0.4, maxXScale=0.13, maxYScale=0.12, squish=1)
        self.scoreLineLabel.reparentTo(aspect2d, 55)
        self.scoreLine.reparentTo(aspect2d, 55)
        self.lines = []
        for i in range(3):
            if Localizer.myLanguage != 'japanese':
                self.lines.append(DirectMaxWidthLabel(text='', pos=(1.0, 0.0, 0.645 - i * 0.115), text_scale=0.13, text_fg=(0.3,
                                                                                                                            0.1,
                                                                                                                            0.1,
                                                                                                                            1), text_shadow=(0,
                                                                                                                                             0,
                                                                                                                                             0,
                                                                                                                                             1), text_shadowOffset=(0.02,
                                                                                                                                                                    0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=0.416, maxXScale=0.13, maxYScale=0.13, squish=0))
            else:
                self.lines.append(DirectMaxScaleLabel(text='', pos=(1.013, 0.0, 0.655 - i * 0.1), text_scale=0.13, text_fg=(0.3,
                                                                                                                            0.1,
                                                                                                                            0.1,
                                                                                                                            1), text_shadow=(0,
                                                                                                                                             0,
                                                                                                                                             0,
                                                                                                                                             1), text_shadowOffset=(0.02,
                                                                                                                                                                    0.02), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=0.416, maxHeight=0.08))
            self.lines[i].reparentTo(aspect2d, 55)

        self.hudElements['mainBackground'] = DirectLabel(scale=(0.44756, 1.0, 0.44756), image='piratepinball/art/hud/mainDisplayBackground.png', relief=None)
        self.hudElements['mainBackground'].setTransparency(1)
        self.hudElements['mainBackground'].setPos(1.02, 0.0, 0.642)
        self.tutorialElements['instructionsBackground'] = DirectLabel(scale=(1.25,
                                                                             1.0,
                                                                             0.2), image='piratepinball/art/hud/longtutbg.png', relief=None)
        self.tutorialElements['instructionsBackground'].setTransparency(1)
        self.tutorialElements['instructionsBackground'].setPos(0, 0, -0.524)
        self.tutorialElements['instructionsBackground'].reparentTo(hidden)
        if Localizer.myLanguage != 'japanese':
            self.instructions = DirectMaxWidthLabel(relief=None, text='', pos=(0, 0.0, -0.58), text_scale=0.3, text_fg=(0,
                                                                                                                        0,
                                                                                                                        0,
                                                                                                                        1), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=2.2, maxXScale=0.25, maxYScale=0.25)
        else:
            self.instructions = DirectMaxScaleLabel(relief=None, text='', pos=(0, 0.0, -0.51), text_scale=0.3, text_fg=(0,
                                                                                                                        0,
                                                                                                                        0,
                                                                                                                        1), text_align=TextNode.ACenter, text_mayChange=1, maxWidth=2.2, maxHeight=0.11)
        self.instructions.reparentTo(aspect2d, 55)
        if Localizer.myLanguage != 'japanese':
            tutText = Localizer.pTutorialLabel
        else:
            tutText = ''
        self.tutorialElements['tutorialLabel'] = DirectLabel(relief=None, pos=(0.01, 0.0, -0.34), text=tutText, text_fg=(1,
                                                                                                                         1,
                                                                                                                         1,
                                                                                                                         1), text_scale=0.11)
        self.tutorialElements['tutorialLabel'].reparentTo(hidden)
        self.mouseGraphic = DirectLabel(scale=(0.7, 1.0, 0.7), image='piratepinball/art/hud/mouse2.png', relief=None)
        self.mouseGraphic.setTransparency(1)
        self.mouseGraphic.setPos(0.73, 0.0, 0.0)
        self.keyboardGraphic = DirectLabel(scale=(0.55, 1.0, 0.27), image='piratepinball/art/hud/keyboard.png', relief=None)
        self.keyboardGraphic.setTransparency(1)
        self.keyboardGraphic.setPos(0.0, 0.0, 0.0)
        self.mouseArrows = []
        for i in range(4):
            self.mouseArrows.append(DirectLabel(scale=(0.15, 1.0, 0.15), image='piratepinball/art/hud/arrow1.png', relief=None))
            self.mouseArrows[i].setTransparency(1)
            x = [0.73, 0.27, 0.73, 1.19]
            y = [0.65, 0, -0.65, 0]
            self.mouseArrows[i].setPos(x[i], 0.0, y[i])
            self.mouseArrows[i].setHpr(0, 0, -90 * i)
            self.mouseArrows[i].reparentTo(hidden)

        self.minigameInstructionBackground = DirectLabel(scale=(0.75, 1.0, 0.37), image='piratepinball/art/hud/popup.png', relief=None)
        self.minigameInstructionBackground.setTransparency(1)
        self.minigameInstructionBackground.setPos(-0.49, 0, 0.567)
        if Localizer.myLanguage != 'japanese':
            self.minigameInstruction1 = DirectMaxWidthLabel(relief=None, pos=(-0.5, 0.0, 0.6119), text=Localizer.ppDisplayMiniGameInstructions1, text_fg=(0,
                                                                                                                                                          0,
                                                                                                                                                          0,
                                                                                                                                                          1), text_scale=0.2, maxWidth=1.026667, maxXScale=0.2, maxYScale=0.2)
            self.minigameInstruction2 = DirectMaxWidthLabel(relief=None, pos=(-0.498, 0.0, 0.4336), text=Localizer.ppDisplayMiniGameInstructions2, text_fg=(0,
                                                                                                                                                            0,
                                                                                                                                                            0,
                                                                                                                                                            1), text_scale=0.2, maxWidth=1.026667, maxXScale=0.2, maxYScale=0.2)
        else:
            self.minigameInstruction1 = DirectMaxScaleLabel(relief=None, pos=(-0.5, 0.0, 0.6119), text=Localizer.ppDisplayMiniGameInstructions1, text_fg=(0,
                                                                                                                                                          0,
                                                                                                                                                          0,
                                                                                                                                                          1), text_scale=0.2, maxWidth=1.026667, maxHeight=0.1)
            self.minigameInstruction2 = DirectMaxScaleLabel(relief=None, pos=(-0.498, 0.0, 0.4336), text=Localizer.ppDisplayMiniGameInstructions2, text_fg=(0,
                                                                                                                                                            0,
                                                                                                                                                            0,
                                                                                                                                                            1), text_scale=0.2, maxWidth=1.026667, maxHeight=0.1)
        self.invertCheckButton = DirectLabel(scale=(0.05, 1.0, 0.05), text_scale=1.5, relief=None, text=Localizer.ppCannonAreaInvert[0])
        self.invertCheckButton.setTransparency(1)
        self.invertCheckButton.setPos(0.0, 0.0, 0.9)
        self.minigameInstructionBackground.reparentTo(hidden)
        self.minigameInstruction1.reparentTo(hidden)
        self.minigameInstruction2.reparentTo(hidden)
        self.invertCheckButton.reparentTo(hidden)
        self.mouseGraphic.reparentTo(hidden)
        self.keyboardGraphic.reparentTo(hidden)
        self.hudElements['ballHolder'] = DirectLabel(scale=(0.18, 1.0, 0.09), image='piratepinball/art/hud/ballHolder.png', relief=None)
        self.hudElements['ballHolder'].setTransparency(1)
        self.hudElements['ballHolder'].setPos(1.02, 0.0, 0.2)
        self.hudElements['ballHolder'].reparentTo(hidden)
        self.ballIcons = []
        for i in range(self.extraBallLimit):
            self.ballIcons.append(DirectLabel(scale=(0.09, 1.0, 0.09), image='piratepinball/art/hud/ball.png', relief=None))
            self.ballIcons[i].setPos(0.94 + i * 0.07, 0, 0.2)
            self.ballIcons[i].setTransparency(1)
            self.ballIcons[i].reparentTo(hidden)

        self.hudElements['leftInstructions1'] = DirectMaxScaleLabel(relief=None, pos=(-0.99, 0.0, -0.88), text=Localizer.pDisplayExitInstructions, text_fg=(0.7,
                                                                                                                                                            0.7,
                                                                                                                                                            1,
                                                                                                                                                            1), text_scale=0.07, maxWidth=0.53, maxHeight=0.07)
        self.hudElements['leftInstructions2'] = DirectMaxScaleLabel(relief=None, pos=(-0.97, 0.0, -0.963), text=Localizer.pDisplayLeftFlipper, text_fg=(0.7,
                                                                                                                                                        0.7,
                                                                                                                                                        1,
                                                                                                                                                        1), text_scale=0.09, maxWidth=0.625, maxHeight=0.07)
        self.hudElements['rightInstructions1'] = DirectMaxScaleLabel(relief=None, pos=(0.98, 0.0, -0.873), text=Localizer.pDisplayStartInstructions, text_fg=(0.7,
                                                                                                                                                              0.7,
                                                                                                                                                              1,
                                                                                                                                                              1), text_scale=0.07, maxWidth=0.55, maxHeight=0.07)
        self.hudElements['rightInstructions2'] = DirectMaxScaleLabel(relief=None, pos=(0.963, 0.0, -0.963), text=Localizer.pDisplayRightFlipper, text_fg=(0.7,
                                                                                                                                                          0.7,
                                                                                                                                                          1,
                                                                                                                                                          1), text_scale=0.09, maxWidth=0.63, maxHeight=0.07)
        if Localizer.myLanguage != 'japanese':
            self.tutorialElements['continueOn'] = DirectLabel(relief=None, pos=(0.0, 0.0, -0.76), text=Localizer.pDisplayContinue, text_fg=(1,
                                                                                                                                            1,
                                                                                                                                            1,
                                                                                                                                            1), text_scale=0.12)
            self.tutorialElements['continueOn'].reparentTo(hidden)
            self.tutorialElements['skipIt'] = DirectLabel(relief=None, pos=(0.0, 0.0, -0.835), text=Localizer.pDisplaySkipIt, text_fg=(1,
                                                                                                                                       1,
                                                                                                                                       1,
                                                                                                                                       1), text_scale=0.07)
            self.tutorialElements['skipIt'].reparentTo(hidden)
        else:
            self.tutorialElements['continueOn'] = DirectMaxScaleLabel(relief=None, pos=(-0.5, 0.0, -0.595), text=Localizer.pDisplayContinue, text_fg=(1,
                                                                                                                                                      1,
                                                                                                                                                      1,
                                                                                                                                                      1), maxWidth=1.0, maxHeight=0.075)
            self.tutorialElements['continueOn'].reparentTo(hidden)
            self.tutorialElements['skipIt'] = DirectMaxScaleLabel(relief=None, pos=(0.5, 0.0, -0.595), text=Localizer.pDisplaySkipIt, text_fg=(1,
                                                                                                                                               1,
                                                                                                                                               1,
                                                                                                                                               1), maxWidth=1.0, maxHeight=0.075)
            self.tutorialElements['skipIt'].reparentTo(hidden)
        PinballDisplay.finishInit(self)
        self.show(Localizer.pDisplayStartMessage)
        return

    def sleep(self):
        PinballDisplay.sleep(self)
        if self.mapMovingSequence != None and self.mapMovingSequence.isPlaying():
            self.mapMovingSequence.finish()
        if self.showMapParallel != None and self.showMapParallel.isPlaying():
            self.showMapParallel.finish()
        return

    def destroy(self):
        PinballDisplay.destroy(self)
        if self.mapMovingSequence != None and self.mapMovingSequence.isPlaying():
            self.mapMovingSequence.finish()
        if self.showMapParallel != None and self.showMapParallel.isPlaying():
            self.showMapParallel.finish()
        self.compass.removeNode()
        self.skullIsland.removeNode()
        for m in self.map:
            m.removeNode()

        self.minigameInstructionBackground.removeNode()
        self.minigameInstruction1.removeNode()
        self.minigameInstruction2.removeNode()
        self.invertCheckButton.removeNode()
        self.mouseGraphic.removeNode()
        for i in range(4):
            self.mouseArrows[i].removeNode()

        return

    def unPause(self):
        PinballDisplay.unPause(self)
        self.show(Localizer.ppDisplayGameName)

    def loadMapElements(self):
        self.compass = DirectLabel(scale=(0.08, 1.0, 0.08), image='piratepinball/art/hud/map/compass.png', relief=None)
        self.compass.setTransparency(1)
        self.compass.setPos(-0.783, 0, 0.626)
        self.compass.setHpr(0, 0, 45)
        self.compass.reparentTo(hidden)
        if Localizer.myLanguage == 'brazilian':
            self.skullIsland = DirectLabel(scale=(0.16, 1.0, 0.08), image='piratepinball/art/hud/map/skullIsland_brazilian.png', relief=None)
        else:
            self.skullIsland = DirectLabel(scale=(0.16, 1.0, 0.08), image='piratepinball/art/hud/map/skullIsland.png', relief=None)
        self.skullIsland.setTransparency(1)
        self.skullIsland.setPos(-0.833, 0, 0.78)
        self.skullIsland.reparentTo(hidden)
        self.skullIsland.setColor(1, 1, 1, 0)
        self.map = []
        for i in range(5):
            self.map.append(DirectLabel(scale=(0.45, 1.0, 0.45), image='piratepinball/art/hud/map/map%d.png' % i, relief=None))
            self.map[i].setTransparency(1)
            self.map[i].setPos(-0.96, 0, 0.68)
            self.map[i].reparentTo(hidden)

        return

    def startMapMoving(self, time=0):
        self.notify.debug('Start map moving')
        self.mapMovingSequence = Sequence(name='mapMovingSequence')
        for i in range(5):
            self.mapMovingSequence.append(Func(self.advanceMap, i))
            self.mapMovingSequence.append(Wait(0.5))

        self.showMap(time)

    def hideMap(self):
        for i in self.map:
            i.reparentTo(hidden)

        if self.mapMovingSequence != None:
            self.mapMovingSequence.finish()
        self.compass.reparentTo(hidden)
        self.skullIsland.reparentTo(hidden)
        return

    def showMap(self, time=0):
        if self.world.gameOver:
            return
        if self.mapMovingSequence != None:
            self.mapMovingSequence.loop()
        for i in self.map:
            i.reparentTo(aspect2d, 50)

        self.compass.reparentTo(aspect2d, 55)
        self.skullIsland.reparentTo(aspect2d, 55)
        if time != 0:
            self.compass.setColor(1, 1, 1, 0)
            self.showMapParallel = Parallel(name='showmapparallel')
            self.showMapParallel.append(LerpColorInterval(self.compass, time, Vec4(1, 1, 1, 1)))
            for i in self.map:
                i.setColor(1, 1, 1, 0)
                self.showMapParallel.append(LerpColorInterval(i, time, Vec4(1, 1, 1, 1)))

            self.showMapParallel.start()
        return

    def advanceMap(self, theone):
        for i in self.map:
            i.reparentTo(hidden)

        self.map[theone].reparentTo(aspect2d, 50)

    def setHudState(self, newState):
        self.notify.debug('PirateDisplay: setHudState: newState = %d ' % newState)
        PinballDisplay.setHudState(self, newState)
        if newState == 1:
            self.showMap()
        else:
            self.hideMap()