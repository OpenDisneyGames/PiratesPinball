import _pyode

def _swig_setattr(self, class_type, name, value):
    if name == 'this':
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value, 'thisown'):
                self.__dict__['thisown'] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    self.__dict__[name] = value
    return


def _swig_getattr(self, class_type, name):
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError(name)
    return


import types
try:
    _object = object
    _newclass = 1
except AttributeError:

    class _object:
        __module__ = __name__


    _newclass = 0

del types
dSINGLE = _pyode.dSINGLE
EFFICIENT_ALIGNMENT = _pyode.EFFICIENT_ALIGNMENT
d_ERR_UNKNOWN = _pyode.d_ERR_UNKNOWN
d_ERR_IASSERT = _pyode.d_ERR_IASSERT
d_ERR_UASSERT = _pyode.d_ERR_UASSERT
d_ERR_LCP = _pyode.d_ERR_LCP
dJointTypeNone = _pyode.dJointTypeNone
dJointTypeBall = _pyode.dJointTypeBall
dJointTypeHinge = _pyode.dJointTypeHinge
dJointTypeSlider = _pyode.dJointTypeSlider
dJointTypeContact = _pyode.dJointTypeContact
dJointTypeUniversal = _pyode.dJointTypeUniversal
dJointTypeHinge2 = _pyode.dJointTypeHinge2
dJointTypeFixed = _pyode.dJointTypeFixed
dJointTypeNull = _pyode.dJointTypeNull
dJointTypeAMotor = _pyode.dJointTypeAMotor
dParamLoStop = _pyode.dParamLoStop
dParamHiStop = _pyode.dParamHiStop
dParamVel = _pyode.dParamVel
dParamFMax = _pyode.dParamFMax
dParamFudgeFactor = _pyode.dParamFudgeFactor
dParamBounce = _pyode.dParamBounce
dParamCFM = _pyode.dParamCFM
dParamStopERP = _pyode.dParamStopERP
dParamStopCFM = _pyode.dParamStopCFM
dParamSuspensionERP = _pyode.dParamSuspensionERP
dParamSuspensionCFM = _pyode.dParamSuspensionCFM
dParamLoStop2 = _pyode.dParamLoStop2
dParamHiStop2 = _pyode.dParamHiStop2
dParamVel2 = _pyode.dParamVel2
dParamFMax2 = _pyode.dParamFMax2
dParamFudgeFactor2 = _pyode.dParamFudgeFactor2
dParamBounce2 = _pyode.dParamBounce2
dParamCFM2 = _pyode.dParamCFM2
dParamStopERP2 = _pyode.dParamStopERP2
dParamStopCFM2 = _pyode.dParamStopCFM2
dParamSuspensionERP2 = _pyode.dParamSuspensionERP2
dParamSuspensionCFM2 = _pyode.dParamSuspensionCFM2
dParamLoStop3 = _pyode.dParamLoStop3
dParamHiStop3 = _pyode.dParamHiStop3
dParamVel3 = _pyode.dParamVel3
dParamFMax3 = _pyode.dParamFMax3
dParamFudgeFactor3 = _pyode.dParamFudgeFactor3
dParamBounce3 = _pyode.dParamBounce3
dParamCFM3 = _pyode.dParamCFM3
dParamStopERP3 = _pyode.dParamStopERP3
dParamStopCFM3 = _pyode.dParamStopCFM3
dParamSuspensionERP3 = _pyode.dParamSuspensionERP3
dParamSuspensionCFM3 = _pyode.dParamSuspensionCFM3
dParamGroup = _pyode.dParamGroup
dAMotorUser = _pyode.dAMotorUser
dAMotorEuler = _pyode.dAMotorEuler

class dJointFeedback(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dJointFeedback, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dJointFeedback, name)

    def __repr__(self):
        return '<C dJointFeedback instance at %s>' % (self.this,)

    __swig_setmethods__['f1'] = _pyode.dJointFeedback_f1_set
    __swig_getmethods__['f1'] = _pyode.dJointFeedback_f1_get
    if _newclass:
        f1 = property(_pyode.dJointFeedback_f1_get, _pyode.dJointFeedback_f1_set)
    __swig_setmethods__['t1'] = _pyode.dJointFeedback_t1_set
    __swig_getmethods__['t1'] = _pyode.dJointFeedback_t1_get
    if _newclass:
        t1 = property(_pyode.dJointFeedback_t1_get, _pyode.dJointFeedback_t1_set)
    __swig_setmethods__['f2'] = _pyode.dJointFeedback_f2_set
    __swig_getmethods__['f2'] = _pyode.dJointFeedback_f2_get
    if _newclass:
        f2 = property(_pyode.dJointFeedback_f2_get, _pyode.dJointFeedback_f2_set)
    __swig_setmethods__['t2'] = _pyode.dJointFeedback_t2_set
    __swig_getmethods__['t2'] = _pyode.dJointFeedback_t2_get
    if _newclass:
        t2 = property(_pyode.dJointFeedback_t2_get, _pyode.dJointFeedback_t2_set)

    def __init__(self, *args):
        _swig_setattr(self, dJointFeedback, 'this', _pyode.new_dJointFeedback(*args))
        _swig_setattr(self, dJointFeedback, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dJointFeedback):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class dJointFeedbackPtr(dJointFeedback):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dJointFeedback, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dJointFeedback, 'thisown', 0)
        _swig_setattr(self, dJointFeedback, self.__class__, dJointFeedback)


_pyode.dJointFeedback_swigregister(dJointFeedbackPtr)
dContactMu2 = _pyode.dContactMu2
dContactFDir1 = _pyode.dContactFDir1
dContactBounce = _pyode.dContactBounce
dContactSoftERP = _pyode.dContactSoftERP
dContactSoftCFM = _pyode.dContactSoftCFM
dContactMotion1 = _pyode.dContactMotion1
dContactMotion2 = _pyode.dContactMotion2
dContactSlip1 = _pyode.dContactSlip1
dContactSlip2 = _pyode.dContactSlip2
dContactApprox0 = _pyode.dContactApprox0
dContactApprox1_1 = _pyode.dContactApprox1_1
dContactApprox1_2 = _pyode.dContactApprox1_2
dContactApprox1 = _pyode.dContactApprox1

