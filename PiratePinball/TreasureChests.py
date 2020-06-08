from pinballbase.PinballErrand import PinballErrand
from .PirateDisplay import PirateDisplay
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pinballbase.PinballElements import *
import Localizer

class TreasureChests(PinballErrand):
    __module__ = __name__

    def __init__(self, board):
        PinballErrand.__init__(self, board)
        self.treasureState = [0, 0, 0, 0]
        self.myZone = 0
        self.chestMovement = None
        self.board.beacons['ChestBeacon4'] = Beacon(board.boatModel.find('**/baconplates:pPlane25'), 'piratepinball/art/main_ship/beacons/YellowLight.png')
        self.board.beacons['ChestBeacon3'] = Beacon(board.boatModel.find('**/baconplates:pPlane26'), 'piratepinball/art/main_ship/beacons/YellowLight.png')
        self.board.beacons['ChestBeacon2'] = Beacon(board.boatModel.find('**/baconplates:pPlane27'), 'piratepinball/art/main_ship/beacons/YellowLight.png')
        self.board.beacons['ChestBeacon1'] = Beacon(board.boatModel.find('**/baconplates:pPlane28'), 'piratepinball/art/main_ship/beacons/YellowLight.png')
        self.board.beacons['CaptainsRoomBeacon'] = Beacon(board.boatModel.find('**/pPlane38'), offTextureName='piratepinball/art/main_ship/beacons/redArrow.png')
        self.treasureLids = []
        self.treasureLids.append(board.boatModel.find('**/chest04Lid'))
        self.treasureLids.append(board.boatModel.find('**/chest03Lid'))
        self.treasureLids.append(board.boatModel.find('**/chest02Lid'))
        self.treasureLids.append(board.boatModel.find('**/chest01Lid'))
        return

    def finishSetup(self):
        pass

    def wake(self):
        pass

    def sleep(self):
        if self.chestMovement != None and self.chestMovement.isPlaying():
            self.chestMovement.finish()
        return

    def changeToZone(self, zoneNumber):
        pass

    def reset(self, time=3):
        self.captainsRoom = 0
        self.board.beacons['CaptainsRoomBeacon'].setState(Beacon.OFF)
        self.chestMovement = Sequence(name='chestMovement')
        chestMove = []
        for i in range(0, 4):
            self.treasureState[i] = 0
            self.board.beacons[('ChestBeacon%d' % (i + 1))].setState(Beacon.OFF)
            chestMove.append(self.treasureLids[i].hprInterval(time, Point3(0.0, 0.0, 0.0), blendType='easeOut'))

        self.chestMovement.append(Parallel(*chestMove))
        self.chestMovement.start()

    def refresh(self, time=3):
        self.chestMovement = Sequence(name='chestMovement')
        chestMove = []
        count = 0
        for i in range(0, 4):
            if self.treasureState[i] == 1:
                count = count + 1
                self.board.beacons[('ChestBeacon%d' % (i + 1))].setState(Beacon.ON)
                chestMove.append(self.treasureLids[i].hprInterval(time, Point3(0.0, 0.0, 57.0)))
            else:
                self.board.beacons[('ChestBeacon%d' % (i + 1))].setState(Beacon.OFF)
                chestMove.append(self.treasureLids[i].hprInterval(time, Point3(0.0, 0.0, 0.0)))

        self.chestMovement.append(Parallel(*chestMove))
        self.chestMovement.start()
        if count == 4:
            self.board.beacons['CaptainsRoomBeacon'].setState(Beacon.ON)
        else:
            self.board.beacons['CaptainsRoomBeacon'].setState(Beacon.OFF)

    def start(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def destroy(self):
        PinballErrand.destroy(self)

    def getStatus(self):
        if self.board.currentZone != self.myZone:
            return
        completed = 0
        for i in self.treasureState:
            completed = completed + i

        if completed == 4:
            return Localizer.ppTreasureChestsGoal3
        elif completed == 0:
            return Localizer.ppTreasureChestsGoal2
        else:
            return Localizer.ppTreasureChestsGoal1 % completed
        return

    def getName(self):
        return 'TreasureChests'

    def getBonus(self):
        return

    def captainsQuartersIn(self, ballIndex, args):
        if self.captainsRoom == 0:
            self.board.display.show(Localizer.ppTreasureChestsRoomFound)
            self.board.updateScore(self.board.pointValues['TreasureRoomEnterNotLit'], 'TreasureRoomEnterNotLit')
            self.board.pirateSounds['PiratePinball_Bell2'].play()
        else:
            self.board.musicMgr.playJingle('Music_Success2', musicContinue=True)
            self.board.dialogueMgr.playDialogue('TreasureChests')
            self.board.display.show(Localizer.ppTreasureChestsCaptainBonus)
            self.board.updateScore(self.board.pointValues['TreasureRoomEnterLit'], 'TreasureRoomEnterLit')
            self.board.pirateSounds['TreasureChests_CaptainsTreasure'].play()
            self.reset(time=2)

    def treasureChestHit(self, ball, args):
        if self.treasureState[(args[0] - 1)] == 0:
            self.treasureState[args[0] - 1] = 1
            self.board.dialogueMgr.playDialogue('Treasure')
            self.board.display.show(Localizer.ppTreasureChestsFoundTreasure)
            self.board.beacons[('ChestBeacon%d' % args[0])].setState(Beacon.ON)
            self.chestMovement = Sequence(name='chestMovement')
            self.chestMovement.append(self.treasureLids[(args[0] - 1)].hprInterval(0.5, Point3(0.0, 0.0, 57.0)))
            self.chestMovement.start()
            self.board.updateScore(self.board.pointValues['TreasureHit'], 'TreasureHit')
            self.board.pirateSounds['TreasureChests_HitTreasureChest'].play()
        elif self.captainsRoom == 1:
            self.board.display.show(Localizer.ppTreasureChestsAimMessage)
            self.board.updateScore(self.board.pointValues['TreasureHitNotLit'], 'TreasureHitNotLit')
            self.board.pirateSounds['TreasureChests_HitTreasureChest'].play()
            return
        else:
            self.board.display.show(Localizer.ppTreasureChestsOpenMessage)
            self.board.updateScore(self.board.pointValues['TreasureHitNotLit'], 'TreasureHitNotLit')
            self.board.pirateSounds['TreasureChests_HitTreasureChest'].play()
            return
        for g in self.treasureState:
            if g == 0:
                return

        self.board.display.show(Localizer.ppTreasureChestsAllChestsMessage)
        self.board.beacons['CaptainsRoomBeacon'].setState(Beacon.BLINK)
        self.board.dialogueMgr.playDialogue('GoldTaunt')
        self.board.pbTaskMgr.doMethodLater(1, self.board.dialogueMgr.playDialogue, 'understairsdialogue', ['UnderStairs'])
        self.board.updateScore(self.board.pointValues['AllFourChests'], 'AllFourChests')
        self.board.pirateSounds['TreasureChests_AllChests'].play()
        self.captainsRoom = 1