from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from direct.task.TaskManagerGlobal import *

class PirateWaterEffects:
    __module__ = __name__

    def __init__(self, board):
        self.board = board
        self.waterWakes = []
        cm1 = CardMaker('planemaker1')
        cm1.setFrame(-2.6, 2.6, -8, 8)
        self.numberOfWakes = 3
        self.waterLevel = -3
        for j in range(self.numberOfWakes):
            littleWakes = []
            littleWakes.append(NodePath(cm1.generate()))
            littleWakes.append(NodePath(cm1.generate()))
            for i in range(len(littleWakes)):
                littleWakes[i].reparentTo(render)
                littleWakes[i].setTexture(loader.loadTexture('piratepinball/art/main_ship/textures/Wake%d.png' % i))
                littleWakes[i].setHpr(20 + 320 * i, 270, 0)
                littleWakes[i].setPos(-11 + i * 22, -22, -2.8 + i * 0.7)
                littleWakes[i].node().setAttrib(LightAttrib.makeAllOff())
                littleWakes[i].setTransparency(1)
                littleWakes[i].setBin('flat', 1 + i)

            self.waterWakes.append(littleWakes)

        self.waterPlanes = []
        cm = CardMaker('plane maker')
        cm.setUvRange(Point2(0.0, 0.0), Point2(4.0, 4.0))
        cm.setFrame(-150, 150, -100, 100)
        self.waterPlanes.append(NodePath(cm.generate()))
        for wp in range(len(self.waterPlanes)):
            self.waterPlanes[wp].reparentTo(render)
            self.waterPlanes[wp].setPos(0, 0 - wp * 200, self.waterLevel)
            self.waterPlanes[wp].setHpr(0, 270, 0)
            self.waterPlanes[wp].setTexture(loader.loadTexture('piratepinball/art/main_ship/textures/Water2.jpg'))
            self.waterPlanes[wp].node().setAttrib(LightAttrib.makeAllOff())

        self.speed = 28
        taskMgr.add(self.update, 'piratesWaterMovementUpdate')
        self.stillMovement = Sequence(name='stillMovement')
        self.stillMovement.append(self.waterPlanes[0].posInterval(self.speed / 3, VBase3(0, 3, self.waterLevel), blendType='easeInOut'))
        self.stillMovement.append(self.waterPlanes[0].posInterval(self.speed / 3, VBase3(0, 0, self.waterLevel), blendType='easeInOut'))
        self.startWaterWake(self.speed / 4.0)
        self.skyDome = loader.loadModelCopy('piratepinball/art/main_ship/Skydome')
        self.skyDome.find('**/pPlane2').reparentTo(hidden)
        self.skyDome.find('**/pPlane1').reparentTo(hidden)
        self.skyDome.setScale(10)
        self.skyDome.setPos(0.0, 0.0, -86.0)
        self.skyDome.node().setAttrib(LightAttrib.makeAllOff())
        self.skyDome.reparentTo(render)

    def wake(self):
        taskMgr.add(self.update, 'piratesWaterMovementUpdate')
        for wp in self.waterPlanes:
            wp.show()

        for ww in self.waterWakes:
            ww[0].show()
            ww[1].show()

        for i in range(self.numberOfWakes):
            offset = self.speed / 4.0 / self.numberOfWakes
            self.bothWaterWakeMovements[i].loop()
            self.bothWaterWakeMovements[i].setT(offset * i)

    def sleep(self):
        taskMgr.remove('piratesWaterMovementUpdate')
        self.stillMovement.finish()
        for wp in self.waterPlanes:
            wp.hide()

        for ww in self.waterWakes:
            ww[0].hide()
            ww[1].hide()

        for wwm in self.bothWaterWakeMovements:
            if wwm != None and wwm.isPlaying():
                wwm.finish()

        return

    def startWaterWake(self, totalTime):
        self.bothWaterWakeMovements = []
        for i in range(self.numberOfWakes):
            self.bothWaterWakeMovements.append(Parallel(name='bothWaterWakeMovement%d' % i))
            for j in range(2):
                waterWake = Sequence(name='waterWake%d%d' % (i, j))
                waterWake.append(Func(self.waterWakes[i][j].setPos, -11 + j * 22, -22, -2.8))
                wakeMove = []
                wakeMove.append(self.waterWakes[i][j].posInterval(totalTime, VBase3(-20 + j * 40, 65, -2.8)))
                wakeMove.append(self.waterWakes[i][j].hprInterval(totalTime, VBase3(40 + 280 * j, 270, 0)))
                wakeMove.append(self.waterWakes[i][j].scaleInterval(totalTime, 3.5))
                waterWake.append(Parallel(*wakeMove))
                self.bothWaterWakeMovements[i].append(waterWake)

            offset = totalTime / self.numberOfWakes
            self.bothWaterWakeMovements[i].loop()
            self.bothWaterWakeMovements[i].setT(offset * i)

    def printMessage(self, message):
        print(message)

    def stopMoving(self):
        for wp in range(len(self.waterPlanes)):
            self.waterPlanes[wp].setPos(0, 0 - wp * 200, self.waterLevel)

        taskMgr.remove('piratesWaterMovementUpdate')
        self.stillMovement.loop()
        for i in self.bothWaterWakeMovements:
            i.finish()

    def startMoving(self):
        for wp in range(len(self.waterPlanes)):
            self.waterPlanes[wp].setPos(0, 0 - wp * 200, self.waterLevel)

        taskMgr.add(self.update, 'piratesWaterMovementUpdate')
        self.stillMovement.finish()
        for i in range(self.numberOfWakes):
            offset = self.speed / 4 / self.numberOfWakes
            self.bothWaterWakeMovements[i].loop()
            self.bothWaterWakeMovements[i].setT(offset * i)

    def turnOff(self):
        self.skyDome.reparentTo(hidden)
        for wp in self.waterPlanes:
            wp.reparentTo(hidden)

    def turnOn(self):
        self.skyDome.reparentTo(render)
        for wp in self.waterPlanes:
            wp.reparentTo(render)

    def update(self, task=None):
        frameTime = taskMgr.currentTime
        offset = -(frameTime / 5.0 % 1)
        self.waterPlanes[0].setTexOffset(TextureStage.getDefault(), VBase2(0, offset))
        return Task.cont