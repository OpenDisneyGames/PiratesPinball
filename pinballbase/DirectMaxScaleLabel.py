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