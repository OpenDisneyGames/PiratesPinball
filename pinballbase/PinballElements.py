# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: PinballElements.py
import math, time
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
import sgode.pyode
from pinballbase.odeConstructs import *
import Localizer

class PandaToMaya:
    __module__ = __name__

    def __init__(self, scaleFactor, posOffset, hprOffset):
        self.scaleFactor = scaleFactor
        self.posOffset = posOffset
        self.hprOffset = hprOffset

    def pandaToMaya(self, pos, hpr):
        x = pos[0] - self.posOffset[0]
        y = pos[1] - self.posOffset[1]
        z = pos[2] - self.posOffset[2]
        mayaPos = Vec3(float(x / self.scaleFactor), float(z / self.scaleFactor), -float(y / self.scaleFactor))
        mayaHpr = Vec3(float(hpr[0] - self.hprOffset[0]), float(hpr[1] - self.hprOffset[1]), float(hpr[2] - self.hprOffset[2]))
        print 'Begin Conversion'
        print 'Panda pos and hpr'
        print pos
        print hpr
        print 'Maya pos and hpr equivalents'
        print mayaPos
        print mayaHpr
        print 'Conversion Complete'


class BumpManager:
    __module__ = __name__
    BUMPLEFT = 100
    BUMPRIGHT = 101
    BUMPUP = 102
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.BumpManager')

    def __init__(self, board, limit=4, force=6000, timeToHealBump=2, flipperHeal=5):
        self.numBumps = 0
        self.board = board
        self.bumpLimit = limit
        self.bumpForce = force
        self.bumpEnabled = True
        self.timeToHealBump = timeToHealBump
        self.flipperHeal = flipperHeal
        self.tiltActive = False
        self.totalNumBumps = 0

    def wake(self):
        self.bumpEnabled = True
        self.tiltActive = False
        self.board.flippersEnabled = True
        self.totalNumBumps = 0

    def sleep(self):
        self.tiltActive = False
        self.board.flippersEnabled = True

    def destroy(self):
        del self.board

    def enable(self):
        self.bumpEnabled = True

    def disable(self):
        self.bumpEnabled = False

    def bump(self, force_id, balls=None):
        if not self.bumpEnabled:
            return
        if self.numBumps >= self.bumpLimit:
            self.tilt()
            return
        self.disable()
        self.totalNumBumps += 1
        self.numBumps += 1
        xForce = 0
        yForce = 0
        cameraMovement = Sequence(name='tiltCameraMovement')
        camPos = camera.getPos()
        camHpr = camera.getHpr()
        camera1stMove = []
        if force_id == self.BUMPUP:
            camera1stMove.append(camera.posInterval(0.05, Point3(camPos[0], camPos[1] - 0.15, camPos[2])))
            camera1stMove.append(camera.hprInterval(0.05, Point3(camHpr[0], camHpr[1] - 0.15, camHpr[2])))
            yForce = self.bumpForce
        elif force_id == self.BUMPLEFT:
            camera1stMove.append(camera.posInterval(0.05, Point3(camPos[0] + 0.15, camPos[1], camPos[2])))
            camera1stMove.append(camera.hprInterval(0.05, Point3(camHpr[0] - 0.15, camHpr[1], camHpr[2])))
            xForce = -self.bumpForce
        elif force_id == self.BUMPRIGHT:
            camera1stMove.append(camera.posInterval(0.05, Point3(camPos[0] - 0.15, camPos[1], camPos[2])))
            camera1stMove.append(camera.hprInterval(0.05, Point3(camHpr[0] + 0.15, camHpr[1], camHpr[2])))
            xForce = self.bumpForce
        cameraMovement.append(Parallel(*camera1stMove))
        camera2ndMove = []
        camera2ndMove.append(camera.posInterval(0.05, Point3(camPos[0], camPos[1], camPos[2])))
        camera2ndMove.append(camera.hprInterval(0.05, Point3(camHpr[0], camHpr[1], camHpr[2])))
        cameraMovement.append(Parallel(*camera2ndMove))
        cameraMovement.append(Func(self.enable))
        cameraMovement.start()
        self.board.pbTaskMgr.doMethodLater(self.timeToHealBump, self.subtractBump, 'subtractbump%d' % self.totalNumBumps)
        if balls != None:
            for b in balls:
                if b.isMovable():
                    b.addForce(xForce, yForce, 0)

        for b in self.board.balls:
            if b.active:
                sgode.pyode.dBodyAddForce(b.body, xForce, yForce, 0)

        return

    def tilt(self):
        self.notify.debug('tilt: tilt occurred')
        self.board.display.show(Localizer.pTilt, alert=True)
        self.board.tiltSound.play()

    def unTilt(self):
        self.tiltActive = False
        self.board.flippersEnabled = True
        self.notify.debug('flippersEnabled')

    def subtractBump(self, taskInstance=None):
        self.numBumps -= 1
        self.notify.debug('subtractBump: decrementing the bump count')


class PolyExplore:
    __module__ = __name__

    def __init__(self, nodePath):
        from direct.tkwidgets.SceneGraphExplorer import SceneGraphExplorerItem

        class CustomSceneGraphExplorerItem(SceneGraphExplorerItem):
            __module__ = __name__

            def getPolyCountString(self):
                return 'polys:%d' % self.getPolyCount(self.nodePath)

            def getPolyCount(self, nodePath):
                if not hasattr(self, 'polyCache'):
                    self.polyCache = {}
                polyCount = 0
                for i in range(nodePath.getNumNodes()):
                    node = nodePath.getNode(i)
                    if node.isGeomNode():
                        for j in range(node.getNumGeoms()):
                            geom = node.getGeom(j)
                            exploded = geom.explode()
                            polyCount += exploded.getNumVertices() / 3

                for child in nodePath.getChildrenAsList():
                    if not self.polyCache.has_key(child):
                        self.polyCache[child] = self.getPolyCount(child)
                    polyCount += self.polyCache[child]

                return polyCount

            def getBoundsString(self):
                try:
                    return 'radius:%.2f' % self.nodePath.node().getBound().getRadius()
                except:
                    return self.nodePath.node().getBound().getType().getName()

            def GetText(self):
                type = self.nodePath.node().getType().getName()
                name = self.nodePath.getName()
                return type + '  ' + name + ' ' + self.getBoundsString() + ' ' + self.getPolyCountString()

            def GetSubList(self):
                sublist = []
                for nodePath in self.nodePath.getChildrenAsList():
                    item = CustomSceneGraphExplorerItem(nodePath)
                    sublist.append(item)

                return sublist

        self.sge = nodePath.explore()
        self.sge._treeItem.__class__ = CustomSceneGraphExplorerItem
        self.sge.update(fUseCachedChildren=False)


