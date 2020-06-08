# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: fpsmeter.py
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
import direct.task.Task, time
from functools import reduce

class FPSMeter(DirectObject):
    __module__ = __name__

    def __init__(self, displayFPS=True, numSamples=20):
        self.displayFPS = displayFPS
        self.numSamples = numSamples
        self.fps = 0.0
        self.samples = []
        if displayFPS:
            self.initLabel()

    def initLabel(self):
        self.fpsLabel = DirectLabel(relief=None, pos=(-0.95, 0, 0.9), text='0.0 fps', color=Vec4(0, 0, 1, 1), text_scale=0.1)
        self.fpsLabel.hide()
        return

    def enable(self):
        self.disable()
        self.samples = []
        self.lastTime = time.time()
        if self.displayFPS:
            self.fpsLabel.show()
        task = Task.Task(self.fpsTask)
        taskMgr.add(task, 'fpsTask')

    def disable(self):
        if self.displayFPS:
            self.fpsLabel.hide()
        taskMgr.remove('fpsTask')

    def fpsTask(self, task):
        self.updateFPS()
        if self.displayFPS:
            self.updateDisplay()
        return Task.cont

    def updateFPS(self):
        t = time.time()
        dt = t - self.lastTime
        self.samples.append(dt)
        if len(self.samples) > self.numSamples:
            self.samples.pop(0)
        self.lastTime = t
        denom = reduce(lambda x, y: x + y, self.samples)
        if denom != 0:
            self.fps = len(self.samples) / denom
        else:
            self.fps = 100.0

    def updateDisplay(self):
        self.fpsLabel['text'] = '% 3.1f fps' % self.fps