# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: PauseMenu.py
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task.TaskManagerGlobal import *
import random

class PauseMenu(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PauseMenu')

    def __init__(self, gameWrapper):
        self.gameWrapper = gameWrapper
        self.gui = loader.loadModelCopy('dgd%sArt/models/pauseMenu' % self.gameWrapper.boardName)
        self.guiScale = 0.198
        self.guiIntervals = {}
        DirectFrame.__init__(self, relief=None, geom=self.gui, geom_scale=self.guiScale, state='normal', frameSize=(-1,
                                                                                                                    1,
                                                                                                                    -1,
                                                                                                                    1), suppressMouse=0)
        self.initialiseoptions(PauseMenu)
        self.reparentTo(aspect2d, 100)
        self.guiElements = {}
        self.guiElements['pause_bg'] = DirectLabel(guiId='PauseMenupause_bg', parent=self, relief=None, image=self.gui.find('**/pause_bg'), scale=self.guiScale, sortOrder=0)
        self.guiElements['resume'] = DirectButton(guiId='PauseMenuresume', parent=self, relief=None, image=[self.gui.find('**/resume_up'), self.gui.find('**/resume_down'), self.gui.find('**/resume_roll'), self.gui.find('**/resume_up')], scale=self.guiScale, pressEffect=True, command=self.gameWrapper.pauseGame)
        self.guiElements['sure'] = DirectDialog(guiId='PauseMenusure', parent=hidden, image='dgd%sArt/textures/quit_bg.png' % self.gameWrapper.boardName, relief=None, scale=(self.guiScale * 0.6, 1, self.guiScale * 1.2), pos=(0,
                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                 0.3), fadeScreen=None, button_relief=None, buttonImageList=[['dgd%sArt/textures/yes_up.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/yes_roll.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/yes_roll.png' % self.gameWrapper.boardName], ['dgd%sArt/textures/no_up.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/no_roll.png' % self.gameWrapper.boardName, 'dgd%sArt/textures/no_roll.png' % self.gameWrapper.boardName]], command=self.processSureDialog, sortOrder=10)
        for i in range(self.guiElements['sure'].numButtons):
            self.guiElements['sure'].buttonList[i]['image_scale'] = Vec3(1.5, 1, 0.5)
            self.guiElements['sure'].buttonList[i]['image_pos'] = Vec3(0, 0, -0.25)

        self.guiElements['sure'].setTransparency(1)
        self.guiElements['quit'] = DirectButton(guiId='PauseMenuquit', parent=self, relief=None, image=[self.gui.find('**/quit_up'), self.gui.find('**/quit_down'), self.gui.find('**/quit_roll'), self.gui.find('**/quit_up')], scale=self.guiScale, pressEffect=True, command=self.guiElements['sure'].reparentTo, extraArgs=[self])
        self.guiElements['highScore'] = DirectButton(guiId='PauseMenuhighScore', parent=self, relief=None, image=[self.gui.find('**/highScore_up'), self.gui.find('**/highScore_down'), self.gui.find('**/highScore_roll'), self.gui.find('**/highScore_up')], scale=self.guiScale, pressEffect=True, command=self.gameWrapper.createHighScore, extraArgs=[True])
        self.guiElements['help'] = DirectButton(guiId='PauseMenuhelp', parent=self, relief=None, image=[self.gui.find('**/help_up'), self.gui.find('**/help_down'), self.gui.find('**/help_roll'), self.gui.find('**/help_up')], scale=self.guiScale, pressEffect=True, command=self.gameWrapper.createHelpMenu, extraArgs=[True])
        return

    def processSureDialog(self, button):
        self.guiElements['sure'].reparentTo(hidden)
        if button == 0:
            self.gameWrapper.quitGame()

    def hide(self, time=0):
        self.reparentTo(hidden)

    def show(self, time=0):
        self.reparentTo(aspect2d)

    def destroy(self):
        while self.guiElements != {}:
            ge = self.guiElements.popitem()
            ge[1].destroy()

        for i in self.guiIntervals.values():
            i.finish()

        self.gui.removeNode()
        DirectFrame.destroy(self)