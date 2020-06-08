# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: odeConstructs.py
import direct.directbase.DirectStart
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import Wait
from direct.interval.IntervalGlobal import Func
from direct.interval.IntervalGlobal import LerpFunc
import sgode.pyode
from direct.actor.Actor import Actor
BALL_CATEGORY = 1 << 0
FLIPPER_CATEGORY = 1 << 1
WALL_CATEGORY = 1 << 2
RUBBER_CATEGORY = 1 << 3
BUMPER_CATEGORY = 1 << 4
SLINGSHOT_CATEGORY = 1 << 5
PLUNGER_CATEGORY = 1 << 6
GROUND_CATEGORY = 1 << 7
TRIGGER_CATEGORY = 1 << 8
DROPPED_CATEGORY = 1 << 9
BUMPER_TRIGGER_CATEGORY = 1 << 10
categories = {BALL_CATEGORY: 'BALL_CATEGORY', FLIPPER_CATEGORY: 'FLIPPER_CATEGORY', WALL_CATEGORY: 'WALL_CATEGORY', RUBBER_CATEGORY: 'RUBBER_CATEGORY', BUMPER_CATEGORY: 'BUMPER_CATEGORY', SLINGSHOT_CATEGORY: 'SLINGSHOT_CATEGORY', PLUNGER_CATEGORY: 'PLUNGER_CATEGORY', GROUND_CATEGORY: 'GROUND_CATEGORY', TRIGGER_CATEGORY: 'TRIGGER_CATEGORY', DROPPED_CATEGORY: 'DROPPED_CATEGORY', BUMPER_TRIGGER_CATEGORY: 'BUMPER_TRIGGER_CATEGORY'}

class ODENodePath(NodePath):
    __module__ = __name__
    geomsToNodePaths = {}
    namesToGeoms = {}

    def __init__(self, geom, odeWorld, isStatic, name, zone=0, category=WALL_CATEGORY):
        baseName = name
        i = 2
        while name in ODENodePath.namesToGeoms:
            name = baseName + repr(i)
            i += 1

        NodePath.__init__(self, name)
        self.name = name
        self.geom = geom
        self.zone = zone
        self.active = True
        self.rubber = False
        self.trigger = False
        self.odeQuat = sgode.pyode.dRealArray(4)
        self.quat = Quat(0, 0, 0, 0)
        self.setCategory(category, True)
        ODENodePath.geomsToNodePaths[geom] = self
        ODENodePath.namesToGeoms[name] = geom
        self.isStatic = isStatic
        if not self.isStatic:
            self.body = sgode.pyode.dBodyCreate(odeWorld)
            sgode.pyode.dGeomSetBody(self.geom, self.body)
        sgode.pyode.dGeomSetCollideBits(self.geom, 0)
        self.bumperPower = 0

    def setActive(self, bool):
        self.active = bool

    def getBumperPower(self):
        return self.bumperPower

    def isRubber(self):
        return self.rubber

    def setRubber(self, rubber):
        self.rubber = rubber
        self.setCategory(self.category, True)

    def isTrigger(self):
        return self.trigger

    def setTrigger(self, trigger):
        self.trigger = trigger

    def setCategory(self, category, set_current):
        self.category = category
        if set_current:
            if self.rubber:
                sgode.pyode.dGeomSetCategoryBits(self.geom, RUBBER_CATEGORY)
            else:
                sgode.pyode.dGeomSetCategoryBits(self.geom, self.category)

    def getCategory(self):
        return self.category

    def drop(self):
        sgode.pyode.dGeomSetCategoryBits(self.geom, DROPPED_CATEGORY)

    def restore(self):
        if self.rubber:
            sgode.pyode.dGeomSetCategoryBits(self.geom, RUBBER_CATEGORY)
        else:
            sgode.pyode.dGeomSetCategoryBits(self.geom, self.category)

    def update(self):
        pos = Point3(*sgode.pyode.dVector3ToTuple(sgode.pyode.dGeomGetPosition(self.geom)))
        sgode.pyode.dGeomGetQuaternion(self.geom, self.odeQuat.cast())
        self.quat.setW(self.odeQuat[3])
        self.quat.setZ(self.odeQuat[2])
        self.quat.setY(self.odeQuat[1])
        self.quat.setX(self.odeQuat[0])
        self.setPos(render, pos)
        self.setQuat(render, self.quat)

    def setODEPos(self, x, y, z):
        if not self.isStatic:
            sgode.pyode.dBodySetPosition(self.body, x, y, z)
        else:
            sgode.pyode.dGeomSetPosition(self.geom, x, y, z)

    def setODEQuat(self, quat):
        odeQuat = sgode.pyode.dRealArray(4)
        odeQuat[0] = quat.getR()
        odeQuat[1] = quat.getI()
        odeQuat[2] = quat.getJ()
        odeQuat[3] = quat.getK()
        if not self.isStatic:
            sgode.pyode.dBodySetQuaternion(self.body, odeQuat.cast())
        else:
            sgode.pyode.dGeomSetQuaternion(self.geom, odeQuat.cast())

    def setODETransformFromNodePath(self):
        pos = self.getPos(render)
        quat = self.getQuat(render)
        self.setODEPos(pos.getX(), pos.getY(), pos.getZ())
        self.setODEQuat(quat)

    def wake(self):
        sgode.pyode.dGeomEnable(self.geom)
        sgode.pyode.dBodyEnable(self.body)
        self.show()

    def sleep(self):
        sgode.pyode.dGeomDisable(self.geom)
        sgode.pyode.dBodyDisable(self.body)
        self.hide()

    def destroy(self):
        if self.geom in ODENodePath.geomsToNodePaths:
            del ODENodePath.geomsToNodePaths[self.geom]
        if self.name in ODENodePath.namesToGeoms:
            del ODENodePath.namesToGeoms[self.name]
        if not self.isStatic:
            sgode.pyode.dBodyDestroy(self.body)
        sgode.pyode.dGeomDestroy(self.geom)
        self.removeNode()

    def getZone(self):
        return self.zone

    def getODEPos(self):
        return Vec3(*sgode.pyode.dVector3ToTuple(sgode.pyode.dBodyGetPosition(self.body)))

    def getODEVel(self):
        return Vec3(*sgode.pyode.dVector3ToTuple(sgode.pyode.dBodyGetLinearVel(self.body)))