class dSurfaceParameters(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dSurfaceParameters, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dSurfaceParameters, name)

    def __repr__(self):
        return '<C dSurfaceParameters instance at %s>' % (self.this,)

    __swig_setmethods__['mode'] = _pyode.dSurfaceParameters_mode_set
    __swig_getmethods__['mode'] = _pyode.dSurfaceParameters_mode_get
    if _newclass:
        mode = property(_pyode.dSurfaceParameters_mode_get, _pyode.dSurfaceParameters_mode_set)
    __swig_setmethods__['mu'] = _pyode.dSurfaceParameters_mu_set
    __swig_getmethods__['mu'] = _pyode.dSurfaceParameters_mu_get
    if _newclass:
        mu = property(_pyode.dSurfaceParameters_mu_get, _pyode.dSurfaceParameters_mu_set)
    __swig_setmethods__['mu2'] = _pyode.dSurfaceParameters_mu2_set
    __swig_getmethods__['mu2'] = _pyode.dSurfaceParameters_mu2_get
    if _newclass:
        mu2 = property(_pyode.dSurfaceParameters_mu2_get, _pyode.dSurfaceParameters_mu2_set)
    __swig_setmethods__['bounce'] = _pyode.dSurfaceParameters_bounce_set
    __swig_getmethods__['bounce'] = _pyode.dSurfaceParameters_bounce_get
    if _newclass:
        bounce = property(_pyode.dSurfaceParameters_bounce_get, _pyode.dSurfaceParameters_bounce_set)
    __swig_setmethods__['bounce_vel'] = _pyode.dSurfaceParameters_bounce_vel_set
    __swig_getmethods__['bounce_vel'] = _pyode.dSurfaceParameters_bounce_vel_get
    if _newclass:
        bounce_vel = property(_pyode.dSurfaceParameters_bounce_vel_get, _pyode.dSurfaceParameters_bounce_vel_set)
    __swig_setmethods__['soft_erp'] = _pyode.dSurfaceParameters_soft_erp_set
    __swig_getmethods__['soft_erp'] = _pyode.dSurfaceParameters_soft_erp_get
    if _newclass:
        soft_erp = property(_pyode.dSurfaceParameters_soft_erp_get, _pyode.dSurfaceParameters_soft_erp_set)
    __swig_setmethods__['soft_cfm'] = _pyode.dSurfaceParameters_soft_cfm_set
    __swig_getmethods__['soft_cfm'] = _pyode.dSurfaceParameters_soft_cfm_get
    if _newclass:
        soft_cfm = property(_pyode.dSurfaceParameters_soft_cfm_get, _pyode.dSurfaceParameters_soft_cfm_set)
    __swig_setmethods__['motion1'] = _pyode.dSurfaceParameters_motion1_set
    __swig_getmethods__['motion1'] = _pyode.dSurfaceParameters_motion1_get
    if _newclass:
        motion1 = property(_pyode.dSurfaceParameters_motion1_get, _pyode.dSurfaceParameters_motion1_set)
    __swig_setmethods__['motion2'] = _pyode.dSurfaceParameters_motion2_set
    __swig_getmethods__['motion2'] = _pyode.dSurfaceParameters_motion2_get
    if _newclass:
        motion2 = property(_pyode.dSurfaceParameters_motion2_get, _pyode.dSurfaceParameters_motion2_set)
    __swig_setmethods__['slip1'] = _pyode.dSurfaceParameters_slip1_set
    __swig_getmethods__['slip1'] = _pyode.dSurfaceParameters_slip1_get
    if _newclass:
        slip1 = property(_pyode.dSurfaceParameters_slip1_get, _pyode.dSurfaceParameters_slip1_set)
    __swig_setmethods__['slip2'] = _pyode.dSurfaceParameters_slip2_set
    __swig_getmethods__['slip2'] = _pyode.dSurfaceParameters_slip2_get
    if _newclass:
        slip2 = property(_pyode.dSurfaceParameters_slip2_get, _pyode.dSurfaceParameters_slip2_set)

    def __init__(self, *args):
        _swig_setattr(self, dSurfaceParameters, 'this', _pyode.new_dSurfaceParameters(*args))
        _swig_setattr(self, dSurfaceParameters, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dSurfaceParameters):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class dSurfaceParametersPtr(dSurfaceParameters):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dSurfaceParameters, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dSurfaceParameters, 'thisown', 0)
        _swig_setattr(self, dSurfaceParameters, self.__class__, dSurfaceParameters)


_pyode.dSurfaceParameters_swigregister(dSurfaceParametersPtr)

class dContactGeom(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dContactGeom, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dContactGeom, name)

    def __repr__(self):
        return '<C dContactGeom instance at %s>' % (self.this,)

    __swig_setmethods__['pos'] = _pyode.dContactGeom_pos_set
    __swig_getmethods__['pos'] = _pyode.dContactGeom_pos_get
    if _newclass:
        pos = property(_pyode.dContactGeom_pos_get, _pyode.dContactGeom_pos_set)
    __swig_setmethods__['normal'] = _pyode.dContactGeom_normal_set
    __swig_getmethods__['normal'] = _pyode.dContactGeom_normal_get
    if _newclass:
        normal = property(_pyode.dContactGeom_normal_get, _pyode.dContactGeom_normal_set)
    __swig_setmethods__['depth'] = _pyode.dContactGeom_depth_set
    __swig_getmethods__['depth'] = _pyode.dContactGeom_depth_get
    if _newclass:
        depth = property(_pyode.dContactGeom_depth_get, _pyode.dContactGeom_depth_set)
    __swig_setmethods__['g1'] = _pyode.dContactGeom_g1_set
    __swig_getmethods__['g1'] = _pyode.dContactGeom_g1_get
    if _newclass:
        g1 = property(_pyode.dContactGeom_g1_get, _pyode.dContactGeom_g1_set)
    __swig_setmethods__['g2'] = _pyode.dContactGeom_g2_set
    __swig_getmethods__['g2'] = _pyode.dContactGeom_g2_get
    if _newclass:
        g2 = property(_pyode.dContactGeom_g2_get, _pyode.dContactGeom_g2_set)

    def __init__(self, *args):
        _swig_setattr(self, dContactGeom, 'this', _pyode.new_dContactGeom(*args))
        _swig_setattr(self, dContactGeom, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dContactGeom):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class dContactGeomPtr(dContactGeom):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dContactGeom, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dContactGeom, 'thisown', 0)
        _swig_setattr(self, dContactGeom, self.__class__, dContactGeom)


