# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: LocalizerHelper.py
from direct.directnotify import DirectNotifyGlobal
import string, Localizer, LocalizerEnglish

class LocalizerHelper:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LocalizerHelper.LocalizerHelper')

    def __init__(self):
        self.allLocalStringNames = dir(LocalizerEnglish)
        self.allLocalStrings = {}
        for s in self.allLocalStringNames:
            exec('value = Localizer.' + s)
            if isinstance(value, list):
                for li in range(len(value)):
                    self.allLocalStrings['%s%d' % (s, li)] = [
                     '%s%d' % (s, li), value[li]]

            elif isinstance(value, str):
                if value.find('sounds') < 0 and value.find('dialogue') < 0 and s != '__doc__' and s != '__file__' and s != '__name__':
                    self.allLocalStrings[s] = [
                     s, value]
            else:
                print('Not list or string!')
                print(s)

        try:
            outfile = open('localizerExcell.txt', 'w')
        except IOError:
            print('There was an error (probably read-only) writing to localizerExcel.txt')
            return

        for s in list(self.allLocalStrings.values()):
            outfile.write(s[0] + '\t' + s[1] + '\n')

        outfile.write('\n\n')
        outfile.close()