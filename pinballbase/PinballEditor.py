from .odeConstructs import *
from .EditorPanel import *
from direct.directtools.DirectCameraControl import *
from direct.tkpanels import Placer
from .PinballElements import *
import shutil

class PinballEditor:
    __module__ = __name__

    def __init__(self, bw, dfn):
        self.defaultFilename = dfn
        self.boardWorld = bw
        for object in list(self.boardWorld.boardObjects.values()):
            object.reparentTo(render)

        for object in list(self.boardWorld.refPoints.values()):
            object.reparentTo(render)

        for point in list(self.boardWorld.proxPoints.values()):
            point.setVisible(True)

        self.boardWorld.filmSize = 60
        lens = OrthographicLens()
        lens.setFilmSize(self.boardWorld.filmSize, self.boardWorld.filmSize)
        lens.setFilmOffset(0 * 0.5, 0 * 0.5)
        lens.setNearFar(-1000, 2000)
        base.camNode.setLens(lens)
        self.boardWorld.camX = 0
        self.boardWorld.camY = 0
        self.boardWorld.camZ = 0
        self.boardWorld.camH = 0
        self.boardWorld.camP = 270
        self.boardWorld.camR = 0
        self.hingesShowing = False
        self.hinges = None
        self.bumperEgg = 'you_forgot_to_call_setBumperEgg_didnt_you'
        self.boardWorld.accept('alt-c', self.makeCylinder)
        self.boardWorld.accept('alt-s', self.saveBoard)
        self.boardWorld.accept('alt-b', self.makeBox)
        self.boardWorld.accept('wheel_down', self.zoomIn)
        self.boardWorld.accept('wheel_up', self.zoomOut)
        self.boardWorld.accept('mouse2-up', self.centerCam)
        self.boardWorld.accept('mouse3-up', self.openPlacer)
        self.boardWorld.accept('mouse1-up', self.updatePanel)
        self.autoCam = True
        if not base.direct:
            print('You do not have Direct Tools enabled in your Config.prc, fix that before continuing')
            return
        self.editorPanel = EditorPanel(self, self.boardWorld)
        return

    def openPlacer(self):
        if not base.direct:
            print('You do not have Direct Tools enabled in your Config.prc, fix that before continuing')
            return
        if base.direct.selected.last != None:
            Placer.place(base.direct.selected.last)
        return

    def centerCam(self):
        if not base.direct:
            print('You do not have Direct Tools enabled in your Config.prc, fix that before continuing')
            return
        if self.autoCam:
            base.direct.cameraControl.spawnMoveToView(5)

    def toggleAutoCam(self):
        self.autoCam = not self.autoCam

    def toggleHoles(self):
        for p in list(self.boardWorld.proxPoints.values()):
            p.toggleHoleVisibility()

    def toggleHinges(self):
        if self.hingesShowing:
            self.hingesShowing = False
            for h in self.hinges:
                h.reparentTo(hidden)

        else:
            self.hingesShowing = True
            if self.hinges != None:
                for h in self.hinges:
                    h.reparentTo(render)

            self.hinges = []
            for f in self.boardWorld.leftFlippers + self.boardWorld.rightFlippers:
                self.hinges.append(self.makeHingePole(f))

        return

    def makeHingePole(self, flipper):
        odeHingePos = sgode.pyode.dRealArray(3)
        sgode.pyode.dJointGetHingeAnchor(flipper.flipperHinge, odeHingePos.cast())
        hingePos = Vec3(odeHingePos[0], odeHingePos[1], odeHingePos[2])
        print(hingePos)
        cylinderModel = loader.loadModelCopy('pinballbase/cylinder')
        cylinderModel.setScale(0.1, 0.1, 3)
        cylinderModel.setPos(hingePos[0], hingePos[1], hingePos[2])
        cylinderModel.reparentTo(render)
        return cylinderModel

    def setBumperEgg(self, bumperEgg):
        self.bumperEgg = bumperEgg

    def reload(self):
        del self.boardWorld.movables[0:len(self.boardWorld.movables)]
        del self.boardWorld.leftFlippers[0:len(self.boardWorld.leftFlippers)]
        del self.boardWorld.rightFlippers[0:len(self.boardWorld.rightFlippers)]
        self.boardWorld.proxPoints.clear()
        self.boardWorld.triggers.clear()
        for b in list(self.boardWorld.boardObjects.values()):
            b.destroy()

        self.boardWorld.boardObjects.clear()
        self.boardWorld.createFlippers()
        self.boardWorld.createSlingshots()
        self.boardWorld.callCreateBoard()
        for object in list(self.boardWorld.boardObjects.values()):
            object.reparentTo(render)

        for point in list(self.boardWorld.proxPoints.values()):
            point.setVisible(True)

    def updatePanel(self):
        if not base.direct:
            print('You do not have Direct Tools enabled in your Config.prc, fix that before continuing')
            return
        if base.direct.selected.last == None or base.direct.selected.last.isEmpty():
            return
        proxPoint = False
        odeElement = False
        refPoint = False
        if base.direct.selected.last.getName() in self.boardWorld.proxPoints:
            proxPoint = True
        if base.direct.selected.last.getName() in self.boardWorld.boardObjects:
            odeElement = True
        if base.direct.selected.last.getName() in self.boardWorld.refPoints:
            refPoint = True
        self.editorPanel.proxNameEntry.delete(0, END)
        self.editorPanel.delayEntry.delete(0, END)
        self.editorPanel.inMethodEntry.delete(0, END)
        self.editorPanel.outMethodEntry.delete(0, END)
        self.editorPanel.timerMethodEntry.delete(0, END)
        self.editorPanel.argsEntry.delete(0, END)
        self.editorPanel.zoneEntry.delete(0, END)
        self.editorPanel.errandEntry.delete(0, END)
        self.editorPanel.triggerDelayEntry.delete(0, END)
        self.editorPanel.bumperPowerEntry.delete(0, END)
        self.editorPanel.bumperEggEntry.delete(0, END)
        if not proxPoint and not odeElement:
            for rb in self.editorPanel.radioButtons:
                rb.config(state=DISABLED)

            self.editorPanel.proxNameEntry.config(state=DISABLED)
            self.editorPanel.delayEntry.config(state=DISABLED)
            self.editorPanel.inMethodEntry.config(state=DISABLED)
            self.editorPanel.outMethodEntry.config(state=DISABLED)
            self.editorPanel.timerMethodEntry.config(state=DISABLED)
            self.editorPanel.argsEntry.config(state=DISABLED)
            self.editorPanel.errandEntry.config(state=DISABLED)
            self.editorPanel.zoneEntry.config(state=DISABLED)
            self.editorPanel.triggerDelayEntry.config(state=DISABLED)
            self.editorPanel.bumperPowerEntry.config(state=DISABLED)
            self.editorPanel.bumperEggEntry.config(state=DISABLED)
            self.editorPanel.applyButton.config(state=DISABLED)
            if refPoint:
                self.editorPanel.proxNameEntry.config(state=NORMAL)
                self.editorPanel.proxNameEntry.insert(END, base.direct.selected.last.getName())
                self.editorPanel.applyButton.config(state=NORMAL)
            return
        self.editorPanel.proxNameEntry.config(state=NORMAL)
        self.editorPanel.inMethodEntry.config(state=NORMAL)
        self.editorPanel.argsEntry.config(state=NORMAL)
        self.editorPanel.errandEntry.config(state=NORMAL)
        self.editorPanel.applyButton.config(state=NORMAL)
        self.editorPanel.zoneEntry.config(state=NORMAL)
        if odeElement:
            self.editorPanel.delayEntry.config(state=DISABLED)
            self.editorPanel.outMethodEntry.config(state=DISABLED)
            self.editorPanel.timerMethodEntry.config(state=DISABLED)
            self.editorPanel.rubberCheckButton.config(state=NORMAL)
            if self.boardWorld.boardObjects[base.direct.selected.last.getName()].isRubber():
                self.editorPanel.rubberCheckButton.select()
                self.editorPanel.rubberChecked.set(1)
            else:
                self.editorPanel.rubberCheckButton.deselect()
                self.editorPanel.rubberChecked.set(0)
            for rb in self.editorPanel.radioButtons:
                rb.config(state=NORMAL)

            self.editorPanel.radioButtons[4].config(state=DISABLED)
            catbits = self.boardWorld.boardObjects[base.direct.selected.last.getName()].getCategory()
            if catbits == WALL_CATEGORY:
                self.editorPanel.cSelect = 'Wall'
                self.editorPanel.radioButtons[0].select()
                self.editorPanel.triggerDelayEntry.config(state=DISABLED)
                self.editorPanel.bumperPowerEntry.config(state=DISABLED)
                self.editorPanel.bumperEggEntry.config(state=DISABLED)
                self.editorPanel.inMethodEntry.config(state=DISABLED)
                self.editorPanel.argsEntry.config(state=DISABLED)
                self.editorPanel.errandEntry.config(state=DISABLED)
            elif catbits == BUMPER_TRIGGER_CATEGORY:
                self.editorPanel.cSelect = 'BumperTrigger'
                self.editorPanel.triggerDelayEntry.config(state=NORMAL)
                self.editorPanel.bumperPowerEntry.config(state=NORMAL)
                self.editorPanel.bumperEggEntry.config(state=NORMAL)
                self.editorPanel.radioButtons[3].select()
                self.editorPanel.bumperPowerEntry.insert(END, self.boardWorld.boardObjects[base.direct.selected.last.getName()].getBumperPower())
                self.editorPanel.bumperEggEntry.insert(END, self.boardWorld.boardObjects[base.direct.selected.last.getName()].eggfile)
            elif catbits == TRIGGER_CATEGORY:
                self.editorPanel.cSelect = 'Trigger'
                self.editorPanel.triggerDelayEntry.config(state=NORMAL)
                self.editorPanel.bumperPowerEntry.config(state=DISABLED)
                self.editorPanel.bumperEggEntry.config(state=DISABLED)
                self.editorPanel.radioButtons[1].select()
            elif catbits == BUMPER_CATEGORY:
                self.editorPanel.cSelect = 'Bumper'
                self.editorPanel.bumperPowerEntry.config(state=NORMAL)
                self.editorPanel.bumperEggEntry.config(state=NORMAL)
                self.editorPanel.triggerDelayEntry.config(state=DISABLED)
                self.editorPanel.bumperPowerEntry.insert(END, self.boardWorld.boardObjects[base.direct.selected.last.getName()].getBumperPower())
                self.editorPanel.bumperEggEntry.insert(END, self.boardWorld.boardObjects[base.direct.selected.last.getName()].eggfile)
                self.editorPanel.radioButtons[2].select()
                self.editorPanel.inMethodEntry.config(state=DISABLED)
                self.editorPanel.argsEntry.config(state=DISABLED)
                self.editorPanel.errandEntry.config(state=DISABLED)
            self.editorPanel.proxNameEntry.insert(END, base.direct.selected.last.getName())
            self.editorPanel.zoneEntry.insert(END, self.boardWorld.boardObjects[base.direct.selected.last.getName()].getZone())
            if (catbits == BUMPER_TRIGGER_CATEGORY or catbits == TRIGGER_CATEGORY) and base.direct.selected.last.getName() in self.boardWorld.triggers:
                currentTrigger = self.boardWorld.triggers[base.direct.selected.last.getName()]
                self.editorPanel.inMethodEntry.insert(END, currentTrigger.callInName)
                self.editorPanel.errandEntry.insert(END, currentTrigger.errand)
                self.editorPanel.triggerDelayEntry.insert(END, currentTrigger.getTriggerDelay())
                args = '%s' % currentTrigger.args
                self.editorPanel.argsEntry.insert(END, args)
        else:
            self.editorPanel.rubberCheckButton.config(state=DISABLED)
        if proxPoint:
            self.editorPanel.delayEntry.config(state=NORMAL)
            self.editorPanel.outMethodEntry.config(state=NORMAL)
            self.editorPanel.timerMethodEntry.config(state=NORMAL)
            self.editorPanel.radioButtons[4].select()
            for rb in self.editorPanel.radioButtons:
                rb.config(state=DISABLED)

            currentPoint = self.boardWorld.proxPoints[base.direct.selected.last.getName()]
            self.editorPanel.proxNameEntry.insert(END, currentPoint.name)
            self.editorPanel.delayEntry.insert(END, currentPoint.time)
            self.editorPanel.inMethodEntry.insert(END, currentPoint.callInName)
            self.editorPanel.outMethodEntry.insert(END, currentPoint.callOutName)
            self.editorPanel.timerMethodEntry.insert(END, currentPoint.callTimerName)
            self.editorPanel.zoneEntry.insert(END, currentPoint.getZone())
            args = '%s' % currentPoint.args
            self.editorPanel.argsEntry.insert(END, args)
            self.editorPanel.errandEntry.insert(END, currentPoint.errand)
        return

    def zoomIn(self):
        self.boardWorld.filmSize = self.boardWorld.filmSize - 5
        if self.boardWorld.filmSize < 5:
            self.boardWorld.filmSize = 5
        lens = base.camNode.getLens()
        lens.setFilmSize(self.boardWorld.filmSize, self.boardWorld.filmSize)
        base.camNode.setLens(lens)

    def zoomOut(self):
        self.boardWorld.filmSize = self.boardWorld.filmSize + 5
        if self.boardWorld.filmSize > 400:
            self.boardWorld.filmSize = 400
        lens = base.camNode.getLens()
        lens.setFilmSize(self.boardWorld.filmSize, self.boardWorld.filmSize)
        base.camNode.setLens(lens)

    def makeRefPoint(self):
        if self.editorPanel.lengthEntry.get() == '':
            length = 1.0
        else:
            length = float(self.editorPanel.lengthEntry.get())
        if self.editorPanel.widthEntry.get() == '':
            width = 1.0
        else:
            width = float(self.editorPanel.widthEntry.get())
        if self.editorPanel.heightEntry.get() == '':
            height = 1.0
        else:
            height = float(self.editorPanel.heightEntry.get())
        pos = self.boardWorld.ballPlacer.getPos()
        rp = RefPoint(pos[0], pos[1], pos[2] + height / 2, 0, 0, 0, 'RefPoint%d' % len(self.boardWorld.refPoints), length=length, width=width, height=height, visible=True)
        self.boardWorld.refPoints[rp.getName()] = rp

    def makeBox(self):
        density = 5
        if self.editorPanel.lengthEntry.get() == '':
            length = 1.0
        else:
            length = float(self.editorPanel.lengthEntry.get())
        if self.editorPanel.widthEntry.get() == '':
            width = 1.0
        else:
            width = float(self.editorPanel.widthEntry.get())
        if self.editorPanel.heightEntry.get() == '':
            height = 1.0
        else:
            height = float(self.editorPanel.heightEntry.get())
        if self.editorPanel.defaultZoneEntry.get() == '':
            zone = 0
        else:
            zone = int(self.editorPanel.defaultZoneEntry.get())
        box = ODEBox(width, length, height, density, self.boardWorld.odeWorld, self.boardWorld.odeSpace, isStatic=True)
        pos = self.boardWorld.ballPlacer.getPos()
        box.setPos(pos[0], pos[1], pos[2] + height / 2)
        self.boardWorld.boardObjects[box.getName()] = box
        self.boardWorld.boardObjects[box.getName()].zone = zone
        box.setODETransformFromNodePath()
        box.reparentTo(render)
        box.update()

    def makeCylinder(self):
        density = 5
        if self.editorPanel.lengthEntry.get() == '':
            length = 1.0
        else:
            length = float(self.editorPanel.lengthEntry.get())
        if self.editorPanel.radiusEntry.get() == '':
            radius = 0.5
        else:
            radius = float(self.editorPanel.radiusEntry.get())
        if self.editorPanel.defaultZoneEntry.get() == '':
            zone = 0
        else:
            zone = int(self.editorPanel.defaultZoneEntry.get())
        cyl = ODECCylinder(radius, length, density, self.boardWorld.odeWorld, self.boardWorld.odeSpace, isStatic=True)
        pos = self.boardWorld.ballPlacer.getPos()
        cyl.setPos(pos[0], pos[1], pos[2] + radius)
        cyl.setHpr(0, 90, 0)
        self.boardWorld.boardObjects[cyl.getName()] = cyl
        self.boardWorld.boardObjects[cyl.getName()].zone = zone
        cyl.setODETransformFromNodePath()
        cyl.reparentTo(render)
        cyl.update()

    def makeProxPoint(self):
        if self.editorPanel.radiusEntry.get() == '':
            radius = 0.5
        else:
            radius = float(self.editorPanel.radiusEntry.get())
        if self.editorPanel.defaultZoneEntry.get() == '':
            zone = 0
        else:
            zone = int(self.editorPanel.defaultZoneEntry.get())
        proxPos = self.boardWorld.ballPlacer.getPos()
        self.boardWorld.proxPoints['Rename Me'] = ProxPoint(self.boardWorld.odeWorld, self.boardWorld.odeSpace, proxPos[0], proxPos[1], proxPos[2] + radius, radius, 3.0, 'Rename Me', visible=True, zone=zone)

    def saveBoard(self, filename=''):
        density = 5.0
        if filename == '':
            filename = self.defaultFilename
        shutil.copy(filename, filename + '.bak')
        try:
            outfile = open(filename, 'w')
        except IOError:
            print('There was an error (probably read-only) writing to ' + filename)
            print('Now your backup is read-only, make sure to switch that back to normal')
            return

        outfile.write('#Auto-Generated Code describing ODE collision solids, triggers, RefPoints, and ProxPoints\n')
        outfile.write('from pinballbase.odeConstructs import *\n')
        outfile.write('from pinballbase.PinballElements import *\n')
        outfile.write('def createBoard( self ):\n')
        for object in list(self.boardWorld.boardObjects.values()):
            oldsca = object.model.getScale()
            newsca = object.getScale()
            sca0 = oldsca[0] * newsca[0]
            sca1 = oldsca[1] * newsca[1]
            sca2 = oldsca[2] * newsca[2]
            sca = Vec3(sca0, sca1, sca2)
            catbits = object.getCategory()
            if isinstance(object, ODEBumper) or catbits == BUMPER_CATEGORY or catbits == BUMPER_TRIGGER_CATEGORY:
                bp = object.getBumperPower()
                if bp == None or bp == '':
                    bp = '20000'
                newBumperPower = int(bp)
                outfile.write('\tpiece = ODEBumper( %f, self.odeWorld, self.odeSpace, "%s", isStatic=True, name= "%s", zone=%d, bumperPower=%d)\n' % (density, object.eggfile, object.getName(), int(object.getZone()), newBumperPower))
            elif isinstance(object, ODEBox):
                outfile.write('\tpiece = ODEBox( %f, %f, %f, %f, self.odeWorld, self.odeSpace, isStatic=True, name= "%s", zone=%d )\n' % (sca[0], sca[1], sca[2], density, object.getName(), int(object.getZone())))
            elif isinstance(object, ODECCylinder):
                outfile.write('\tpiece = ODECCylinder( %f, %f, %f, self.odeWorld, self.odeSpace, isStatic=True, name= "%s", zone=%d )\n' % (sca[0], sca[2], density, object.getName(), int(object.getZone())))
            elif isinstance(object, ODESphere):
                outfile.write('\tpiece = ODESphere( %f, %f, self.odeWorld, self.odeSpace, isStatic=True, name="%s", zone=%d )\n' % (sca[1], density, object.getName(), int(object.getZone())))
            pos = object.getPos()
            hpr = object.getHpr()
            outfile.write('\tpiece.setPos( %f, %f, %f )\n' % (pos[0], pos[1], pos[2]))
            outfile.write('\tpiece.setHpr( %f, %f, %f )\n' % (hpr[0], hpr[1], hpr[2]))
            outfile.write('\tself.boardObjects[piece.getName()] = piece \n')
            outfile.write('\tpiece.setCategory( %s, True )\n' % categories[catbits])
            if object.isRubber():
                outfile.write('\tpiece.setRubber(True)\n')
            if catbits == TRIGGER_CATEGORY or catbits == BUMPER_TRIGGER_CATEGORY:
                outfile.write('\tpiece.setTrigger(True)\n')
                t = self.boardWorld.triggers[object.getName()]
                if t.args == '':
                    t.args = []
                if t.callInName == '':
                    t.callInName = 'dummy'
                td = t.getTriggerDelay()
                if td == None or td == '':
                    td = '0.05'
                if t.errand != '':
                    outfile.write('\tself.triggers["%s"] = Trigger( "%s", "%s", callMethodIn=self.errands["%s"].%s, args=%s, triggerDelay=%f )\n' % (object.getName(), object.getName(), t.errand, t.errand, t.callInName, t.args, float(td)))
                else:
                    outfile.write('\tself.triggers["%s"] = Trigger( "%s", callMethodIn=self.%s, args=%s, triggerDelay=%f )\n' % (object.getName(), object.getName(), t.callInName, t.args, float(td)))

        outfile.write('\n')
        outfile.write('\tfor object in self.boardObjects.values():\n')
        outfile.write('\t\tobject.setODETransformFromNodePath()\n')
        outfile.write('\t\tif ( object.normallySeen ) :\n')
        outfile.write('\t\t\tobject.reparentTo( render )\n')
        outfile.write('\t\t\tobject.update() # sanity check\n')
        outfile.write('\n\n\t#Add all the proximity triggers\n')
        for point in list(self.boardWorld.proxPoints.values()):
            if not point.writeOut:
                continue
            oldsca = point.getScale()
            sca0 = oldsca[0]
            pos = point.getPos()
            writeString = '\tself.proxPoints["%s"] = ProxPoint( self.odeWorld, self.odeSpace, %f, %f, %f, %f, %f, "%s", "%s"' % (point.name, pos[0], pos[1], pos[2], sca0, point.time, point.name, point.errand)
            if point.errand == '':
                firstPart = 'self.'
            else:
                firstPart = 'self.errands["%s"].' % point.errand
            if point.callInName != '':
                inFunc = point.callInName
                writeString = writeString + ', callMethodIn = %s%s' % (firstPart, inFunc)
            if point.callOutName != '':
                outFunc = point.callOutName
                writeString = writeString + ', callMethodOut = %s%s' % (firstPart, outFunc)
            if point.callTimerName != '':
                timerFunc = point.callTimerName
                writeString = writeString + ', callMethodTimer = %s%s' % (firstPart, timerFunc)
            writeString = writeString + ', args=%s ' % point.args
            writeString = writeString + ', zone=%d ' % int(point.getZone())
            writeString = writeString + ')\n'
            outfile.write(writeString)

        outfile.write('\n\n\t#Add all the RefPoints\n')
        for point in list(self.boardWorld.refPoints.values()):
            pos = point.getPos()
            hpr = point.getHpr()
            scale = point.getScale()
            writeString = '\tself.refPoints["%s"] = RefPoint( %f, %f, %f, %f, %f, %f, "%s", %f, %f, %f )\n' % (point.getName(), pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2], point.getName(), scale[0], scale[1], scale[2])
            outfile.write(writeString)

        outfile.write('\n\n')
        outfile.close()
        print('File written successfully')
        return