_pyode.dContactGeom_swigregister(dContactGeomPtr)

class dContact(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dContact, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dContact, name)

    def __repr__(self):
        return '<C dContact instance at %s>' % (self.this,)

    __swig_setmethods__['surface'] = _pyode.dContact_surface_set
    __swig_getmethods__['surface'] = _pyode.dContact_surface_get
    if _newclass:
        surface = property(_pyode.dContact_surface_get, _pyode.dContact_surface_set)
    __swig_setmethods__['geom'] = _pyode.dContact_geom_set
    __swig_getmethods__['geom'] = _pyode.dContact_geom_get
    if _newclass:
        geom = property(_pyode.dContact_geom_get, _pyode.dContact_geom_set)
    __swig_setmethods__['fdir1'] = _pyode.dContact_fdir1_set
    __swig_getmethods__['fdir1'] = _pyode.dContact_fdir1_get
    if _newclass:
        fdir1 = property(_pyode.dContact_fdir1_get, _pyode.dContact_fdir1_set)

    def __init__(self, *args):
        _swig_setattr(self, dContact, 'this', _pyode.new_dContact(*args))
        _swig_setattr(self, dContact, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dContact):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class dContactPtr(dContact):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dContact, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dContact, 'thisown', 0)
        _swig_setattr(self, dContact, self.__class__, dContact)


_pyode.dContact_swigregister(dContactPtr)
dMassSetZero = _pyode.dMassSetZero
dMassSetParameters = _pyode.dMassSetParameters
dMassSetSphere = _pyode.dMassSetSphere
dMassSetSphereTotal = _pyode.dMassSetSphereTotal
dMassSetCappedCylinder = _pyode.dMassSetCappedCylinder
dMassSetCappedCylinderTotal = _pyode.dMassSetCappedCylinderTotal
dMassSetCylinder = _pyode.dMassSetCylinder
dMassSetCylinderTotal = _pyode.dMassSetCylinderTotal
dMassSetBox = _pyode.dMassSetBox
dMassSetBoxTotal = _pyode.dMassSetBoxTotal
dMassAdjust = _pyode.dMassAdjust
dMassTranslate = _pyode.dMassTranslate
dMassRotate = _pyode.dMassRotate
dMassAdd = _pyode.dMassAdd

class dMass(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dMass, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dMass, name)

    def __repr__(self):
        return '<C dMass instance at %s>' % (self.this,)

    __swig_setmethods__['mass'] = _pyode.dMass_mass_set
    __swig_getmethods__['mass'] = _pyode.dMass_mass_get
    if _newclass:
        mass = property(_pyode.dMass_mass_get, _pyode.dMass_mass_set)
    __swig_setmethods__['c'] = _pyode.dMass_c_set
    __swig_getmethods__['c'] = _pyode.dMass_c_get
    if _newclass:
        c = property(_pyode.dMass_c_get, _pyode.dMass_c_set)
    __swig_setmethods__['I'] = _pyode.dMass_I_set
    __swig_getmethods__['I'] = _pyode.dMass_I_get
    if _newclass:
        I = property(_pyode.dMass_I_get, _pyode.dMass_I_set)

    def __init__(self, *args):
        _swig_setattr(self, dMass, 'this', _pyode.new_dMass(*args))
        _swig_setattr(self, dMass, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dMass):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class dMassPtr(dMass):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dMass, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dMass, 'thisown', 0)
        _swig_setattr(self, dMass, self.__class__, dMass)