class LostBallManager:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.LostBallManager')

    def __init__(self, board, mermaid=False):
        self.board = board
        self.mermaid = mermaid
        self.velTolerance = 0.8
        self.sleeping = False
        self.active = True
        self.tutorialMode = False

    def gameStarted(self):
        self.board.pbTaskMgr.doMethodLater(1, self.checkForLostBalls, 'checkforlostballs')

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False

    def gameOver(self):
        pass

    def dontWorry(self):
        self.active = False

    def worry(self):
        self.active = True
        self.board.pbTaskMgr.doMethodLater(1, self.checkForLostBalls, 'checkforlostballs')

    def startTutorial(self):
        self.tutorialMode = True

    def stopTutorial(self):
        self.tutorialMode = False
        self.board.pbTaskMgr.doMethodLater(1, self.checkForLostBalls, 'checkforlostballs')

    def checkForLostBalls(self, inactiveCounter=0, launchLaneCounter=0, stillCounter=0):
        if self.board.gameOver or self.sleeping or not self.active or self.tutorialMode:
            return
        if self.mermaid:
            self.checkForLostBallsMermaid(inactiveCounter, launchLaneCounter, stillCounter)
            return
        if not self.board.launchLaneEmpty:
            launchLaneCounter += 1
            if launchLaneCounter == 25:
                self.board.pullPlunger()
            if launchLaneCounter == 27:
                self.board.releasePlunger()
            if launchLaneCounter > 30:
                self.board.gateIn(0, [])
        else:
            launchLaneCounter = 0
        if self.board.ballsOnTable <= 0:
            if inactiveCounter == 6:
                self.board.display.show(Localizer.pLooking)
            if inactiveCounter > 12:
                inactiveCounter = 0
                self.autoFindBall()
                return
            else:
                inactiveCounter += 1
        else:
            inactiveCounter = 0
        allFlippersDown = True
        for f in self.board.leftFlippers + self.board.rightFlippers:
            if self.board.flippersEnabled:
                if f.flipperOn:
                    allFlippersDown = False

        if allFlippersDown:
            allNotMoving = True
            for b in self.board.balls:
                if b.active:
                    vel = b.getODEVel()
                    if abs(vel[0]) > self.velTolerance or abs(vel[1]) > self.velTolerance or abs(vel[2]) > self.velTolerance:
                        allNotMoving = False

            if allNotMoving and launchLaneCounter == 0:
                if stillCounter == 6:
                    self.board.display.show(Localizer.pLooking)
                if stillCounter > 12:
                    stillCounter = 0
                    self.autoFindBall()
                    return
                else:
                    stillCounter += 1
            else:
                stillCounter = 0
        self.board.pbTaskMgr.doMethodLater(1, self.checkForLostBalls, 'checkforlostballs', [inactiveCounter, launchLaneCounter, stillCounter])

    def autoFindBall(self):
        print ''
        print '------------------------------ Auto-finding ball --------------------------------'
        print ''
        for b in self.board.balls:
            self.board.deactivateBall(-1, b)

        self.board.ballsOnTable = 0
        self.board.gateIn(0, [])
        newPos = self.board.refPoints[('Zone%dStart' % self.board.currentZone)].getPos()
        self.board.dropBall(False, bx=newPos[0], by=newPos[1], bz=newPos[2])
        self.board.pbTaskMgr.doMethodLater(1, self.checkForLostBalls, 'checkforlostballs')

    def checkForLostBallsMermaid(self, inactiveCounter=0, launchLaneCounter=0, stillCounter=0):
        if not self.board.launchLaneEmpty:
            launchLaneCounter += 1
            if launchLaneCounter == 25:
                self.board.pullPlunger()
            if launchLaneCounter == 27:
                self.board.releasePlunger()
            if launchLaneCounter > 30:
                self.board.gateIn(0, [])
        else:
            launchLaneCounter = 0
        if self.board.ballMgr.numActiveBalls <= 0:
            if inactiveCounter == 6:
                self.board.display.show(Localizer.pLooking)
            if inactiveCounter > 12:
                inactiveCounter = 0
                self.autoFindBallMermaid()
                return
            else:
                inactiveCounter += 1
        else:
            inactiveCounter = 0
        allFlippersDown = True
        for f in self.board.leftFlippers + self.board.rightFlippers:
            if self.board.flippersEnabled:
                if f.flipperOn:
                    allFlippersDown = False

        if allFlippersDown:
            allNotMoving = True
            for b in self.board.ballMgr.balls:
                if b.isActive():
                    vel = b.getODEVel()
                    if abs(vel[0]) > self.velTolerance or abs(vel[1]) > self.velTolerance or abs(vel[2]) > self.velTolerance:
                        allNotMoving = False

            if allNotMoving and launchLaneCounter == 0:
                if stillCounter == 6:
                    self.board.display.show(Localizer.pLooking)
                if stillCounter > 12:
                    stillCounter = 0
                    self.autoFindBallMermaid()
                    return
                else:
                    stillCounter += 1
            else:
                stillCounter = 0
        self.board.pbTaskMgr.doMethodLater(1, self.checkForLostBalls, 'checkforlostballs', [inactiveCounter, launchLaneCounter, stillCounter])

    def autoFindBallMermaid(self):
        print ''
        print '------------------------------ Auto-finding ball --------------------------------'
        print ''
        self.board.ballMgr.deactivateAll(forceLocked=True)
        self.board.gateIn(0, [])
        newPos = self.board.refPoints[('Zone%dStart' % self.board.currentZone)].getPos()
        self.board.ballMgr.dropBall(False, ballPos=newPos)
        self.board.pbTaskMgr.doMethodLater(1, self.checkForLostBalls, 'checkforlostballs')


