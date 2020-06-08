from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task.TaskManagerGlobal import *
import random, Localizer

class MainMenu(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('MainMenu')

    def __init__(self, gameWrapper):
        self.gameWrapper = gameWrapper
        self.gui = loader.loadModelCopy('dgd%sArt/models/mainMenu' % self.gameWrapper.boardName)
        self.guiScale = 0.198
        self.guiIntervals = {}
        DirectFrame.__init__(self, relief=None, state='normal', frameSize=(-1, 1, -1,
                                                                           1), suppressMouse=0)
        self.initialiseoptions(MainMenu)
        self.reparentTo(aspect2d)
        self.guiElements = {}
        self.menuSounds = {}
        self.guiElements['background_front'] = DirectLabel(guiId='MainMenubackground_front', parent=self, relief=None, image=self.gui.find('**/background_front'), scale=self.guiScale, sortOrder=2)
        self.guiElements['sure'] = DirectDialog(guiId='MainMenusure', parent=hidden, image='dgd%sArt/textures/quit_bg.png' % self.gameWrapper.boardName, relief=None, scale=(self.guiScale * 0.6, 1, self.guiScale * 1.2), pos=(0,
                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                0.3), fadeScreen=None, button_relief=None, buttonImageList=[['dgd%sArt/textures/yes_up.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/yes_roll.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/yes_roll.png' % self.gameWrapper.boardName], ['dgd%sArt/textures/no_up.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/no_roll.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/no_roll.png' % self.gameWrapper.boardName]], command=self.processSureDialog, sortOrder=10)
        for i in range(self.guiElements['sure'].numButtons):
            self.guiElements['sure'].buttonList[i]['image_scale'] = Vec3(1.5, 1, 0.5)
            self.guiElements['sure'].buttonList[i]['image_pos'] = Vec3(0, 0, -0.25)

        self.guiElements['sure'].setTransparency(1)
        self.guiElements['startGame'] = DirectButton(guiId='MainMenustartGame', parent=self, relief=None, image=[self.gui.find('**/startGame_up'), self.gui.find('**/startGame_down'), self.gui.find('**/startGame_roll'), self.gui.find('**/startGame_up')], scale=self.guiScale, sortOrder=3, pressEffect=True, command=self.runBoard)
        self.guiElements['quitGame'] = DirectButton(guiId='MainMenuquitGame', parent=self, relief=None, image=[self.gui.find('**/quitGame_up'), self.gui.find('**/quitGame_down'), self.gui.find('**/quitGame_roll'), self.gui.find('**/quitGame_up')], scale=self.guiScale, sortOrder=3, pressEffect=True, command=self.guiElements['sure'].reparentTo, extraArgs=[aspect2d, 100])
        self.guiElements['highScore'] = DirectButton(guiId='MainMenuhighScore', parent=self, relief=None, image=[self.gui.find('**/highScore_up'), self.gui.find('**/highScore_down'), self.gui.find('**/highScore_roll'), self.gui.find('**/highScore_up')], scale=self.guiScale, sortOrder=3, pressEffect=True, command=self.gameWrapper.createHighScore)
        self.guiElements['helpMenu'] = DirectButton(guiId='MainMenuhelpMenu', parent=self, relief=None, image=[self.gui.find('**/helpMenu_up'), self.gui.find('**/helpMenu_down'), self.gui.find('**/helpMenu_roll'), self.gui.find('**/helpMenu_up')], scale=self.guiScale, sortOrder=3, pressEffect=True, command=self.gameWrapper.createHelpMenu)
        if self.gameWrapper.boardName == 'Aladdin':
            self.menuSounds['music'] = base.loadSfx(Localizer.apCaveMusic)
            self.randomWaitRange = (1, 1)
            self.last = 11
            for i in range(10):
                self.guiElements['star%d' % i] = DirectLabel(guiId='MainMenustar%d' % i, parent=self, relief=None, geom=self.gui.find('**/star%d' % i), geom_pos=(0,
                                                                                                                                                                  0,
                                                                                                                                                                  0), pos=self.gui.find('**/star%d' % i).getPos() * self.guiScale, scale=0.05, sortOrder=4)

        else:
            if self.gameWrapper.boardName == 'Mermaid':
                self.menuSounds['bubbles'] = base.loadSfx(Localizer.mpBubbles)
                self.menuSounds['music'] = base.loadSfx(Localizer.mpTritonPalace)
                self.randomWaitRange = (3, 7)
                self.guiElements['arialBlink'] = DirectLabel(guiId='MainMenuarialBlink', parent=hidden, relief=None, image=self.gui.find('**/arialBlink'), scale=self.guiScale, sortOrder=3)
                self.guiElements['background_back'] = DirectLabel(guiId='MainMenubackground_back', parent=self, relief=None, image=self.gui.find('**/background_back'), scale=self.guiScale, sortOrder=0)
                self.blinkSequence = Sequence(Func(self.guiElements['arialBlink'].reparentTo, self), Wait(0.3), Func(self.guiElements['arialBlink'].reparentTo, hidden), Wait(0.2), Func(self.guiElements['arialBlink'].reparentTo, self), Wait(0.1), Func(self.guiElements['arialBlink'].reparentTo, hidden))
                self.guiElements['bubbles_0'] = DirectLabel(guiId='MainMenububbles_0', parent=hidden, relief=None, image=self.gui.find('**/bubbles_0'), scale=self.guiScale, sortOrder=3)
                self.guiElements['bubbles_1'] = DirectLabel(guiId='MainMenububbles_1', parent=hidden, relief=None, image=self.gui.find('**/bubbles_1'), scale=self.guiScale, sortOrder=3)
                self.guiElements['bubbles_2'] = DirectLabel(guiId='MainMenububbles_2', parent=hidden, relief=None, image=self.gui.find('**/bubbles_2'), scale=self.guiScale, sortOrder=3)
                self.bubble = 0
                self.bubbleTex0 = loader.loadTexture('dgdMermaidArt/textures/bubbles_0.png')
                self.bubbleTex1 = loader.loadTexture('dgdMermaidArt/textures/bubbles_1.png')
                self.bubbleTex2 = loader.loadTexture('dgdMermaidArt/textures/bubbles_2.png')
                pos = self.guiElements['bubbles_0'].getPos()
                self.bubbleSequence0 = Parallel(LerpPosInterval(self.guiElements['bubbles_0'], 2.5, Vec3(pos[0], pos[1], pos[2] + 1.5)), Sequence(Func(self.menuSounds['bubbles'].play), Func(self.guiElements['bubbles_0'].reparentTo, self), LerpHprInterval(self.guiElements['bubbles_0'], 0.6, Vec3(0, 0, 25)), LerpHprInterval(self.guiElements['bubbles_0'], 1.9, Vec3(0, 0, -40)), Func(self.guiElements['bubbles_0'].reparentTo, hidden), Func(self.guiElements['bubbles_0'].setPos, pos)))
                pos = self.guiElements['bubbles_1'].getPos()
                self.bubbleSequence1 = Parallel(LerpPosInterval(self.guiElements['bubbles_1'], 2.5, Vec3(pos[0], pos[1], pos[2] + 1.5)), Sequence(Func(self.menuSounds['bubbles'].play), Func(self.guiElements['bubbles_1'].reparentTo, self), LerpHprInterval(self.guiElements['bubbles_1'], 0.6, Vec3(0, 0, 25)), LerpHprInterval(self.guiElements['bubbles_1'], 1.9, Vec3(0, 0, -40)), Func(self.guiElements['bubbles_1'].reparentTo, hidden), Func(self.guiElements['bubbles_1'].setPos, pos)))
                pos = self.guiElements['bubbles_2'].getPos()
                self.bubbleSequence2 = Parallel(LerpPosInterval(self.guiElements['bubbles_2'], 2.5, Vec3(pos[0], pos[1], pos[2] + 1.5)), Sequence(Func(self.menuSounds['bubbles'].play), Func(self.guiElements['bubbles_2'].reparentTo, self), LerpHprInterval(self.guiElements['bubbles_2'], 0.6, Vec3(0, 0, 25)), LerpHprInterval(self.guiElements['bubbles_2'], 1.9, Vec3(0, 0, -40)), Func(self.guiElements['bubbles_2'].reparentTo, hidden), Func(self.guiElements['bubbles_2'].setPos, pos)))
            if self.gameWrapper.boardName == 'Pirate':
                self.randomWaitRange = (0, 0)
                self.menuSounds['music'] = base.loadSfx(Localizer.ppMusic_BoneBrig)
                self.menuSounds['creak'] = base.loadSfx(Localizer.BoatCreak)
                self.guiElements['shipFlat'] = DirectLabel(guiId='MainMenushipFlat', parent=self, relief=None, geom=self.gui.find('**/shipFlat'), geom_pos=(0,
                                                                                                                                                            0,
                                                                                                                                                            0), pos=self.gui.find('**/shipFlat').getPos() * self.guiScale, scale=self.guiScale, sortOrder=4)
                self.menuSounds['creak'].setLoop(1)
                self.shipSequence = Parallel(Func(self.menuSounds['creak'].play), Sequence(LerpHprInterval(self.guiElements['shipFlat'], 4, Vec3(0, 2.5, -2.5), blendType='easeOut'), LerpHprInterval(self.guiElements['shipFlat'], 6, Vec3(0, -1.25, 1.25), blendType='easeInOut'), LerpHprInterval(self.guiElements['shipFlat'], 2, Vec3(0, 0, 0))))
        taskMgr.doMethodLater(random.randint(self.randomWaitRange[0], self.randomWaitRange[1]), getattr(self, 'setup%s' % self.gameWrapper.boardName), '%sAnimation' % self.gameWrapper.boardName)
        self.menuSounds['music'].setVolume(0.5)
        self.menuSounds['music'].setLoop()
        self.menuSounds['music'].play()
        return

    def processSureDialog(self, button):
        if button == 0:
            self.gameWrapper.exit()
        self.guiElements['sure'].reparentTo(hidden)

    def runBoard(self):
        for sound in list(self.menuSounds.values()):
            sound.stop()

        self.gameWrapper.runBoard()

    def setupAladdin(self, task=None):
        self.randomSpecialWaitRange = (4, 25)
        i = random.randint(0, 9)
        while i == self.last:
            i = random.randint(0, 9)

        self.last = i
        self.flashSequence = Sequence(Parallel(LerpScaleInterval(self.guiElements[('star%d' % i)], 0.4, 0.25), Sequence(LerpHprInterval(self.guiElements[('star%d' % i)], 0.2, Vec3(0, 0, 10)), LerpHprInterval(self.guiElements[('star%d' % i)], 0.2, Vec3(0, 0, 0)))), Parallel(LerpScaleInterval(self.guiElements[('star%d' % i)], 0.4, 0.05), Sequence(LerpHprInterval(self.guiElements[('star%d' % i)], 0.2, Vec3(0, 0, -10)), LerpHprInterval(self.guiElements[('star%d' % i)], 0.2, Vec3(0, 0, 0)))))
        self.flashSequence.start()
        taskMgr.doMethodLater(random.randint(self.randomSpecialWaitRange[0], self.randomSpecialWaitRange[1]) * 0.1, getattr(self, 'setup%s' % self.gameWrapper.boardName), '%sAnimation' % self.gameWrapper.boardName)

    def setupMermaid(self, task=None):
        ran = random.randint(0, 2)
        self.guiElements[('bubbles_%d' % ran)].setTexture(getattr(self, 'bubbleTex%d' % (int(task.time) % 3)))
        getattr(self, 'bubbleSequence%d' % ran).start()
        self.blinkSequence.start()
        taskMgr.doMethodLater(random.randint(self.randomWaitRange[0], self.randomWaitRange[1]), getattr(self, 'setup%s' % self.gameWrapper.boardName), '%sAnimation' % self.gameWrapper.boardName)

    def setupPirate(self, task=None):
        self.shipSequence.loop()

    def hide(self):
        if self.gameWrapper.boardName == 'Aladdin':
            self.flashSequence.finish()
        elif self.gameWrapper.boardName == 'Mermaid':
            self.blinkSequence.finish()
            self.bubbleSequence0.finish()
            self.bubbleSequence1.finish()
            self.bubbleSequence2.finish()
        else:
            self.shipSequence.finish()
            self.menuSounds['creak'].stop()
        taskMgr.remove('%sAnimation' % self.gameWrapper.boardName)
        self.reparentTo(hidden)

    def show(self, fromGameWrapper=False):
        if fromGameWrapper:
            self.menuSounds['music'].play()
        self.flag = 0
        self.bubble = 0
        taskMgr.doMethodLater(random.randint(self.randomWaitRange[0], self.randomWaitRange[1]), getattr(self, 'setup%s' % self.gameWrapper.boardName), '%sAnimation' % self.gameWrapper.boardName)
        self.reparentTo(aspect2d)

    def destroy(self):
        for (key, p) in list(self.menuSounds.items()):
            del p
            del self.menuSounds[key]

        if self.gameWrapper.boardName == 'Aladdin':
            self.flashSequence.finish()
        elif self.gameWrapper.boardName == 'Mermaid':
            self.blinkSequence.finish()
            self.bubbleSequence0.finish()
            self.bubbleSequence1.finish()
            self.bubbleSequence2.finish()
        else:
            self.shipSequence.finish()
        taskMgr.remove('%sAnimation' % self.gameWrapper.boardName)
        while self.guiElements != {}:
            ge = self.guiElements.popitem()
            ge[1].destroy()

        for i in list(self.guiIntervals.values()):
            i.finish()

        self.gui.removeNode()
        DirectFrame.destroy(self)