_pyode.dMass_swigregister(dMassPtr)
dWorldCreate = _pyode.dWorldCreate
dWorldDestroy = _pyode.dWorldDestroy
dWorldSetGravity = _pyode.dWorldSetGravity
dWorldGetGravity = _pyode.dWorldGetGravity
dWorldSetERP = _pyode.dWorldSetERP
dWorldGetERP = _pyode.dWorldGetERP
dWorldSetCFM = _pyode.dWorldSetCFM
dWorldGetCFM = _pyode.dWorldGetCFM
dWorldStep = _pyode.dWorldStep
dWorldImpulseToForce = _pyode.dWorldImpulseToForce
dWorldQuickStep = _pyode.dWorldQuickStep
dWorldSetQuickStepNumIterations = _pyode.dWorldSetQuickStepNumIterations
dWorldGetQuickStepNumIterations = _pyode.dWorldGetQuickStepNumIterations
dWorldSetQuickStepW = _pyode.dWorldSetQuickStepW
dWorldGetQuickStepW = _pyode.dWorldGetQuickStepW
dWorldSetContactMaxCorrectingVel = _pyode.dWorldSetContactMaxCorrectingVel
dWorldGetContactMaxCorrectingVel = _pyode.dWorldGetContactMaxCorrectingVel
dWorldSetContactSurfaceLayer = _pyode.dWorldSetContactSurfaceLayer
dWorldGetContactSurfaceLayer = _pyode.dWorldGetContactSurfaceLayer
dWorldStepFast1 = _pyode.dWorldStepFast1
dWorldSetAutoEnableDepthSF1 = _pyode.dWorldSetAutoEnableDepthSF1
dWorldGetAutoEnableDepthSF1 = _pyode.dWorldGetAutoEnableDepthSF1
dWorldGetAutoDisableLinearThreshold = _pyode.dWorldGetAutoDisableLinearThreshold
dWorldSetAutoDisableLinearThreshold = _pyode.dWorldSetAutoDisableLinearThreshold
dWorldGetAutoDisableAngularThreshold = _pyode.dWorldGetAutoDisableAngularThreshold
dWorldSetAutoDisableAngularThreshold = _pyode.dWorldSetAutoDisableAngularThreshold
dWorldGetAutoDisableSteps = _pyode.dWorldGetAutoDisableSteps
dWorldSetAutoDisableSteps = _pyode.dWorldSetAutoDisableSteps
dWorldGetAutoDisableTime = _pyode.dWorldGetAutoDisableTime
dWorldSetAutoDisableTime = _pyode.dWorldSetAutoDisableTime
dWorldGetAutoDisableFlag = _pyode.dWorldGetAutoDisableFlag
dWorldSetAutoDisableFlag = _pyode.dWorldSetAutoDisableFlag
dBodyGetAutoDisableLinearThreshold = _pyode.dBodyGetAutoDisableLinearThreshold
dBodySetAutoDisableLinearThreshold = _pyode.dBodySetAutoDisableLinearThreshold
dBodyGetAutoDisableAngularThreshold = _pyode.dBodyGetAutoDisableAngularThreshold
dBodySetAutoDisableAngularThreshold = _pyode.dBodySetAutoDisableAngularThreshold
dBodyGetAutoDisableSteps = _pyode.dBodyGetAutoDisableSteps
dBodySetAutoDisableSteps = _pyode.dBodySetAutoDisableSteps
dBodyGetAutoDisableTime = _pyode.dBodyGetAutoDisableTime
dBodySetAutoDisableTime = _pyode.dBodySetAutoDisableTime
dBodyGetAutoDisableFlag = _pyode.dBodyGetAutoDisableFlag
dBodySetAutoDisableFlag = _pyode.dBodySetAutoDisableFlag
dBodySetAutoDisableDefaults = _pyode.dBodySetAutoDisableDefaults
dBodyCreate = _pyode.dBodyCreate
dBodyDestroy = _pyode.dBodyDestroy
dBodySetData = _pyode.dBodySetData
dBodyGetData = _pyode.dBodyGetData
dBodySetPosition = _pyode.dBodySetPosition
dBodySetRotation = _pyode.dBodySetRotation
dBodySetQuaternion = _pyode.dBodySetQuaternion
dBodySetLinearVel = _pyode.dBodySetLinearVel
dBodySetAngularVel = _pyode.dBodySetAngularVel
dBodyGetPosition = _pyode.dBodyGetPosition
dBodyGetRotation = _pyode.dBodyGetRotation
dBodyGetQuaternion = _pyode.dBodyGetQuaternion
dBodyGetLinearVel = _pyode.dBodyGetLinearVel
dBodyGetAngularVel = _pyode.dBodyGetAngularVel
dBodySetMass = _pyode.dBodySetMass
dBodyGetMass = _pyode.dBodyGetMass
dBodyAddForce = _pyode.dBodyAddForce
dBodyAddTorque = _pyode.dBodyAddTorque
dBodyAddRelForce = _pyode.dBodyAddRelForce
dBodyAddRelTorque = _pyode.dBodyAddRelTorque
dBodyAddForceAtPos = _pyode.dBodyAddForceAtPos
dBodyAddForceAtRelPos = _pyode.dBodyAddForceAtRelPos
dBodyAddRelForceAtPos = _pyode.dBodyAddRelForceAtPos
dBodyAddRelForceAtRelPos = _pyode.dBodyAddRelForceAtRelPos
dBodyGetForce = _pyode.dBodyGetForce
dBodyGetTorque = _pyode.dBodyGetTorque
dBodySetForce = _pyode.dBodySetForce
dBodySetTorque = _pyode.dBodySetTorque
dBodyGetRelPointPos = _pyode.dBodyGetRelPointPos
dBodyGetRelPointVel = _pyode.dBodyGetRelPointVel
dBodyGetPointVel = _pyode.dBodyGetPointVel
dBodyGetPosRelPoint = _pyode.dBodyGetPosRelPoint
dBodyVectorToWorld = _pyode.dBodyVectorToWorld
dBodyVectorFromWorld = _pyode.dBodyVectorFromWorld
dBodySetFiniteRotationMode = _pyode.dBodySetFiniteRotationMode
dBodySetFiniteRotationAxis = _pyode.dBodySetFiniteRotationAxis
dBodyGetFiniteRotationMode = _pyode.dBodyGetFiniteRotationMode
dBodyGetFiniteRotationAxis = _pyode.dBodyGetFiniteRotationAxis
dBodyGetNumJoints = _pyode.dBodyGetNumJoints
dBodyGetJoint = _pyode.dBodyGetJoint
dBodyEnable = _pyode.dBodyEnable
dBodyDisable = _pyode.dBodyDisable
dBodyIsEnabled = _pyode.dBodyIsEnabled
dBodySetGravityMode = _pyode.dBodySetGravityMode
dBodyGetGravityMode = _pyode.dBodyGetGravityMode
dJointCreateBall = _pyode.dJointCreateBall
dJointCreateHinge = _pyode.dJointCreateHinge
dJointCreateSlider = _pyode.dJointCreateSlider
dJointCreateContact = _pyode.dJointCreateContact
dJointCreateHinge2 = _pyode.dJointCreateHinge2
dJointCreateUniversal = _pyode.dJointCreateUniversal
dJointCreateFixed = _pyode.dJointCreateFixed
dJointCreateAMotor = _pyode.dJointCreateAMotor
dJointDestroy = _pyode.dJointDestroy
dJointGroupCreate = _pyode.dJointGroupCreate
dJointGroupDestroy = _pyode.dJointGroupDestroy
dJointGroupEmpty = _pyode.dJointGroupEmpty
dJointAttach = _pyode.dJointAttach
dJointSetData = _pyode.dJointSetData
dJointGetData = _pyode.dJointGetData
dJointGetType = _pyode.dJointGetType
dJointGetBody = _pyode.dJointGetBody
dJointSetFeedback = _pyode.dJointSetFeedback
dJointGetFeedback = _pyode.dJointGetFeedback
dJointSetBallAnchor = _pyode.dJointSetBallAnchor
dJointSetHingeAnchor = _pyode.dJointSetHingeAnchor
dJointSetHingeAxis = _pyode.dJointSetHingeAxis
dJointSetHingeParam = _pyode.dJointSetHingeParam
dJointAddHingeTorque = _pyode.dJointAddHingeTorque
dJointSetSliderAxis = _pyode.dJointSetSliderAxis
dJointSetSliderParam = _pyode.dJointSetSliderParam
dJointAddSliderForce = _pyode.dJointAddSliderForce
dJointSetHinge2Anchor = _pyode.dJointSetHinge2Anchor
dJointSetHinge2Axis1 = _pyode.dJointSetHinge2Axis1
dJointSetHinge2Axis2 = _pyode.dJointSetHinge2Axis2
dJointSetHinge2Param = _pyode.dJointSetHinge2Param
dJointAddHinge2Torques = _pyode.dJointAddHinge2Torques
dJointSetUniversalAnchor = _pyode.dJointSetUniversalAnchor
dJointSetUniversalAxis1 = _pyode.dJointSetUniversalAxis1
dJointSetUniversalAxis2 = _pyode.dJointSetUniversalAxis2
dJointSetUniversalParam = _pyode.dJointSetUniversalParam
dJointAddUniversalTorques = _pyode.dJointAddUniversalTorques
dJointSetFixed = _pyode.dJointSetFixed
dJointSetAMotorNumAxes = _pyode.dJointSetAMotorNumAxes
dJointSetAMotorAxis = _pyode.dJointSetAMotorAxis
dJointSetAMotorAngle = _pyode.dJointSetAMotorAngle
dJointSetAMotorParam = _pyode.dJointSetAMotorParam
dJointSetAMotorMode = _pyode.dJointSetAMotorMode
dJointAddAMotorTorques = _pyode.dJointAddAMotorTorques
dJointGetBallAnchor = _pyode.dJointGetBallAnchor
dJointGetBallAnchor2 = _pyode.dJointGetBallAnchor2
dJointGetHingeAnchor = _pyode.dJointGetHingeAnchor
dJointGetHingeAnchor2 = _pyode.dJointGetHingeAnchor2
dJointGetHingeAxis = _pyode.dJointGetHingeAxis
dJointGetHingeParam = _pyode.dJointGetHingeParam
dJointGetHingeAngle = _pyode.dJointGetHingeAngle
dJointGetHingeAngleRate = _pyode.dJointGetHingeAngleRate
dJointGetSliderPosition = _pyode.dJointGetSliderPosition
dJointGetSliderPositionRate = _pyode.dJointGetSliderPositionRate
dJointGetSliderAxis = _pyode.dJointGetSliderAxis
dJointGetSliderParam = _pyode.dJointGetSliderParam
dJointGetHinge2Anchor = _pyode.dJointGetHinge2Anchor
dJointGetHinge2Anchor2 = _pyode.dJointGetHinge2Anchor2
dJointGetHinge2Axis1 = _pyode.dJointGetHinge2Axis1
dJointGetHinge2Axis2 = _pyode.dJointGetHinge2Axis2
dJointGetHinge2Param = _pyode.dJointGetHinge2Param
dJointGetHinge2Angle1 = _pyode.dJointGetHinge2Angle1
dJointGetHinge2Angle1Rate = _pyode.dJointGetHinge2Angle1Rate
dJointGetHinge2Angle2Rate = _pyode.dJointGetHinge2Angle2Rate
dJointGetUniversalAnchor = _pyode.dJointGetUniversalAnchor
dJointGetUniversalAnchor2 = _pyode.dJointGetUniversalAnchor2
dJointGetUniversalAxis1 = _pyode.dJointGetUniversalAxis1
dJointGetUniversalAxis2 = _pyode.dJointGetUniversalAxis2
dJointGetUniversalParam = _pyode.dJointGetUniversalParam
dJointGetUniversalAngle1 = _pyode.dJointGetUniversalAngle1
dJointGetUniversalAngle2 = _pyode.dJointGetUniversalAngle2
dJointGetUniversalAngle1Rate = _pyode.dJointGetUniversalAngle1Rate
dJointGetUniversalAngle2Rate = _pyode.dJointGetUniversalAngle2Rate
dJointGetAMotorNumAxes = _pyode.dJointGetAMotorNumAxes
dJointGetAMotorAxis = _pyode.dJointGetAMotorAxis
dJointGetAMotorAxisRel = _pyode.dJointGetAMotorAxisRel
dJointGetAMotorAngle = _pyode.dJointGetAMotorAngle
dJointGetAMotorAngleRate = _pyode.dJointGetAMotorAngleRate
dJointGetAMotorParam = _pyode.dJointGetAMotorParam
dJointGetAMotorMode = _pyode.dJointGetAMotorMode
dAreConnected = _pyode.dAreConnected
dAreConnectedExcluding = _pyode.dAreConnectedExcluding
dSimpleSpaceCreate = _pyode.dSimpleSpaceCreate
dHashSpaceCreate = _pyode.dHashSpaceCreate
dQuadTreeSpaceCreate = _pyode.dQuadTreeSpaceCreate
dSpaceDestroy = _pyode.dSpaceDestroy
dHashSpaceSetLevels = _pyode.dHashSpaceSetLevels
dHashSpaceGetLevels = _pyode.dHashSpaceGetLevels
dSpaceSetCleanup = _pyode.dSpaceSetCleanup
dSpaceGetCleanup = _pyode.dSpaceGetCleanup
dSpaceAdd = _pyode.dSpaceAdd
dSpaceRemove = _pyode.dSpaceRemove
dSpaceQuery = _pyode.dSpaceQuery
dSpaceClean = _pyode.dSpaceClean
dSpaceGetNumGeoms = _pyode.dSpaceGetNumGeoms
dSpaceGetGeom = _pyode.dSpaceGetGeom
dGeomDestroy = _pyode.dGeomDestroy
dGeomSetData = _pyode.dGeomSetData
dGeomGetData = _pyode.dGeomGetData
dGeomSetBody = _pyode.dGeomSetBody
dGeomGetBody = _pyode.dGeomGetBody
dGeomSetPosition = _pyode.dGeomSetPosition
dGeomSetRotation = _pyode.dGeomSetRotation
dGeomSetQuaternion = _pyode.dGeomSetQuaternion
dGeomGetPosition = _pyode.dGeomGetPosition
dGeomGetRotation = _pyode.dGeomGetRotation
dGeomGetQuaternion = _pyode.dGeomGetQuaternion
dGeomGetAABB = _pyode.dGeomGetAABB
dGeomIsSpace = _pyode.dGeomIsSpace
dGeomGetSpace = _pyode.dGeomGetSpace
dGeomGetClass = _pyode.dGeomGetClass
dGeomSetCategoryBits = _pyode.dGeomSetCategoryBits
dGeomSetCollideBits = _pyode.dGeomSetCollideBits
dGeomGetCategoryBits = _pyode.dGeomGetCategoryBits
dGeomGetCollideBits = _pyode.dGeomGetCollideBits
dGeomEnable = _pyode.dGeomEnable
dGeomDisable = _pyode.dGeomDisable
dGeomIsEnabled = _pyode.dGeomIsEnabled
dCollide = _pyode.dCollide
dSpaceCollide = _pyode.dSpaceCollide
dSpaceCollide2 = _pyode.dSpaceCollide2
dMaxUserClasses = _pyode.dMaxUserClasses
dSphereClass = _pyode.dSphereClass
dBoxClass = _pyode.dBoxClass
dCCylinderClass = _pyode.dCCylinderClass
dCylinderClass = _pyode.dCylinderClass
dPlaneClass = _pyode.dPlaneClass
dRayClass = _pyode.dRayClass
dGeomTransformClass = _pyode.dGeomTransformClass
dTriMeshClass = _pyode.dTriMeshClass
dFirstSpaceClass = _pyode.dFirstSpaceClass
dSimpleSpaceClass = _pyode.dSimpleSpaceClass
dHashSpaceClass = _pyode.dHashSpaceClass
dQuadTreeSpaceClass = _pyode.dQuadTreeSpaceClass
dLastSpaceClass = _pyode.dLastSpaceClass
dFirstUserClass = _pyode.dFirstUserClass
dLastUserClass = _pyode.dLastUserClass
dGeomNumClasses = _pyode.dGeomNumClasses
dCreateSphere = _pyode.dCreateSphere
dGeomSphereSetRadius = _pyode.dGeomSphereSetRadius
dGeomSphereGetRadius = _pyode.dGeomSphereGetRadius
dGeomSpherePointDepth = _pyode.dGeomSpherePointDepth
dCreateBox = _pyode.dCreateBox
dGeomBoxSetLengths = _pyode.dGeomBoxSetLengths
dGeomBoxGetLengths = _pyode.dGeomBoxGetLengths
dGeomBoxPointDepth = _pyode.dGeomBoxPointDepth
dCreatePlane = _pyode.dCreatePlane
dGeomPlaneSetParams = _pyode.dGeomPlaneSetParams
dGeomPlaneGetParams = _pyode.dGeomPlaneGetParams
dGeomPlanePointDepth = _pyode.dGeomPlanePointDepth
dCreateCCylinder = _pyode.dCreateCCylinder
dGeomCCylinderSetParams = _pyode.dGeomCCylinderSetParams
dGeomCCylinderGetParams = _pyode.dGeomCCylinderGetParams
dGeomCCylinderPointDepth = _pyode.dGeomCCylinderPointDepth
dCreateRay = _pyode.dCreateRay
dGeomRaySetLength = _pyode.dGeomRaySetLength
dGeomRayGetLength = _pyode.dGeomRayGetLength
dGeomRaySet = _pyode.dGeomRaySet
dGeomRayGet = _pyode.dGeomRayGet
dGeomRaySetClosestHit = _pyode.dGeomRaySetClosestHit
dGeomRayGetClosestHit = _pyode.dGeomRayGetClosestHit
dCreateGeomTransform = _pyode.dCreateGeomTransform
dGeomTransformSetGeom = _pyode.dGeomTransformSetGeom
dGeomTransformGetGeom = _pyode.dGeomTransformGetGeom
dGeomTransformSetCleanup = _pyode.dGeomTransformSetCleanup
dGeomTransformGetCleanup = _pyode.dGeomTransformGetCleanup
dGeomTransformSetInfo = _pyode.dGeomTransformSetInfo
dGeomTransformGetInfo = _pyode.dGeomTransformGetInfo
dClosestLineSegmentPoints = _pyode.dClosestLineSegmentPoints
dBoxTouchesBox = _pyode.dBoxTouchesBox
dInfiniteAABB = _pyode.dInfiniteAABB
dCloseODE = _pyode.dCloseODE