class PinballDelayedCallManager:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.PinballDelayedCallManager')

    def __init__(self):
        self.wake()

    def wake(self):
        self.delayedMethods = []
        self.pauseTime = None
        taskMgr.add(self.stepTask, 'PinballDelayedCallManager')
        return

    def sleep(self):
        self.destroy()

    def destroy(self):
        taskMgr.remove('PinballDelayedCallManager')
        while self.delayedMethods != []:
            item = self.delayedMethods.pop()
            del item

    def isMethodRunning(self, methodName):
        for item in self.delayedMethods:
            if item[2] == methodName:
                return True

        return False

    def doMethodLater(self, delay, callable, name, args=[]):
        returnValue = 0
        if isinstance(delay, int):
            delay = float(delay)
        if not isinstance(delay, float):
            self.notify.error('doMethodLater: delay specified is neither an int or a float for method named %s' % name)
        for item in self.delayedMethods:
            if item[2] == name:
                self.delayedMethods.remove(item)
                returnValue = 1
                self.notify.warning('doMethodLater: callable with name %s was overwritten with newer call' % name)

        if not isinstance(args, list):
            args = [
             args]
        targetTime = ClockObject.getGlobalClock().getRealTime() + delay
        self.delayedMethods.append((targetTime, callable, name, args))
        return returnValue

    def removeDelayedMethod(self, name):
        retValue = False
        for item in self.delayedMethods:
            if item[2] == name:
                self.delayedMethods.remove(item)
                retValue = True

        return retValue

    def pause(self):
        if self.pauseTime == None:
            taskMgr.remove('PinballDelayedCallManager')
            self.pauseTime = ClockObject.getGlobalClock().getRealTime()
            self.notify.debug('pause: pause occured at %f' % self.pauseTime)
        else:
            self.notify.warning('pause: already paused prior to pause call')
        return

    def resume(self):
        if self.pauseTime != None:
            pauseDuration = ClockObject.getGlobalClock().getRealTime() - self.pauseTime
            self.notify.debug('resume: pause duration of %f being added to all method delays' % pauseDuration)
            for i in range(len(self.delayedMethods)):
                currentDelayMethodTuple = self.delayedMethods.pop()
                newDelayMethodTuple = (currentDelayMethodTuple[0] + pauseDuration, currentDelayMethodTuple[1], currentDelayMethodTuple[2], currentDelayMethodTuple[3])
                self.delayedMethods.insert(0, newDelayMethodTuple)

            self.pauseTime = None
            taskMgr.add(self.stepTask, 'PinballDelayedCallManager')
        else:
            self.notify.warning('resume: attempted to resume an unpaused manager.')
        return

    def stepTask(self, task):
        if len(self.delayedMethods):
            currentTime = ClockObject.getGlobalClock().getRealTime()
            self.delayedMethods.sort()
            while len(self.delayedMethods) > 0 and self.delayedMethods[0][0] <= currentTime:
                (targetTime, callable, name, args) = self.delayedMethods.pop(0)
                callable(*args)

        return Task.cont


class DialogueManager:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.DialogueManager')

    def __init__(self, board, allDialogue):
        self.board = board
        self.allDialogue = allDialogue
        self.dialogueEnabled = True
        self.dialogueToBePlayed = []
        self.dialogueCurrentlyPlaying = None
        self.lastSoundTime = 0.0
        return

    def enable(self):
        self.dialogueEnabled = True

    def disable(self):
        self.dialogueEnabled = False

    def enabled(self):
        return self.dialogueEnabled

    def changeZone(self):
        self.notify.debug('Changing zones, kill all dialogue from the old zone and clear the queue.')
        self.notify.debug(self.dialogueToBePlayed)
        self.dialogueToBePlayed = []
        if self.dialogueCurrentlyPlaying != None and self.dialogueCurrentlyPlaying.status() == AudioSound.PLAYING:
            self.dialogueCurrentlyPlaying.stop()
            self.dialogueCurrentlyPlaying = None
        return

    def pause(self):
        if self.dialogueCurrentlyPlaying != None and self.dialogueCurrentlyPlaying.status() == AudioSound.PLAYING:
            self.lastSoundTime = self.dialogueCurrentlyPlaying.getTime()
            self.dialogueCurrentlyPlaying.stop()
        return

    def resume(self):
        if self.lastSoundTime != 0.0:
            self.dialogueCurrentlyPlaying.setTime(self.lastSoundTime)
            self.dialogueCurrentlyPlaying.play()
            self.lastSoundTime = 0.0

    def destroy(self):
        if self.dialogueCurrentlyPlaying != None and self.dialogueCurrentlyPlaying.status() == AudioSound.PLAYING:
            self.dialogueCurrentlyPlaying.stop()
        del self.allDialogue
        del self.board
        self.board = None
        return

    def playDialogue(self, name, priority=False, callbackFunction=None, defaultTimeToCallback=1, args=None):
        if self.board == None:
            return
        if self.dialogueEnabled:
            if self.dialogueCurrentlyPlaying != None and self.dialogueCurrentlyPlaying.status() == AudioSound.PLAYING:
                if not priority:
                    self.dialogueToBePlayed.append([name, callbackFunction, defaultTimeToCallback, args])
                    return
                else:
                    self.notify.debug('Priority dialogue: %s' % name)
                    self.dialogueToBePlayed = []
                    self.dialogueCurrentlyPlaying.stop()
            self.board.musicMgr.lowerPlayingVolume()
            self.dialogueCurrentlyPlaying = self.allDialogue[name]
            self.dialogueCurrentlyPlaying.play()
            self.board.pbTaskMgr.doMethodLater(self.allDialogue[name].length(), self.dialogueDone, 'dialoguedonecallback%s' % name, [callbackFunction, args])
        elif callbackFunction != None and callable(callbackFunction):
            if args == None:
                self.board.pbTaskMgr.doMethodLater(defaultTimeToCallback, callbackFunction, 'dialoguecallback%s' % callbackFunction)
            else:
                self.board.pbTaskMgr.doMethodLater(defaultTimeToCallback, callbackFunction, 'dialoguecallback%s' % callbackFunction, args)
        return

    def dialogueDone(self, callbackFunction, args):
        self.dialogueCurrentlyPlaying = None
        self.board.musicMgr.restorePlayingVolume()
        if callbackFunction != None and callable(callbackFunction):
            if args == None:
                callbackFunction()
            else:
                callbackFunction(args)
        if len(self.dialogueToBePlayed) > 0:
            nextDialogue = self.dialogueToBePlayed.pop(0)
            self.playDialogue(nextDialogue[0], False, nextDialogue[1], nextDialogue[2], nextDialogue[3])
        return