class ODEBox(ODENodePath):
    __module__ = __name__

    def __init__(self, width, length, height, density, odeWorld, odeSpace, isStatic=False, name=None, normallySeen=False, zone=0):
        if name == None:
            name = 'ODEBox'
        ODENodePath.__init__(self, sgode.pyode.dCreateBox(odeSpace, width, length, height), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetBox(mass, density, width, length, height)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.normallySeen = normallySeen
        boxModel = loader.loadModelCopy('pinballbase/cube')
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        boxModel.setScale(width, length, height)
        boxModel.reparentTo(self)
        self.model = boxModel
        return


class ODESphere(ODENodePath):
    __module__ = __name__

    def __init__(self, radius, density, odeWorld, odeSpace, isStatic=False, name=None, normallySeen=False, zone=0):
        if name == None:
            name = 'ODESphere'
        ODENodePath.__init__(self, sgode.pyode.dCreateSphere(odeSpace, radius), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetSphere(mass, density, radius)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.normallySeen = normallySeen
        sphereModel = loader.loadModelCopy('pinballbase/sphere')
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        sphereModel.setScale(radius)
        sphereModel.reparentTo(self)
        self.model = sphereModel
        return


class ODECCylinder(ODENodePath):
    __module__ = __name__

    def __init__(self, radius, length, density, odeWorld, odeSpace, isStatic=False, name=None, normallySeen=False, zone=0):
        if name == None:
            name = 'ODECCylinder'
        ODENodePath.__init__(self, sgode.pyode.dCreateCCylinder(odeSpace, radius, length), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetCappedCylinder(mass, density, 3, radius, length)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.normallySeen = normallySeen
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        cylinderModel = loader.loadModelCopy('pinballbase/cylinder')
        cylinderModel.setScale(radius, radius, length)
        cylinderModel.reparentTo(self)
        topCapModel = loader.loadModelCopy('pinballbase/cap')
        topCapModel.setScale(radius)
        topCapModel.setZ(length / 2.0)
        topCapModel.reparentTo(self)
        bottomCapModel = loader.loadModelCopy('pinballbase/cap')
        bottomCapModel.setP(180)
        bottomCapModel.setScale(radius)
        bottomCapModel.setZ(-length / 2.0)
        bottomCapModel.reparentTo(self)
        self.model = cylinderModel
        return


class ODEMesh(ODENodePath):
    __module__ = __name__

    def __init__(self, nodePath, density, odeWorld, odeSpace, isStatic=False, name=None, zone=0):
        if name == None:
            name = 'ODEMesh'
        triMeshData = sgode.pyode.dGeomTriMeshDataCreate()
        sgode.pyode.dGeomTriMeshDataBuildSimple(triMeshData, vertices, vertexCount, indices, indexCount)
        ODENodePath.__init__(self, sgode.pyode.dCreateTriMesh(odeSpace, triMeshData, None, None, None), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetSphere(mass, density, radius)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        sphereModel = loader.loadModelCopy('pinballbase/sphere')
        sphereModel.setScale(radius)
        sphereModel.reparentTo(self)
        return

    def fillVertsAndInds(self, nodePath, verts, inds):
        for i in range(nodePath.getNumNodes()):
            node = nodePath.getNode(i)
            if node is GeomNode:
                for j in range(node.getNumGeoms()):
                    indexOffset = len(verts)
                    geom = node.getGeom(i)
                    if geom is GeomTriStrip or geom is GeomTriFan:
                        pass
                    else:
                        print("can't handle", type(geom))


class Slingshot(NodePath):
    __module__ = __name__

    def __init__(self, length, velocity, density, odeWorld, odeSpace, width=0.4, height=1.0, name=None, zone=0, slingProperties=[VBase3(87, 0, 0), VBase3(0.2, 0, 0), VBase3(15, 9.6, 20)]):
        if name == None:
            name = 'Slingshot'
        NodePath.__init__(self, name)
        self.velocity = velocity
        self.name = name
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        self.slinging = False
        self.top = ODEBox(width, length * 0.5, height, density, odeWorld, odeSpace, isStatic=False, name=self.name + 'BaseLeft', zone=zone)
        self.top.setY(length * 0.25)
        self.top.setODETransformFromNodePath()
        self.top.reparentTo(self)
        self.top.setCategory(SLINGSHOT_CATEGORY, True)
        self.bottom = ODEBox(width, length * 0.5, height, density, odeWorld, odeSpace, isStatic=False, name=self.name + 'BaseRight', zone=zone)
        self.bottom.setY(-length * 0.25)
        self.bottom.setODETransformFromNodePath()
        self.bottom.reparentTo(self)
        self.bottom.setCategory(SLINGSHOT_CATEGORY, True)
        self.bottom.model.reparentTo(hidden)
        self.top.model.reparentTo(hidden)
        self.slingActor = Actor('pinballbase/Bumper', {'sling': 'pinballbase/Bumper'})
        self.slingActor.setHpr(slingProperties[0])
        self.slingActor.setPos(slingProperties[1])
        self.slingActor.setScale(slingProperties[2])
        self.slingActor.reparentTo(self)
        self.slingActor.setPlayRate(1.2, 'sling')
        self.slingTime = self.slingActor.getDuration('sling')
        self.hinge = sgode.pyode.dJointCreateHinge(odeWorld, None)
        sgode.pyode.dJointAttach(self.hinge, self.top.body, self.bottom.body)
        self.hingePos = Vec3(0.0, 0.0, 0.0)
        sgode.pyode.dJointSetHingeAxis(self.hinge, 0.0, 0.0, 1.0)
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamLoStop, 0.0)
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamHiStop, math.atan(0.5))
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamFMax, 80000.0)
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamFudgeFactor, 0.2)
        self.topAnchor = sgode.pyode.dBodyCreate(odeWorld)
        self.topPos = Vec3(0.0, length * 0.5, 0.0)
        self.bottomAnchor = sgode.pyode.dBodyCreate(odeWorld)
        self.bottomPos = Vec3(0.0, -length * 0.5, 0.0)
        self.topSlider = sgode.pyode.dJointCreateSlider(odeWorld, None)
        sgode.pyode.dJointAttach(self.topSlider, None, self.topAnchor)
        sgode.pyode.dJointSetSliderParam(self.topSlider, sgode.pyode.dParamLoStop, 0.0)
        sgode.pyode.dJointSetSliderParam(self.topSlider, sgode.pyode.dParamHiStop, 0.0)
        sgode.pyode.dJointSetSliderParam(self.topSlider, sgode.pyode.dParamBounce, 0.0)
        self.topSliderAxis = Vec3(0.0, -1.0, 0.0)
        self.bottomSlider = sgode.pyode.dJointCreateSlider(odeWorld, None)
        sgode.pyode.dJointAttach(self.bottomSlider, self.bottomAnchor, None)
        sgode.pyode.dJointSetSliderParam(self.bottomSlider, sgode.pyode.dParamLoStop, 0.0)
        sgode.pyode.dJointSetSliderParam(self.bottomSlider, sgode.pyode.dParamHiStop, 0.0)
        sgode.pyode.dJointSetSliderParam(self.bottomSlider, sgode.pyode.dParamBounce, 0.0)
        self.bottomSliderAxis = Vec3(0.0, 1.0, 0.0)
        self.topHinge = sgode.pyode.dJointCreateHinge(odeWorld, None)
        sgode.pyode.dJointAttach(self.topHinge, self.top.body, self.topAnchor)
        self.topHingePos = Vec3(0.0, length * 0.5, 0.0)
        sgode.pyode.dJointSetHingeAxis(self.topHinge, 0.0, 0.0, 1.0)
        self.bottomHinge = sgode.pyode.dJointCreateHinge(odeWorld, None)
        sgode.pyode.dJointAttach(self.bottomHinge, self.bottom.body, self.bottomAnchor)
        self.bottomHingePos = Vec3(0.0, -length * 0.5, 0.0)
        sgode.pyode.dJointSetHingeAxis(self.bottomHinge, 0.0, 0.0, 1.0)
        self.updateAfterTransformation()
        return

    def update(self):
        self.top.update()
        self.bottom.update()

    def updateAfterTransformation(self):
        self.top.setODETransformFromNodePath()
        self.bottom.setODETransformFromNodePath()
        mat = self.getMat(render)
        hingePos = mat.xformPoint(self.hingePos)
        topPos = mat.xformPoint(self.topPos)
        bottomPos = mat.xformPoint(self.bottomPos)
        topSliderAxis = mat.xformVec(self.topSliderAxis)
        bottomSliderAxis = mat.xformVec(self.bottomSliderAxis)
        topHingePos = mat.xformPoint(self.topHingePos)
        bottomHingePos = mat.xformPoint(self.bottomHingePos)
        sgode.pyode.dJointSetHingeAnchor(self.hinge, hingePos.getX(), hingePos.getY(), hingePos.getZ())
        sgode.pyode.dBodySetPosition(self.topAnchor, topPos.getX(), topPos.getY(), topPos.getZ())
        sgode.pyode.dBodySetPosition(self.bottomAnchor, bottomPos.getX(), bottomPos.getY(), bottomPos.getZ())
        sgode.pyode.dJointSetSliderAxis(self.topSlider, topSliderAxis.getX(), topSliderAxis.getY(), topSliderAxis.getZ())
        sgode.pyode.dJointSetSliderAxis(self.bottomSlider, bottomSliderAxis.getX(), bottomSliderAxis.getY(), bottomSliderAxis.getZ())
        sgode.pyode.dJointSetHingeAnchor(self.topHinge, topHingePos.getX(), topHingePos.getY(), topHingePos.getZ())
        sgode.pyode.dJointSetHingeAnchor(self.bottomHinge, bottomHingePos.getX(), bottomHingePos.getY(), bottomHingePos.getZ())

    def enableSlingshotForce(self):
        if not self.slinging:
            self.slinging = True
            self.slingActor.play('sling')
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamVel, self.velocity)

    def disableSlingshotForce(self):
        self.slinging = False
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamVel, -self.velocity)

    def destroy(self):
        self.top.destroy()
        self.bottom.destroy()
        self.slingActor.removeNode()
        self.removeNode()