class dGeomClass(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dGeomClass, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dGeomClass, name)

    def __repr__(self):
        return '<C dGeomClass instance at %s>' % (self.this,)

    __swig_setmethods__['bytes'] = _pyode.dGeomClass_bytes_set
    __swig_getmethods__['bytes'] = _pyode.dGeomClass_bytes_get
    if _newclass:
        bytes = property(_pyode.dGeomClass_bytes_get, _pyode.dGeomClass_bytes_set)
    __swig_setmethods__['collider'] = _pyode.dGeomClass_collider_set
    __swig_getmethods__['collider'] = _pyode.dGeomClass_collider_get
    if _newclass:
        collider = property(_pyode.dGeomClass_collider_get, _pyode.dGeomClass_collider_set)
    __swig_setmethods__['aabb'] = _pyode.dGeomClass_aabb_set
    __swig_getmethods__['aabb'] = _pyode.dGeomClass_aabb_get
    if _newclass:
        aabb = property(_pyode.dGeomClass_aabb_get, _pyode.dGeomClass_aabb_set)
    __swig_setmethods__['aabb_test'] = _pyode.dGeomClass_aabb_test_set
    __swig_getmethods__['aabb_test'] = _pyode.dGeomClass_aabb_test_get
    if _newclass:
        aabb_test = property(_pyode.dGeomClass_aabb_test_get, _pyode.dGeomClass_aabb_test_set)
    __swig_setmethods__['dtor'] = _pyode.dGeomClass_dtor_set
    __swig_getmethods__['dtor'] = _pyode.dGeomClass_dtor_get
    if _newclass:
        dtor = property(_pyode.dGeomClass_dtor_get, _pyode.dGeomClass_dtor_set)

    def __init__(self, *args):
        _swig_setattr(self, dGeomClass, 'this', _pyode.new_dGeomClass(*args))
        _swig_setattr(self, dGeomClass, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dGeomClass):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class dGeomClassPtr(dGeomClass):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dGeomClass, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dGeomClass, 'thisown', 0)
        _swig_setattr(self, dGeomClass, self.__class__, dGeomClass)