class MusicManager:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.MusicManager')

    def __init__(self, board, allMusic):
        self.board = board
        self.allMusic = allMusic
        self.musicEnabled = True
        self.currentMusic = None
        self.oldMusic = None
        self.musicVolume = 0.55
        self.volFadeInterval = None
        self.jingleSong = None
        self.jingleTimeStopped = 0
        self.jinglePlaying = False
        self.musicQueue = None
        self.musicThatWasPlaying = None
        self.musicTimeStopped = 0.0
        return

    def enable(self):
        self.musicEnabled = True
        if self.musicThatWasPlaying != None:
            self.playMusic(self.musicThatWasPlaying)
        return

    def disable(self):
        self.musicEnabled = False
        self.musicThatWasPlaying = self.stopMusic()

    def enabled(self):
        return self.musicEnabled

    def changeZone(self):
        pass

    def startTutorial(self):
        ivalMgr.finishIntervalsMatching('volFadeInterval')
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.volFadeInterval = Sequence(name='volFadeInterval')
            self.volFadeInterval.append(LerpFunctionInterval(self.changeMusicVolume, duration=0.5, fromData=self.musicVolume, toData=self.musicVolume / 2.0))
            self.volFadeInterval.start()

    def stopTutorial(self):
        ivalMgr.finishIntervalsMatching('volFadeInterval')
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.volFadeInterval = Sequence(name='volFadeInterval')
            self.volFadeInterval.append(LerpFunctionInterval(self.changeMusicVolume, duration=0.5, fromData=self.musicVolume / 2.0, toData=self.musicVolume))
            self.volFadeInterval.start()

    def stopJingle(self, musicContinue=False):
        self.jinglePlaying = False
        self.jingleSong = None
        if musicContinue:
            if self.musicQueue == None:
                if self.currentMusic != None:
                    self.allMusic[self.currentMusic].setLoop()
                    self.allMusic[self.currentMusic].setTime(self.musicTimeStopped)
                    self.allMusic[self.currentMusic].play()
                    self.musicTimeStopped = 0.0
            else:
                self.stopMusic(0)
                self.playMusic(self.musicQueue[0], self.musicQueue[1], self.musicQueue[2])
                self.musicQueue = None
        return

    def playJingle(self, jingle, musicContinue=False):
        if not self.allMusic.has_key(jingle):
            self.notify.warning(" playJingle: Looking to play %s, wasn't found in music list" % jingle)
            return
        self.jinglePlaying = True
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            if musicContinue:
                self.musicTimeStopped = self.allMusic[self.currentMusic].getTime()
                self.allMusic[self.currentMusic].stop()
            else:
                self.allMusic[self.currentMusic].stop()
        self.jingleSong = jingle
        self.allMusic[jingle].play()
        self.board.pbTaskMgr.doMethodLater(self.allMusic[jingle].length(), self.stopJingle, 'jingledonestop%s' % jingle, [musicContinue])

    def pauseMusicPlaying(self):
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.musicTimeStopped = self.allMusic[self.currentMusic].getTime()
            self.allMusic[self.currentMusic].stop()

    def resumeMusicPlaying(self):
        if self.musicTimeStopped != 0.0:
            self.allMusic[self.currentMusic].setTime(self.musicTimeStopped)
            self.allMusic[self.currentMusic].play()
            self.musicTimeStopped = 0.0

    def pause(self):
        ivalMgr.finishIntervalsMatching('volFadeInterval')
        if self.jingleSong != None and self.jinglePlaying:
            self.jingleTimeStopped = self.allMusic[self.jingleSong].getTime()
            self.allMusic[self.jingleSong].stop()
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.volFadeInterval = Sequence(name='volFadeInterval')
            self.volFadeInterval.append(LerpFunctionInterval(self.changeMusicVolume, duration=0.5, fromData=self.musicVolume, toData=0.0))
            self.volFadeInterval.append(Func(self.pauseMusicPlaying))
            self.volFadeInterval.start()
        return

    def resume(self):
        ivalMgr.finishIntervalsMatching('volFadeInterval')
        if self.jingleSong != None and self.jinglePlaying:
            self.allMusic[self.jingleSong].setTime(self.jingleTimeStopped)
            self.allMusic[self.jingleSong].play()
            self.jingleTimeStopped = 0.0
        if self.allMusic.has_key(self.currentMusic) and self.musicTimeStopped != 0.0 and not self.jinglePlaying:
            self.volFadeInterval = Sequence(name='volFadeInterval')
            self.volFadeInterval.append(Func(self.resumeMusicPlaying))
            self.volFadeInterval.append(LerpFunctionInterval(self.changeMusicVolume, duration=0.5, fromData=0.0, toData=self.musicVolume))
            self.volFadeInterval.start()
        return

    def destroy(self):
        i = ivalMgr.getInterval('jinglesequence')
        if i != None:
            ivalMgr.removeInterval(i)
        if self.jingleSong != None and self.jinglePlaying and self.allMusic.has_key(self.jingleSong):
            self.allMusic[self.jingleSong].stop()
        if self.volFadeInterval != None and not self.volFadeInterval.isStopped():
            self.volFadeInterval.finish()
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.allMusic[self.currentMusic].setLoop(False)
            self.allMusic[self.currentMusic].stop()
        if self.allMusic.has_key(self.oldMusic) and self.allMusic[self.oldMusic].status() == AudioSound.PLAYING:
            self.allMusic[self.oldMusic].setLoop(False)
            self.allMusic[self.oldMusic].stop()
        del self.allMusic
        del self.board
        return

    def changeMusicVolume(self, volDelta):
        if self.currentMusic == None:
            return
        self.allMusic[self.currentMusic].setVolume(volDelta)
        return

    def lowerPlayingVolume(self):
        if self.currentMusic == None:
            return
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.allMusic[self.currentMusic].setVolume(self.musicVolume / 2.0)
        return

    def restorePlayingVolume(self):
        if self.currentMusic == None:
            return
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.allMusic[self.currentMusic].setVolume(self.musicVolume)
        return

    def stopMusic(self, fadeTime=0.5):
        ivalMgr.finishIntervalsMatching('volFadeInterval')
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            self.volFadeInterval = Sequence(name='volFadeInterval')
            self.volFadeInterval.append(LerpFunctionInterval(self.changeMusicVolume, duration=fadeTime, fromData=self.musicVolume, toData=0.0))
            self.volFadeInterval.append(Func(self.allMusic[self.currentMusic].stop))
            self.volFadeInterval.start()
        musicThatWasPlaying = self.currentMusic
        self.currentMusic = None
        return musicThatWasPlaying

    def playMusic(self, name=None, fadeTime=0.7, pauseTime=0):
        if not self.musicEnabled:
            return
        if self.jinglePlaying:
            self.musicQueue = [
             name, fadeTime, pauseTime]
            self.notify.warning('playMusic: playMusic waiting on %s because jingle is still playing.' % name)
            return
        if name == None:
            return
        if self.currentMusic == name:
            return
        if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
            ivalMgr.finishIntervalsMatching('volFadeInterval')
            self.volFadeInterval = Sequence(name='volFadeInterval')
            self.volFadeInterval.append(LerpFunctionInterval(self.fadeVolume, duration=fadeTime, fromData=0.0, toData=self.musicVolume))
            self.volFadeInterval.append(Func(self.allMusic[self.currentMusic].stop))
            self.volFadeInterval.start()
            if self.allMusic.has_key(self.oldMusic) and self.allMusic[self.oldMusic].status() == AudioSound.PLAYING:
                self.allMusic[self.oldMusic].stop()
            self.oldMusic = self.currentMusic
            self.currentMusic = name
            self.allMusic[self.currentMusic].setVolume(0.0)
            self.allMusic[self.currentMusic].setLoop()
            self.allMusic[self.currentMusic].play()
        else:
            ivalMgr.finishIntervalsMatching('volFadeInterval')
            self.volFadeInterval = Sequence(name='volFadeInterval')
            self.volFadeInterval.append(LerpFunctionInterval(self.fadeVolume, duration=fadeTime, fromData=0.0, toData=self.musicVolume))
            self.volFadeInterval.start()
            if self.allMusic.has_key(self.currentMusic) and self.allMusic[self.currentMusic].status() == AudioSound.PLAYING:
                self.allMusic[self.currentMusic].stop()
            if self.allMusic.has_key(self.oldMusic) and self.allMusic[self.oldMusic].status() == AudioSound.PLAYING:
                self.allMusic[self.oldMusic].stop()
            self.oldMusic = self.currentMusic
            self.currentMusic = name
            self.allMusic[self.currentMusic].setVolume(0.0)
            self.allMusic[self.currentMusic].setLoop()
            self.allMusic[self.currentMusic].play()
        return

    def fadeVolume(self, volDelta):
        if self.currentMusic != None:
            self.allMusic[self.currentMusic].setVolume(volDelta)
        if self.oldMusic != None:
            self.allMusic[self.oldMusic].setVolume(self.musicVolume - volDelta)
        return