class Plunger(NodePath):
    __module__ = __name__

    def __init__(self, velocity, fmax, density, odeWorld, odeSpace, timeToFullDepress=2.0, length=4.0, width=1.0, height=1.0, name=None, zone=0):
        if name == None:
            name = 'Plunger'
        NodePath.__init__(self, name)
        self.timeToFullDepress = timeToFullDepress
        self.setTag('selectLevel', name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        self.velocity = velocity
        self.fmax = fmax
        self.loStop = -length * 0.8
        self.hiStopInterval = LerpFunc(self.setHiStop, duration=timeToFullDepress, fromData=0.0, toData=self.loStop)
        self.plungerBack = False
        self.box = ODEBox(width, length, height, density, odeWorld, odeSpace, isStatic=False, name='PlungerBox', zone=zone)
        self.box.setY(-length * 0.5)
        self.box.setODETransformFromNodePath()
        self.box.reparentTo(self)
        self.box.setCategory(PLUNGER_CATEGORY, True)
        self.box.active = False
        self.slider = sgode.pyode.dJointCreateSlider(odeWorld, None)
        sgode.pyode.dJointAttach(self.slider, None, self.box.body)
        sgode.pyode.dJointSetSliderParam(self.slider, sgode.pyode.dParamLoStop, self.loStop)
        sgode.pyode.dJointSetSliderParam(self.slider, sgode.pyode.dParamHiStop, 0.0)
        sgode.pyode.dJointSetSliderParam(self.slider, sgode.pyode.dParamBounce, 0.0)
        sgode.pyode.dJointSetSliderParam(self.slider, sgode.pyode.dParamFMax, self.fmax)
        sgode.pyode.dJointSetSliderParam(self.slider, sgode.pyode.dParamFudgeFactor, 0.2)
        sgode.pyode.dJointSetSliderParam(self.slider, sgode.pyode.dParamVel, self.velocity)
        self.sliderAxis = Vec3(0.0, 1.0, 0.0)
        self.updateAfterTransformation()
        return

    def pullPlunger(self):
        if not self.plungerBack:
            self.plungerBack = True
            self.box.active = True
            self.hiStopInterval.start()

    def releasePlunger(self):
        self.hiStopInterval.finish()
        self.setHiStop(0.0)
        self.plungerBack = False

    def setHiStop(self, value):
        sgode.pyode.dJointSetSliderParam(self.slider, sgode.pyode.dParamHiStop, value)

    def update(self):
        self.box.update()

    def updateAfterTransformation(self):
        self.box.setODETransformFromNodePath()
        mat = self.getMat(render)
        sliderAxis = mat.xformVec(self.sliderAxis)
        sgode.pyode.dJointSetSliderAxis(self.slider, sliderAxis.getX(), sliderAxis.getY(), sliderAxis.getZ())

    def destroy(self):
        self.box.destroy()
        self.removeNode()


class ODEBall(ODENodePath):
    __module__ = __name__

    def __init__(self, radius, density, odeWorld, odeSpace, isStatic=False, name=None, normallySeen=False, zone=0, eggfile='pinballbase/ball'):
        if name == None:
            name = 'Ball'
        ODENodePath.__init__(self, sgode.pyode.dCreateSphere(odeSpace, radius), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetSphere(mass, density, radius)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.normallySeen = normallySeen
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        ballModel = loader.loadModelCopy(eggfile)
        ballModel.setScale(24 * radius)
        ballModel.reparentTo(self)
        self.model = ballModel
        self.active = False
        self.fakeBall = False
        self.setCategory(BALL_CATEGORY, True)
        sgode.pyode.dGeomSetCollideBits(self.geom, 4294967295 ^ DROPPED_CATEGORY)
        return

    def setActive(self, bool):
        self.active = bool


class ODEBumper(ODENodePath):
    __module__ = __name__

    def __init__(self, density, odeWorld, odeSpace, eggfile, isStatic=False, name=None, zone=0, bumperPower=20000, bumperDelay=0.02):
        if name == None:
            name = 'ODEBumper'
        ODENodePath.__init__(self, sgode.pyode.dCreateCCylinder(odeSpace, 1, 1), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetCappedCylinder(mass, density, 3, 1, 1)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.eggfile = eggfile
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        self.normallySeen = True
        bumperActor = Actor(eggfile, {'bump': eggfile})
        bumperActor.setScale(9.6)
        bumperActor.setPos(0, 0, -0.5)
        bumperActor.reparentTo(self)
        bumperActor.setPlayRate(1.5, 'bump')
        self.model = bumperActor
        self.bumperPower = bumperPower
        self.bumperDelay = bumperDelay
        self.justHit = False
        return

    def showODEModel(self):
        cylinderModel = loader.loadModelCopy('pinballbase/cylinder')
        cylinderModel.setScale(1, 1, 1)
        cylinderModel.reparentTo(self)
        topCapModel = loader.loadModelCopy('pinballbase/cap')
        topCapModel.setScale(1)
        topCapModel.setZ(1 / 2.0)
        topCapModel.reparentTo(self)
        bottomCapModel = loader.loadModelCopy('pinballbase/cap')
        bottomCapModel.setP(180)
        bottomCapModel.setScale(1)
        bottomCapModel.setZ(-1 / 2.0)
        bottomCapModel.reparentTo(self)
        self.othermodel = cylinderModel

    def gotHit(self, ball):
        if self.justHit:
            return False
        forceVec = Vec3(ball.getPos(render) - self.getPos(render))
        forceVec.setZ(0.0)
        forceVec.normalize()
        self.model.play('bump')
        forceVec *= self.bumperPower
        sgode.pyode.dBodyAddForce(ball.body, forceVec.getX(), forceVec.getY(), forceVec.getZ())
        self.justHit = True
        taskMgr.doMethodLater(self.bumperDelay, setattr, '%sdelayTimer' % self.name, [self, 'justHit', False])
        return True

    def getBumperPower(self):
        return self.bumperPower


class Gate(ODENodePath):
    __module__ = __name__

    def __init__(self, width, odeWorld, odeSpace, isStatic=False, name=None, normallySeen=False, zone=0):
        length = 0.4
        height = 2
        density = 5
        if name == None:
            name = 'ODEGate'
        ODENodePath.__init__(self, sgode.pyode.dCreateBox(odeSpace, width, length, height), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetBox(mass, density, width, length, height)
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.normallySeen = normallySeen
        boxModel = loader.loadModelCopy('pinballbase/cube')
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        boxModel.setScale(width, length, height)
        boxModel.reparentTo(self)
        self.model = boxModel
        return


class ODESpinner(ODENodePath):
    __module__ = __name__

    def __init__(self, dimensions, boxPos, boxHpr, density, hingePos, hingeAxis, frictionForce, odeWorld, odeSpace, name=None, isStatic=False, zone=0):
        self.boxModel = None
        self.hinge = None
        self.spinnerModel = None
        self.callbackFunction = None
        self.callbackArgs = None
        self.oldAngle = -0.1
        if name == None:
            name = 'ODESpinner'
        ODENodePath.__init__(self, sgode.pyode.dCreateBox(odeSpace, dimensions[0], dimensions[1], dimensions[2]), odeWorld, isStatic, name, zone)
        mass = sgode.pyode.dMassPtr()
        sgode.pyode.dMassSetBox(mass, density, dimensions[0], dimensions[1], dimensions[2])
        if not self.isStatic:
            sgode.pyode.dBodySetMass(self.body, mass)
        self.setTag('selectLevel', self.name)
        if base.direct:
            base.direct.selected.addTag('selectLevel')
        self.setPos(boxPos)
        self.setHpr(boxHpr)
        self.setODETransformFromNodePath()
        self.boxModel = loader.loadModelCopy('pinballbase/cube')
        self.boxModel.setScale(dimensions[0], dimensions[1], dimensions[2])
        self.boxModel.reparentTo(self)
        self.boxModel.hide()
        self.hinge = sgode.pyode.dJointCreateHinge(odeWorld, None)
        sgode.pyode.dJointAttach(self.hinge, self.body, None)
        sgode.pyode.dJointSetHingeAnchor(self.hinge, hingePos[0], hingePos[1], hingePos[2])
        sgode.pyode.dJointSetHingeAxis(self.hinge, hingeAxis[0], hingeAxis[1], hingeAxis[2])
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamVel, 0)
        sgode.pyode.dJointSetHingeParam(self.hinge, sgode.pyode.dParamFMax, frictionForce)
        self.setCategory(WALL_CATEGORY, True)
        return

    def loadModel(self, modelFile, relPos=Point3(0, 0, 0), relHpr=Point3(0, 0, 0), scale=1.0):
        self.spinnerModel = loader.loadModelCopy(modelFile)
        self.spinnerModel.setPos(relPos)
        self.spinnerModel.setHpr(relHpr)
        self.spinnerModel.setScale(scale)
        self.spinnerModel.reparentTo(self)

    def setCallback(self, callbackFunction, extraArgs):
        self.callbackFunction = callbackFunction
        self.callbackArgs = extraArgs

    def update(self):
        ODENodePath.update(self)
        if self.callbackFunction != None:
            angle = sgode.pyode.dJointGetHingeAngle(self.hinge)
            if abs(angle) > 0.523:
                if angle * self.oldAngle < 0:
                    self.oldAngle = angle
                    if self.callbackArgs != None:
                        self.callbackFunction(self.callbackArgs)
                    else:
                        self.callbackFunction()
        return

    def pause(self):
        sgode.pyode.dBodyDisable(self.body)
        sgode.pyode.dGeomDisable(self.geom)

    def resume(self):
        sgode.pyode.dBodyEnable(self.body)
        sgode.pyode.dGeomEnable(self.geom)

    def showBox(self):
        self.boxModel.show()

    def hideBox(self):
        self.boxModel.hide()