_pyode.dGeomClass_swigregister(dGeomClassPtr)
dCreateGeomClass = _pyode.dCreateGeomClass
dGeomGetClassData = _pyode.dGeomGetClassData
dCreateGeom = _pyode.dCreateGeom
dRealArrayGet = _pyode.dRealArrayGet
dRealArraySet = _pyode.dRealArraySet
dContactArrayGet = _pyode.dContactArrayGet
dContactArraySet = _pyode.dContactArraySet

class CollisionInfo(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CollisionInfo, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CollisionInfo, name)

    def __repr__(self):
        return '<C CollisionInfo instance at %s>' % (self.this,)

    __swig_setmethods__['geom1'] = _pyode.CollisionInfo_geom1_set
    __swig_getmethods__['geom1'] = _pyode.CollisionInfo_geom1_get
    if _newclass:
        geom1 = property(_pyode.CollisionInfo_geom1_get, _pyode.CollisionInfo_geom1_set)
    __swig_setmethods__['geom2'] = _pyode.CollisionInfo_geom2_set
    __swig_getmethods__['geom2'] = _pyode.CollisionInfo_geom2_get
    if _newclass:
        geom2 = property(_pyode.CollisionInfo_geom2_get, _pyode.CollisionInfo_geom2_set)
    __swig_setmethods__['numContacts'] = _pyode.CollisionInfo_numContacts_set
    __swig_getmethods__['numContacts'] = _pyode.CollisionInfo_numContacts_get
    if _newclass:
        numContacts = property(_pyode.CollisionInfo_numContacts_get, _pyode.CollisionInfo_numContacts_set)
    __swig_setmethods__['contacts'] = _pyode.CollisionInfo_contacts_set
    __swig_getmethods__['contacts'] = _pyode.CollisionInfo_contacts_get
    if _newclass:
        contacts = property(_pyode.CollisionInfo_contacts_get, _pyode.CollisionInfo_contacts_set)
    __swig_setmethods__['next'] = _pyode.CollisionInfo_next_set
    __swig_getmethods__['next'] = _pyode.CollisionInfo_next_get
    if _newclass:
        next = property(_pyode.CollisionInfo_next_get, _pyode.CollisionInfo_next_set)

    def __init__(self, *args):
        _swig_setattr(self, CollisionInfo, 'this', _pyode.new_CollisionInfo(*args))
        _swig_setattr(self, CollisionInfo, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_CollisionInfo):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class CollisionInfoPtr(CollisionInfo):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, CollisionInfo, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, CollisionInfo, 'thisown', 0)
        _swig_setattr(self, CollisionInfo, self.__class__, CollisionInfo)