class Beacon:
    __module__ = __name__
    OFF = 0
    ON = 1
    BLINK = 2
    ONCE = 3
    NOB = 0
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.Beacon')

    def __init__(self, plane, offTextureName='', onTextureName='', rate=2):
        self.name = 'Beacon%d' % Beacon.NOB
        Beacon.NOB += 1
        self.rate = float(rate)
        self.plane = plane
        self.parent = self.plane.getParent()
        self.onTexture = []
        self.plane.setTransparency(1)
        self.plane.setBin('flat', 100)
        if offTextureName == '':
            self.offTexture = loader.loadTexture('pinballbase/blank.png')
        else:
            self.offTexture = loader.loadTexture(offTextureName)
        if onTextureName == '':
            onTextureName = []
            onTextureName.append(offTextureName[0:len(offTextureName) - 4] + 'Lit.png')
        if isinstance(onTextureName, str):
            onTextureName = [
             onTextureName]
        for i in range(0, len(onTextureName)):
            self.onTexture.append(loader.loadTexture(onTextureName[i]))

        self.wake()

    def vanish(self):
        self.plane.reparentTo(hidden)

    def appear(self):
        self.plane.reparentTo(self.parent)

    def wake(self):
        self.plane.reparentTo(self.parent)
        self.currentOnState = 0
        self.state = self.OFF
        self.plane.setTexture(self.offTexture, 1)
        self.blinkState = self.ON

    def sleep(self):
        self.plane.reparentTo(hidden)
        taskMgr.remove('revert')
        taskMgr.remove('blink')

    def destroy(self):
        self.plane.removeNode()
        del self.offTexture
        for t in self.onTexture:
            del t

        del self.onTexture
        taskMgr.remove('revert')
        taskMgr.remove('blink')

    def setState(self, newState, fake=False, onceTime=1):
        if fake:
            self.realState = self.state
        if newState == self.state:
            return
        self.state = newState
        if self.state == self.ON:
            self.plane.setTexture(self.onTexture[self.currentOnState], 1)
        elif self.state == self.OFF:
            self.plane.setTexture(self.offTexture, 1)
        elif self.state == self.BLINK:
            self.plane.setTexture(self.onTexture[self.currentOnState], 1)
            taskMgr.doMethodLater(1 / self.rate / 2, self.blink, 'blink')
        elif self.state == self.ONCE:
            self.realState = self.OFF
            self.plane.setTexture(self.onTexture[self.currentOnState], 1)
            self.revertTask = taskMgr.doMethodLater(onceTime, self.revert, 'revert')

    def setCurrentOnState(self, newOnState):
        if newOnState >= len(self.onTexture):
            self.notify.warning('setCurrentOnState: state %d is too high for this beacon' % newOnState)
            return
        if newOnState != self.currentOnState:
            self.currentOnState = newOnState
            if self.state == self.ON:
                self.plane.setTexture(self.onTexture[self.currentOnState], 1)

    def getCurrentOnState(self):
        return self.currentOnState

    def getState(self):
        return self.state

    def revert(self, taskInstance):
        self.setState(self.realState)

    def blink(self, taskInstance):
        if self.state == self.BLINK:
            taskMgr.doMethodLater(1 / self.rate / 2, self.blink, 'blink')
        else:
            self.blinkState = self.ON
            return
        if self.blinkState == self.ON:
            self.plane.setTexture(self.offTexture, 1)
            self.blinkState = self.OFF
            return
        if self.blinkState == self.OFF:
            self.plane.setTexture(self.onTexture[self.currentOnState], 1)
            self.blinkState = self.ON
            return


