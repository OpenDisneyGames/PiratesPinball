from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.gui.OnscreenText import OnscreenText
import random

class HighScore(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('HighScore')
    fromDomestic = False

    def __init__(self, gameWrapper, nameList, scoreList, scoreEntry, default):
        self.gameWrapper = gameWrapper
        self.scoreEntry = scoreEntry
        self.defaultInitials = default
        self.gui = loader.loadModelCopy('dgd%sArt/models/highScoreMenu' % self.gameWrapper.boardName)
        self.guiScale = 0.198
        self.gameWrapper.ignore('escape')
        self.gameWrapper.ignore('p')
        self.guiIntervals = {}
        DirectFrame.__init__(self, relief=None, geom_scale=self.guiScale, state='normal', frameSize=(-1,
                                                                                                     1,
                                                                                                     -1,
                                                                                                     1), suppressMouse=0)
        self.initialiseoptions(HighScore)
        self.reparentTo(aspect2d, 100)
        self.guiElements = {}
        self.guiElements['backgroundImage'] = DirectLabel(guiId='HighScoreBackgroundImage', parent=self, relief=None, image=self.gui.find('**/backgroundImage'), scale=self.guiScale, sortOrder=0)
        self.guiElements['logo'] = DirectLabel(guiId='HighScoreLogo', parent=self, relief=None, image=self.gui.find('**/logo'), scale=self.guiScale, sortOrder=0)
        if self.fromDomestic:
            self.guiElements['uploadScore'] = DirectButton(guiId='HighScoreuploadScore', parent=self, relief=None, image=[self.gui.find('**/uploadScore_up'), self.gui.find('**/uploadScore_down'), self.gui.find('**/uploadScore_roll'), self.gui.find('**/uploadScore_up')], scale=self.guiScale, pressEffect=True, command=self.uploadScore)
        if scoreEntry < 10:
            self.guiElements['back'] = DirectButton(guiId='HighScoreback', parent=self, relief=None, image=[self.gui.find('**/back_up'), self.gui.find('**/back_down'), self.gui.find('**/back_roll'), self.gui.find('**/back_up')], scale=self.guiScale, pressEffect=True, command=self.processClick)
        else:
            self.guiElements['back'] = DirectButton(guiId='HighScoreback', parent=self, relief=None, image=[self.gui.find('**/back_up'), self.gui.find('**/back_down'), self.gui.find('**/back_roll'), self.gui.find('**/back_up')], scale=self.guiScale, pressEffect=True, command=self.gameWrapper.exitHighScore)
        self.guiElements['sure'] = DirectDialog(guiId='HighScoresure', parent=hidden, image='dgd%sArt/textures/upload_bg.png' % self.gameWrapper.boardName, relief=None, scale=(self.guiScale * 0.6, 1, self.guiScale * 1.2), pos=(0,
                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                   0.3), fadeScreen=None, button_relief=None, buttonImageList=[['dgd%sArt/textures/yes_up.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/yes_roll.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/yes_roll.png' % self.gameWrapper.boardName], ['dgd%sArt/textures/no_up.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/no_roll.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/no_roll.png' % self.gameWrapper.boardName]], command=self.processSureDialog)
        for i in range(self.guiElements['sure'].numButtons):
            self.guiElements['sure'].buttonList[i]['image_scale'] = Vec3(1.5, 1, 0.5)
            self.guiElements['sure'].buttonList[i]['image_pos'] = Vec3(0, 0, -0.25)

        self.guiElements['sure'].setTransparency(1)
        for i in range(10):
            if i == scoreEntry:
                name = self.gui.find('**/name%d' % i)
                self.guiElements['name%d' % i] = DirectEntry(parent=self, guiId='HighScorename%d' % i, scale=self.guiScale, numLines=1, focus=1, cursorKeys=1, text_scale=(1,
                                                                                                                                                                           0.52), text_fg=(1.0,
                                                                                                                                                                                           0.9,
                                                                                                                                                                                           0.05,
                                                                                                                                                                                           1), text_shadow=(0,
                                                                                                                                                                                                            0,
                                                                                                                                                                                                            0,
                                                                                                                                                                                                            1), text_shadowOffset=(0.02,
                                                                                                                                                                                                                                   0.02), pos=(-0.64, 0, 0.363 - i * 0.129), command=self.dirtyWordFilter, sortOrder=1)
                self.guiElements[('name%d' % i)].setup()
                self.guiElements[('name%d' % i)].set(self.defaultInitials)
                self.guiElements[('name%d' % i)].guiItem.setMaxChars(3)
                self.guiElements[('name%d' % i)]['relief'] = None
                cursor = self.guiElements[('name%d' % i)].guiItem.getCursorDef().setScale(1, 1, 0.4)
            else:
                name = self.gui.find('**/name%d' % i)
                self.guiElements['name%d' % i] = DirectLabel(parent=self, guiId='HighScorename%d' % i, relief=None, scale=self.guiScale, text='%s' % nameList[i], text_scale=(1,
                                                                                                                                                                              0.52), text_fg=(1,
                                                                                                                                                                                              1,
                                                                                                                                                                                              1,
                                                                                                                                                                                              1), text_shadow=(0,
                                                                                                                                                                                                               0,
                                                                                                                                                                                                               0,
                                                                                                                                                                                                               1), text_shadowOffset=(0.02,
                                                                                                                                                                                                                                      0.02), text_align=TextNode.ALeft, textMayChange=1, text_pos=(name.getX() - 0.8, name.getZ() - 0.13))
            score = self.gui.find('**/score%d' % i)
            self.guiElements['score%d' % i] = DirectLabel(parent=self, guiId='HighScorescore%d' % i, relief=None, scale=self.guiScale, text=self.gameWrapper.addCommas(str(scoreList[i])), text_scale=(1,
                                                                                                                                                                                                       0.6), text_fg=(1,
                                                                                                                                                                                                                      1,
                                                                                                                                                                                                                      1,
                                                                                                                                                                                                                      1), text_shadow=(0,
                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                       1), text_shadowOffset=(0.02,
                                                                                                                                                                                                                                                              0.02), text_align=TextNode.ACenter, textMayChange=1, text_pos=(score.getX() - 0.05, score.getZ() - 0.12))
            self.guiElements['error'] = DirectLabel(parent=hidden, text='Sorry, try another name.', frameColor=(0,
                                                                                                                0,
                                                                                                                0,
                                                                                                                0), text_pos=(0,
                                                                                                                              -1.1), scale=self.guiScale, text_fg=(1,
                                                                                                                                                                   0,
                                                                                                                                                                   0,
                                                                                                                                                                   1), relief=None, text_shadow=(0,
                                                                                                                                                                                                 0,
                                                                                                                                                                                                 0,
                                                                                                                                                                                                 1), text_shadowOffset=(0.02,
                                                                                                                                                                                                                        0.02), sortOrder=5)
            self.errorSound = base.loadSfx('pinballbase/error')

        return

    def dirtyWordFilter(self, initials):
        print('filter')
        badWords = [
         'ASS', 'FCK', 'DIK', 'DIC', 'TIT', 'CUM', 'FAG', 'SEX', 'GAY', 'FUK', 'VAG', 'PEE', 'HO', 'FU', 'FUC', 'KKK']
        self.flag = False
        if initials.upper() in badWords or not initials.isalpha():
            self.guiElements[('name%d' % self.scoreEntry)].setFocus()
            seq = Sequence(Func(self.guiElements['error'].reparentTo, self), Func(self.guiElements[('name%d' % self.scoreEntry)].reparentTo, hidden), Func(self.errorSound.play), Wait(1), Func(self.guiElements[('name%d' % self.scoreEntry)].reparentTo, self), Func(self.guiElements['error'].reparentTo, hidden))
            seq.start()
            self.flag = True
            return False
        else:
            self.guiElements['error'].reparentTo(hidden)
            if self.flag:
                textObject.destroy()
            self.gameWrapper.nameList[self.scoreEntry] = initials.upper()
            self.gameWrapper.defaultInitials = initials.upper()
            self.guiElements[('name%d' % self.scoreEntry)].set(initials.upper())
            self.guiElements[('name%d' % self.scoreEntry)]['state'] = DISABLED
            return True

    def processClick(self):
        if self.dirtyWordFilter(self.guiElements[('name%d' % self.scoreEntry)].get()):
            self.gameWrapper.exitHighScoreGame()

    def processSureDialog(self, button):
        if button == 0:
            self.gameWrapper.uploadScore()
        self.guiElements['sure'].reparentTo(hidden)

    def uploadScore(self):
        self.guiElements['sure'].reparentTo(self)

    def hide(self, time=0):
        self.reparentTo(hidden)

    def show(self, time=0):
        self.reparentTo(aspect2d)

    def destroy(self):
        while self.guiElements != {}:
            ge = self.guiElements.popitem()
            ge[1].destroy()

        for i in list(self.guiIntervals.values()):
            i.finish()

        self.gui.removeNode()
        DirectFrame.destroy(self)