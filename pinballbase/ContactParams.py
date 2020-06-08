# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: ContactParams.py
import sgode.pyode
from pinballbase.odeConstructs import *

def getCategoryIndex(category):
    for i in range(32):
        if category & 1 << i > 0:
            return i

    return -1


def setupContactParams(worldInfo):
    worldInfo.defaultContactParams.surface.mode = sgode.pyode.dContactBounce
    worldInfo.defaultContactParams.surface.mu = 10.0
    worldInfo.defaultContactParams.surface.bounce = 0.1
    worldInfo.defaultContactParams.surface.bounce_vel = 0.1
    i = getCategoryIndex(FLIPPER_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 30.0
    contactParams.surface.bounce = 0.05
    contactParams.surface.bounce_vel = 0.1
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)
    i = getCategoryIndex(WALL_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 0.1
    contactParams.surface.bounce = 0.1
    contactParams.surface.bounce_vel = 0.1
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)
    i = getCategoryIndex(GROUND_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 0.1
    contactParams.surface.bounce = 0
    contactParams.surface.bounce_vel = 0.1
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)
    i = getCategoryIndex(RUBBER_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 20.0
    contactParams.surface.bounce = 1.0
    contactParams.surface.bounce_vel = 0.01
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)
    i = getCategoryIndex(BUMPER_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 20.0
    contactParams.surface.bounce = 1.0
    contactParams.surface.bounce_vel = 0.01
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)
    i = getCategoryIndex(SLINGSHOT_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 30.0
    contactParams.surface.bounce = 0.05
    contactParams.surface.bounce_vel = 0.1
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)
    i = getCategoryIndex(TRIGGER_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 0.1
    contactParams.surface.bounce = 0.1
    contactParams.surface.bounce_vel = 0.1
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)
    i = getCategoryIndex(BUMPER_TRIGGER_CATEGORY)
    contactParams = sgode.pyode.dContactArrayGet(worldInfo.contactParams, i)
    contactParams.surface.mode = sgode.pyode.dContactBounce
    contactParams.surface.mu = 20.0
    contactParams.surface.bounce = 1.0
    contactParams.surface.bounce_vel = 0.01
    sgode.pyode.dContactArraySet(worldInfo.contactParams, i, contactParams)