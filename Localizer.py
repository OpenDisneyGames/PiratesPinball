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

print('Localizer: Running in language: %s' % language)
_languageModule = 'Localizer' + string.capitalize(language)
exec('from ' + _languageModule + ' import *')
try:
    exec('import ' + _languageModule)
    exec('reload( %s )' % _languageModule)
    exec('from ' + _languageModule + ' import *')
except:
    print("Couldn't reload language module.")

if checkLanguage:
    l = {}
    g = {}
    englishModule = __import__('LocalizerEnglish', g, l)
    foreignModule = __import__(_languageModule, g, l)
    for (key, val) in list(englishModule.__dict__.items()):
        if key not in foreignModule.__dict__:
            print('WARNING: Foreign module: %s missing key: %s' % (_languageModule, key))
            locals()[key] = val

    for key in list(foreignModule.__dict__.keys()):
        if key not in englishModule.__dict__:
            print('WARNING: Foreign module: %s extra key: %s' % (_languageModule, key))