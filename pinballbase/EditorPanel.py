# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: EditorPanel.py
import Tkinter
from Tkinter import *
from tkFileDialog import asksaveasfilename
import Pmw
from pinballbase.odeConstructs import *
import sgode.pyode
from PinballElements import *

class EditorPanel:
    __module__ = __name__

    def __init__(self, pe, bw):
        root = Tk()
        root.title('Pinball Editor')
        self.pinballEditor = pe
        self.boardWorld = bw
        frame = Frame(root)
        self.makeMenuBar(frame)
        self.defaultProperties(frame)
        self.makeButtons(frame)
        self.colType = StringVar()
        self.rubberChecked = IntVar()
        self.makeRadioButtons(frame)
        self.makeCheckBoxes(frame)
        self.textEntries(frame)
        frame.pack(side=TOP)
        self.cSelect = 'Wall'
        root.bind('<Return>', self.makeChanges)

    def makeChanges(self, ignore=None):
        if base.direct.selected.last == None and not base.direct.selected.last.isEmpty():
            return
        proxPoint = False
        odeElement = False
        refPoint = False
        if self.boardWorld.proxPoints.has_key(base.direct.selected.last.getName()):
            proxPoint = True
        if self.boardWorld.boardObjects.has_key(base.direct.selected.last.getName()):
            odeElement = True
        if self.boardWorld.refPoints.has_key(base.direct.selected.last.getName()):
            refPoint = True
        if refPoint:
            currentPoint = self.boardWorld.refPoints[base.direct.selected.last.getName()]
            oldName = base.direct.selected.last.getName()
            currentPoint.setName(self.proxNameEntry.get())
            self.boardWorld.refPoints[currentPoint.getName()] = currentPoint
            del self.boardWorld.refPoints[oldName]
            print 'RefPoint Changes Made'
            return
        if not proxPoint and not odeElement:
            return
        if proxPoint:
            currentPoint = self.boardWorld.proxPoints[base.direct.selected.last.getName()]
            currentPoint.name = self.proxNameEntry.get()
            currentPoint.time = float(self.delayEntry.get())
            currentPoint.callInName = self.inMethodEntry.get()
            currentPoint.callOutName = self.outMethodEntry.get()
            currentPoint.callTimerName = self.timerMethodEntry.get()
            currentPoint.args = self.argsEntry.get()
            currentPoint.errand = self.errandEntry.get()
            currentPoint.zone = self.zoneEntry.get()
            self.bumperPowerEntry.config(state=DISABLED)
            self.bumperEggEntry.config(state=DISABLED)
            self.triggerDelayEntry.config(state=DISABLED)
            if base.direct.selected.last.getName() != currentPoint.name:
                self.boardWorld.proxPoints[currentPoint.name] = currentPoint
                del self.boardWorld.proxPoints[base.direct.selected.last.getName()]
                base.direct.selected.last.setName(currentPoint.name)
        if odeElement:
            currentElement = self.boardWorld.boardObjects[base.direct.selected.last.getName()]
            currentElement.zone = self.zoneEntry.get()
            if self.rubberChecked.get():
                currentElement.setRubber(True)
            else:
                currentElement.setRubber(False)
            if self.cSelect == 'Wall':
                currentElement.setCategory(WALL_CATEGORY, True)
                self.bumperPowerEntry.config(state=DISABLED)
                self.bumperEggEntry.config(state=DISABLED)
                self.triggerDelayEntry.config(state=DISABLED)
                self.inMethodEntry.config(state=DISABLED)
                self.argsEntry.config(state=DISABLED)
                self.errandEntry.config(state=DISABLED)
            elif self.cSelect == 'Trigger':
                currentElement.setCategory(TRIGGER_CATEGORY, True)
                self.triggerDelayEntry.config(state=NORMAL)
                self.bumperPowerEntry.config(state=DISABLED)
                self.bumperEggEntry.config(state=DISABLED)
                self.inMethodEntry.config(state=NORMAL)
                self.argsEntry.config(state=NORMAL)
                self.errandEntry.config(state=NORMAL)
            elif self.cSelect == 'Bumper':
                currentElement.setCategory(BUMPER_CATEGORY, True)
                self.bumperPowerEntry.config(state=NORMAL)
                self.bumperEggEntry.config(state=NORMAL)
                self.triggerDelayEntry.config(state=DISABLED)
                self.inMethodEntry.config(state=DISABLED)
                self.argsEntry.config(state=DISABLED)
                currentElement.bumperPower = self.bumperPowerEntry.get()
                currentElement.eggfile = self.bumperEggEntry.get()
            elif self.cSelect == 'BumperTrigger':
                currentElement.setCategory(BUMPER_TRIGGER_CATEGORY, True)
                self.bumperPowerEntry.config(state=NORMAL)
                self.bumperEggEntry.config(state=NORMAL)
                self.triggerDelayEntry.config(state=NORMAL)
                self.inMethodEntry.config(state=NORMAL)
                self.argsEntry.config(state=NORMAL)
                self.errandEntry.config(state=NORMAL)
                currentElement.bumperPower = self.bumperPowerEntry.get()
                currentElement.eggfile = self.bumperEggEntry.get()
            if self.boardWorld.triggers.has_key(base.direct.selected.last.getName()) and self.cSelect != 'Trigger' and self.cSelect != 'BumperTrigger':
                self.delayEntry.delete(0, END)
                self.inMethodEntry.delete(0, END)
                self.outMethodEntry.delete(0, END)
                self.timerMethodEntry.delete(0, END)
                self.argsEntry.delete(0, END)
                self.errandEntry.delete(0, END)
                self.bumperPowerEntry.delete(0, END)
                self.bumperEggEntry.delete(0, END)
                self.triggerDelayEntry.delete(0, END)
                del self.boardWorld.triggers[base.direct.selected.last.getName()]
            if self.boardWorld.triggers.has_key(base.direct.selected.last.getName()) and (self.cSelect == 'Trigger' or self.cSelect == 'BumperTrigger'):
                print 'updating info'
                currentTrigger = self.boardWorld.triggers[base.direct.selected.last.getName()]
                currentTrigger.name = self.proxNameEntry.get()
                currentTrigger.callInName = self.inMethodEntry.get()
                currentTrigger.args = self.argsEntry.get()
                currentTrigger.errand = self.errandEntry.get()
                currentTrigger.triggerDelay = self.triggerDelayEntry.get()
                if base.direct.selected.last.getName() != currentTrigger.name:
                    self.boardWorld.boardObjects[currentTrigger.name] = currentElement
                    self.boardWorld.triggers[currentTrigger.name] = currentTrigger
                    del self.boardWorld.triggers[base.direct.selected.last.getName()]
                    del self.boardWorld.boardObjects[base.direct.selected.last.getName()]
                    base.direct.selected.last.setName(currentTrigger.name)
            if not self.boardWorld.triggers.has_key(base.direct.selected.last.getName()) and (self.cSelect == 'Trigger' or self.cSelect == 'BumperTrigger'):
                currentTrigger = Trigger(self.proxNameEntry.get())
                currentTrigger.callInName = self.inMethodEntry.get()
                currentTrigger.args = self.argsEntry.get()
                currentTrigger.errand = self.errandEntry.get()
                currentTrigger.triggerDelay = self.triggerDelayEntry.get()
                if base.direct.selected.last.getName() != currentTrigger.name:
                    self.boardWorld.boardObjects[currentTrigger.name] = currentElement
                    self.boardWorld.triggers[currentTrigger.name] = currentTrigger
                    del self.boardWorld.boardObjects[base.direct.selected.last.getName()]
                    base.direct.selected.last.setName(currentTrigger.name)
                else:
                    self.boardWorld.triggers[currentTrigger.name] = currentTrigger
            if not self.boardWorld.triggers.has_key(base.direct.selected.last.getName()) and self.cSelect != 'Trigger' and self.cSelect != 'BumperTrigger':
                if base.direct.selected.last.getName() != self.proxNameEntry.get():
                    self.boardWorld.boardObjects[self.proxNameEntry.get()] = currentElement
                    del self.boardWorld.boardObjects[base.direct.selected.last.getName()]
                    base.direct.selected.last.setName(self.proxNameEntry.get())
        print 'Changes Made'
        return

    def makeChanges1(self):
        self.cSelect = 'Wall'
        self.makeChanges()

    def makeChanges2(self):
        self.cSelect = 'Trigger'
        self.makeChanges()

    def makeChanges3(self):
        self.cSelect = 'Bumper'
        self.makeChanges()

    def makeChanges4(self):
        self.cSelect = 'BumperTrigger'
        self.makeChanges()

    def makeChangesRubber(self):
        if self.rubberChecked.get() == 1:
            self.rubberChecked.set(0)
        else:
            self.rubberChecked.set(1)
        self.makeChanges()

    def defaultProperties(self, frame):
        textent = Frame(frame)
        labelFrame = Frame(textent)
        Label(labelFrame, text='Default Box, Cylinder, and ProxPoint Properties').pack(side=TOP)
        labelFrame.pack(side=TOP)
        dimFrame = Frame(textent)
        self.lengthEntry = Entry(dimFrame, width=5)
        self.lengthEntry.insert(END, '1')
        Label(dimFrame, text='Length').pack(side=LEFT)
        self.lengthEntry.pack(side=LEFT)
        self.widthEntry = Entry(dimFrame, width=5)
        self.widthEntry.insert(END, '1')
        Label(dimFrame, text='Width').pack(side=LEFT)
        self.widthEntry.pack(side=LEFT)
        self.heightEntry = Entry(dimFrame, width=5)
        self.heightEntry.insert(END, '1')
        Label(dimFrame, text='Height').pack(side=LEFT)
        self.heightEntry.pack(side=LEFT)
        dimFrame.pack(side=TOP)
        dimFrame1 = Frame(textent)
        self.radiusEntry = Entry(dimFrame1, width=5)
        self.radiusEntry.insert(END, '.5')
        Label(dimFrame1, text='Radius').pack(side=LEFT)
        self.radiusEntry.pack(side=LEFT)
        self.defaultZoneEntry = Entry(dimFrame1, width=2)
        self.defaultZoneEntry.insert(END, '0')
        Label(dimFrame1, text='Default Zone').pack(side=LEFT)
        self.defaultZoneEntry.pack(side=LEFT)
        dimFrame1.pack(side=TOP)
        textent.pack(side=TOP)

    def makeRadioButtons(self, frame):
        textent = Frame(frame)
        labelFrame = Frame(textent)
        Label(labelFrame, text='Properties').pack(side=TOP)
        labelFrame.pack(side=TOP)
        radioFrame = Frame(textent)
        self.radioButtons = []
        b = Radiobutton(radioFrame, variable=self.colType, value='Wall', text='Wall', command=self.makeChanges1)
        self.radioButtons.append(b)
        b = Radiobutton(radioFrame, variable=self.colType, value='Trigger', text='Trigger', command=self.makeChanges2)
        self.radioButtons.append(b)
        b = Radiobutton(radioFrame, variable=self.colType, value='Bumper', text='Bumper', command=self.makeChanges3)
        self.radioButtons.append(b)
        b = Radiobutton(radioFrame, variable=self.colType, value='BumperTrigger', text='BumperTrigger', command=self.makeChanges4)
        self.radioButtons.append(b)
        self.radioButtons.append(Radiobutton(radioFrame, variable=self.colType, value='ProxPoint', text='ProxPoint'))
        for rb in self.radioButtons:
            rb.pack(side=TOP)
            rb.config(state=DISABLED)

        radioFrame.pack(side=TOP)
        textent.pack(side=TOP)

    def makeCheckBoxes(self, frame):
        textent = Frame(frame)
        checkbuttonFrame = Frame(textent)
        self.checkbuttons = []
        self.rubberCheckButton = Checkbutton(checkbuttonFrame, variable=self.rubberChecked, text='Rubber', command=self.makeChangesRubber)
        self.checkbuttons.append(self.rubberCheckButton)
        for cb in self.checkbuttons:
            cb.pack(side=TOP)
            cb.config(state=DISABLED)

        checkbuttonFrame.pack(side=TOP)
        textent.pack(side=TOP)

    def textEntries(self, frame):
        textent = Frame(frame)
        nameFrame = Frame(textent)
        self.proxNameEntry = Entry(nameFrame)
        self.proxNameEntry.pack(side=RIGHT)
        Label(nameFrame, text='Name').pack(side=LEFT)
        nameFrame.pack(side=TOP)
        delayFrame = Frame(textent)
        self.delayEntry = Entry(delayFrame)
        self.delayEntry.pack(side=RIGHT)
        Label(delayFrame, text='Timer Delay').pack(side=LEFT)
        delayFrame.pack(side=TOP)
        inFrame = Frame(textent)
        self.inMethodEntry = Entry(inFrame)
        self.inMethodEntry.pack(side=RIGHT)
        Label(inFrame, text='In Method').pack(side=LEFT)
        inFrame.pack(side=TOP)
        outFrame = Frame(textent)
        self.outMethodEntry = Entry(outFrame)
        self.outMethodEntry.pack(side=RIGHT)
        Label(outFrame, text='Out Method').pack(side=LEFT)
        outFrame.pack(side=TOP)
        timerFrame = Frame(textent)
        self.timerMethodEntry = Entry(timerFrame)
        self.timerMethodEntry.pack(side=RIGHT)
        Label(timerFrame, text='Timer Method').pack(side=LEFT)
        timerFrame.pack(side=TOP)
        argFrame = Frame(textent)
        self.argsEntry = Entry(argFrame)
        self.argsEntry.pack(side=RIGHT)
        Label(argFrame, text='Extra Arguments []').pack(side=LEFT)
        argFrame.pack(side=TOP)
        errandFrame = Frame(textent)
        self.errandEntry = Entry(errandFrame)
        self.errandEntry.pack(side=RIGHT)
        Label(errandFrame, text='Errand').pack(side=LEFT)
        errandFrame.pack(side=TOP)
        zoneFrame = Frame(textent)
        self.zoneEntry = Entry(zoneFrame)
        self.zoneEntry.pack(side=RIGHT)
        Label(zoneFrame, text='Zone').pack(side=LEFT)
        zoneFrame.pack(side=TOP)
        bumperPowerFrame = Frame(textent)
        self.bumperPowerEntry = Entry(bumperPowerFrame)
        self.bumperPowerEntry.pack(side=RIGHT)
        Label(bumperPowerFrame, text='Bumper Power').pack(side=LEFT)
        bumperPowerFrame.pack(side=TOP)
        bumperEggFrame = Frame(textent)
        self.bumperEggEntry = Entry(bumperEggFrame)
        self.bumperEggEntry.pack(side=RIGHT)
        Label(bumperEggFrame, text='Bumper Egg').pack(side=LEFT)
        bumperEggFrame.pack(side=TOP)
        triggerDelayFrame = Frame(textent)
        self.triggerDelayEntry = Entry(triggerDelayFrame)
        self.triggerDelayEntry.pack(side=RIGHT)
        Label(triggerDelayFrame, text='Trigger Delay').pack(side=LEFT)
        triggerDelayFrame.pack(side=TOP)
        applyFrame = Frame(textent)
        self.applyButton = Button(applyFrame, text='Apply', command=self.makeChanges)
        self.applyButton.pack(side=TOP)
        applyFrame.pack(side=TOP)
        textent.pack(side=BOTTOM)

    def txtfr(self, frame):
        textfr = Frame(frame)
        self.text = Text(textfr, height=1, width=50, background='white')
        self.text.pack(side=LEFT)
        textfr.pack(side=TOP)

    def makeMenuBar(self, frame):
        frame.tk_menuBar(self.fileMenu(frame))
        frame.pack(fill=X, side=LEFT)

    def fileMenu(self, frame):
        file_btn = Tkinter.Menubutton(frame, text='File', underline=0)
        file_btn.pack(side=TOP, padx='2m')
        file_btn.menu = Tkinter.Menu(file_btn)
        file_btn.menu.add_command(label='Save', underline=0, command=self.pinballEditor.saveBoard)
        file_btn.menu.add_command(label='Save As', underline=0, command=self.saveAs)
        file_btn['menu'] = file_btn.menu
        return file_btn

    def makeButtons(self, frame):
        buttonBox1 = Pmw.ButtonBox(frame)
        buttonBox1.pack(fill='x')
        buttonBox1.add('Make Box', command=self.pinballEditor.makeBox)
        buttonBox1.add('Make Cylinder', command=self.pinballEditor.makeCylinder)
        buttonBox1.add('Make ProxPoint', command=self.pinballEditor.makeProxPoint)
        buttonBox1.add('Make RefPoint', command=self.pinballEditor.makeRefPoint)
        buttonBox2 = Pmw.ButtonBox(frame)
        buttonBox2.pack(fill='x')
        buttonBox2.add('Toggle AutoCam', command=self.pinballEditor.toggleAutoCam)
        buttonBox2.add('Toggle Holes', command=self.pinballEditor.toggleHoles)
        buttonBox2.add('Toggle Hinges', command=self.pinballEditor.toggleHinges)
        buttonBox2.add('Reload', command=self.pinballEditor.reload, state=DISABLED)

    def saveAs(self):
        filename = asksaveasfilename(filetypes=[('allfiles', '*'), ('pythonfiles', '*.py')])
        self.pinballEditor.saveBoard(filename)