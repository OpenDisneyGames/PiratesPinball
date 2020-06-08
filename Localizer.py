# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: Localizer.py
"""
This module determines what language to run the game in
and imports the appropriate language module.
Import this module, not the individual language modules
to use in the game.
"""
from pandac.PandaModules import *
import string
try:
    language = getConfigExpress().GetString('language', 'english')
    checkLanguage = getConfigExpress().GetBool('check-language', 1)
except:
    language = simbase.config.GetString('language', 'english')
    checkLanguage = simbase.config.GetBool('check-language', 1)

print 'Localizer: Running in language: %s' % language
_languageModule = 'Localizer' + string.capitalize(language)
exec 'from ' + _languageModule + ' import *'
try:
    exec 'import ' + _languageModule
    exec 'reload( %s )' % _languageModule
    exec 'from ' + _languageModule + ' import *'
except:
    print "Couldn't reload language module."

if checkLanguage:
    l = {}
    g = {}
    englishModule = __import__('LocalizerEnglish', g, l)
    foreignModule = __import__(_languageModule, g, l)
    for (key, val) in englishModule.__dict__.items():
        if not foreignModule.__dict__.has_key(key):
            print 'WARNING: Foreign module: %s missing key: %s' % (_languageModule, key)
            locals()[key] = val

    for key in foreignModule.__dict__.keys():
        if not englishModule.__dict__.has_key(key):
            print 'WARNING: Foreign module: %s extra key: %s' % (_languageModule, key)