_pyode.CollisionInfo_swigregister(CollisionInfoPtr)

class WorldInfo(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WorldInfo, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WorldInfo, name)

    def __repr__(self):
        return '<C WorldInfo instance at %s>' % (self.this,)

    __swig_setmethods__['world'] = _pyode.WorldInfo_world_set
    __swig_getmethods__['world'] = _pyode.WorldInfo_world_get
    if _newclass:
        world = property(_pyode.WorldInfo_world_get, _pyode.WorldInfo_world_set)
    __swig_setmethods__['space'] = _pyode.WorldInfo_space_set
    __swig_getmethods__['space'] = _pyode.WorldInfo_space_get
    if _newclass:
        space = property(_pyode.WorldInfo_space_get, _pyode.WorldInfo_space_set)
    __swig_setmethods__['contactGroup'] = _pyode.WorldInfo_contactGroup_set
    __swig_getmethods__['contactGroup'] = _pyode.WorldInfo_contactGroup_get
    if _newclass:
        contactGroup = property(_pyode.WorldInfo_contactGroup_get, _pyode.WorldInfo_contactGroup_set)
    __swig_setmethods__['defaultContactParams'] = _pyode.WorldInfo_defaultContactParams_set
    __swig_getmethods__['defaultContactParams'] = _pyode.WorldInfo_defaultContactParams_get
    if _newclass:
        defaultContactParams = property(_pyode.WorldInfo_defaultContactParams_get, _pyode.WorldInfo_defaultContactParams_set)
    __swig_setmethods__['contactParams'] = _pyode.WorldInfo_contactParams_set
    __swig_getmethods__['contactParams'] = _pyode.WorldInfo_contactParams_get
    if _newclass:
        contactParams = property(_pyode.WorldInfo_contactParams_get, _pyode.WorldInfo_contactParams_set)
    __swig_setmethods__['collisionInfoList'] = _pyode.WorldInfo_collisionInfoList_set
    __swig_getmethods__['collisionInfoList'] = _pyode.WorldInfo_collisionInfoList_get
    if _newclass:
        collisionInfoList = property(_pyode.WorldInfo_collisionInfoList_get, _pyode.WorldInfo_collisionInfoList_set)

    def __init__(self, *args):
        _swig_setattr(self, WorldInfo, 'this', _pyode.new_WorldInfo(*args))
        _swig_setattr(self, WorldInfo, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_WorldInfo):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass


