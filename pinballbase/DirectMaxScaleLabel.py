# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: DirectMaxScaleLabel.py
from direct.gui.DirectGui import DirectLabel

class DirectMaxScaleLabel(DirectLabel):
    """
        DirectMaxScaleLabel(parent) - Creates a DirectLabel which enforces it's text it to display
        within the max width specified. 
        """
    __module__ = __name__

    def __init__(self, parent=None, **kw):
        optiondefs = (
         ('maxWidth', 1, None), ('maxHeight', 1, None))
        self.defineoptions(kw, optiondefs)
        DirectLabel.__init__(self, parent)
        self.initialiseoptions(DirectMaxScaleLabel)
        return

    def setText(self):
        DirectLabel.setText(self)
        for i in range(self['numStates']):
            ost = self.component('text' + repr(i))
            lineWidth = ost.textNode.getWidth()
            lineHeight = ost.textNode.getHeight()
            if lineWidth == 0:
                return
            largestWidthScale = float(self['maxWidth'] / lineWidth)
            largestHeightScale = float(self['maxHeight'] / lineHeight)
            scale = min(largestWidthScale, largestHeightScale)
            ost['scale'] = scale