class ProxPoint(NodePath):
    __module__ = __name__

    def __init__(self, odeWorld, odeSpace, px, py, pz, radius, time, name, errand='', callMethodIn=None, callMethodOut=None, callMethodTimer=None, args=[], visible=False, zone=0, color=Vec4(1, 0, 1, 1), writeOut=True):
        NodePath.__init__(self, name)
        self.reparentTo(render)
        self.setPos(px, py, pz)
        self.xPos = px
        self.yPos = py
        self.zPos = pz
        self.tol = radius * radius
        self.holeTol = self.tol
        self.args = args
        self.outside = [
         True, True, True, True, True, True, True]
        self.activationTimers = []
        self.callMethodIn = callMethodIn
        self.callMethodOut = callMethodOut
        self.callMethodTimer = callMethodTimer
        self.time = time
        self.errand = errand
        self.hole = False
        self.active = True
        self.holeSeen = False
        self.zone = zone
        self.writeOut = writeOut
        self.pbTaskMgr = None
        if name.find('HOLE') > 0:
            self.hole = True
            self.holeTol = (radius + 1) * (radius + 1)
            self.holeParts = []
            self.makeHole(odeWorld, odeSpace, px, py, pz - 1.05, radius + 0.1, radius + 2, 1, 50, self.holeParts, [1, 1, 1, 1, 1, 1, 1, 1], myColor=Vec4(1, 1, 1, 1), tilt=0, normSeen=False, trans=1, numberOfSides=4)
            for object in self.holeParts:
                object.setODETransformFromNodePath()
                object.update()

        self.name = name
        if callMethodIn:
            self.callInName = callMethodIn.__name__
        else:
            self.callInName = ''
        if callMethodOut:
            self.callOutName = callMethodOut.__name__
        else:
            self.callOutName = ''
        if callMethodTimer:
            self.callTimerName = callMethodTimer.__name__
        else:
            self.callTimerName = ''
        self.sphereModel = loader.loadModelCopy('pinballbase/sphere')
        self.sphereModel.setName(self.name)
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        self.setScale(radius)
        self.setColor(color)
        self.setTransparency(1)
        self.setAlphaScale(0.3)
        self.sphereModel.reparentTo(self)
        self.setVisible(visible)
        return

    def setPBTaskMgr(self, pbTaskMgr):
        self.pbTaskMgr = pbTaskMgr

    def wake(self):
        self.show()

    def sleep(self):
        self.hide()
        while self.activationTimers != []:
            t = self.activationTimers.pop()
            del t

        if self.hole:
            for hp in self.holeParts:
                sgode.pyode.dGeomDisable(hp.geom)

    def destroy(self):
        del self.pbTaskMgr
        while self.activationTimers != []:
            t = self.activationTimers.pop()
            del t

        if self.hole:
            while self.holeParts != []:
                hp = self.holeParts.pop()
                hp.destroy()

    def makeHole(self, odeWorld, odeSpace, hx, hy, hz, innerRadius, outerRadius, depth, density, listToAppend, wallBooleans=[
 1, 1, 1, 1, 1, 1, 1, 1], myColor=Vec4(1, 1, 1, 1), tilt=0, normSeen=False, trans=1, numberOfSides=8):
        size = outerRadius - innerRadius
        radius = innerRadius + size / 2
        offX = hx
        offY = hy
        offZ = hz
        wallLength = math.sqrt(4 * (outerRadius * outerRadius / (math.cos(math.pi / numberOfSides) * math.cos(math.pi / numberOfSides)) - outerRadius * outerRadius))
        for i in range(0, numberOfSides):
            if wallBooleans[i]:
                boxPiece = ODEBox(wallLength, size, depth, density, odeWorld, odeSpace, isStatic=True, normallySeen=normSeen)
                boxPiece.setPos(radius * math.sin(i * (2 * math.pi / numberOfSides)) + offX, radius * math.cos(i * (2 * math.pi / numberOfSides)) + offY, offZ)
                boxPiece.setHpr((numberOfSides - i) * (360 / numberOfSides), tilt, 0)
                boxPiece.setColor(myColor)
                if trans != 1:
                    boxPiece.setTransparency(1)
                    boxPiece.setAlphaScale(trans)
                listToAppend.append(boxPiece)

    def setActive(self, act):
        self.active = act

    def getActive(self):
        return self.active

    def getZone(self):
        return self.zone

    def setVisible(self, vis):
        if vis:
            self.sphereModel.reparentTo(self)
        else:
            self.sphereModel.reparentTo(hidden)

    def toggleHoleVisibility(self):
        if not self.hole:
            return
        if self.holeSeen:
            self.holeSeen = False
            for object in self.holeParts:
                object.reparentTo(hidden)

        self.holeSeen = True
        for object in self.holeParts:
            object.reparentTo(render)

    def calcDistanceSquared(self, x1, y1, z1, x2, y2, z2):
        xd = x2 - x1
        yd = y2 - y1
        zd = z2 - z1
        return xd * xd + yd * yd + zd * zd

    def reset(self):
        self.outside = [
         True, True, True, True, True, True, True]

    def checkPoint(self, ballIndex, cPos, geom):
        if not self.writeOut:
            distance = self.calcDistanceSquared(self.getPos(render)[0], self.getPos(render)[1], self.getPos(render)[2], cPos[0], cPos[1], cPos[2])
        else:
            distance = (cPos[0] - self.xPos) * (cPos[0] - self.xPos) + (cPos[1] - self.yPos) * (cPos[1] - self.yPos) + (cPos[2] - self.zPos) * (cPos[2] - self.zPos)
        return_val = 0
        if self.outside[ballIndex] and distance <= self.tol:
            if self.callMethodTimer != None:
                self.pbTaskMgr.doMethodLater(self.time, self.callMethodTimer, '%s-%d-timer' % (self.name, ballIndex), [ballIndex, self.args])
            self.outside[ballIndex] = False
            if self.hole:
                sgode.pyode.dGeomSetCollideBits(geom, 4294967295 ^ GROUND_CATEGORY)
            if self.callMethodIn != None:
                self.callMethodIn(ballIndex, self.args)
            return_val = 1
        if not self.outside[ballIndex] and distance > self.holeTol:
            self.outside[ballIndex] = True
            if self.callMethodOut != None:
                self.callMethodOut(ballIndex, self.args)
            return_val = 2
        return return_val


class Trigger:
    __module__ = __name__

    def __init__(self, name, errand='', callMethodIn=None, args=[], triggerDelay=0.5):
        self.name = name
        self.callMethodIn = callMethodIn
        self.args = args
        self.beingHit = False
        self.errand = errand
        self.triggerDelay = triggerDelay
        if callMethodIn:
            self.callInName = callMethodIn.__name__
        else:
            self.callInName = ''

    def wake(self):
        self.beingHit = False

    def sleep(self):
        pass

    def destroy(self):
        del self.errand

    def gotHit(self, ball):
        if not self.beingHit:
            self.beingHit = True
            taskMgr.doMethodLater(self.triggerDelay, self.beingHitFalse, 'beinghitfalse')
            self.callMethodIn(ball, self.args)

    def getTriggerDelay(self):
        return self.triggerDelay

    def beingHitFalse(self, taskInstance):
        self.beingHit = False


