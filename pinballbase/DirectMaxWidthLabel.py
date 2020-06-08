# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: DirectMaxWidthLabel.py
from direct.gui.DirectGui import DirectLabel

class DirectMaxWidthLabel(DirectLabel):
    """
        DirectMaxWidthLabel(parent) - Creates a DirectLabel which enforces it's text it to display
        within the max width specified. If squish is true only scale the text along the x axis
        """
    __module__ = __name__

    def __init__(self, parent=None, **kw):
        self.idealScale = None
        self.myConstraints = []
        optiondefs = (
         ('maxWidth', 1, None), ('maxXScale', 0.5, None), ('maxYScale', 0.5, None), ('squish', 0, None))
        self.defineoptions(kw, optiondefs)
        DirectLabel.__init__(self, parent)
        self.initialiseoptions(DirectMaxWidthLabel)
        return

    def setText(self):
        DirectLabel.setText(self)
        for i in range(self['numStates']):
            ost = self.component('text' + `i`)
            lineWidth = ost.textNode.getWidth()
            if lineWidth == 0:
                self.idealScale = 1
                return
            largestScale = float(self['maxWidth'] / lineWidth)
            if largestScale > self['maxXScale']:
                ost['scale'] = (
                 self['maxXScale'], self['maxYScale'])
            else:
                if self['squish']:
                    ost['scale'] = (
                     largestScale, self['maxYScale'])
                    self.idealScale = (largestScale, self['maxYScale'])
                else:
                    ost['scale'] = (
                     largestScale, self['maxYScale'] * largestScale / self['maxXScale'])
                    self.idealScale = (largestScale, self['maxYScale'] * largestScale / self['maxXScale'])
                if len(self.myConstraints) > 0:
                    self.checkConstraints()

    def getCurrentScreenWidth(self):
        if self.hascomponent('text0'):
            return self.component('text0').textNode.getWidth() * self.component('text0')['scale'][0]
        else:
            return 0

    def getCurrentScreenHeight(self):
        if self.hascomponent('text0'):
            return self.component('text0').textNode.getHeight() * self.component('text0')['scale'][1]
        else:
            return 0

    def getIdealScale(self):
        if not isinstance(self.idealScale, tuple) and not isinstance(self.idealScale, list):
            if self.idealScale == None:
                self.idealScale = 1.0
            return (
             self.idealScale, self.idealScale)
        else:
            return self.idealScale
        return

    def addConstraintLabel(self, label):
        self.myConstraints.append(label)

    def checkConstraints(self):
        iAmSmallest = True
        smallestScale = self.getIdealScale()
        for label in self.myConstraints:
            if label.getIdealScale()[0] < smallestScale[0]:
                smallestScale = label.getIdealScale()
                iAmSmallest = False

        if iAmSmallest:
            for label in self.myConstraints:
                label['text_scale'] = smallestScale

        else:
            self['text_scale'] = smallestScale