class WorldInfoPtr(WorldInfo):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, WorldInfo, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, WorldInfo, 'thisown', 0)
        _swig_setattr(self, WorldInfo, self.__class__, WorldInfo)


_pyode.WorldInfo_swigregister(WorldInfoPtr)
clearCollisionInfoList = _pyode.clearCollisionInfoList
newCollisionInfo = _pyode.newCollisionInfo
appendCollisionInfo = _pyode.appendCollisionInfo
getCollisionInfoFromPointer = _pyode.getCollisionInfoFromPointer

class dMassPtr(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dMassPtr, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dMassPtr, name)

    def __repr__(self):
        return '<C dMassPtr instance at %s>' % (self.this,)

    def __init__(self, *args):
        _swig_setattr(self, dMassPtr, 'this', _pyode.new_dMassPtr(*args))
        _swig_setattr(self, dMassPtr, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dMassPtr):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass

    def assign(*args):
        return _pyode.dMassPtr_assign(*args)

    def value(*args):
        return _pyode.dMassPtr_value(*args)

    def cast(*args):
        return _pyode.dMassPtr_cast(*args)

    __swig_getmethods__['frompointer'] = lambda x: _pyode.dMassPtr_frompointer
    if _newclass:
        frompointer = staticmethod(_pyode.dMassPtr_frompointer)


class dMassPtrPtr(dMassPtr):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dMassPtr, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dMassPtr, 'thisown', 0)
        _swig_setattr(self, dMassPtr, self.__class__, dMassPtr)


_pyode.dMassPtr_swigregister(dMassPtrPtr)
dMassPtr_frompointer = _pyode.dMassPtr_frompointer

class dRealArray(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dRealArray, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dRealArray, name)

    def __repr__(self):
        return '<C dRealArray instance at %s>' % (self.this,)

    def __init__(self, *args):
        _swig_setattr(self, dRealArray, 'this', _pyode.new_dRealArray(*args))
        _swig_setattr(self, dRealArray, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dRealArray):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass

    def __getitem__(*args):
        return _pyode.dRealArray___getitem__(*args)

    def __setitem__(*args):
        return _pyode.dRealArray___setitem__(*args)

    def cast(*args):
        return _pyode.dRealArray_cast(*args)

    __swig_getmethods__['frompointer'] = lambda x: _pyode.dRealArray_frompointer
    if _newclass:
        frompointer = staticmethod(_pyode.dRealArray_frompointer)


class dRealArrayPtr(dRealArray):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dRealArray, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dRealArray, 'thisown', 0)
        _swig_setattr(self, dRealArray, self.__class__, dRealArray)


_pyode.dRealArray_swigregister(dRealArrayPtr)
dRealArray_frompointer = _pyode.dRealArray_frompointer

class dContactArray(_object):
    __module__ = __name__
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, dContactArray, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, dContactArray, name)

    def __repr__(self):
        return '<C dContactArray instance at %s>' % (self.this,)

    def __init__(self, *args):
        _swig_setattr(self, dContactArray, 'this', _pyode.new_dContactArray(*args))
        _swig_setattr(self, dContactArray, 'thisown', 1)

    def __del__(self, destroy=_pyode.delete_dContactArray):
        try:
            if self.thisown:
                destroy(self)
        except:
            pass

    def __getitem__(*args):
        return _pyode.dContactArray___getitem__(*args)

    def __setitem__(*args):
        return _pyode.dContactArray___setitem__(*args)

    def cast(*args):
        return _pyode.dContactArray_cast(*args)

    __swig_getmethods__['frompointer'] = lambda x: _pyode.dContactArray_frompointer
    if _newclass:
        frompointer = staticmethod(_pyode.dContactArray_frompointer)


class dContactArrayPtr(dContactArray):
    __module__ = __name__

    def __init__(self, this):
        _swig_setattr(self, dContactArray, 'this', this)
        if not hasattr(self, 'thisown'):
            _swig_setattr(self, dContactArray, 'thisown', 0)
        _swig_setattr(self, dContactArray, self.__class__, dContactArray)


_pyode.dContactArray_swigregister(dContactArrayPtr)
dContactArray_frompointer = _pyode.dContactArray_frompointer

def dVector3ToTuple(dVector3):
    x = dRealArrayGet(dVector3, 0)
    y = dRealArrayGet(dVector3, 1)
    z = dRealArrayGet(dVector3, 2)
    return (x, y, z)


def dVector4ToTuple(dVector4):
    x = dRealArrayGet(dVector4, 0)
    y = dRealArrayGet(dVector4, 1)
    z = dRealArrayGet(dVector4, 2)
    w = dRealArrayGet(dVector4, 3)
    return (x, y, z, w)


def dMatrix4ToTuple(dMatrix4):
    m00 = dRealArrayGet(dMatrix4, 0)
    m01 = dRealArrayGet(dMatrix4, 1)
    m02 = dRealArrayGet(dMatrix4, 2)
    m03 = dRealArrayGet(dMatrix4, 3)
    m10 = dRealArrayGet(dMatrix4, 4)
    m11 = dRealArrayGet(dMatrix4, 5)
    m12 = dRealArrayGet(dMatrix4, 6)
    m13 = dRealArrayGet(dMatrix4, 7)
    m20 = dRealArrayGet(dMatrix4, 8)
    m21 = dRealArrayGet(dMatrix4, 9)
    m22 = dRealArrayGet(dMatrix4, 10)
    m23 = dRealArrayGet(dMatrix4, 11)
    m30 = dRealArrayGet(dMatrix4, 12)
    m31 = dRealArrayGet(dMatrix4, 13)
    m32 = dRealArrayGet(dMatrix4, 14)
    m33 = dRealArrayGet(dMatrix4, 15)
    return (m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33)


def dQuaternionToTuple(dQuaternion):
    x = dRealArrayGet(dQuaternion, 0)
    y = dRealArrayGet(dQuaternion, 1)
    z = dRealArrayGet(dQuaternion, 2)
    w = dRealArrayGet(dQuaternion, 3)
    return (x, y, z, w)


nearCallback = _pyode.nearCallback