class RefPoint(NodePath):
    __module__ = __name__

    def __init__(self, x, y, z, h, p, r, name, scale0=1, scale1=1, scale2=1, length=1, width=1, height=1, visible=False):
        NodePath.__init__(self, name)
        self.setPos(x, y, z)
        self.setHpr(h, p, r)
        self.setScale(scale0, scale1, scale2)
        self.model = loader.loadModelCopy('pinballbase/cube')
        self.setTag('selectLevel', name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        self.model.setScale(width, length, height)
        self.model.setColor(0, 1, 1, 1)
        self.model.reparentTo(self)
        if visible:
            self.reparentTo(render)
        else:
            self.reparentTo(hidden)

    def wake(self):
        pass

    def sleep(self):
        pass

    def destroy(self):
        self.removeNode()


class BillboardManager:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.BillboardManager')

    def __init__(self, name, howManyAtOnce, textureName, numberOfTextures, seconds, scale=1):
        self.myBillboards = []
        for i in range(howManyAtOnce):
            self.myBillboards.append([0, AnimatedBillboard(name, textureName, numberOfTextures, i, self.reportIn, seconds, scale)])
            self.myBillboards[i][1].reparentTo(render)

    def wake(self):
        for bb in self.myBillboards:
            bb[1].wake()

    def sleep(self):
        for bb in self.myBillboards:
            bb[1].sleep()

    def destroy(self):
        while self.myBillboards != []:
            mbp = self.myBillboards.pop()
            mbp[1].destroy()

    def startHere(self, pos):
        for i in self.myBillboards:
            if i[0] == 0:
                i[0] = 1
                i[1].go(pos)
                return True

        return False

    def reportIn(self, number):
        self.notify.debug('reportIn: Billboard number %d reporting done' % number)
        self.myBillboards[number][0] = 0


class AnimatedBillboard(NodePath):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.AnimatedBillboard')

    def __init__(self, name, textureName, numberOfTextures, number, doneMethod, seconds, scale):
        NodePath.__init__(self, name)
        self.doneMethod = doneMethod
        cm = CardMaker('animatedBillboardNode')
        cm.setFrame(-1, 1, -1, 1)
        self.billboardNode = NodePath(cm.generate())
        self.billboardNode.reparentTo(self)
        self.billboardNode.setTransparency(1)
        self.billboardNode.reparentTo(hidden)
        self.billboardNode.node().setAttrib(LightAttrib.makeAllOff())
        self.billboardNode.setScale(scale)
        self.billboardTextures = []
        self.billboardSequence = Sequence(name='billboardSequence%s%d' % (name, number))
        self.billboardSequence.append(Func(self.billboardNode.reparentTo, self))
        for i in range(1, numberOfTextures + 1):
            self.billboardTextures.append(loader.loadTexture('%s%d.png' % (textureName, i)))
            self.billboardSequence.append(Func(self.billboardNode.setTexture, self.billboardTextures[(i - 1)]))
            self.billboardSequence.append(Wait(float(seconds / numberOfTextures)))

        self.billboardSequence.append(Func(self.billboardNode.reparentTo, hidden))
        self.billboardSequence.append(Func(self.doneMethod, number))
        self.node().setEffect(BillboardEffect.makePointEye())

    def wake(self):
        pass

    def sleep(self):
        self.billboardNode.reparentTo(hidden)
        if self.billboardSequence.isPlaying():
            self.billboardSequence.finish()

    def destroy(self):
        self.billboardNode.removeNode()
        self.removeNode()
        if self.billboardSequence.isPlaying():
            self.billboardSequence.finish()
        while self.billboardTextures != []:
            t = self.billboardTextures.pop()
            del t

    def go(self, pos):
        self.setPos(pos)
        self.notify.debug('Playing billboard %s' % self.getName())
        self.billboardSequence.start()


class BallSaveManager:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.BallSaveManager')

    def __init__(self, ballSaveBeacon, timeToBlink=15, timeFromBlinkToEnd=5):
        self.myBeacon = ballSaveBeacon
        self.timeToBlink = timeToBlink
        self.timeFromBlinkToEnd = timeFromBlinkToEnd
        self.beaconInUse = False
        self.reset()
        self.ballSaveStateSequence = None
        return

    def wake(self):
        pass

    def sleep(self):
        i = ivalMgr.getInterval('ballSaveStateSequence')
        if i != None:
            ivalMgr.removeInterval(i)
        return

    def destroy(self):
        i = ivalMgr.getInterval('ballSaveStateSequence')
        if i != None:
            ivalMgr.removeInterval(i)
        del self.myBeacon
        return

    def reset(self):
        self.ballSaveStateSequence = None
        self.ballSaveState = 0
        self.startBallSave = False
        if not self.beaconInUse:
            self.myBeacon.setState(Beacon.OFF)
        return

    def setBeaconInUse(self, bool):
        self.beaconInUse = bool

    def startSaveState(self):
        self.ballSaveState = 1
        self.myBeacon.setState(Beacon.ON)
        self.startBallSave = True

    def gateIn(self):
        if self.startBallSave:
            self.startBallSave = False
            self.ballSaveStateSequence = Sequence(name='ballSaveStateSequence')
            self.ballSaveStateSequence.append(Wait(self.timeToBlink))
            self.ballSaveStateSequence.append(Func(self.resetBallSaveState))
            self.ballSaveStateSequence.start()

    def drainIn(self):
        if self.ballSaveState > 0:
            self.ballSaveState = 3

    def isSaved(self):
        if self.ballSaveState > 0:
            return True
        else:
            return False

    def resetBallSaveState(self, taskInstance=None):
        self.notify.debug('resetBallSaveState: resetballsave state %d ' % self.ballSaveState)
        if self.ballSaveState == 1:
            if not self.beaconInUse:
                self.myBeacon.setState(Beacon.BLINK)
            self.ballSaveState = 2
            self.ballSaveStateSequence = Sequence(name='ballSaveStateSequence')
            self.ballSaveStateSequence.append(Wait(self.timeFromBlinkToEnd))
            self.ballSaveStateSequence.append(Func(self.resetBallSaveState))
            self.ballSaveStateSequence.start()
        elif self.ballSaveState == 2:
            if not self.beaconInUse:
                self.myBeacon.setState(Beacon.OFF)
            self.ballSaveState = 0

    def pause(self):
        if self.ballSaveStateSequence != None:
            self.ballSaveStateSequence.pause()
        return

    def resume(self):
        if self.ballSaveStateSequence != None:
            self.ballSaveStateSequence.resume()
        return


class BonusManager:
    __module__ = __name__

    def __init__(self, board):
        self.board = board
        self.showingBonus = False
        self.bonusSequence = None
        self.finalBonusScore = 0
        self.timeBetweenMessages = 1
        return

    def wake(self):
        self.finalBonusScore = 0

    def sleep(self):
        if self.bonusSequence != None and self.bonusSequence.isPlaying():
            self.bonusSequence.finish()
        return

    def destroy(self):
        if self.bonusSequence != None and self.bonusSequence.isPlaying():
            self.bonusSequence.finish()
        return

    def newGameStarted(self):
        self.showingBonus = False
        if self.bonusSequence != None:
            self.bonusSequence.finish()
        return

    def showBonus(self, gameOver=False):
        self.showingBonus = True
        self.finalBonusScore = 0
        self.bonusSequence = Sequence(name='bonussequence')
        self.bonusSequence.append(Func(self.board.display.show, Localizer.pDisplayBonusStart, False, True))
        self.bonusSequence.append(Wait(self.timeBetweenMessages))
        for e in self.board.errands.values():
            bonusResult = e.getBonus()
            if bonusResult != None:
                if bonusResult[1] != 0:
                    if self.board.scoreWrite and self.board.scoreFile != None:
                        self.board.scoreFile.write('%s\t%d\t%d\t%s\t%d\t%d\n' % (self.board.BOARDNAME, bonusResult[1] * bonusResult[2], self.board.multiplier, 'bonus-%s' % bonusResult[0], self.board.myScore, int(time.time() - self.board.gameStartTime)))
                    self.bonusSequence.append(Func(self.board.display.unlockDisplay))
                    if Localizer.myLanguage == 'japanese':
                        self.bonusSequence.append(Func(self.board.display.show, '%s%s%dX%d%s%d' % (bonusResult[0], Localizer.japanSep, bonusResult[1], bonusResult[2], Localizer.japanSep, bonusResult[1] * bonusResult[2]), False, True))
                    else:
                        self.bonusSequence.append(Func(self.board.display.show, '%s | %d X %d | %d' % (bonusResult[0], bonusResult[1], bonusResult[2], bonusResult[1] * bonusResult[2]), False, True))
                    self.bonusSequence.append(Wait(self.timeBetweenMessages))
                    self.finalBonusScore = self.finalBonusScore + bonusResult[1] * bonusResult[2]

        self.bonusSequence.append(Func(self.board.display.unlockDisplay))
        if Localizer.myLanguage == 'japanese':
            self.bonusSequence.append(Func(self.board.display.show, '%s%s%d' % (Localizer.pDisplayTotalBonus, Localizer.japanSep, self.finalBonusScore)))
        else:
            self.bonusSequence.append(Func(self.board.display.show, '%s | %d' % (Localizer.pDisplayTotalBonus, self.finalBonusScore)))
        self.bonusSequence.append(Wait(self.timeBetweenMessages))
        if gameOver:
            self.bonusSequence.append(Func(self.board.updateScore, self.board.myScore + self.board.multiplier * self.finalBonusScore, 'bonus_gameover'))
        else:
            self.bonusSequence.append(Func(self.board.updateScore, self.board.multiplier * self.finalBonusScore, 'bonus'))
        if self.board.multiplier > 1:
            self.bonusSequence.append(Func(self.board.display.unlockDisplay))
            if Localizer.myLanguage == 'japanese':
                self.bonusSequence.append(Func(self.board.display.show, '%s%s%d X %d%s%d' % (Localizer.pDisplayMultiplier, Localizer.japanSep, self.board.multiplier, self.finalBonusScore, Localizer.japanSep, self.board.multiplier * self.finalBonusScore)))
            else:
                self.bonusSequence.append(Func(self.board.display.show, '%s | %d X %d | %d' % (Localizer.pDisplayMultiplier, self.board.multiplier, self.finalBonusScore, self.board.multiplier * self.finalBonusScore)))
            self.bonusSequence.append(Wait(self.timeBetweenMessages))
        self.bonusSequence.append(Func(self.board.display.unlockDisplay))
        if gameOver:
            self.bonusSequence.append(Func(self.board.display.show, Localizer.pGameOver))
            if self.board.fromPalace:
                self.board.sentScoreAlready = True
                messenger.send('reportPinballScore', [self.board.BOARDNAME, self.board.myScore + self.board.multiplier * self.finalBonusScore, self.board.display.playTimer.getTime()])
            if not self.board.fromPalace:
                messenger.send('reportPinballScore', [self.board.BOARDNAME, self.board.myScore + self.board.multiplier * self.finalBonusScore])
            self.board.updateScore(0, 'refresh')
        else:
            self.bonusSequence.append(Func(self.board.display.show, Localizer.pDisplayLaunch))
        self.bonusSequence.append(Wait(self.timeBetweenMessages))
        self.bonusSequence.append(Func(self.board.display.unlockDisplay))
        if gameOver:
            if not self.board.fromPalace:
                self.bonusSequence.append(Func(messenger.send, 'bonusDoneShowing'))
        self.bonusSequence.start()
        return


class PlayTimer:
    """
        Track how long the player is actually playing the game vs in menus or help
        screens.
        """
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PinballElements.PlayTimer')

    def __init__(self):
        self.runningTime = 0.0
        self.startTime = None
        return

    def playing(self):
        """
                Called when the player starts playing the game. Repeated calls have
                no effect.
                """
        self.notify.debug('PLAYING............................................PLAYING')
        if self.startTime == None:
            self.startTime = time.time()
        return

    def stop(self):
        """
                Called when the player stops playing the game.
                """
        self.notify.debug('STOPPED............................................STOPPED')
        if self.startTime != None:
            self.runningTime += time.time() - self.startTime
            self.startTime = None
        return

    def getTime(self):
        """
                Returns total time spent playing (in milliseconds) as an integer
                since the last reset. 
                """
        return_value = self.runningTime
        if self.startTime != None:
            return_value += time.time() - self.startTime
        self.notify.debug('getTime: %d secs............................................GET_TIME' % int(return_value))
        return int(return_value * 1000)

    def reset(self):
        """
                Reset running time. Stops playing mode.
                """
        self.notify.debug('RESET............................................RESET')
        self.startTime = None
        self.runningTime = 0.0
        return