# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: HelpMenu.py
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task.TaskManagerGlobal import *
import random

class HelpMenu(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('HelpMenu')
    version = 'v3.0'

    def __init__(self, gameWrapper):
        self.gameWrapper = gameWrapper
        self.gui = loader.loadModelCopy('dgd%sArt/models/helpMenu' % self.gameWrapper.boardName)
        self.guiScale = 0.198
        self.gameWrapper.ignore('escape')
        self.gameWrapper.ignore('p')
        self.guiIntervals = {}
        DirectFrame.__init__(self, relief=None, geom=self.gui, geom_scale=self.guiScale, state='normal', frameSize=(-1,
                                                                                                                    1,
                                                                                                                    -1,
                                                                                                                    1), suppressMouse=0)
        self.initialiseoptions(HelpMenu)
        self.reparentTo(aspect2d, 100)
        self.guiElements = {}
        self.guiElements['backgroundImage'] = DirectLabel(guiId='HelpMenubackgroundImage', parent=self, relief=None, image=self.gui.find('**/backgroundImage'), scale=self.guiScale, sortOrder=0)
        self.tips = loader.loadTexture('dgd%sArt/textures/tips_bg.jpg' % self.gameWrapper.boardName)
        self.control = loader.loadTexture('dgd%sArt/textures/control_bg.jpg' % self.gameWrapper.boardName)
        self.pressed = False
        self.guiElements['next'] = DirectButton(guiId='HelpMenunext', parent=self, relief=None, image=[self.gui.find('**/next_up'), self.gui.find('**/next_down'), self.gui.find('**/next_roll'), self.gui.find('**/next_up')], scale=self.guiScale, pressEffect=True, command=self.__next__)
        self.guiElements['back'] = DirectButton(guiId='HelpMenuback', parent=self, relief=None, image=[self.gui.find('**/back_up'), self.gui.find('**/back_down'), self.gui.find('**/back_roll'), self.gui.find('**/back_up')], scale=self.guiScale, pressEffect=True, command=self.back)
        self.guiElements['logo'] = DirectLabel(guiId='HelpMenulogo', parent=self, relief=None, image=self.gui.find('**/logo'), scale=self.guiScale, sortOrder=0)
        self.guiElements['version'] = DirectLabel(guiId='HelpVersion', parent=self, relief=None, pos=(1.23,
                                                                                                      0,
                                                                                                      -0.96), scale=0.1, text_scale=0.4, color=(1,
                                                                                                                                                1,
                                                                                                                                                1,
                                                                                                                                                1), text=self.version, sortOrder=4)
        return

    def __next__(self):
        if not self.pressed:
            self.pressed = True
            self.guiElements['backgroundImage'].setTexture(self.tips, 1)
            self.guiElements['next'].hide()

    def back(self):
        if self.pressed:
            self.pressed = False
            self.guiElements['backgroundImage'].setTexture(self.control, 1)
            self.guiElements['next'].show()
        else:
            self.gameWrapper.exitHelpMenu()

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