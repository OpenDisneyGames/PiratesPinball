from direct.gui.DirectGui import DirectButton

class DirectMaxScaleButton(DirectButton):
    """
        DirectMaxScaleButton(parent) - Creates a DirectButton which enforces it's text it to display
        within the max width specified.
        """
    __module__ = __name__

    def __init__(self, parent=None, **kw):
        optiondefs = (
         ('maxWidth', 1, None), ('maxHeight', 1, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(DirectMaxScaleButton)
        return

    def setText(self):
        DirectButton.setText(self)
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