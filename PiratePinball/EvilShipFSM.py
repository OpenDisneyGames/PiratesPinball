# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: EvilShipFSM.py
from PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
from pinballbase.odeConstructs import *
import Localizer
from direct.fsm.FSM import FSM

class EvilShipFSM(FSM):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('EvilShipFSM')

    def __init__(self, name, board, cannonArea, number):
        FSM.__init__(self, name)
        self.board = board
        self.cannonArea = cannonArea
        self.myNumber = number
        self.howManyTimesHit = 0
        self.hitThreshold = 3
        self.myRoute = 1
        self.sailingSequence = None
        self.sinkingSequence = None
        self.myRedColor = 0.0
        self.currentCourse = []
        self.evilShip = Actor('piratepinball/art/skull_island/EvilPirateShip', {'sink': 'piratepinball/art/skull_island/EvilPirateShip'})
        self.evilShip.setPos(self.board.refPoints['ES_SP_Center1'].getPos())
        self.evilShip.setHpr(self.board.refPoints['ES_SP_Center1'].getHpr())
        self.evilShip.reparentTo(render)
        self.evilShip.node().setAttrib(LightAttrib.makeAllOff())
        self.canGetHit = True
        self.totalTimeToAttack = 20
        self.myExplosionManager = BillboardManager(name='evilShip%d' % self.myNumber, howManyAtOnce=2, textureName='piratepinball/art/explosions/HitShip', numberOfTextures=6, seconds=0.3, scale=2.0)
        self.evilRoutes = [
         [
          'ES_SP_Left', 'ES_CP_Left', 'ES_FP_Left'], ['ES_SP_Center1', 'ES_CP_Center1A', 'ES_CP_Center1B', 'ES_FP_Center'], ['ES_SP_Center2', 'ES_CP_Center2A', 'ES_CP_Center2B', 'ES_FP_Center'], ['ES_SP_Right', 'ES_CP_Right', 'ES_FP_Right'], ['ES_SP_Left', 'ES_CP_Left']]
        self.board.proxPoints['EvilShip%d0' % self.myNumber] = ProxPoint(self.board.odeWorld, self.board.odeSpace, 0, 4, 11, 6.0, 3.0, 'EvilShip%d0' % self.myNumber, 'CannonArea', callMethodIn=self.gotHit, args=[self.myNumber, 0], zone=2, writeOut=False)
        self.board.proxPoints[('EvilShip%d0' % self.myNumber)].reparentTo(self.evilShip)
        self.board.proxPoints['EvilShip%d1' % self.myNumber] = ProxPoint(self.board.odeWorld, self.board.odeSpace, 0, 6.5, 3, 5.0, 3.0, 'EvilShip%d1' % self.myNumber, 'CannonArea', callMethodIn=self.gotHit, args=[self.myNumber, 1], zone=2, writeOut=False)
        self.board.proxPoints[('EvilShip%d1' % self.myNumber)].reparentTo(self.evilShip)
        self.board.proxPoints['EvilShip%d2' % self.myNumber] = ProxPoint(self.board.odeWorld, self.board.odeSpace, 0, -4, 3.0, 5.0, 3.0, 'EvilShip%d2' % self.myNumber, 'CannonArea', callMethodIn=self.gotHit, args=[self.myNumber, 2], zone=2, writeOut=False)
        self.board.proxPoints[('EvilShip%d2' % self.myNumber)].reparentTo(self.evilShip)
        return

    def gotHit(self, ballIndex, args):
        if self.canGetHit and self.state == 'Sailing':
            self.canGetHit = False
            self.myExplosionManager.startHere(self.board.balls[ballIndex].getPos())
            currentPos = self.board.balls[ballIndex].getPos()
            self.board.deactivateBall(ballIndex)
            self.howManyTimesHit += 1
            self.notify.debug('EvilShip %d got hit in proxPoint %d' % (args[0], args[1]))
            if args[1] == 4:
                self.board.pirateSounds['CannonArea_SailHit'].play()
            else:
                vol = 0.75 - currentPos[0] / -300
                if vol <= 0.1:
                    vol = 0.1
                self.board.pirateSounds['CannonArea_ShipHit'].setVolume(vol)
                self.board.pirateSounds['CannonArea_ShipHit'].play()
            self.evilShip.setColorScale(1, 0, 0, 1)
            self.myRedColor += 0.33
            self.board.pbTaskMgr.doMethodLater(0.1, self.evilShip.setColorScale, 'shipcolor%d' % self.myNumber, [VBase4(1, 1.0 - self.myRedColor, 1.0 - self.myRedColor, 1)])
            self.board.pbTaskMgr.doMethodLater(0.1, setattr, 'shiphitagain%d' % self.myNumber, [self, 'canGetHit', True])
            if self.howManyTimesHit >= self.hitThreshold:
                self.request('Sinking')

    def enterDocked(self):
        if self.sailingSequence != None and self.sailingSequence.isPlaying():
            self.sailingSequence.pause()
            self.sailingSequence.finish()
        self.evilShip.setPos(self.board.refPoints[self.evilRoutes[self.myRoute][0]].getPos())
        self.evilShip.setHpr(self.board.refPoints[self.evilRoutes[self.myRoute][0]].getHpr())
        self.evilShip.stop()
        self.evilShip.pose('sink', 0)
        self.evilShip.setColorScale(1, 1, 1, 1)
        self.howManyTimesHit = 0
        self.myRedColor = 0
        self.hitThreshold = 3
        self.totalTimeToAttack = 20
        self.evilShip.reparentTo(hidden)
        return

    def filterDocked(self, request, args):
        if request == 'Sailing':
            return 'Sailing'
        return self.defaultFilter(request, args)

    def exitDocked(self):
        pass

    def enterSailing(self):
        self.evilShip.reparentTo(render)
        self.sailingSequence = Sequence(name='sailingSequence%d' % self.myNumber)
        timeForEachWayPoint = self.totalTimeToAttack / len(self.evilRoutes[self.myRoute])
        for wayPoint in range(1, len(self.evilRoutes[self.myRoute])):
            parSail = []
            parSail.append(self.evilShip.hprInterval(timeForEachWayPoint, self.board.refPoints[self.evilRoutes[self.myRoute][wayPoint]].getHpr()))
            parSail.append(self.evilShip.posInterval(timeForEachWayPoint, self.board.refPoints[self.evilRoutes[self.myRoute][wayPoint]].getPos()))
            self.sailingSequence.append(Parallel(*parSail))

        if self.myRoute != 4:
            self.sailingSequence.append(Func(self.printString, 'About to be boarded.'))
            self.sailingSequence.append(Func(self.request, 'Boarded'))
        self.sailingSequence.start()

    def printString(self, string):
        print string

    def filterSailing(self, request, args):
        if request == 'Sinking':
            return 'Sinking'
        if request == 'Boarded':
            return 'Boarded'
        if request == 'Docked':
            return 'Docked'
        return self.defaultFilter(request, args)

    def exitSailing(self):
        pass

    def enterSinking(self):
        self.cannonArea.shipReportIn(self.myNumber, self.howManyTimesHit, 'sunk')
        self.sailingSequence.pause()
        if self.myRoute == 4:
            self.evilShip.play('sink')
            return
        self.cannonArea.courseStatus[self.myRoute] -= 1
        self.myRoute = self.cannonArea.getNewDock(self.myNumber)
        self.sinkingSequence = Sequence(name='sinkingSequence%d' % self.myNumber)
        self.sinkingSequence.append(self.evilShip.actorInterval('sink', playRate=1.5))
        self.sinkingSequence.append(Func(self.request, 'Docked'))
        self.sinkingSequence.start()
        vol = 0.8 - self.evilShip.getPos()[0] / -300
        if vol <= 0.1:
            vol = 0.1
        self.board.pirateSounds['CannonArea_ShipSink'].setVolume(vol)
        self.board.pirateSounds['CannonArea_ShipSink'].play()
        self.notify.debug('You sank ship number %d' % self.myNumber)

    def filterSinking(self, request, args):
        if request == 'Docked':
            return 'Docked'
        return self.defaultFilter(request, args)

    def exitSinking(self):
        pass

    def enterBoarded(self):
        self.cannonArea.shipReportIn(self.myNumber, self.howManyTimesHit, 'boarded')
        self.sailingSequence.pause()
        self.notify.debug('Ship number %d boarded you' % self.myNumber)

    def filterBoarded(self, request, args):
        if request == 'Docked':
            return 'Docked'
        return self.defaultFilter(request, args)

    def exitBoarded(self):
        pass

    def wake(self):
        self.myExplosionManager.wake()

    def sleep(self):
        self.myExplosionManager.sleep()
        i = ivalMgr.getInterval('sailingSequence%d' % self.myNumber)
        if i != None:
            ivalMgr.removeInterval(i)
        i = ivalMgr.getInterval('sinkingSequence%d' % self.myNumber)
        if i != None:
            ivalMgr.removeInterval(i)
        return

    def destroy(self):
        self.cleanup()

    def cleanup(self):
        self.myExplosionManager.destroy()
        i = ivalMgr.getInterval('sailingSequence%d' % self.myNumber)
        if i != None:
            ivalMgr.removeInterval(i)
        i = ivalMgr.getInterval('sinkingSequence%d' % self.myNumber)
        if i != None:
            ivalMgr.removeInterval(i)
        FSM.cleanup(self)
        del self.sailingSequence
        del self.sinkingSequence
        del self.board
        del self.cannonArea
        return